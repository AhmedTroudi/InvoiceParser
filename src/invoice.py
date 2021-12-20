import re
import logging


class Invoice:
    def __init__(self, structured_text):
        self.structured_text = structured_text
        self.customer_name: str = 'Not Found'  # default value in case parsing fails
        self.customer_address: str = 'Not Found'
        self.loan_balance: dict = {'key': 'Not found', 'value': None}
        self.payment_amount: dict = {'key': 'Not found', 'value': None}
        self.loan_interest: dict = {'key': 'Not found', 'value': None}
        self.payment_account: str = 'Not Found'
        self.loan_fees: dict = {'key': 'Not found', 'value': None}

    def parse_customer_name(self):
        rx_customer_name = re.compile(r'''[A-Z]\w+\s[A-Z]\w+''')

        customer_name_obj = re.search(rx_customer_name, self.structured_text)
        if customer_name_obj is not None:
            self.customer_name = customer_name_obj.group().replace('\n', '')
        logging.info(f'Customer Name: {self.customer_name}')

    def parse_customer_address(self):
        rx_customer_address = re.compile(
            r'''[A-Z]\w+\s?\d+?(\n)?\s?\d+?(\n)?(\s?(\d\s?)+\s[A-Z]\w+)?(\n)?(\s[A-Z]\w+)?''')

        customer_address_obj = re.search(rx_customer_address, self.structured_text)
        if customer_address_obj is not None:
            self.customer_address = customer_address_obj.group().replace('\n', '')
        logging.info(f'Customer Address: {self.customer_address}')

    def parse_loan_balance(self):
        rx_loan_balance = re.compile(r'(?P<loan_key>(?i)skuld\D+)(?P<loan_value>(\d\s?[.]?)+(,|[.]|\s)?\d+)')

        loan_balance_obj = re.search(rx_loan_balance, self.structured_text)
        if loan_balance_obj is not None:
            self.loan_balance['key'] = loan_balance_obj.group('loan_key')
            self.loan_balance['value'] = loan_balance_obj.group('loan_value')
        logging.info(f'Loan Balance: {self.loan_balance}')

    def parse_payment_amount(self):
        rx_payment_amount = re.compile(
            r'(?P<payment_amount_key>Att betala\D+:?)(?P<payment_amount_value>(\d\s?)+(,|[.]|\s)?(\s)?(\d+))?')

        payment_amount_obj = re.search(rx_payment_amount, self.structured_text)
        if payment_amount_obj is not None:
            self.payment_amount['key'] = payment_amount_obj.group('payment_amount_key') \
                .replace('\n', '').replace('-', '').replace(' ', '')
            self.payment_amount['value'] = payment_amount_obj.group('payment_amount_value')\
                .replace(',', '.').replace(' ', '')
        logging.info(f'Payment Amount: {self.payment_amount}')

    def parse_loan_interest(self):
        rx_loan_interest_percent = re.compile(
            r'(?P<loan_interest_key>årsränta\D+(\s)?)(?P<loan_interest_value>(\d+,)+\d+)(\s)?%')
        loan_interest_obj = re.search(rx_loan_interest_percent, self.structured_text)
        if loan_interest_obj is not None:
            self.loan_interest['key'] = loan_interest_obj.group('loan_interest_key')
            self.loan_interest['value'] = loan_interest_obj.group('loan_interest_value').replace(',', '.').replace(' ', '')
        logging.info(f'Loan Interest {self.loan_interest}')

    def parse_payment_account(self):
        rx_payment_account = re.compile(r'(\d{3}-\d{4})')
        payment_account_obj = re.search(rx_payment_account, self.structured_text)
        if payment_account_obj is not None:
            self.payment_account = payment_account_obj.group()
        logging.info(f'Payment Account: {self.payment_account}')

    def parse_loan_fees(self):
        rx_loan_fees = re.compile(r'(?P<loan_fees_key>avgift\D+)(?P<loan_fees_value>\d+,)+\d+')

        loan_fees_iterator = re.finditer(rx_loan_fees, self.structured_text)
        if loan_fees_iterator is not None:
            fees_keys = ''
            fees_value = 0
            for fee in loan_fees_iterator:
                fees_keys = fee.group('loan_fees_key') + '-' + fees_keys
                fees_value = float(fee.group('loan_fees_value').replace(',', '.').replace(' ', '')) + fees_value
            self.loan_fees['key'] = fees_keys
            self.loan_fees['value'] = fees_value
        logging.info(f'Loan Fees: {self.loan_fees}')

    def get_invoice_data(self) -> dict:
        self.parse_customer_name()
        self.parse_customer_address()
        self.parse_loan_balance()
        self.parse_payment_amount()
        self.parse_loan_interest()
        self.parse_payment_account()
        self.parse_loan_fees()
        data = {
            "customer name": self.customer_name,
            "customer address": self.customer_address,
            "loan balance": self.loan_balance['value'],
            "payment amount": self.payment_amount['value'],
            "loan interest": self.loan_interest['value'],
            "payment account": self.payment_account,
            "loan fees": self.loan_fees['value']
        }
        return data


