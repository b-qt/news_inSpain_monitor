from python:3.9-slim


run apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

workdir /app

copy requirements.txt .

run pip install --no-cache--dir -r requirements.txt

copy . .

expose 8501

cmd ["python", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]


# you must have a dockerfile to install dependencies