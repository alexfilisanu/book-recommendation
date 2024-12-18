FROM python:3.9

WORKDIR /auth

COPY ./requirements.txt /auth/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /auth

EXPOSE 3100

CMD ["python3", "auth.py"]
