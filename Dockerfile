FROM python:slim
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev ffmpeg sox libsox-fmt-all libsndfile1 && \
    rm -rf /var/lib/apt/lists/*