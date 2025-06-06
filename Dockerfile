FROM public.ecr.aws/docker/library/python:3.12-alpine
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter

ENV PORT=8000

WORKDIR /var/task
COPY requirements.txt ./

RUN python -m pip install -r requirements.txt
COPY src/*.py ./

CMD exec uvicorn --port=$PORT src.main:app
