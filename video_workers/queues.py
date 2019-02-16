from queue import Queue

input_queue = Queue(maxsize=512)
output_queue = Queue(maxsize=512)
input_result_queue = Queue(maxsize=1)
output_result_queue = Queue(maxsize=1)
current_frame_full = Queue(maxsize=1)