FROM python:3

WORKDIR /Users/aswini.prasad/Documents/checkin-screen-service-master 2/flaskapp

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "flaskapp.py"]