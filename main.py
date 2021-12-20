import json

import pandas as pd

from src.utils import get_credentials
from src.read_image import VisionClient
from src.process_text import restructure_text, parse_invoice
import logging


def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    credentials_path = 'credentials.json'
    image_path = 'dataset/6.png'
    n_clusters = 3  # optional argument
    endpoint, key = get_credentials(credentials_path)
    vision_client = VisionClient(endpoint, key)
    ocr_result = vision_client.read_image(image_path)
    structured_text = restructure_text(ocr_result)
    data = parse_invoice(structured_text)
    with open('data.json', 'w+') as f:
        json.dump(data, f)
    df = pd.DataFrame(data, index=[0])
    df.to_csv('data.csv', index=False)


if __name__ == '__main__':
    main()
