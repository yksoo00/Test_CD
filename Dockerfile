From python:slim
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./app /app
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
WORKDIR /app
CMD ["uvicorn", "main:app", "--reload"]