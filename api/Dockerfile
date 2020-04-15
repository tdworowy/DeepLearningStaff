# Dockerfile
FROM python:latest
COPY ../../. .
ENV PYTHONPATH $PWD/../../deep_learning_app
RUN pip install -r /../requirements.txt
EXPOSE 5000
CMD ["python","-u", "main_distributed.py"]