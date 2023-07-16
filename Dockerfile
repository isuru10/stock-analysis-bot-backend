FROM public.ecr.aws/lambda/python:3.8
COPY src/ ${LAMBDA_TASK_ROOT}/src/
COPY .env ${LAMBDA_TASK_ROOT}
COPY requirements.txt .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
CMD ["src/lambda_function.lambda_handler"]
