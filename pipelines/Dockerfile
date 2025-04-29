FROM python:3.12.10-slim-bookworm

RUN pip install \
    dagster \
    dagster-postgres \
    dagster-docker

# Add code location code
WORKDIR /opt/dagster/aquaduct
COPY . /opt/dagster/aquaduct

EXPOSE 4266

# Dagster deployment docs say to run a broken/undocumented command (`dagster code-space`). Use `dagster api grpc`.
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4266", "-m", "pipelines.definitions"]