# 1 导入库
import requests
from bs4 import BeautifulSoup
import csv
import time

# 2 发送请求函数
def send_request():
    # 创建csv并写入表头
    with open('books.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Price'])

    for page_num in range(1, 11):
        url = f'http://books.toscrape.com/catalogue/page-{page_num}.html'
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76'
        }

        try:
            time.sleep(1)
            response = requests.get(url, headers=headers)
            response.raise_for_status() # 如果出现请求失败会抛出异常

            # 解析当前页面的数据并保存
            parse_and_save_data(response.text)

            print(f"已处理第 {page_num} 页")

        except requests.exceptions.RequestException as e:
            print(f"第{page_num}请求失败: {e}")
            continue

# 3 解析并保存数据函数
def parse_and_save_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    # 查找所有书籍元素
    all_books = soup.select('article.product_pod')

    with open('books.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        for book in all_books:
            # 提取书名
            title_tag = book.find('a', title=True)
            if title_tag and 'title' in title_tag.attrs:
                book_title = title_tag['title']

            # 提取价格
            price_tag = book.find('p', class_='price_color')
            if price_tag:
                book_price = price_tag.get_text() #获取文本内容

            # 写入CSV
            writer.writerow([book_title, book_price])


if __name__ == "__main__":
    send_request()
    print("爬取完成！数据已保存到 books.csv")
