import itertools
import re

import pandas as pd
from sklearn.cluster import KMeans
from azure.cognitiveservices.vision.computervision.models import ReadOperationResult
import logging

def restructure_text(ocr_result: ReadOperationResult, n_clusters: int = 3) -> str:
    """
    :param ocr_result: OCR result of the read operation
    :param n_clusters: number of clusters for k-means, in order to disable k-means use n_clusters = 0
    :return:
    """
    # Retrieve the lines and their bounding boxes from the API into a dictionary
    if n_clusters > 0:
        d = {line.text: line.bounding_box for res in ocr_result.analyze_result.read_results for line in res.lines}
        df_tmp = pd.DataFrame(d.items(), columns=['Lines', 'Coordinates'])
        df = pd.DataFrame(df_tmp['Coordinates'].to_list(),
                          columns=['top-left-x', 'top-left-y', 'top-right-x', 'top-right-y', 'bottom-right-x',
                                   'bottom-right-y', 'bottom-left-x', 'bottom-left-y'],
                          index=df_tmp['Lines'])
        kmeans_clusters = KMeans(n_clusters, random_state=0).fit_predict(df)
        df['cluster'] = kmeans_clusters
        df = df.reset_index()
        document = [[line for line in df['Lines'][df['cluster'] == i]] for i in range(n_clusters)]
        flattened_doc = list(itertools.chain(*document))
        structured_text = "\n ".join(sorted(set(flattened_doc), key=flattened_doc.index))
    else:  # clustering disabled
        text = [line.text.replace(",", ".") for text_result in ocr_result.analyze_result.read_results
                for line in text_result.lines]
        structured_text = ",".join(text)

    return structured_text


def parse_invoice(structured_text: str):
    rx_customer_name = re.compile(r'''[A-Z]\w+\s[A-Z]\w+''')

    rx_customer_address = re.compile(r'''[A-Z]\w+\s?\d+?(\n)?\s?\d+?(\n)?(\s?(\d\s?)+\s[A-Z]\w+)?(\n)?(\s[A-Z]\w+)?''')

    rx_loan_balance = re.compile(r'(?P<loan_key>(?i)skuld\D+)(?P<loan_value>(\d\s?[.]?)+(,|[.]|\s)?\d+)')

    rx_payment_amount = re.compile(
        r'(?P<payment_amount_key>(?i)Inbetal\D+)(?P<payment_amount_value>(\d\s?)+(,|[.]|\s)?(\s)?(\d+))?')

    rx_loan_interest_percent = re.compile(
        r'(?P<loan_interest_key>årsränta\D+(\s)?)(?P<loan_interest_value>(\d+,)+\d+)(\s)?%')

    rx_payment_account = re.compile(r'(\d{3}-\d{4})')

    rx_loan_fees = re.compile(r'(?P<loan_fees_key>avgift\D+)(?P<loan_fees_value>\d+,)+\d+')

    customer_name_obj = re.search(rx_customer_name, structured_text)
    customer_name: str = 'Not Found'  # default value
    if customer_name_obj is not None:
        customer_name = customer_name_obj.group().replace('\n', '')
    logging.info(f'Customer Name: {customer_name}')

    customer_address_obj = re.search(rx_customer_address, structured_text)
    customer_address: str = 'Not Found'
    if customer_address_obj is not None:
        customer_address = customer_address_obj.group().replace('\n', '')
    logging.info(f'Customer Address: {customer_address}')

    loan_balance_obj = re.search(rx_loan_balance, structured_text)
    loan_balance = {'key': 'Not found', 'value': None}
    if loan_balance_obj is not None:
        loan_balance['key'] = loan_balance_obj.group('loan_key')
        loan_balance['value'] = loan_balance_obj.group('loan_value')
    logging.info(f'Loan Balance: {loan_balance}')

    payment_amount_obj = re.search(rx_payment_amount, structured_text)
    payment_amount = {'key': 'Not found', 'value': None}
    if payment_amount_obj is not None:
        payment_amount['key'] = payment_amount_obj.group('payment_amount_key') \
            .replace('\n', '').replace('-', '').replace(' ', '')
        payment_amount['value'] = payment_amount_obj.group('payment_amount_value').replace(',', '.').replace(' ', '')
    logging.info(f'Payment Amount: {payment_amount}')

    loan_interest_obj = re.search(rx_loan_interest_percent, structured_text)
    loan_interest = {'key': 'Not found', 'value': None}
    if loan_interest_obj is not None:
        loan_interest['key'] = loan_interest_obj.group('loan_interest_key')
        loan_interest['value'] = loan_interest_obj.group('loan_interest_value').replace(',', '.').replace(' ', '')
    logging.info(f'Loan Interest {loan_interest}')

    payment_account_obj = re.search(rx_payment_account, structured_text)
    payment_account: str = 'Not Found'
    if payment_account_obj is not None:
        payment_account = payment_account_obj.group()
    logging.info(f'Payment Account: {payment_account}')

    loan_fees_iterator = re.finditer(rx_loan_fees, structured_text)
    loan_fees = {'key': 'Not found', 'value': None}
    if loan_fees_iterator is not None:
        fees_keys = ''
        fees_value = 0
        for fee in loan_fees_iterator:
            fees_keys = fee.group('loan_fees_key') + '-' + fees_keys
            fees_value = float(fee.group('loan_fees_value').replace(',', '.').replace(' ', '')) + fees_value
        loan_fees['key'] = fees_keys
        loan_fees['value'] = fees_value
    logging.info(f'Loan Fees: {loan_fees}')

    data = {
        "customer name": customer_name,
        "customer address": customer_address,
        "loan balance": loan_balance['value'],
        "payment amount": payment_amount['value'],
        "loan interest": loan_interest['value'],
        "payment account": payment_account,
        "loan fees": loan_fees['value']
    }
    return data
