FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install pipenv
RUN pipenv install
ENV FLASK_APP=./src/main.py
ENV PYTHONPATH=/app
EXPOSE 5003
CMD ["pipenv", "run", "python", "src/main.py"]
