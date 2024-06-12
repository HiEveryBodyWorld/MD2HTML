import markdown
import os
import shutil
from bs4 import BeautifulSoup
import uuid
import argparse


def md2html(src_folder, dest_folder):
    for item in os.listdir(src_folder):
        item_path = os.path.join(src_folder, item)
        dest_item_path = os.path.join(dest_folder, item)

        # 如果是文件夹，则递归调用函数处理子文件夹
        if os.path.isdir(item_path):
            os.makedirs(dest_item_path, exist_ok=True)
            md2html(item_path, dest_item_path)

        # 如果是文件且以.md结尾，则复制并转换文件
        elif os.path.isfile(item_path) and item.endswith('.md'):
            dest_item_path = dest_item_path[:-3] + '.html'  # 替换文件后缀为.html
            with open(item_path, 'r', encoding='utf-8') as md_file:
                md_content = md_file.read()
            html_content = markdown.markdown(md_content)
            # 添加HTML结构
            # 使用BeautifulSoup库解析html
            soup = BeautifulSoup(html_content, 'html.parser')

            # 遍历所有的标签，并添加id属性
            for tag in soup.find_all(True):
                tag['id'] = str(uuid.uuid4())  # 生成一个随机的UUID作为id

            # 输出添加id属性后的html
            html_with_uuid = str(soup)

            # 手动添加<html>, <head>, <title>, <meta> 和<body>标签
            html_full_page = f"<!DOCTYPE html>\n<html id='{uuid.uuid4()}'>\n<head id='{uuid.uuid4()}'>\n<title id='{uuid.uuid4()}'>{os.path.basename(item_path)}</title>\n<meta id='{uuid.uuid4()}' charset='UTF-8'>\n</head>\n<body id='{uuid.uuid4()}'>\n{html_with_uuid}\n</body>\n</html>"

            with open(dest_item_path, 'w', encoding='utf-8') as html_file:
                html_file.write(html_full_page)

        # 非md文件正常复制
        else:
            shutil.copy2(item_path, dest_item_path)


def main():
    parser = argparse.ArgumentParser(description='Convert markdown to html.')
    parser.add_argument('src_folder', type=str, help='The source folder that contains the markdown files.')
    parser.add_argument('dest_folder', type=str,
                        help='The destination folder that will store the generated html files.')

    args = parser.parse_args()

    md2html(args.src_folder, args.dest_folder)


if __name__ == "__main__":
    main()
