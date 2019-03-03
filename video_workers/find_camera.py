import time
from queue import Queue
from threading import Thread
import urllib
from urllib.error import HTTPError, URLError
import cv2

# f = open("login_files\\camera_login_pass.txt")
# camera_str = f.read().split()
# camera_login = camera_str[0]
# camera_password = camera_str[1]
# f.close()

ip_net_from = 17
ip_net_to = 23
ip_range = 256
queue_size = (ip_net_to - ip_net_from) * ip_range
results = Queue(maxsize=queue_size)
threads = []

def check(ip1, ip2):
    ip = str(ip1) + '.' + str(ip2)
    # print(ip)
    try:
        urllib.request.urlopen(
            'http://10.240.' + ip + ':13147/videostream.cgi?loginuse=' + camera_login + '&loginpas=' + camera_password,
            timeout=1)
    except HTTPError as error:
        print('Data not retrieved because %s\nURL: %s'.format(error, ip))
    except URLError as error:
        results.put((ip, False))
        return

    cap = cv2.VideoCapture(
        'http://10.240.' + ip + ':13147/videostream.cgi?loginuse=' + camera_login + '&loginpas=' + camera_password)
    ret, frame = cap.read()
    cap.release()
    # brit = np.sum(frame)
    # print(brit)

    results.put((ip, True))
    cv2.imwrite(ip + " rec_frame.jpg", frame)


def find_camera():
    threads = []
    for ip1 in range(ip_net_from, ip_net_to):
        for ip2 in range(255):
            t = Thread(target=check, args=((ip1, ip2)))
            t.daemon = True
            t.start()
            threads.append(t)

    results_count = 0
    while results_count < queue_size - 1:
        result = results.get()
        # print(result)
        results_count += 1
        if result[1] == True:
            return result[0]

    for t in threads:
        t.join()
    return None


def form_http_connection_string(ip):
    f = open("login_files\\camera_login_pass.txt")
    camera_str = f.read().split()
    camera_login = camera_str[0]
    camera_password = camera_str[1]
    f.close()

    return 'http://10.240.' + ip + ':13147/videostream.cgi?loginuse=' + camera_login + '&loginpas=' + camera_password


def form_rtsp_connection_string(ip):
    f = open("login_files\\camera_login_pass.txt")
    camera_str = f.read().split()
    camera_login = camera_str[0]
    camera_password = camera_str[1]
    f.close()

    return 'rtsp://' + camera_login + ':' + camera_password + '@10.240.' + ip + ':10554/tcp/av0_0'
