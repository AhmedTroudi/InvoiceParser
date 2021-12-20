FROM python:3.7
RUN mkdir /invoice-parser
ADD . /invoice-parser
WORKDIR /invoice-parser
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "./invoice_parser.py"]