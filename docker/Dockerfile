FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl build-essential git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia archivos de dependencias desde un nivel superior
COPY ../pyproject.toml ../uv.lock ./

# Instala dependencias usando uv (lee pyproject.toml + uv.lock)
RUN curl -Ls https://astral.sh/uv/install.sh | bash && \
    /root/.local/bin/uv pip install --system --no-cache .

# Copia el código de la aplicación
COPY ../app ./app
COPY ../.env .env

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

