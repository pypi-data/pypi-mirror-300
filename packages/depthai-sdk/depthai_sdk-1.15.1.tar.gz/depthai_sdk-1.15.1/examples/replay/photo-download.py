from depthai_sdk import OakCamera
from pathlib import Path

path = Path.home() / 'Documents' / 'projects' / 'parking'
with OakCamera(replay=path) as oak:
    oak.replay.set_fps(10)
    color = oak.create_camera('color')
    model_config = {
        'source': 'roboflow', # Specify that we are downloading the model from Roboflow
        'model':'parking-spot-detector-a84ql/1',
        'key':'dDOP8nChA9rZUWUTG8ia' # Fake API key, replace with your own!
    }
    nn = oak.create_nn(model_config, color, tracker=True)
    nn.config_nn(resize_mode='CROP')
    # nn = oak.create_nn('mobilenet-ssd', color)
    oak.visualize([nn])
    oak.start(blocking=True)
m