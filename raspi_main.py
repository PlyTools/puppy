from control.camera import Camera
from transfer.raspiberry.stream_client import StreamClient


if __name__ == "__main__":
    camera = Camera()
    stream_host = ('192.168.1.100', 8000)
    streamClient = StreamClient(stream_host)
    streamClient.transfer(camera.getFrameArray())
