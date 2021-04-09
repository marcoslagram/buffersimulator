import threading
from time import sleep
import random

global buffer_level
buffer_level = 0

lock = threading.Lock()

def main():

    creator_thread = threading.Thread(target=creator)
    consumer_thread = threading.Thread(target=consumer)

    consumer_thread.start()
    creator_thread.start()

    consumer_thread.join()
    creator_thread.join()


def creator():
    global buffer_level
    min = 0.75
    max = 1.25
    while True:
        sleep_time = min + (max-min)*random.random()
        sleep(sleep_time)
        lock.acquire()
        buffer_level += 1
        represent_buffer(buffer_level)
        lock.release()
        if buffer_level >= 20:
            print("Buffer overflow so EXIT")
            break
        
def consumer():
    global buffer_level
    first_time = True
    initializing = True
    while True:
        lock.acquire()
        if buffer_level > 3:
            initializing = False

        if not initializing:
            buffer_level -= 1
        represent_buffer(buffer_level)
        if buffer_level < 0:
            print("Buffer empty so EXIT")
            lock.release()
            break
        lock.release()
        sleep(1)

def represent_buffer(buffer_level):
    print(buffer_level, end='')
    print (" [", end='')
    for i in range (0, buffer_level):
        print("#", end='')
    for i in range (buffer_level, 20):
        print(" ", end='')
    print("]", end='\r')

if __name__ == "__main__":
    main()