from process_manage import ProcessManager
from thread_manage import ThreadManager
from spiders import BaiDu,Danbooru

if __name__ == "__main__":
    pm = ProcessManager()
    tm = ThreadManager()
    # bd = BaiDu()
    db = Danbooru()
    # db.start_crawling(None)

    # pm.add_process(db.start_crawling,None)
    # pm.wait_for_processes()

    tm.add_thread(db.start_crawling,None)
    tm.wait_for_threads()