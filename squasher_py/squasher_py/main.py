import sys

import cv2
import numpy as np
import pyqtgraph as pg
from imagehash import average_hash
from PIL import Image
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

capture = cv2.VideoCapture(0)

if not capture.isOpened():
    raise RuntimeError("Could not open camera/file")


app = QApplication([])
win = pg.GraphicsLayoutWidget(
    show=True,
    size=(500, 500),
    title="pyqtgraph example: Plotting",
)

plot = win.addPlot(title="ads")
curve = plot.plot(pen="y")

fps = 60
n_samples = 500
fo = 1
data = np.zeros(n_samples)

iter = 0


def update():
    global curve, data, iter, fps, fo, n_samples

    ret, frame = capture.read()

    cv2.imshow("camera", frame)

    hash = average_hash(Image.fromarray(frame))

    fo = 0.1 + iter / n_samples
    t = (1.0 / fps) * iter
    idx = iter % n_samples
    data[idx] = int(str(hash), base=16)

    print(f"{iter:.2f}\t{t:.2f}\t{data[idx]}\t{hash}", end="\r")
    pos = idx + 1 if idx < n_samples else 0
    curve.setData(np.r_[data[pos:n_samples], data[0:pos]])
    iter += 1

    if cv2.waitKey(1) & 0xFF == ord("q"):
        exit(0)


timer = QTimer()
timer.timeout.connect(update)
timer.start(int(1 / fps * 1000))

if __name__ == "__main__":
    if sys.flags.interactive == 1:
        raise RuntimeError("This script is not meant to be run interactively.")

    instance = QApplication.instance()

    if instance is None:
        raise RuntimeError("No QApplication instance found.")

    instance.exec()
    capture.release()
    cv2.destroyAllWindows()
