From python:slim
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
WORKDIR /app