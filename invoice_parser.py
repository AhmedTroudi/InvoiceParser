import json

import pandas as pd

from src.utils import get_credentials
from src.read_image import VisionClient
from src.process_text import restructure_text
from src.invoice import Invoice
import logging

import argparse


def main(args):
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    # command-line args
    credentials_path = args.credentials
    image_path = args.image_path_or_url
    n_clusters = args.n_clusters
    output_path = args.output_path
    # authenticating client
    endpoint, key = get_credentials(credentials_path)
    vision_client = VisionClient(endpoint, key)
    # getting ocr results and structuring text
    ocr_result = vision_client.read_image(image_path)
    structured_text = restructure_text(ocr_result, n_clusters)
    # parsing invoice fields and save results to a csv
    invoice = Invoice(structured_text)
    data = invoice.get_invoice_data()
    df = pd.DataFrame(data, index=[0])
    df.to_csv(output_path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='InvoiceParser')
    parser.add_argument('--image_path_or_url', '-i', type=str, required=True,
                        help="specifies image local path (includes filename) or url")
    parser.add_argument('--credentials', '-c', type=str, required=False, default='credentials.json',
                        help="specifies path to credentials (includes filename)")
    parser.add_argument('--output_path', '-o', type=str, required=False, default='parsed_data.csv',
                        help="specifies data local output path, by default saves 'parsed_data.csv' to project directory")
    parser.add_argument('--n_clusters', '-n', type=int, required=False, default=3,
                        help="indicates number of clusters to use. You can disable clustering by using a value of 0")

    arguments = parser.parse_args()
    main(arguments)
