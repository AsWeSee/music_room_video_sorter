import os
import time
import cv2
import subprocess as sp
from video_workers.queues import output_result_queue, output_queue
from video_workers.output_paths import Paths


def write_video():
    print("start write")

    paths = Paths("music room camera grabber")

    path = paths.path
    path_full = paths.path_full
    path_empty = paths.path_empty
    path_dark_motion = paths.path_dark_motion

    fps = 13.0
    width = 1280.0
    height = 720.0
    format = "XVID"
    fourcc = cv2.VideoWriter_fourcc(*format)

    pipe_write = new_out_pipe(path_empty)

    count = 0
    start = time.time()

    full = False
    dark_motion = False
    room_was_full = False
    room_was_dark_motion = False
    sleeps_count = 0
    check = False
    while True:
        if output_result_queue.qsize() > 0 or os.path.isfile(path + "\\end.txt"):
            break

        if not os.path.isfile(path + "\\check.txt"):
            check = False

        if os.path.isfile(paths.path + "\\check.txt") and check == False:
            check = True
            if dark_motion:
                pipe_write.stdin.close()
                pipe_write = new_out_pipe(path_dark_motion)
            elif full:
                pipe_write.stdin.close()
                pipe_write = new_out_pipe(path_full)
            elif not full:
                pipe_write.stdin.close()
                pipe_write = new_out_pipe(path_empty)

        # while (output_queue.empty()):
        #     print("writer sleep")
        #     time.sleep(1)
        #     if output_result_queue.qsize() > 0:
        #         sleeps_count += 1
        #         print("writer sleeps count" + str(sleeps_count))
        #         return

        image, full, dark_motion = output_queue.get()
        if dark_motion and not room_was_dark_motion:
            pipe_write.stdin.close()
            pipe_write = new_out_pipe(path_dark_motion)
        elif full and not room_was_full:
            pipe_write.stdin.close()
            pipe_write = new_out_pipe(path_full)
        elif not full and room_was_full:
            pipe_write.stdin.close()
            pipe_write = new_out_pipe(path_empty)

        pipe_write.stdin.write(image)
        pipe_write.stdin.flush()
        image = None

        # if count % 100 == 0:
        #     print("writer count " + str(count))

        room_was_full = full
        room_was_dark_motion = dark_motion
        count += 1

    timeres = time.time() - start
    print("time = " + str(timeres))
    fps = count / timeres
    print(str(fps))

    if pipe_write:
        pipe_write.stdin.close()
        if pipe_write.stderr is not None:
            pipe_write.stderr.close()
            pipe_write.wait()

def new_out_pipe(path):
    filename = calculate_filename(path)
    command = ["ffmpeg.exe",
               '-y',  # (optional) overwrite output file if it exists
               '-f', 'rawvideo',
               '-vcodec', 'rawvideo',
               '-s', '1280x720',  # size of one frame
               '-pix_fmt', 'rgb24',
               '-r', '15',  # frames per second
               '-i', '-',  # The imput comes from a pipe
               '-an',  # Tells FFMPEG not to expect any audio
               '-vcodec', 'h264_nvenc',  # h264_nvenc
               '-b:v', '400k',
               '-vf', 'colorchannelmixer=rr=0:rb=1:br=1:bb=0',
               filename]
                # 'D:\\music room camera grabber\\output_videofile.mp4']

    pipe_write = sp.Popen(command, stdin=sp.PIPE, stderr=None, bufsize=10 ** 2)
    return pipe_write

def calculate_filename(path):
    filecount = 1
    filename = "filename" + "_" + str(filecount) + ".avi"
    while os.path.isfile(path + "\\" + filename):
        filecount += 1
        filename = "filename" + "_" + str(filecount) + ".avi"

    return path + "\\" + filename
