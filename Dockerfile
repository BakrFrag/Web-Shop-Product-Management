FROM python:3.12-slim

WORKDIR /app


RUN apt update && apt install -y \
    sqlite3 libsqlite3-dev curl git ca-certificates gnupg && \
    rm -rf /var/lib/apt/lists/*

RUN pip install poetry

ENV PATH="/root/.local/bin:$PATH"

#debug
RUN python --version && poetry --version && sqlite3 --version

COPY pyproject.toml  /app/

# Install dependencies without creating a virtual environment
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-root

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
