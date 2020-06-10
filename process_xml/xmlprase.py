# -*- coding:utf-8 -*-
from xml.dom.minidom import parse
from bs4 import BeautifulSoup
from tqdm import tqdm
import re


# 文件1

def readXML_1():
    # 存储文件
    fw = open("page_1.txt", 'w', encoding='utf-8')
    f = open("entity_pages_1_copy.xml", 'r', encoding='utf-8')
    text = f.read()
    pages = text.split('</page>')
    print(len(pages))

    # 开始整理
    for p in tqdm(pages):
        # 解析生成soup
        p += '</page>'
        soup = BeautifulSoup(p, "xml")

        title = soup.find('title')
        meta = soup.find('meta', attrs={'name': 'description'})
        if title and meta:
            content = meta['content'].replace('\t', '').replace('\n', '').replace('\r', '').replace('...', '')
            fw.write(
                title.string + ":::" + content + "\n")
    f.close()
    fw.close()

    # # test
    # page_1 = soup.page
    # title = page_1.title
    # meta = page_1.find('meta', attrs={'name': 'description'})
    # print(title.string)
    # print(meta['content'])


# 文件3

def content_filter(text):
    pat_1 = re.compile(r'(<ref )(.*)(</ref>)')
    pat_2 = re.compile(r'(<ref>)(.*)(</ref>)')
    # pat_3 = re.compile(r'({\\|)(.*)(\\|})')
    text = pat_1.sub('', text)
    text = pat_2.sub('', text)
    # text = pat_3.sub('',text)
    return text


def readXML_3():
    # 存储文件
    f = open("../page_3.txt", 'w', encoding='utf-8')

    # xml文档解析
    doc = parse("pages_xml/entity_pages_3.xml")
    root = doc.documentElement
    print(root.nodeName)

    pages = root.getElementsByTagName("page")
    for page in pages:
        title = page.getElementsByTagName("title")[0]
        text = page.getElementsByTagName("text")[0]
        name = title.childNodes[0].data.strip()
        content = text.childNodes[0].data.strip()
        content = content_filter(content)
        f.write(name + ':::' + content + '\n')
    f.close()


if __name__ == "__main__":
    # readXML_1()
    readXML_3()
