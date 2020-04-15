# Dockerfile
FROM python:latest
COPY ../../. .
ENV PYTHONPATH $PWD/../../deep_learning_app
RUN pip install -r /../requirements.txt
EXPOSE 4222
CMD ["python","-u", "Node.py"]