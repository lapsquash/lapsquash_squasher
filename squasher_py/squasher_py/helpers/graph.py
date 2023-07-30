import cv2
import numpy as np
import pyqtgraph as pg

img = pg.GraphicsLayoutWidget()
capture = cv2.VideoCapture(0)

fps = 60
n_samples = 500


def table():
    table = pg.TableWidget()
    table.setData([["会社A", "2000", "4000"], ["会社B", "1200", "60"]])
    table.resizeRowsToContents()
    return table


def graph():
    graph = pg.GraphicsLayoutWidget()
    x = np.arange(1000)
    y = np.random.normal(size=1000)

    graph.addPlot(title="データ", x=x, y=y, pen="red")
    return graph


def camera():
    global img, capture
    _, frame = capture.read()
    frameBuff = pg.ImageItem()
    frameBuff.setImage(frame)
    img.addItem(frameBuff)


def Setup_Window():
    win = pg.LayoutWidget()

    # win.addWidget(table(), row=0, col=0)
    # win.addWidget(graph(), row=1, col=0)
    camera()
    win.addWidget(img, row=0, col=0)

    return win


def update():
    global img, capture
    _, frame = capture.read()
    img.addItem(pg.ImageItem(frame))


if __name__ == "__main__":
    app = pg.mkQApp()

    win = Setup_Window()
    win.show()
    app.exec()
