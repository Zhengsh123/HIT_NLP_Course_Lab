"""
本文件主要功能是为整体代码功能实现的时候提供一些共性简单部分支撑
"""
# coding=utf-8
import re
def readText(text_path):
    """
    读取文件
    :param text_path:文件地址
    :return:文件内容的list，文件中的每一行是list中的一个元素
    """
    text_list=[]
    try:
        with open(text_path, 'r',encoding='utf-8')as f:
            for line in f.readlines():
                line = line.replace('\n', '').replace('\r', '')
                # line = re.sub('[0-9]*[-][0-9]*[-][0-9]{3}[-][0-9]{3}', '', line)
                if len(line) > 0:
                    text_list.append(line)
                else:
                    text_list.append('\n')
        f.close()
    except:
        with open(text_path, 'r', encoding='gbk')as f:
            for line in f.readlines():
                line = line.replace('\n', '').replace('\r', '')
                # line = re.sub('[0-9]*[-][0-9]*[-][0-9]{3}[-][0-9]{3}', '', line)
                if len(line) > 0:
                    text_list.append(line)
                else:
                    text_list.append('\n')
        f.close()
    return text_list

def readDic(path):
    '''
    将词典中的词抽取出来
    :param path: 词典地址
    :return: 词典中所有的词
    '''
    dic_list=[]
    max_len=0
    with open(path,'r')as f:
        for line in f.readlines():
            line=line.strip()
            if len(line)>0:
                dic_list.append(line.split('\t')[0])
                max_len=max(len(line.split('\t')[0]),max_len)
    return dic_list,max_len

def binary_search(dic, word):
    """
    二分查找
    :param dic:整个字典，是一个list，按首字母排序
    :param word:需要寻找的词
    :return:如果存在则返回True，如果不存在返回False
    """
    dic_size=len(dic)-1
    left=0
    right=dic_size
    while left<=right:
        mid=int((left+right)/2)
        if word<dic[mid]:
            right=mid-1
        elif word>dic[mid]:
            left=mid+1
        else:
            return True
    return False

def writeTime(text, seg_list):
    '''
    用于判断需要分词的部分是否存在时间格式
    :param text:需要分词的部分
    :param seg_list: 需要写入分词结果的list
    :return:
    '''
    prog = re.compile('[0-9]*[-][0-9]*[-][0-9]{3}[-][0-9]{3}')
    ret=prog.match(text)
    if ret:
        seg_list.append(str(ret.group()))
        text=re.sub('[0-9]*[-][0-9]*[-][0-9]{3}[-][0-9]{3}', '',text)
    return text

def writeRes(seg_list,write_path):
    '''
    把分词结果写入
    :param seg_list:分词结果，n*m list，list的每一行存储一句话的分词结果
    :param write_path: 写入的结果地址
    :return:
    '''
    row_num=len(seg_list)
    with open(write_path,'w')as fw:
        for row in range(row_num):
            if seg_list[row][0]=='\n':
                continue
            col_num = len(seg_list[row])
            for col in range(col_num):
                fw.write(seg_list[row][col]+'/ ')
            fw.write('\n')
