FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]