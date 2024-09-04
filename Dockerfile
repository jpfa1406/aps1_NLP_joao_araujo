FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN pip install --no-cache-dir pytest && pytest --disable-warnings
    
EXPOSE 1506

CMD ["uvicorn", "app.main:app", "--host", "10.103.0.28", "--port", "1506"]