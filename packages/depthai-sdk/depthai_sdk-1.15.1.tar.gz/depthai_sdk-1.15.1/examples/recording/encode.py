from depthai_sdk import OakCamera, RecordType

with OakCamera() as oak:
    left = oak.create_camera('left', resolution='800p', fps=60, encode='jpeg')
    right = oak.create_camera('right', resolution='800p', fps=60, encode='jpeg')

    # Sync & save all (encoded) streams
    oak.record([left.out.encoded, right.out.encoded], './encode', RecordType.VIDEO) \
        .configure_syncing(enable_sync=True, threshold_ms=50)

    oak.visualize([left.out.encoded], fps=True)

    oak.start(blocking=True)
