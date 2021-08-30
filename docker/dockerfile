FROM python:3.7

LABEL mantainer="gootsev@gmail.com"

WORKDIR /app/
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app.py /app/

EXPOSE 5000
ENTRYPOINT ["python3", "/app/app.py"]