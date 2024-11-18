FROM python:3.9

WORKDIR /bookshelf

COPY ./requirements.txt /bookshelf/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /bookshelf

EXPOSE 3050

CMD ["python3", "bookshelf.py"]
