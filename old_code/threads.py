import threading
import time


def play_audio():
    print('Sleeping 1 second...')
    time.sleep(1)
    print('Done sleeping...')


t1 = threading.Thread(target=play_audio)
t2 = threading.Thread(target=play_audio)

t1.start()
t2.start()

t1.join()
t2.join()