FROM python:3
COPY . /code
WORKDIR /code
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
