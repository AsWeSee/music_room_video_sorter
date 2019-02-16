import time
from threading import Thread
from queue import Queue
import cv2
import numpy as np
import os
start_time = time.time()
out = None

room_queue = Queue(maxsize=512)
result = Queue(maxsize=1)

fps = ""
width = ""
height = ""
format = "XVID"
fourcc = cv2.VideoWriter_fourcc(*format)

t = Thread(target=read_files, args=())
t.daemon = True
t.start()

time.sleep(1)
room_was_empty = True
filenum = 0
j = 0
while result.empty() or not room_queue.empty() :

    while (room_queue.empty()):
        print("writer sleep " + str(result.empty()))
        time.sleep(1)
        if not result.empty():
            break

    (room_empty, frame, filename, fps, width, height) = room_queue.get()
    j += 1

    if out is None:
        room_was_empty = room_empty
        if room_empty:
            dir_name = "D:\\music room\\3 empty"
        else:
            dir_name = "D:\\music room\\2 full"

        out = cv2.VideoWriter(dir_name + "\\" + filename + "_" + str(filenum) + ".avi", fourcc, fps, (int(width), int(height)))
        filenum += 1

    if not room_empty and room_was_empty:
        out.release()
        room_was_empty = False
        out = cv2.VideoWriter("D:\\music room\\2 full\\" + filename + "_" + str(filenum) + ".avi", fourcc, fps, (int(width), int(height)))
        filenum += 1

    if room_empty and not room_was_empty:
        out.release()
        room_was_empty = True
        out = cv2.VideoWriter("D:\\music room\\3 empty\\" + filename + "_" + str(filenum) + ".avi", fourcc, fps, (int(width), int(height)))
        filenum += 1

    # if j % 100 == 0:
    #     print("writer " + str(j))

    out.write(frame)

out.release()
elapsed_time = time.time() - start_time

print("Elapsed time: " + str(elapsed_time))
print("finished")