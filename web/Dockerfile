FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser

RUN chown -R appuser:appuser /app

EXPOSE 8000

USER appuser

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]