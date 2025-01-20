FROM python:3.12.8-alpine AS builder
RUN apk update && apk add \
    zlib-dev \
    jpeg-dev \
    gcc \
    musl-dev \
    && rm -rf /var/cache/apk/*
RUN mkdir /app
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM python:3.12.8-alpine AS final
RUN addgroup -S app && adduser -S app -G app && \
    mkdir /app && \
    chown -R app:app /app
RUN mkdir -p /logs/tripmixer && \
    chown -R app:app /logs/tripmixer
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
WORKDIR /app
COPY --chown=app:app . .
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
USER app
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "tripmixer.wsgi:application"]
