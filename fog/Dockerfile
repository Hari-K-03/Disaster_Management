FROM python:3.13-slim
WORKDIR  /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY fog_gateway.py .
EXPOSE 5000
CMD ["python", "fog_gateway.py"]