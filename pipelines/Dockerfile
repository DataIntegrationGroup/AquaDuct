FROM python:3.12.10-slim-bookworm

RUN pip install \
    dagster \
    dagster-postgres \
    dagster-docker \
    uv

WORKDIR /aquaduct
COPY . /aquaduct

EXPOSE 4266

#Hack to make uv sync install dependencies globally
ENV UV_PROJECT_ENVIRONMENT=/usr/local

RUN uv sync --frozen --no-dev --no-install-project

# Dagster deployment docs say to run a broken/undocumented command (`dagster code-space`). Use `dagster api grpc`.
CMD ["dagster", "code-server", "start", "-h", "0.0.0.0", "-p", "4266", "-m", "pipelines.definitions"]