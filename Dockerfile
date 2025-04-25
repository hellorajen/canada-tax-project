FROM python:3.12-slim

# Set working directory (will create /app in container)
WORKDIR /app

# Install dependencies first (caching optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ALL files (except .dockerignore exclusions)
COPY . .

# Set Flask environment variables, # Module-style import
ENV FLASK_APP=canada_tax_app.app  
ENV FLASK_DEBUG=1

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]