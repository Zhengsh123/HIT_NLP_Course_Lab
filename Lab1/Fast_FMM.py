# coding=utf-8
from utils import *
import time
from HashSet import *
def BinarySearchFMM(dicPath,textPath):
    """
    使用二分法的FMM
    :param dicPath:字典所在地址
    :param textPath:需要分词的文本所在地址
    :return:需要输出分词时间
    """
    rawDic=readText(dicPath)
    text_list=readText(textPath)
    dic=[]
    dicSize=len(rawDic)
    maxLen=0
    ##构造dic
    for i in range(dicSize):
        dicWord=rawDic[i].split('\t')[0]
        dic.append(dicWord)
        maxLen=max(len(dicWord),maxLen)
    dic.sort()

    start_time=time.time()
    text_len = len(text_list)
    fmm_seg_list = []
    for i in range(text_len):
        temp_text=text_list[i]
        temp_list = []
        temp_text=writeTime(temp_text, temp_list)
        while len(temp_text)>0:
            length = min(maxLen, len(temp_text))
            match_word = temp_text[0:length]
            while binary_search(dic,match_word)==False:
                if len(match_word) == 1:
                    break
                match_word = match_word[0:len(match_word) - 1]
            temp_list.append(match_word)
            temp_text=temp_text[len(match_word):]
        fmm_seg_list.append(temp_list)
    end_time=time.time()
    return end_time-start_time

def HashFMM(dicPath,textPath):
    """
    使用哈希表的FMM
    :param dicPath:字典所在地址
    :param textPath:需要分词的文本所在地址
    :return:需要输出分词时间
    """
    rawDic,maxLen = readDic(dicPath)
    text_list = readText(textPath)
    dic = HashSet(1000000)
    dicSize = len(rawDic)
    ##构造dic
    for i in range(dicSize):
        dic.add(rawDic[i])
    print('hash is ok')
    text_len = len(text_list)
    fmm_seg_list = []
    start_time = time.time()
    for i in range(text_len):
        temp_text = text_list[i]
        temp_list = []
        temp_text = writeTime(temp_text, temp_list)
        while len(temp_text) > 0:
            length = min(maxLen, len(temp_text))
            match_word = temp_text[0:length]
            while match_word not in dic:
                if len(match_word) == 1:
                    break
                match_word = match_word[0:len(match_word) - 1]
            temp_list.append(match_word)
            temp_text = temp_text[len(match_word):]
        fmm_seg_list.append(temp_list)
    end_time = time.time()
    writeRes(fmm_seg_list, './output/seg_FMM.txt')
    return end_time-start_time
def HashBMM(dicPath,textPath):
    """
    使用哈希表的BMM
    :param dicPath:字典所在地址
    :param textPath:需要分词的文本所在地址
    :return:需要输出分词时间
    """
    rawDic, maxLen = readDic(dicPath)
    text_list = readText(textPath)
    dic = HashSet(1000000)
    dicSize = len(rawDic)
    ##构造dic
    for i in range(dicSize):
        dic.add(rawDic[i])
    print('hash is ok')
    text_len = len(text_list)
    bmm_seg_list = []
    start_time = time.time()
    for i in range(text_len):
        temp_list = []
        temp_text = writeTime(text_list[i], temp_list)
        while len(temp_text) > 0:
            match_word = temp_text[len(temp_text) - min(maxLen, len(temp_text)):]
            while match_word not in dic:
                if len(match_word) == 1:  # 词典中没有匹配得上的词
                    break
                match_word = match_word[1:]
            temp_list.insert(1, match_word)  # BMM注意插入分词结果的顺序
            temp_text = temp_text[:len(temp_text) - len(match_word)]
        bmm_seg_list.append(temp_list)
    end_time = time.time()
    writeRes(bmm_seg_list,'./output/seg_BMM.txt')
    return end_time - start_time
