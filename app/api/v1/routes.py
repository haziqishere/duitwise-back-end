from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Request
from fastapi.responses import JSONResponse
from PIL import Image
import io
from app.models.schemas import StressTestRequest, StressTestResponse, ReceiptResponse
from app.services.stress_test import StressTestService
from app.services.receipt_processor import receipt_processor
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
stress_test_service = StressTestService()

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
async def process_receipt(
    file: UploadFile = File(description="Receipt image file"),
    # Add debugging fields
    content_type: str = Form(default=None),
    filename: str = Form(default=None)
):
    if not file:
        logger.error("File not provided in the request")
        raise HTTPException(status_code=400, detail="No file provided")
    
    logger.info(f"Received request - Content-Type: {content_type}, Filename: {filename}")
    
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        result = receipt_processor.process_receipt(image)
        return result
    except Exception as e:
        logger.error(f"Error processing receipt: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))