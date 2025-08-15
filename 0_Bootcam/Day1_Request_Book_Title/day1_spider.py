# 1 导入库
import requests
from bs4 import BeautifulSoup

# 2 设置请求头模拟浏览器 请求数据
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 11.0; Win64; x64)'}
response = requests.get('http://books.toscrape.com/', headers= headers)

# 3 解析数据
soup = BeautifulSoup(response.text,'html.parser')

# 确认状态码正常
if response.status_code == 200:
    book_titles = []

    # 找到所有书籍容器
    all_books = soup.select('article.product_pod')

    # 遍历每个书籍容器
    for book in all_books:
        # 在当前书籍中查找带title属性的<a>标签
        title_tag = book.find('a', title=True)

        # 如果找到了标签
        if title_tag:
            # 提取title属性值
            book_title = title_tag['title']
            # 添加到结果列表
            book_titles.append(book_title)
    print(book_titles)
else:
    print(f'状态异常，状态码：{response.status_code}')