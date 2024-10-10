from depthai_sdk import OakCamera
from depthai_sdk.fps import FPSHandler

fps = FPSHandler()

def cb(packet):
    fps.nextIter()
    print(fps.fps())

with OakCamera() as oak:
    left = oak.create_camera('left', resolution='800p', fps=120)
    oak.callback([left], cb)
    oak.start(blocking=True)
