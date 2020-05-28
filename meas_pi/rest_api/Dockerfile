FROM arm32v6/alpine
WORKDIR /code
COPY requirements.txt ./
RUN apk add python3-dev
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["rest.py"]

