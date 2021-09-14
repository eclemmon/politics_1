import multiprocessing
import time


def count_to_ten(queue):
    count = 0
    while True:
        time.sleep(1.3)
        if count < 10:
            count += 1
            queue.put(count)
            print("count to ten: ", count)
        else:
            break



def main():
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=count_to_ten, args=(queue,))
    p.start()
    main_count = 0
    while True:
        time.sleep(0.5)
        if main_count < 10:
            main_count += 1
            queue.put(main_count)
            print("main count: ", main_count)
        else:
            break
    p.join()
    print(dump_queue(queue))

def dump_queue(q):
    q.put(None)
    return list(iter(lambda : q.get(timeout=0.00001), None))


if __name__ == "__main__":
    main()
