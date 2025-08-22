# 导入外部库
import requests
from bs4 import BeautifulSoup
import time
from requests import RequestException
from urllib.parse import urljoin
import os.path

# 设置请求头
url = f'http://books.toscrape.com/catalogue/page-1.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76'
}

# 创建保存目录
_dir = './images'  # 定义图片保存的目录名为'images'
if not os.path.isdir(_dir):  # 检查目录是否存在
    os.mkdir(_dir)  # 如果不存在则创建目录

# 发送请求
try:
    time.sleep(1)
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 如果出现请求失败会抛出异常

    # 解析图片数据
    soup = BeautifulSoup(response.text, 'html.parser')
    all_books = soup.select('article.product_pod')

    for book in all_books:
        images= book.find('img')
        src = images['src'] # 直接通过属性名作为键访问
        # print(src) # 发现url是相对路径而非绝对路径
        # 使用urljoin进行url路径拼接
        full_url = urljoin('http://books.toscrape.com/', src)
        print(full_url) # 获取完整url

        img_name = os.path.basename(src) #从url路径（\最后一部分）中提取文件名

        try:
            img_response = requests.get(full_url, headers=headers)
            img_response.raise_for_status()

            with open(f'{_dir}/{img_name}.jpg', 'wb') as f: # 文件路径会是: './images/2cdad67c44b002e7ead0cc35693c0e8b.jpg' 图片以二进制形式写入
                f.write(img_response.content)  # 将二进制数据写入文件
                print(f'{img_name}.jpg下载成功')
                time.sleep(1)

        except RequestException as e:
            print(f'下载图片失败: {e}')

except RequestException as e:
    print(f'请求失败{e}')
    exit()

