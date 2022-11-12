FROM python:3.10-alpine

WORKDIR /event_planner

EXPOSE ${EVENT_PORT}

RUN apk add build-base

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

COPY . .

CMD uvicorn event_planner:app --host 0.0.0.0 --port ${EVENT_PORT} --loop uvloop