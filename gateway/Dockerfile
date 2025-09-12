FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install pipenv
RUN pipenv install
ENV FLASK_APP=./src/main.py
EXPOSE 5001
CMD ["pipenv", "run", "flask", "run", "-h", "0.0.0.0", "-p",  "5001"]

