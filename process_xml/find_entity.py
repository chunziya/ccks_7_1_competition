from tqdm import tqdm

if __name__ == '__main__':
    test_file = open("../entity_validation.txt", 'r', encoding='utf-8')
    test_entity = [line.strip('\n') for line in test_file.readlines()]
    print('共有实体'+str(len(test_entity))+'个')

    dic = {}
    filelist = ['entity_pages_1.xml', 'entity_pages_2.xml', 'entity_pages_3.xml', 'entity_pages_4.xml']
    for file in filelist:
        f = open('../' + file, 'r', encoding='utf-8')
        dic[file] = f.read()

    count_dic = {'entity_pages_1.xml': 0, 'entity_pages_2.xml': 0, 'entity_pages_3.xml': 0, 'entity_pages_4.xml': 0,
                 'not_found': 0}
    for en in tqdm(test_entity):
        if en in dic['entity_pages_1.xml']:
            count_dic['entity_pages_1.xml'] += 1
        elif en in dic['entity_pages_2.xml']:
            count_dic['entity_pages_2.xml'] += 1
        elif en in dic['entity_pages_3.xml']:
            count_dic['entity_pages_3.xml'] += 1
        elif en in dic['entity_pages_4.xml']:
            count_dic['entity_pages_4.xml'] += 1
        else:
            count_dic['not_found'] += 1

    print(count_dic)
    print(sum(count_dic.values()))
    print(str(count_dic['not_found'])+'个实体未找到')
