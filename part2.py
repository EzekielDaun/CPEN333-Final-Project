# Group #: G35
# Student Names: Yifei Liu, Liying Xian

import threading
import queue
import time, random


def consumerWorker(queue: queue.Queue):
    """target worker for a consumer thread"""

    while True:
        # wait for an item from the queue
        item = queue.get()
        print(f"Item consumed: {item}")
        # signal that the task is done
        queue.task_done()
        # wait for 100-300ms
        time.sleep(round(random.uniform(0.1, 0.3), 2))


def producerWorker(queue: queue.Queue):
    """target worker for a producer thread"""

    number_of_items = 3  # items per producer thread produces
    for _ in range(number_of_items):
        # generate a random integer between 1 and 100
        item = random.randint(1, 100)
        # put the item in the queue
        queue.put(item)
        print(f"Item produced: {item}")
        # wait for 100-300ms
        time.sleep(round(random.uniform(0.1, 0.3), 2))


if __name__ == "__main__":
    buffer = queue.Queue()

    # 4 producer threads
    producers = [
        threading.Thread(target=producerWorker, args=(buffer,)) for _ in range(4)
    ]

    # 5 consumer threads
    consumers = [
        threading.Thread(target=consumerWorker, args=(buffer,), daemon=True)
        for _ in range(5)
    ]

    # start all producers
    for p in producers:
        p.start()

    # start all consumers
    for c in consumers:
        c.start()

    # wait for all producers to finish
    for p in producers:
        p.join()

    # wait for all daemon consumers to "finish" (consume all items in the buffer queue)
    buffer.join()

    print("All Done!")
