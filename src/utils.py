import json
from typing import Tuple


# Azure Computer Vision API variables
def get_credentials(credentials_path: str) -> Tuple[str, str]:
    with open(credentials_path) as f:
        data = json.load(f)
        endpoint = data['endpoint']  # full endpoint from the Azure portal
        subscription_key = data['api_key']  # api-key
    return endpoint, subscription_key
