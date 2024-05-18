import argparse
import threading
from queue import Queue
from time import time, sleep

from ultralytics import YOLO
import cv2


def fun_thread_read(path_video: str, frame_queue: Queue, event_stop: threading.Event):
    cap = cv2.VideoCapture(path_video)
    ind = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame!")
            break
        frame_queue.put((frame, ind))
        ind += 1
        # time.sleep(0.0001)
    event_stop.set()


def fun_thread_write(length: int, fps: int, out_queue: Queue, out_path: str):
    t = threading.current_thread()
    frames = [None] * length
    while getattr(t, "do_run", True):
        try:
            frame, ind = out_queue.get(timeout=1)
            frames[ind] = frame
        except Exception as e:
            print(e)
    print("Stopping to write.")

    print("Starting to compose.")
    width, height = frames[0].shape[1], frames[0].shape[0]
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for frame in frames:
        out.write(frame)
    out.release()


def fun_thread_safe_predict(frame_queue: Queue, out_queue: Queue, event_stop: threading.Event):
    local_model = YOLO(model="yolov8s-pose.pt", verbose=False)
    while True:
        try:
            frame, ind = frame_queue.get(timeout=1)
            results = local_model.predict(source=frame, device='cpu', verbose=False)[0].plot()
            out_queue.put((results, ind))
        except Exception as e:
            print(e)
            if event_stop.is_set():
                print(f'Thread {threading.get_ident()} final!')
                break


def main(input_video, output_path, thread_num):
    threads = []
    frame_queue = Queue()
    out_queue = Queue()
    event_stop = threading.Event()

    video_capture = cv2.VideoCapture(input_video)
    length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    video_capture.release()

    thread_read = threading.Thread(target=fun_thread_read, args=(input_video, frame_queue, event_stop,))
    thread_read.start()

    thread_write = threading.Thread(target=fun_thread_write, args=(length, fps, out_queue, output_path,))
    thread_write.start()

    start_t = time()

    for _ in range(thread_num):
        thread = threading.Thread(target=fun_thread_safe_predict, args=(frame_queue, out_queue, event_stop,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    thread_read.join()

    thread_write.do_run = False
    thread_write.join()

    end_t = time()
    print(f'Time: {end_t - start_t}')


def my_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('intput_video', type=str)
    parser.add_argument('output_path', type=str)
    parser.add_argument('thread', type=int)
    args = parser.parse_args()
    return args.intput_video, args.output_path, args.thread


if __name__ == "__main__":
    # main('walk.mp4', 'res.mp4', 1)    #101.33534526824951
    # main('walk.mp4', 'res.mp4', 2)    #68.36214351654053
    # main('walk.mp4', 'res.mp4', 3)    #68.71401953697205
    # main('walk.mp4', 'res.mp4', 4)    #61.45627212524414
    # main('walk.mp4', 'res.mp4', 5)    #60.86203360557556
    # main('walk.mp4', 'res.mp4', 6)    #67.06606698036194
    # main('walk.mp4', 'res.mp4', 12)   #70.10418915748596

    main(*my_parser())
