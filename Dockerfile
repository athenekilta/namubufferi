# syntax=docker/dockerfile:1

# Build stage for React app
FROM node:16 as react-build
WORKDIR /tmp/reactapp/
COPY reactapp/package.json reactapp/yarn.lock ./
RUN yarn install
COPY reactapp/public/ ./public/
COPY reactapp/src/ ./src/
RUN yarn build

# Build and runtime stage for Python app
FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m appuser

# Set up the working directory
WORKDIR /srv/namubufferi/

# Install pipenv temporarily to generate requirements.txt
RUN pip install --no-cache-dir pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Generate requirements.txt from Pipfile and replace psycopg2 with psycopg2-binary
RUN pipenv requirements > requirements.txt && \
    sed -i 's/psycopg2==2.9.3/psycopg2-binary==2.9.3/' requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Remove pipenv as it's no longer needed
RUN pip uninstall -y pipenv

# Copy application code
COPY . .
# Copy React build files
COPY --from=react-build /tmp/reactapp/static/ ./reactapp/static/

# Update entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set ownership to non-root user
RUN chown -R appuser:appuser /srv/namubufferi/

# Switch to non-root user
USER appuser

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["gunicorn", "namubufferi.wsgi"]