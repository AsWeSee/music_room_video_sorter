from threading import Thread

from video_workers.video_grabber import load_video_from_camera
from video_workers.video_writer import write_video
from video_workers.video_processor import process_video


def start_video_threads():
    t1 = Thread(target=load_video_from_camera, args=())
    t1.daemon = True
    t1.start()

    t2 = Thread(target=process_video, args=())
    t2.daemon = True
    t2.start()

    t3 = Thread(target=write_video, args=())
    t3.daemon = True
    t3.start()

    print("1 join")
    t1.join()
    print("2 join")
    t2.join()
    print("3 join")
    t3.join()
    print("end join")

#запуск для обработки данных с камеры
if __name__ == '__main__':
    start_video_threads()
    print("end")