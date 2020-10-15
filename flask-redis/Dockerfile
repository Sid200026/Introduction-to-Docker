ARG PYTHON_VERSION
FROM python:$PYTHON_VERSION
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir  -r requirements.txt
COPY . .
CMD flask run --host=0.0.0.0
EXPOSE 5000