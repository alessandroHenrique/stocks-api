FROM python:3.10-slim

# Configurações básicas
WORKDIR /app
COPY . /app

# Instalar dependências
RUN pip install poetry
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi
COPY . .
# Expor a porta
EXPOSE 8000

# Configuração padrão
ENV DJANGO_SETTINGS_MODULE=config.settings.base

# Comando padrão
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
