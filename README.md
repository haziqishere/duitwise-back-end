# back-end
 Endpoint

1. For Windows PC(Devloment):
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

2. For MacBook Pro:
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip3 install -r requirements.txt

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000




 Stress Test endpoint: POST http://localhost:8000/api/v1/stress-test
Receipt Processing endpoint: POST http://localhost:8000/api/v1/receipt
