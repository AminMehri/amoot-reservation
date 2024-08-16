# استفاده از تصویر رسمی Python
FROM python:3.10

# تنظیم دایرکتوری کاری در داخل کانتینر
WORKDIR /app

# کپی کردن فایل‌های مورد نیاز به کانتینر
COPY . /app/

# نصب ابزارهای لازم
RUN apt-get update && apt-get install -y netcat-traditional

# نصب وابستگی‌ها
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# تنظیم دستور پیش‌فرض برای اجرای کانتینر
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
