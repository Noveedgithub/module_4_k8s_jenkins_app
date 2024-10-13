FROM python:latest
WORKDIR /app
COPY . /app
RUN pip install -r ./flask_2/requirements.txt
EXPOSE 5500
CMD ["python", "./flask_2/appv2.py"]