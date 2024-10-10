import cv2

from depthai_sdk import OakCamera
from depthai_sdk.components.stereo_component import WLSLevel
from depthai_sdk.visualize.configs import StereoColor

def cb(packet):
    print(packet)


with OakCamera(device='19443010D116992E00') as oak1, OakCamera(device='19443010710A9D2E00') as oak2:
    for i, oak in enumerate([oak1, oak2]):
        color = oak.create_camera('color', resolution='800p', fps=25)
        stereo = oak.create_stereo('800p', fps=25)
        stereo.config_stereo(align=color)
        stereo.node.setAlphaScaling(1.0)
        oak.callback([
                stereo.out.depth.set_name(f"Depth {i}"),
                color.out.main.set_name(f"Color {i}"),
            ], cb).configure_syncing(True, threshold_ms=20)
        oak.start()

    run = True
    while run:
        for oak in [oak1, oak2]:
            oak.poll()
            if not oak.running():
                run = False
