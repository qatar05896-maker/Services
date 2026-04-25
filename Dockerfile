FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# الأمر اللي بيشغل السيرفر على بورت 8000 عشان يتطابق مع ملف fly.toml
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
