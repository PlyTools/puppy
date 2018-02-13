from control.camera import Camera
from control.ultrasonic import Ultrasound
from transfer.raspiberry.stream_client import StreamClient


if __name__ == "__main__":
    camera = Camera()
    image_host = ('192.168.1.100', 8000)
    streamClient = StreamClient(image_host)
    streamClient.send(camera.getFrameArray())

    ultrasound = Ultrasound()
    ultra_host = ('192.168.1.100', 8002)
    streamClient = StreamClient(ultra_host)
    streamClient.send(ultrasound.get_distance())

