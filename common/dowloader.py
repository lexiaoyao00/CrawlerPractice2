import os
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
# from curl_cffi import requests

from logger import my_logger
class Downloader:
    def __init__(self, threads=10):
        self.threads = threads

    def download_file(self, url, filename, show_progress=True):
        """下载单个文件"""
        try:
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            progress = tqdm(total=total_size, unit='iB', unit_scale=True, unit_divisor=1024, disable=not show_progress)

            with open(filename, 'wb') as file:
                for data in response.iter_content(block_size):
                    if data:
                        file.write(data)
                        progress.update(len(data))
                        progress.set_postfix(file=filename)

            progress.close()
            # print(f"下载完成: {filename}")
        except Exception as e:
            # print(f"下载失败: {filename}, 错误: {e}")
            my_logger.error(f"下载失败: {filename}, 错误: {e}")

    def download_files(self, urls, directory, show_progress=True):
        """批量下载文件"""
        os.makedirs(directory, exist_ok=True)

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            for url in urls:
                filename = os.path.join(directory, os.path.basename(url))
                future = executor.submit(self.download_file, url, filename, show_progress=False)
                futures.append(future)

            if show_progress:
                progress = tqdm(total=len(futures), unit='file')
                for future in futures:
                    future.result()
                    progress.update(1)
            else:
                for future in futures:
                    future.result()