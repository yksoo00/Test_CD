FROM python:slim
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Seoul
EXPOSE 8000
WORKDIR /app
