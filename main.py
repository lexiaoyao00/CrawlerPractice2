from process_manage import ProcessManager
from thread_manage import ThreadManager
from spiders import BaiDu,Danbooru

if __name__ == "__main__":
    db = Danbooru()
    db.start_crawling(None)