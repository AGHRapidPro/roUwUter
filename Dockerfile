FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /root/.cache

RUN python -c "from mac_vendor_lookup import MacLookup; MacLookup().update_vendors()"

COPY . /app/

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--worker-class", "gthread", "--threads", "50", "app:app"]
