import os, io
from base64 import b64encode
import requests
import json

from google.cloud import vision


def visionAPIDemoUsingAuthToken(img_path):

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"<Path-to-API-Token>"
    client = vision.ImageAnnotatorClient()

    with io.open(img_path, 'rb') as img_file:
        content = img_file.read()

    img = vision.Image(content=content)
    response = client.text_detection(image=img)
    texts = response.text_annotations

    print("Texts:- ")
    print(texts[0].description)

def visionAPIDemoUsingAPIKey(img_path):

    f = open(img_path, 'rb')
    ctxt = b64encode(f.read()).decode()

    ENDPOINT_URL = "https://vision.googleapis.com/v1/images:annotate"
    api_key = "API-Key"

    image = json.dumps({"requests": [{'image': {'content': ctxt},
                                      'features': [{'type': 'DOCUMENT_TEXT_DETECTION',
                                                    'maxResults': 1}]}
                                     ]}).encode()
    # Call google vision API for ocr on an image
    response = requests.post(ENDPOINT_URL,
                             data=image,
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        print("Response - ", response.json()['responses'][0])
    else:
        print("API failed with response status - ", response.status_code)

if __name__ == '__main__':
    img_path = "./handwritten.jpg"
    visionAPIDemoUsingAuthToken(img_path)
    visionAPIDemoUsingAPIKey(img_path)
