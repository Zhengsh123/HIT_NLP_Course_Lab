"""
本文件实现一元文法分词
"""
from utils import readText,writeTime,writeRes
from math import log
def generate_pre_dic(dic_path):
    """
    生成前缀词典
    :param dic_path:统计词典所在地址
    :return: 生成前缀词典和词典中词频之和
    """
    pre_dic={}
    total_fre=0
    rawDic=readText(dic_path)
    for line in rawDic:
        if len(line)==0:
            continue
        ##提取统计词典中的词
        split_line=line.strip().split('\t')
        word=split_line[0]
        frequency=int(split_line[2])
        if word not in pre_dic:
            pre_dic[word]=frequency
        else:
            pre_dic[word]+=frequency
        total_fre+=frequency
        ##取出前缀词
        for i in range(len(word)):
            pre_word=word[:i+1]
            if pre_word not in pre_dic:
                pre_dic[pre_word]=0
    return pre_dic,total_fre
def generate_DAG(sentence,dic):
    """
    为句子生成一个DAG
    :param sentence:需要分词的句子
    :param dic:前缀词典，每一个词对应其在训练数据集中出现的频率
    :return:dic存储的一个DAG
    """
    DAG={}
    sen_length=len(sentence)
    for i in range(sen_length):
        temp=[]#存储当前字开头的路径
        cur=sentence[i]
        j=i
        while j<sen_length and cur in dic:
            if dic[cur]>0:
                temp.append(j)
            j+=1
            cur=sentence[i:j+1]
        if not temp:
            temp.append(i)
        DAG[i]=temp
    return DAG
def find_best_route(sentence,dic,total_fre):
    """
    寻找一个句子的最佳分词方式
    :param sentence:需要分词的句子
    :param dic:前缀词典
    :param total_fre:前缀词典中词频之和
    :return:句子中的每一个字对应的最优分词方式(dic储存)
    """
    sen_len=len(sentence)
    route={}
    log_total=log(total_fre)
    DAG=generate_DAG(sentence,dic)
    route[sen_len]=(0,0)##结束标志
    for i in range(sen_len-1,-1,-1):
        route[i] = max((log(dic.get(sentence[i: x+1]) or 1) - log_total + route[x + 1][0], x) for x in DAG[i])
    return route

def Uni_seg(text_path,dic_path):
    """
    一元文法分词
    :param text_path:需要分词的文本的地址
    :param dic_path:词典地址
    :return:分词结果
    """
    dic,total_num=generate_pre_dic(dic_path)
    text=readText(text_path)
    seg=[]
    for sentence in text:
        sentence=sentence.strip()
        sentence_seg = []
        if len(sentence)!=0:
            ##处理开头的时间信息
            sentence = writeTime(sentence, sentence_seg)
            route = find_best_route(sentence, dic, total_num)
            sen_len = len(sentence)
            i = 0
            while i < sen_len:
                sentence_seg.append(sentence[i:route[i][1] + 1])
                i= (route[i][1]+1)
        else:
            sentence_seg.append('\n')
        seg.append(sentence_seg)
    return seg
if __name__=="__main__":
    seg=Uni_seg('./dataset/199803_sent.txt','./output/dic.txt')
    writeRes(seg,'./output/seg_LM3.txt')
