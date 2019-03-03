import os
import sys
import time
import cv2

import video_workers.find_camera as find_camera
from video_workers.output_paths import Paths
from video_workers.queues import input_queue, input_result_queue

from os import listdir
from os.path import isfile, join

stored_ip = "10.240.17.168"

def load_video_from_camera():
    print("start load")
    paths = Paths("music room")
    cap = connect_to_camera()

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
    format = "XVID"
    fourcc = cv2.VideoWriter_fourcc(*format)
    print(width)
    print(height)
    print(fps)

    frames_count = 0
    while True:

        if os.path.isfile(paths.path_income + "end.txt"):
            cap.release()
            input_result_queue.put(True)
            break

        ret, frame = cap.read()

        if not ret:
            print("ret is none")
            time.sleep(5)
            cap = connect_to_camera()
            continue

        frames_count += 1
        if frames_count % 100 == 0:
            print("reader frames_count " + str(frames_count))

        while (input_queue.full()):
            print("reader sleep")
            time.sleep(1)
        input_queue.put(frame)

    input_result_queue.put(True)


def connect_to_camera():
    print("find_camera")
    ip = find_camera.find_camera()
    none_count = 0
    while ip is None:
        time.sleep(100)
        none_count += 1
        print("ip is None " + str(none_count))
        ip = find_camera.find_camera()
    print("new ip " + ip)
    stored_ip = ip
    connection_string = find_camera.form_rtsp_connection_string(ip)
    return cv2.VideoCapture(connection_string)


def load_video_from_files():

    paths = Paths("music room")
    filenames = [f for f in listdir(paths.path_income) if isfile(join(paths.path_income, f))]
    filenames_count = len(filenames)

    filenum = 0
    for file in filenames:
        filenum += 1
        print("New file started to processing: " + file)

        start = time.time()
        cap = cv2.VideoCapture(paths.path_income + file)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
        pixels = width * height


        frames_count = 0
        was_opened = False
        while(cap.isOpened()):
            was_opened = True
            while(input_queue.full()):
                #print("reader sleep")
                time.sleep(1)

            ret, frame = cap.read()

            frames_count += 1

            if not ret:
                end = time.time()
                print("ret is none. frames_count " + str(frames_count))
                print("Time spended " + str(end - start))
                print("fps: " + str(float(frames_count)/(end - start)))
                break

            input_queue.put(frame)

            if frames_count % 100 == 0:
                print(file + " " + str(filenum) + " from " + str(filenames_count) + ". " + str(frames_count) + " " + str(input_queue.qsize()))

        cap.release()
        if was_opened:
            os.rename(paths.path_income + file, paths.path_corrects + file)
        else:
            os.rename(paths.path_income + file, paths.path_errors + file)

    input_result_queue.put(True)
