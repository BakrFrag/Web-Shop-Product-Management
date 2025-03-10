FROM python:3.12-slim
WORKDIR /app
RUN apt update && apt install -y \
    sqlite3 libsqlite3-dev curl git && \
    rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
RUN python --version && poetry --version && sqlite3 --version
COPY pyproject.toml /app/
RUN poetry shell 
RUN poetry add 
COPY . .
WORKDIR src
CMD ["uvicorn","src/app.py"]
