FROM python:3.13.2
WORKDIR /app
COPY off_chain/pyproject.toml off_chain/poetry.lock ./

# Installiamo le dipendenze di sistema per PyQt5
RUN apt-get update && apt-get install -y \
    libegl1 \
    libopengl0 \
    libxcb-xinerama0 \
    libxkbcommon-x11-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry && poetry install --no-dev

# Disabilitiamo gli ambienti virtuali Poetry (per Docker)
ENV POETRY_VIRTUALENVS_CREATE=false

COPY off_chain/ .
CMD ["poetry", "run", "python", "app.py"]





