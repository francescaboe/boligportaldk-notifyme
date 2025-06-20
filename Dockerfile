# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of app
COPY . .

# Command to run app
CMD ["python", "main.py"]
