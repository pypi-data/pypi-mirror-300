from typing import List
from depthai_sdk import OakCamera, RecordType
import depthai as dai

FPS = 30

# infos = dai.Device.getAllAvailableDevices()
oaks: List[OakCamera] = []
for _ in range(1):
    oak = OakCamera()
    oaks.append(oak)
    color = oak.create_camera('CAM_A', resolution='1080p', encode='mjpeg', fps=FPS)
    color.config_color_camera(isp_scale=(2,3))
    stereo = oak.create_stereo(resolution='720p', fps=FPS)
    stereo.config_stereo(align=color, subpixel=True, lr_check=True)
    stereo.node.setOutputSize(640, 360)

    # On-device post processing for stereo depth
    config = stereo.node.initialConfig.get()
    stereo.node.setPostProcessingHardwareResources(3, 3)
    config.postProcessing.speckleFilter.enable = True
    config.postProcessing.speckleFilter.speckleRange = 50
    config.postProcessing.temporalFilter.enable = False
    config.postProcessing.thresholdFilter.minRange = 400
    config.postProcessing.thresholdFilter.maxRange = 7000
    config.postProcessing.decimationFilter.decimationFactor = 2
    config.postProcessing.decimationFilter.decimationMode = dai.StereoDepthConfig.PostProcessing.DecimationFilter.DecimationMode.NON_ZERO_MEDIAN
    config.postProcessing.brightnessFilter.maxBrightness = 255
    stereo.node.initialConfig.set(config)


    # DB3 / ROSBAG. ROSBAG doesn't require having ROS installed, while DB3 does.
    record_components = [stereo.out.depth, color.out.encoded]
    oak.record(record_components, 'depth_video', record_type=RecordType.VIDEO).configure_syncing(True, threshold_ms=500/30)

    # Visualize only color stream
    # oak.visualize([
        # color.out.encoded.set_name('color'+ oak.device.getMxId()),
        # stereo.out.depth.set_name('stereo' + oak.device.getMxId())
    # ])
    # oak.callback([
    #     color.out.encoded.set_name('color'),
    #     stereo.out.disparity.set_name('stereo')
    #     ], oak_vis.cb, main_thread=True).configure_syncing(True, 500/20)

    # oak.start(blocking=True)
    oak.start(blocking=False)

import threading
import signal

quitEvent = threading.Event()
signal.signal(signal.SIGTERM, lambda *_args: quitEvent.set())
signal.signal(signal.SIGINT, lambda *_args: quitEvent.set())
print("\nRecording started. Press 'Ctrl+C' to stop.")

while not quitEvent.is_set():
    for oak in oaks:
        oak.poll()

print ("Stopping recording...")
for oak in oaks:
    oak.close()


