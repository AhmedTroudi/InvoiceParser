import time

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import ReadOperationResult
import logging


class VisionClient:

    def __init__(self, endpoint: str, subscription_key: str):
        self.client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    def read_image(self, image_url: str) -> ReadOperationResult:
        """
        :param image_url: can be path to local image or a url to read image remotely
        :return: OCR result of the read operation
        """
        if image_url.startswith('http'):
            # Call API with URL and raw response (allows you to get the operation location)
            read_response = self.client.read(image_url, raw=True)
        else:
            image = open(image_url, "rb")
            read_response = self.client.read_in_stream(image, raw=True)

        # Get the operation location (URL with an ID at the end) from the response
        read_operation_location = read_response.headers["Operation-Location"]
        # Grab the ID from the URL
        operation_id = read_operation_location.split("/")[-1]

        # Call the "GET" API and wait for it to retrieve the results
        while True:
            ocr_result = self.client.get_read_result(operation_id)
            if ocr_result.status not in ['notStarted', 'running']:
                break
            logging.info('Waiting for result...')
            time.sleep(1)
        return ocr_result
