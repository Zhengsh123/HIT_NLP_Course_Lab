# -*- coding: UTF-8 -*-
import re
def preProcess(seg_path):
    """
    为了处理标准答案中的一些误差，并把标准答案转换成和自己做出的分词一样的格式，方便比较
    :param seg_path:文件地址
    :return:二维list，表示分词结果，每一行就是一行的分词结果
    """
    seg_list=[]
    with open(seg_path,'r')as f:
        for line in f.readlines():
            if line == '\n':
                continue
            new_line = []  # 保存处理过后的一行
            for word in line.split():
                #目前的处理只有去掉词前的[和词后的]
                temp_word=word[1 if word[0] == '[' else 0:word.index('/')]
                if len(temp_word)==0:
                    continue
                if temp_word[-1]==']':
                    temp_word=temp_word[0:-1]
                new_line.append(temp_word)
            seg_list.append(new_line)
    f.close()
    return seg_list

def calc(standard_path,my_seg_path):
    """
    计算评估指标
    :param standard_path:标准答案路径
    :param my_seg_path: 自己分类的路径
    :return:准确率，召回率，F值
    """
    standard_seg=preProcess(standard_path)
    my_seg=preProcess(my_seg_path)#这一步不起到预处理作用，只是将文件转换为list读入
    standard_seg_num=0
    my_seg_num = 0
    right_seg_num=0
    text_length=len(standard_seg)
    for i in range(text_length):
        my_seg_list=my_seg[i]
        standard_seg_list=standard_seg[i]
        standard_seg_num+=len(standard_seg_list)
        my_seg_num+=len(my_seg_list)

        m=0
        n=0
        while m<len(my_seg_list) and n<len(standard_seg_list):
            ##遍历句子中的每一个分词
            my_word=my_seg_list[m]
            standard_word=standard_seg_list[n]
            if my_word==standard_word:
                right_seg_num+=1
                m+=1
                n+=1
            else:
                while True:
                    if len(my_word)<len(standard_word):
                        m+=1
                        my_word=my_word+my_seg_list[m]
                    elif len(my_word)>len(standard_word):
                        n+=1
                        standard_word=standard_word+standard_seg_list[n]
                    elif my_word==standard_word:
                        m+=1
                        n+=1
                        break
    precision=right_seg_num/float(my_seg_num)
    recall=right_seg_num/float(standard_seg_num)
    f=2*precision*recall/(precision+recall)
    return precision,recall,f

if __name__=="__main__":
    print(calc('./dataset/test_standard.txt','./output/seg_Optimize.txt'))