import time
import os
from multiprocessing import Process
import threading
from threading import current_thread
def task_p(x):
    time.sleep(2)
    print(f"Sub processes - {os.getpid()}: task - {x}: Result - {2**x})")

def run_single_process():
    print("**** single process ****")
    print(f"main process - {os.getpid()}")
    start = time.time()
    for i in range(10):
        task_p(i)
    end = time.time()
    print(f"main process - {os.getpid()} taken - {end - start:.3f}s")
def run_multi_process():
    print("**** multi process ****")
    print(f"main process - {os.getpid()}")
    start = time.time()
    # p1 = Process(target=task_p, args=(1,))
    # p2 = Process(target=task_p, args=(2,))
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()
    # for i in range(10):
    #     p = Process(target=task_p, args=(i,))
    #     p.start()
    #     p.join()
    processes = []
    for i in range(32):
        p = Process(target=task_p, args=(i,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    end = time.time()
    print(f"main process - {os.getpid()} taken - {end - start:.3f}s")
def task_t(x):
    time.sleep(2)
    print(f"Sub thread - {current_thread().name}: task - {x}: Result - {2**x})")
def run_multiple_threads():
    print("**** multiple threads ****")
    print(f"main process - {os.getpid()}")
    start = time.time()
    thread_p = []
    for i in range(32):
        t = threading.Thread(target=task_t, args=(i,))
        t.start()
        thread_p.append(t)
    for t in thread_p:
        t.join()

    end = time.time()
    print(f"main process - {os.getpid()} taken - {end - start:.3f}s")


if __name__ == "__main__":
    run_multi_process()
    run_multiple_threads()
