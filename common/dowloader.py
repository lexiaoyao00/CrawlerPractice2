import os
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
# from curl_cffi import requests
from PyQt5.QtWidgets import QProgressBar

from logger import my_logger
class Downloader:
    def __init__(self, threads=10):
        self.threads = threads

    def download_file(self, url, filename, progress_bar:QProgressBar=None, show_console_progress=False):
        """下载单个文件"""
        try:
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024

            if progress_bar is None and show_console_progress:
                progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, unit_divisor=1024)
            elif progress_bar is not None:
                progress_bar.setMaximum(total_size)
                progress_bar.setValue(0)

            with open(filename, 'wb') as file:
                downloaded = 0
                for data in response.iter_content(block_size):
                    if data:
                        file.write(data)
                        downloaded += len(data)
                        if progress_bar is None and show_console_progress:
                            progress_bar.update(len(data))
                        elif progress_bar is not None:
                            progress_bar.setValue(downloaded)

            if progress_bar is None and show_console_progress:
                progress_bar.close()
            # print(f"下载完成: {filename}")
        except Exception as e:
            raise f"下载失败: {filename}, 错误: {e}"

    def download_files(self, urls, directory, progress_bar:QProgressBar=None, show_console_progress=False):
        """批量下载文件"""
        os.makedirs(directory, exist_ok=True)

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            for url in urls:
                filename = os.path.join(directory, os.path.basename(url))
                future = executor.submit(self.download_file, url, filename, progress_bar, show_console_progress)
                futures.append(future)

            if progress_bar is None and show_console_progress:
                progress_bar = tqdm(total=len(futures), unit='file')
                for future in futures:
                    future.result()
                    progress_bar.update(1)
            elif progress_bar is not None:
                progress_bar.setMaximum(len(futures))
                progress_bar.setValue(0)
                for future in futures:
                    future.result()
                    progress_bar.setValue(progress_bar.value() + 1)
            else:
                for future in futures:
                    future.result()