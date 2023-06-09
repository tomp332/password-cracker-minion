FROM python:slim

WORKDIR /app

COPY requirements.txt .
COPY password_cracker_minion ./password_cracker_minion

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "password_cracker_minion.src.server:main_api_router", "--host", "0.0.0.0", "--port", "5000"]
