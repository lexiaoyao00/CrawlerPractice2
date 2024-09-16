import threading
import time

from logger import main_logger
class ThreadManager(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ThreadManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.threads = []
        self.terminate_events = {}

    def add_thread(self, target, args=None):
        terminate_event = threading.Event()
        if args is None:
            thread = threading.Thread(target=target, args=(terminate_event,))
        else:
            thread = threading.Thread(target=target, args=(args, terminate_event))
        self.threads.append(thread)
        self.terminate_events[thread] = terminate_event
        thread.start()
    
    def terminate_thread(self, thread_index):
        if thread_index < len(self.threads):
            thread = self.threads[thread_index]
            self.terminate_events[thread].set()
        else:
            # print(f"Invalid thread index: {thread_index}")
            main_logger.debug(f"Invalid thread index: {thread_index}")

    def terminate_threads(self):
        # self.terminate_event.set()
        for terminate_event in self.terminate_events.values():
            terminate_event.set()

    def wait_for_threads(self):
        for thread in self.threads:
            thread.join()

# def worker(args, terminate_event):
#     num = args[0]
#     print(f"Worker {num} started")
#     while not terminate_event.is_set():
#         # 执行任务
#         print("do something before terminate")
#         time.sleep(1)
#     print(f"Worker {num} terminated")

# if __name__ == "__main__":
#     manager = ThreadManager()

#     # 添加线程
#     manager.add_thread(worker, args=(1,))
#     manager.add_thread(worker, args=(2,))
#     manager.add_thread(worker, args=(3,))

#     # 等待一段时间
#     time.sleep(5)

#     # 终止线程
#     manager.terminate_threads()

#     # 等待线程完成
#     manager.wait_for_threads()
