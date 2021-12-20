import itertools

import pandas as pd
from sklearn.cluster import KMeans
from azure.cognitiveservices.vision.computervision.models import ReadOperationResult
import logging


def restructure_text(ocr_result: ReadOperationResult, n_clusters: int) -> str:
    """
    :param ocr_result: OCR result of the read operation
    :param n_clusters: number of clusters for k-means, in order to disable k-means use n_clusters = 0
    :return:
    """
    # Retrieve the lines and their bounding boxes from the API into a dictionary
    if n_clusters > 0:
        logging.info("Clustering text using bounding boxes information...")
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
        logging.info("Clustering is disabled, collecting text as is...")
        text = [line.text.replace(",", ".") for text_result in ocr_result.analyze_result.read_results
                for line in text_result.lines]
        structured_text = ",".join(text)

    return structured_text
