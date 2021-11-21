FROM python:3.9

# Create /app directory and use it as default directory address
WORKDIR /app

# Export PYTHONPATH Environment Variable
ENV PYTHONPATH="/app"

# Copy requirements and add it to /app. It should be copied separately for optimization concerns.
COPY requirements.txt .

# Installing requirements.
RUN pip install -r requirements.txt

# Copy all files to /app directory.
COPY . .

# run the server
CMD ["python3", "main.py"]
