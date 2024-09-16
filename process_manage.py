import multiprocessing
import time

from logger import main_logger

class ProcessManager(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ProcessManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.processes = []
        # self.terminate_event = multiprocessing.Event()
        self.terminate_events = {}

    def add_process(self, target, args=None):
        # process = multiprocessing.Process(target=target, args=(args,self.terminate_event))
        # self.processes.append(process)
        # process.start()

        terminate_event = multiprocessing.Event()
        if args is None:
            process = multiprocessing.Process(target=target, args=(terminate_event,))
        else:
            process = multiprocessing.Process(target=target, args=(args, terminate_event))
        self.processes.append(process)
        self.terminate_events[process] = terminate_event
        process.start()

    def terminate_process(self, process_index):
        if process_index < len(self.processes):
            process = self.processes[process_index]
            self.terminate_events[process].set()
        else:
            # print(f"Invalid process index: {process_index}")
            main_logger.debug(f"Invalid process index: {process_index}")

    def terminate_processes(self):
        # self.terminate_event.set()
        for terminate_event in self.terminate_events.values():
            terminate_event.set()

    def wait_for_processes(self):
        for process in self.processes:
            process.join()


# def worker(args,terminate_event):
#     num = args[0]
#     print(f"Worker {num} started")
#     while not terminate_event.is_set():
#         # 执行任务
#         print("do something before terminate")
#         time.sleep(1)
#     print(f"Worker {num} terminated")

# if __name__ == "__main__":
#     manager = ProcessManager()

#     # 添加进程
#     manager.add_process(worker, args=(1,))
#     manager.add_process(worker, args=(2,))
#     manager.add_process(worker, args=(3,))

#     # 等待一段时间
#     time.sleep(5)

#     # 终止进程
#     manager.terminate_processes()

#     # 等待进程完成
#     manager.wait_for_processes()
