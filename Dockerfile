FROM python:3.10-slim

WORKDIR /app

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set Python path and environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=canada_tax_app.app
ENV FLASK_ENV=production

EXPOSE 5000

# Updated command - point to correct module
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "canada_tax_app.app:app"]