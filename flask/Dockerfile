FROM python:latest
WORKDIR /app
COPY . /app
RUN pip install -r flask/requirements.txt
EXPOSE 5500
CMD ["python", "./flask/app.py"]