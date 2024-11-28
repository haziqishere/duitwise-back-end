from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image
import io
from app.models.schemas import StressTestRequest, StressTestResponse, ReceiptResponse
from app.services.stress_test import StressTestService
from app.services.receipt_processor import ReceiptProcessor

router = APIRouter()
stress_test_service = StressTestService()
receipt_processor = ReceiptProcessor()

@router.post("/stress-test", response_model=StressTestResponse)
async def calculate_stress_test(request: StressTestRequest):
    """
    Calculate DSR and monthly payments for a new loan application.
    Returns DSR value and payment details without categorization.
    """
    try:
        return stress_test_service.calculate_stress_test(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/receipt", response_model=ReceiptResponse)
async def process_receipt(file: UploadFile = File(...)):
    """
    Extract key information from receipt image.
    Returns store name, date, subtotal, and tax relief category.
    """
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        return receipt_processor.process_receipt(image)
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail="Failed to process receipt. Please ensure image is clear and contains valid receipt information."
        )