# back-end
 Endpoint

 Note: Require python 3.11.9

1. For Windows PC(Devloment):
# Create virtual environment
py -3.11 -m venv venv
python -m venv venv
.\venv\Scripts\activate

# Install torch 
### Kalau ada NVIDIA GPU:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
### Kalau takde:
pip install torch torchvision torchaudio

# Install requirements
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

2. For MacBook Pro:
# Create virtual environment

(make sure python 3.11.9)
python3 -m venv venv
source venv/bin/activate

# Install torch
pip3 install torch torchvision torchaudio

# Install requirements
pip3 install -r requirements.txt

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000




 Stress Test endpoint: POST http://localhost:8000/api/v1/stress-test
Receipt Processing endpoint: POST http://localhost:8000/api/v1/receipt
