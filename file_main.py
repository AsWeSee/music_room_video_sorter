import time
from threading import Thread

from video_workers.video_grabber import load_video_from_files
from video_workers.video_writer import write_video
from video_workers.video_processor import process_video


def start_video_threads():
    t = Thread(target=load_video_from_files, args=())
    t.daemon = True
    t.start()

    t = Thread(target=process_video, args=())
    t.daemon = True
    t.start()

    t = Thread(target=write_video, args=())
    t.daemon = True
    t.start()

#запуск для работы из файлов
if __name__ == '__main__':
    start_time = time.time()

    start_video_threads()

    elapsed_time = time.time() - start_time

    print("Elapsed time: " + str(elapsed_time))
    print("finished")
