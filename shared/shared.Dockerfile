FROM python:3.14-slim

WORKDIR /shared

COPY shared/requirements.txt /shared

RUN pip install -r requirements.txt

COPY /shared /shared

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]