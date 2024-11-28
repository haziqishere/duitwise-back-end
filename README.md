# back-end
 Endpoint

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload




 Stress Test endpoint: POST http://localhost:8000/api/v1/stress-test
Receipt Processing endpoint: POST http://localhost:8000/api/v1/receipt
