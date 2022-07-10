FROM python:3.9

EXPOSE 80

RUN python -m pip install --upgrade pip

COPY . ./app

WORKDIR /app

RUN pip install -r requiriments.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

