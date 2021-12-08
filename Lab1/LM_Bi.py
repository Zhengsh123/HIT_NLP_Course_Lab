#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/11/28 21:45
# @Author  : ZSH
# 实现二元文法
from LM_Uni import generate_pre_dic,generate_DAG
from utils import readText,writeTime,writeRes
from math import log
from HMM import HMM
import re
Hmm=HMM('./util/hmm_par.pkl')

def generate_Bi_pre_dic(dic_path):
    """
    生成前缀词典
    :param dic_path:统计词典所在地址
    :return: 生成前缀词典和词典中词频之和
    """
    pre_dic={}
    rawDic = readText(dic_path)
    for line in rawDic:
        if len(line) == 0:
            continue
        split_line = line.strip().split('\t')
        word1,word2,freq=split_line[:3]
        freq=int(freq)
        if word1 not in pre_dic:
            temp_dic={}
            temp_dic[word2]=freq
            pre_dic[word1]=temp_dic
        else:
            pre_dic[word1][word2]=freq
    return pre_dic
def cal_log(word1,word2,dic,Bi_dic):
    """
    计算word1之后是word2的概率的log
    :param word1:第一个词
    :param word2:第二个词
    :param dic:一元前缀词典
    :param Bi_dic:二元前缀词典
    :return:log值
    """
    p_word1=0
    p_word2=0
    if word1 in dic:
        p_word1=dic[word1]
    if word2 in Bi_dic:
        if word1 in Bi_dic[word2]:
            p_word2=Bi_dic[word2][word1]
    p_word2+=0.75#平滑
    p_word1+=0.75*len(dic.keys())
    return log(p_word2)-log(p_word1)

def find_best_route(sentence,dic,Bi_dic,sentence_seg):
    """
    寻找一个句子的最佳分词方式
    :param sentence:需要分词的句子
    :param dic:一元前缀词典
    :param Bi_dic:二元前缀词典
    :return:返回分词结果
    """
    ##处理百分号
    prog = '[０-９]*[·]?[０-９]+[％]'
    num_oov_0 = re.findall(prog, sentence)
    flag_0 = False
    if num_oov_0:
        flag_0 = True
        for word in num_oov_0:
            sentence = sentence.replace(word, '^', 1)
    ##把年月日处理成特殊字符
    prog = '[０-９]{4}[年]'
    num_oov_1 = re.findall(prog, sentence)
    flag_1 = False
    if num_oov_1:
        flag_1=True
        for word in num_oov_1:
            sentence=sentence.replace(word,'|',1)
    prog = '[０-９]+[月]?[日]?'
    num_oov_2= re.findall(prog, sentence)
    flag_2=False
    if num_oov_2:
        flag_2=True
        for word in num_oov_2:
            sentence=sentence.replace(word,'_',1)

    DAG = generate_DAG(sentence, dic)
    route={}
    n=5
    length=len(sentence)-5 #减掉结尾的<EOS>

    pre_graph = {'<BOS>': {}}#记录了当前字为开始对应词的对数概率
    follow_graph={}#记录了当前词节点对应的上一个相连词的图
    for x in DAG[5]:#初始化前词是BOS的情况
        pre_graph['<BOS>'][(5,x+1)]=cal_log("<BOS>",sentence[5:x+1],dic,Bi_dic)
    #对每一个字可能的分词方式生成下一个词的词典
    while n<length:
        i=DAG[n]
        for x in i:
            pre=sentence[n:x+1]
            current=x+1
            current_idx=DAG[x+1]#当前位置对应的后续分词
            temp={}
            for char_i in current_idx:
                word=sentence[current:char_i+1]
                if word=="<":#已经到句尾了
                    temp['<EOS>']=cal_log(pre,'<EOS>',dic,Bi_dic)
                else:
                    temp[(current,char_i+1)]=cal_log(pre,word,dic,Bi_dic)
            pre_graph[(n,x+1)]=temp #对每一个以n开头的词都建立一个关于下一个词的词典
        n+=1

    words=list(pre_graph.keys())
    for pre in words:
        for word in pre_graph[pre].keys():#遍历pre_word的后一个词
            follow_graph[word]=follow_graph.get(word,list())
            follow_graph[word].append(pre)
    words.append('<EOS>')
    ##动态规划
    for word in words:
        if word=='<BOS>':
            route[word]=(0.0,'<BOS>')
        else:
            if word in follow_graph:
                nodes=follow_graph[word]
            else:
                route[word]=(-65507,'<BOS>')
                continue
            route[word]=max((pre_graph[node][word]+route[node][0],node)for node in nodes)

    end="<EOS>"
    while True:
        end=route[end][1]
        if end=='<BOS>':
            break
        sentence_seg.insert(1,sentence[end[0]:end[1]])
    #还原日期等
    if flag_0:
        j=0
        for i in range(len(sentence_seg)):
            if sentence_seg[i]=='^':
                sentence_seg[i]=num_oov_0[j]
                j+=1
    if flag_1:
        j=0
        for i in range(len(sentence_seg)):
            if sentence_seg[i]=='|':
                sentence_seg[i]=num_oov_1[j]
                j+=1
    if flag_2:
        j = 0
        for i in range(len(sentence_seg)):
            if sentence_seg[i] == '_':
                sentence_seg[i] = num_oov_2[j]
                j += 1
    return sentence_seg

def Bi_seg(text_path,dic_path,dic2_path):
    """
    一元文法分词
    :param text_path:需要分词的文本的地址
    :param dic_path:词典地址
    :param dic_path:二元词典地址
    :return:分词结果
    """
    dic, total_num = generate_pre_dic(dic_path)
    Bi_dic=generate_Bi_pre_dic(dic2_path)
    text = readText(text_path)
    seg=[]
    for sentence in text:
        sentence = sentence.strip()
        sentence_seg = []
        if len(sentence) != 0:
            ##处理开头的时间信息
            sentence = writeTime(sentence, sentence_seg)
            head_time=''
            if len(sentence_seg)!=0:
                head_time=sentence_seg[0]
            sentence='<BOS>'+sentence+'<EOS>'
            sentence_seg = find_best_route(sentence, dic, Bi_dic,sentence_seg)
            ##未登录词处理
            seg_OOV=[]
            if head_time!='':
                seg_OOV=Hmm.line_seg(sentence_seg[1:], seg_OOV)
            else:
                seg_OOV = Hmm.line_seg(sentence_seg, seg_OOV)
            if head_time!='':
                seg_OOV.insert(0,head_time)
            seg.append(seg_OOV)
    return seg

if __name__=="__main__":
    dic_path='./util/LM_dic.txt'
    dic2_path='./util/Bi_dic.txt'
    text_path='./dataset/test.txt'
    seg=Bi_seg(text_path,dic_path,dic2_path)
    writeRes(seg, './output/seg_Bigram_OOV.txt')
