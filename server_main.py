from threading import Thread

from video_workers.video_grabber import load_video_from_camera
from video_workers.video_writer import write_video
from video_workers.video_processor import process_video


def start_video_threads():
    t = Thread(target=load_video_from_camera, args=())
    t.daemon = True
    t.start()

    t = Thread(target=process_video, args=())
    t.daemon = True
    t.start()

    t = Thread(target=write_video, args=())
    t.daemon = True
    t.start()

#запуск для обработки данных с камеры
if __name__ == '__main__':
    start_video_threads()