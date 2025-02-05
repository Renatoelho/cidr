FROM python:3.10-slim

WORKDIR /src

COPY ./src /src

RUN apt update && apt install iproute2 -y && pip install fastapi==0.115.6 uvicorn==0.32.1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
