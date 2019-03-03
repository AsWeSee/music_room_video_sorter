import time

import cv2
import numpy as np

from video_workers.queues import input_queue, output_queue, input_result_queue, output_result_queue, current_frame_full


def process_video():


    prev_blurred_image = None
    motion_counter = 0
    motion = False

    counter = 0
    sleeps_count = 0
    while True:

        if counter % 100 == 0:
            print("processor load " + str(input_queue.qsize())+ " " + str(output_queue.qsize()))


        # while (input_queue.empty()):
            # print("processor read sleep")
            # time.sleep(1)

            # Если пришел сигнал что все файлы на входе обработаны, значит пора выходить
        if input_queue.empty() and input_result_queue.qsize() > 0:
            output_result_queue.put(sleeps_count)
            print("processor sleeps count" + str(sleeps_count))
            sleeps_count += 1
            return

        image = input_queue.get()
        full = check_is_full(image)

        if current_frame_full.full():
            current_frame_full.get()
        current_frame_full.put((full, image))

        motion_result, prev_blurred_image = check_motion(prev_blurred_image, image, counter)
        if not full:
            if motion_result:
                motion_counter += 1
                if motion_counter > 10:
                    motion = True
            else:
                motion_counter = 0
                motion = False
        else:
            motion = False

        while (output_queue.full()):
            # print("processor out sleep")
            sleeps_count += 1
            time.sleep(1)

        output_queue.put((image.tostring(), full, motion))
        counter +=1


# можно считать движение в течении 10 кадров. Если оно наблюдается, значит действительно есть
def check_motion(prev_image, image, counter):
    motion = False
    if prev_image is None:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        return False, gray

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    frameDelta = cv2.absdiff(prev_image, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    brit = np.sum(thresh)
    if counter % 100 == 0:
        print("treshold " + str(brit))
        if brit > 100000:
            cv2.imwrite("gray.jpg", gray)
            cv2.imwrite("GaussianBlur.jpg", gray)
            cv2.imwrite("frameDelta.jpg", frameDelta)
            cv2.imwrite("thresh.jpg", thresh)


    return False, gray


def check_is_full(image):
    brit = np.sum(image)

    pixels = 1280 * 720
    pixel_brit = brit / pixels

    if pixel_brit > 200:
        return True
    else:
        return False
