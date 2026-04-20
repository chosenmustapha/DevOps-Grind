
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r /aws-ci-tools-demo/requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]