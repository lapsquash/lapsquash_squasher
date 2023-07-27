from __future__ import print_function, unicode_literals

import cv2
from imagehash import average_hash
from PIL import Image

capture = cv2.VideoCapture(0)

f = 0

while True:
    ret, frame = capture.read()
    hash = average_hash(Image.fromarray(frame))

    f += 1
    h = int(str(hash), base=16)
    t = f / 30

    print(f"{f} ({t:.2f}s)\t{hash}\t->\t{h}", end="\r")

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()
cv2.destroyAllWindows()
