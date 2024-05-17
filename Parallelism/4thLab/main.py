import time
import argparse
import threading
from queue import Queue
import logging

import cv2


logging.basicConfig(filename='logs/logfile.log', level=logging.ERROR)


class Sensor:
    def get(self):
        raise NotImplementedError()


class SensorX(Sensor):
    def __init__(self, delay):
        self._delay = delay
        self._data = 0

    def get(self):
        time.sleep(self._delay)
        self._data += 1
        return self._data


class SensorCam(Sensor):
    def __init__(self, name: str, resolution: tuple[int, int]):
        try:
            self._video = cv2.VideoCapture(name)
            self._video.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
            self._video.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
            if not self._video.isOpened():
                raise ValueError("Camera couldn't be opened")
        except Exception as e:
            logging.error(f"Error initializing Camera: {e}")
            raise

    def get(self):
        ret, frame = self._video.read()
        if not ret:
            logging.error("Error reading frame from camera")
            return None
        return frame

    def __del__(self):
        try:
            self._video.release()
        except Exception as e:
            logging.error(f"Error releasing Camera: {e}")
            
            
class SensorThread:
    def __init__(self, sensor):
        self.queue = Queue()
        self._sensor = sensor
        self._run = False
        self._thread = threading.Thread(target=self.run).start()

    def __del__(self):
        self._run = False
        self._thread.join()

    def run(self):
        self._run = True
        while self._run:
            data = self._sensor.get()
            self.queue.put(data)
            

class WindowImage:
    def __init__(self, freq: int):
        self._delay = int(1000 / freq)
        self._name = 'Lab 4 window'

    def show(self, img):
        cv2.imshow(self._name, img)
        if cv2.waitKey(self._delay) == ord('q'):
            return True
        return False

    def __del__(self):
        cv2.destroyAllWindows()

def get_camera_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('cam_name', type=int)
    parser.add_argument('cam_res', type=str)
    parser.add_argument('cam_framerate', type=int)
    args = parser.parse_args()
    cam_name = args.cam_name
    cam_res = tuple(map(int, args.cam_res.split('x')))
    cam_framerate = args.cam_framerate
    return cam_name, cam_res, cam_framerate

def main():
    params = get_camera_params()
    print(params)
    sensor_cam = SensorCam(*(params[:2]))
    window_image = WindowImage(params[2])

    sensor_x1 = SensorThread(SensorX(0.01))
    sensor_x2 = SensorThread(SensorX(0.1))
    sensor_x3 = SensorThread(SensorX(1))
    sensor_cam = SensorThread(SensorCam(*(params[:2])))

    sensor_x1_data = 0
    sensor_x2_data = 0
    sensor_x3_data = 0
    cam_frame = sensor_cam.queue.get()
    
    try:
        while True:
            print("Start processing")
            while not sensor_cam.queue.empty():
                cam_frame = sensor_cam.queue.get()
            while not sensor_x2.queue.empty():
                sensor_x2_data = sensor_x2.queue.get()
            while not sensor_x3.queue.empty():
                sensor_x3_data = sensor_x3.queue.get()
            while not sensor_x1.queue.empty():
                sensor_x1_data = sensor_x1.queue.get()
            cv2.putText(cam_frame,
                        f'Sensor1 data: {sensor_x1_data} Sensor2 data: {sensor_x2_data} Sensor3 data: {sensor_x3_data}',
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 2,
                        cv2.LINE_AA)
            if window_image.show(cam_frame):
                break
    finally:
        del sensor_cam
        del sensor_x1
        del sensor_x2
        del sensor_x3
        del window_image


if __name__ == "__main__":
    main()