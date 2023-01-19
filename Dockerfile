# syntax=docker/dockerfile:1.4
FROM python:3.10-alpine AS builder 

WORKDIR /code

COPY requirements.txt /code
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /code

EXPOSE 5000

ENTRYPOINT ["python"]
CMD [ "-m", "flask", "run", "--host=0.0.0.0" ]