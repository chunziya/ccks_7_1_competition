# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import csv

''' 
解析页面1
'''


def readXML_1():
    print("---------page_1 开始解析--------")

    # 存储文件
    # fw = open("../out/page_1.txt", 'w', encoding='utf-8')
    f = open("../entity_pages_1.xml", 'r', encoding='utf-8')
    text = f.read()
    pat_1 = re.compile(r'<!DOCTYPE html>\n<!--STATUS OK-->\n<html>')
    text = pat_1.sub('', text)
    pages = text.split('</page>')
    print("共 " + str(len(pages)) + " 条")

    # 开始整理
    title_count = 0
    meta_count = 0
    for p in tqdm(pages):
        # 解析生成soup
        p += '</page>'
        soup = BeautifulSoup(p, "xml")

        title = soup.find('title')
        meta = soup.find('meta', attrs={'name': 'description'})
        if title:
            title_count += 1
        if meta:
            meta_count += 1
        # if title and meta:
        #     fw.write(
        #         title.string + ":::" + meta['content'].replace('\t', '').replace('\n', '').replace('\r', '') + "\n")
    f.close()
    # fw.close()

    print('title_count: ' + str(title_count))
    print('meta_count: ' + str(meta_count))
    print("page_1 解析完毕！")


''' 
解析页面2
'''


def readXML_2():
    print("--------page_2 开始解析--------")
    # fw = open("../out/page_2.txt", 'w', encoding='utf-8')
    f = open("../entity_pages_2.xml", 'r', encoding='utf-8')
    text = f.read()

    # 解析生成soup
    soup = BeautifulSoup(text, "lxml")
    pages = soup.find_all("page")
    print("共 " + str(len(pages)) + " 条")

    title_count = 0
    meta_count = 0
    for p in tqdm(pages):
        title = p.find('title')
        meta = p.find('meta', attrs={'name': 'description'})
        if title:
            title_count += 1
        if meta:
            meta_count += 1
        # if title and meta:
        #     fw.write(
        #         title.string + ":::" + meta['content'].replace('\t', '').replace('\n', '').replace('\r', '') + "\n")
    f.close()
    # fw.close()

    print('title_count: ' + str(title_count))
    print('meta_count: ' + str(meta_count))
    print("page_2 解析完毕！")


''' 
解析页面3
'''


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def readXML_3():
    print("--------page_3 开始解析--------")
    puc = ['。', '，']

    fw = open("../out/page_3.txt", 'w', encoding='utf-8')
    f = open("../entity_pages_3.xml", 'r', encoding='utf-8')
    text = f.read()

    soup = BeautifulSoup(text, "lxml")
    pages = soup.find_all("page")
    print("共" + str(len(pages)) + "条")

    title_count = 0
    meta_count = 0
    for p in tqdm(pages):
        title = p.find('title')
        text = p.find('text')
        text = text.string

        if title:
            title_count += 1
        if text:
            meta_count += 1
        inial_text = []
        if title and text:
            flag = False
            for word in text:
                if word == '（' or flag:
                    flag = True
                    if flag:
                        inial_text.append(word)
                    if word == '）':
                        flag = False
                        continue
                elif word in puc or is_Chinese(word):
                    inial_text.append(word)
                elif word == '!':
                    continue
                else:
                    word = ' '
                    inial_text.append(word)

            descreption = ''.join(inial_text)
            descreption = re.sub(' +', '', descreption)
        fw.write(
            title.string + ":::" + descreption.replace('\t', '').replace('\n', '').replace('\r', '') + "\n")
    f.close()
    fw.close()

    print('title_count: ' + str(title_count))
    print('meta_count: ' + str(meta_count))
    print("page_3 解析完毕！")


''' 
解析页面4
'''


def readXML_4():
    print("--------page_4 开始解析--------")
    # fw = open("../out/page_4.txt", 'w', encoding='utf-8')
    f = open("../entity_pages_4.xml", 'r', encoding='utf-8')
    text = f.read()

    # 解析生成soup
    soup = BeautifulSoup(text, "lxml")
    pages = soup.find_all("page")
    print("共" + str(len(pages)) + "条")

    # 开始解析存储
    title_count = 0
    meta_count = 0
    for p in tqdm(pages):
        title = p.find('title')
        meta = p.find('meta', attrs={'name': 'description'})
        if title:
            title_count += 1
        if meta:
            meta_count += 1
            # fw.write(
            #     title.string + ":::" + meta['content'].replace('\t', '').replace('\n', '').replace('\r', '') + "\n")
    f.close()
    # fw.close()
    print('title_count: ' + str(title_count))
    print('meta_count: ' + str(meta_count))
    print("page_4 解析完毕！")


''' 
合并测试集结果
'''


def combine_entity_validation(file_list):
    print("--------验证集数据--------")
    csvfile = open('../out/test_data.csv', 'w+', newline='', encoding='utf-8')
    test_file = open("../entity_validation.txt", 'r', encoding='utf-8')
    test_entity = [line.strip('\n') for line in test_file.readlines()]
    print("验证集实体数据共 " + str(len(test_entity)) + " 条")

    # 实体-描述字典
    des_dic = {}
    for file in file_list:
        f = open('../out/' + file, 'r', encoding='utf-8')
        for line in f.readlines():
            data = line.split(':::')
            entity = data[0].strip()
            des = data[1].strip().replace(' ', '')
            des_dic[entity] = des
        f.close()

    count = 0
    headers = ['name', 'descreption']
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(headers)
    for entity in test_entity:
        if entity in des_dic:
            writer.writerow([entity, des_dic[entity]])
            count += 1
        else:
            writer.writerow([entity, ' '])

    csvfile.close()
    print("最终整理数据 " + str(count) + " 条，合并结束！")


''' 
合并解析结果
'''


def combine(file_list):
    print("--------训练集数据--------")
    csvfile = open('../out/train_data.csv', 'w+', newline='', encoding='utf-8')

    # 实体-类型字典
    type_dic = {}
    type_file = open('../entity_type.txt', 'r', encoding='utf-8')
    for line in type_file.readlines():
        data = line.split('\t')
        entity = data[0].strip()
        type_dic[entity] = data[1].strip()
    type_file.close()
    print("实体-类别数据共 " + str(len(type_dic)) + " 条")

    # 实体-描述字典
    des_dic = {}
    dup_count = 0  # 重复描述统计
    for file in file_list:
        des_file = open('../out/' + file, 'r', encoding='utf-8')
        for line in des_file.readlines():
            data = line.split(':::')
            entity = data[0].strip()
            des = data[1].strip().replace(' ', '')
            if entity not in des_dic:
                des_dic[entity] = des
            else:
                des_dic[entity] = des + des_dic[entity]
                dup_count += 1
        des_file.close()
    print("实体-描述数据共 " + str(len(des_dic)) + " 条，" + "重复描述有 " + str(dup_count) + " 条")

    # 合并整理
    count = 0
    headers = ['name', 'type', 'descreption']
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(headers)
    for entity in type_dic.keys():
        if entity in des_dic:
            writer.writerow([entity, type_dic[entity], des_dic[entity]])
            count += 1
        else:
            writer.writerow([entity, type_dic[entity], ' '])

    csvfile.close()
    print("最终整理数据 " + str(count) + " 条，合并结束！\n")


if __name__ == "__main__":
    readXML_1()
    readXML_2()
    readXML_3()
    readXML_4()
    filelist = ['page_1.txt', 'page_2.txt', 'page_3.txt', 'page_4.txt']
    combine(filelist)
    combine_entity_validation(filelist)
