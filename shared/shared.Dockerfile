FROM python:3.14-slim AS builder

WORKDIR /app

COPY shared/requirements.txt ./

RUN python3 -m venv venv && . venv/bin/activate && pip install --upgrade pip wheel setuptools && pip install --no-cache-dir -r requirements.txt

COPY /shared ./

RUN chmod +x entrypoint.sh

FROM python:3.14-slim

WORKDIR /app

COPY --from=builder /app /app

ENV PATH="/app/venv/bin:$PATH"

CMD ["./entrypoint.sh"]