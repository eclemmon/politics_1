import threading
import time


def count_to_ten():
    count = 0
    while True:
        time.sleep(1.3)
        if count <= 10:
            count += 1
            print(count)
        else:
            break


class Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        count_to_ten()
        print("done")
        return True

def main():
    t = Thread()
    t.start()
    main_count = 0
    while True:
        time.sleep(0.5)
        if main_count <= 10:
            main_count += 1
            print(main_count)
        else:
            break

if __name__ == "__main__":
    main()