from process_manage import ProcessManager
from spiders import BaiDu

if __name__ == "__main__":
    pm = ProcessManager()
    bd = BaiDu()
    pm.add_process(bd.start_crawling,None)

    pm.wait_for_processes()