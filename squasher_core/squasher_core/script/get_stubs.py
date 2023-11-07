import os

import cv2
import requests

url: str = "https://raw.githubusercontent.com/bschnurr/python-type-stubs/add-opencv/cv2/__init__.pyi"

path = os.path.join(
    os.path.dirname(cv2.__file__),
    "cv2.pyi",
)

data = requests.get(url).content

with open(path, "wb") as f:
    f.write(data)
