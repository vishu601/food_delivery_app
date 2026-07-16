# 1. Official Python image use karenge
FROM python:3.10-slim

# 2. Linux environment variables set karenge taaki Python smooth chale
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Working directory set karenge container ke andar
WORKDIR /app

# 4. System dependencies install karenge (agar temporary kisi cheez ki zaroorat ho)
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# 5. requirements.txt copy karke libraries install karenge
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Poora project code copy karenge
COPY . /app/

# 7. Django server start karne ki command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
