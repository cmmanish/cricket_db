FROM python:3.8-alpine
EXPOSE 5000

WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "app/app.py" ]