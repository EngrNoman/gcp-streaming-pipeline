FROM python:3.11-slim

WORKDIR /app

# Sabse pehle requirements copy aur install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baki ka script copy karein
COPY main.py .

# -u flag se logs real-time mai terminal par show hotay hain
CMD ["python", "-u", "main.py"]