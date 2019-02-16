import os
import sys
import time
import cv2

import video_workers.find_camera as find_camera
from video_workers.output_paths import Paths
from video_workers.queues import input_queue, input_result_queue

from os import listdir
from os.path import isfile, join

path = "D:\\music room\\1 from camera"

def load_video_from_camera():
    print("start load")
    paths = Paths("music room camera grabber")
    cap = connect_to_camera()

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
    format = "XVID"
    fourcc = cv2.VideoWriter_fourcc(*format)
    print(width)
    print(height)
    print(fps)

    count = 0
    while True:

        if os.path.isfile(paths.path + "\\end.txt"):
            cap.release()
            input_result_queue.put(True)
            break

        ret, frame = cap.read()

        if not ret:
            print("ret is none")
            time.sleep(5)
            cap = connect_to_camera()
            continue

        count +=1
        if count % 100 == 0:
            print("reader count " + str(count))

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
        none_count +=1
        print("ip is None " + str(none_count))
        ip = find_camera.find_camera()
    print("new ip " + ip)
    connection_string = find_camera.form_rtsp_connection_string(ip)
    return cv2.VideoCapture(connection_string)


def load_video_from_files():

    filenames = [f for f in listdir(path) if isfile(join(path, f))]
    filenum = 0

    for file in filenames:
        filenames_count = len(filenames)
        filenum += 1
        print(file)

        start = time.time()
        cap = cv2.VideoCapture(path + file)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
        pixels = width * height

        #cap = cv2.VideoCapture("rtsp://operator1:123412349qQ@10.240.16.11:10554/tcp/av0_0")
        count = 0

        was_opened = False
        while(cap.isOpened()):
            was_opened = True
            while(input_queue.full()):
                #print("reader sleep")
                time.sleep(1)

            ret, frame = cap.read()

            count += 1


            if not ret:
                end = time.time()
                print("ret is none. count " + str(count))
                print("Time spended " + str(end - start))
                print("fps: " + str(float(count)/(end - start)))
                break

            input_queue.put(frame)

            # if count % 100 == 0:
                # print(file + " " + str(filenum) + " from " + str(filenames_count) + ". " + str(count) + " " + str(room_queue.qsize()))

        cap.release()
        if was_opened:
            os.rename(path + file, 'D:\\music room\\4_1 corrects' + file)
        else:
            os.rename(path + file, 'D:\\music room\\4 error\\' + file)


    result.put(True)