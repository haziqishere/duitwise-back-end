from PIL import Image
import torch
from app.models.ml_models import ml_models
from app.models.schemas import ReceiptResponse
from app.utils.categories import get_store_category
import re

class ReceiptProcessor:
    def __init__(self):
        self.processor = ml_models.processor
        self.model = ml_models.model
        self.device = ml_models.device

    def process_receipt(self, image: Image.Image) -> ReceiptResponse:
        xml_output = self._generate_xml(image)
        receipt_data = self._extract_receipt_data(xml_output)
        
        return ReceiptResponse(
            store_name=receipt_data["store_name"],
            date=receipt_data["date"],
            subtotal=receipt_data["subtotal"],
            category=get_store_category(receipt_data["store_name"])
        )

    def _generate_xml(self, image: Image.Image) -> str:
        pixel_values = self.processor(image, return_tensors="pt").pixel_values
        decoder_input_ids = self.processor.tokenizer("<s_receipt>", add_special_tokens=False, return_tensors="pt")["input_ids"]

        outputs = self.model.generate(
            pixel_values.to(self.device),
            decoder_input_ids=decoder_input_ids.to(self.device),
            max_length=self.model.decoder.config.max_position_embeddings,
            early_stopping=True,
            pad_token_id=self.processor.tokenizer.pad_token_id,
            eos_token_id=self.processor.tokenizer.eos_token_id,
            use_cache=True,
            num_beams=1,
            bad_words_ids=[[self.processor.tokenizer.unk_token_id]],
            return_dict_in_generate=True
        )

        sequence = self.processor.batch_decode(outputs.sequences)[0]
        return sequence.replace(self.processor.tokenizer.eos_token, "").replace(self.processor.tokenizer.pad_token, "")

    def _extract_receipt_data(self, xml_output: str) -> dict:
        raw_data = self.processor.token2json(xml_output)
        
        return {
            "store_name": raw_data.get("store_name", "").strip().title(),
            "date": raw_data.get("date", "").strip(),
            "subtotal": self._clean_monetary_value(raw_data.get("subtotal", "0"))
        }

    def _clean_monetary_value(self, value: str) -> float:
        if not isinstance(value, str):
            value = str(value)
        value = re.sub(r'[A-Za-z$£€¥RM\s,]', '', value)
        matches = re.findall(r'\d+\.?\d*', value)
        return round(float(matches[0]), 2) if matches else 0.00