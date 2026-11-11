# ---------- app: Django + gunicorn ----------
FROM python:3.14-slim AS app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # matplotlib needs a writable cache folder; the app runs as a non-root user
    MPLCONFIGDIR=/tmp/matplotlib

WORKDIR /app

# Dependencies first, so code changes don't reinstall them on every build
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Collect static files into /app/staticfiles for nginx; the key is only needed to import settings
RUN SECRET_KEY=collectstatic-only python manage.py collectstatic --noinput \
    && chmod +x docker/entrypoint.sh \
    && useradd --create-home appuser

USER appuser

EXPOSE 8000
ENTRYPOINT ["docker/entrypoint.sh"]
CMD ["gunicorn", "gymHelper.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]


# ---------- nginx: serves static files and proxies to the app ----------
FROM nginx:1.27-alpine AS nginx

COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=app /app/staticfiles /static
