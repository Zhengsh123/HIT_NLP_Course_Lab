#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/11/30 21:48
# @Author  : ZSH
"""
本文件用于HMM分词
"""
import pickle
from utils import readText,writeTime,writeRes
from math import log
import re
import time
MIN=-3.14e+100 #标志一个最小值
pre={'B': 'ES', 'M': 'MB', 'S': 'SE', 'E': 'BM'}#标志可以出现在当前状态之前的状态
states=['B', 'M', 'E', 'S'] #状态集

class HMM():
    def __init__(self,model_path):
        """
        初始化
        :param model_path: 模型参数存储地址
        """
        self.pi = {}  # 初始状态集
        self.A = {}  # 状态转移概率
        self.B = {}  # 发射概率

        with open(model_path, "rb") as f:
            self.pi = pickle.load(f)
            self.A = pickle.load(f)
            self.B = pickle.load(f)
        f.close()
    def viterbi(self,text):
        """
        viterbi算法，为text标注BEMS
        :param text:输入的文本
        :return:输出带标注的文本
        """
        path={}#存储路径
        W=[{}]#存储到达每一个位置的时候的最优选择及其对应的值
        for state in states:
            W[0][state]=self.pi[state]+self.B[state].get(text[0],MIN)
            path[state]=[state]
        for i in range(1,len(text)):
            W.append({})
            temp_path={}
            for state in states:
                emit=self.B[state].get(text[i],MIN)
                cost=MIN
                cur_state=''
                for s in pre[state]:
                    temp=W[i-1][s]+emit+self.A[s].get(state,MIN)
                    if temp>cost:
                        cost=temp
                        cur_state=s
                temp_path[state]=path[cur_state]+[state]
                W[i][state] = cost
            path=temp_path
        (cost,state)=max([(W[len(text)-1][state],state)for state in 'ES'])#只有E和S有可能出现在末尾
        return cost,path[state]

    def word_seg(self, words):
        """
        处理连续输入的单字的分词，例如输入[w1,w2,w3]，输出[w1,w2w3]
        :param words:需要处理的单字
        :return:分词结果
        """
        if len(words) == 1:
            return [words]
        seg_list = self.viterbi(words)[1]
        res = ''
        for i in range(len(words)):
            tag = seg_list[i]
            if tag == 'B' or tag == 'M':
                res += words[i]
            elif tag == 'E' or tag == 'S':
                res += words[i] + '/'
        res = res.rstrip()
        res = res.split('/')[0:-1]
        return res
    def line_seg(self, word_list, sentence_seg=[]):
        """
        对已经处理过的句子进行分词，句子形如[w1,w2,w3w4w5]
        :param word_list: 需要进一步分词的句子
        :param sentence_seg: 分词结果
        :return:分词结果
        """
        operate_queue=''
        for i in range(len(word_list)):
            if len(word_list[i])==1:
                if operate_queue:
                    for j in range(len(self.word_seg(operate_queue))):
                        sentence_seg.append(self.word_seg(operate_queue)[j])
                    operate_queue=''
                sentence_seg.append(word_list[i])
            else:#非单字
                if operate_queue:
                    for j in range(len(self.word_seg(operate_queue))):
                        sentence_seg.append(self.word_seg(operate_queue)[j])
                    operate_queue=''
                sentence_seg.append(word_list[i])
        return sentence_seg

    def hmm(self,text_path,io_path):
        """
        使用HMM对文本进行分词
        :param text_path: 需要分词的文本所在地址
        :param io_path:分词结果输出地址
        :return:
        """
        text=readText(text_path)
        seg=[]
        for sentence in text:
            sentence = sentence.strip()
            sentence_seg = []
            if len(sentence) != 0:
                ##处理开头的时间信息
                sentence = writeTime(sentence, sentence_seg)
                sentence=list(sentence)
                sentence_seg=self.line_seg(sentence, sentence_seg)
                seg.append(sentence_seg)
        writeRes(seg,io_path)

class HMMTRAIN():
    """
    使用EM算法对HMM的参数进行训练
    """
    def __init__(self):
        self.pi = {}  # 初始状态集
        self.A = {}  # 状态转移概率
        self.B = {}  # 发射概率
        self.line_num = 0  # 统计句子数
        self.word_dic = set()  # 保存出现过的词
        self.state_num={} #记录每一个状态出现的次数
        for state in states:
            self.state_num[state]=0.0
            self.pi[state]=0.0
            self.A[state]={}
            self.B[state]={}
            for temp_state in states:
                self.A[state][temp_state]=0.0 #state->temp_state的转移概率初始化
    def write_res(self,save_model_path):
        """
        保存训练得到的参数
        :param save_model_path:保存地址
        :return:
        """
        with open(save_model_path, "wb") as f:
            pickle.dump(self.pi, f)
            pickle.dump(self.A, f)
            pickle.dump(self.B, f)
        f.close()
    def tag_line(self,line):
        """
        给一行文本标注，返回一行中每一个字对应的[B,M,E,S]
        :param line:需要标注的文本
        :return:标注结果，例如BMESSBE
        """
        line_word=[]
        line_tag=[]
        i=0
        for word in line.split():
            word = word[1 if word[0] == '[' else 0:word.index('/')]
            self.line_num+=1
            if len(word)==0:
                continue
            if word[-1] == ']':
                word = word[0:-1]

            line_word.extend(list(word))
            self.word_dic.add(word)
            #对句首状态进行记录
            if i==0 and len(word)==1:
                self.pi['S']+=1
            elif i==0 and len(word)!=1:
                self.pi['B'] += 1
            if len(word)==1:
                line_tag.append('S')
            else:
                line_tag.append('B')
                line_tag.extend(['M'] * (len(word) - 2))
                line_tag.append('E')
        assert len(line_tag)==len(line_word)
        return line_word,line_tag

    def tag_text(self,text_path,res_path,text_path2,text_path3):
        """
        通过标注整个文本来训练参数（pi，A，B）
        :param text_path: 需要标注的文本的地址
        :param res_path: 参数写入的地址
        :param text_path2: 需要标注的文本的地址2
        :param text_path2: 需要标注的文本的地址3
        :return: 训练出的参数写入文本文件
        """
        text=readText(text_path)
        text3=readText(text_path3)
        flag=False
        if text_path2!=None:
            text2=readText(text_path2)
            flag=True
        for line in text:
            if line=='\n':
                continue
            line = re.sub('[0-9]*[-][0-9]*[-][0-9]{3}[-][0-9]{3}', '', line)
            word,tag=self.tag_line(line)

            for i in range(len(tag)):
                self.state_num[tag[i]]+=1
                self.B[tag[i]][word[i]]=self.B[tag[i]].get(word[i],0)+1#发射概率
                if i>0:#转移概率
                    self.A[tag[i-1]][tag[i]]+=1
        if flag:
            for line in text2:
                if line == '\n':
                    continue
                line = re.sub('[0-9]*[-][0-9]*[-][0-9]{3}[-][0-9]{3}', '', line)
                word, tag = self.tag_line(line)

                for i in range(len(tag)):
                    self.state_num[tag[i]] += 1
                    self.B[tag[i]][word[i]] = self.B[tag[i]].get(word[i], 0) + 1  # 发射概率
                    if i > 0:  # 转移概率
                        self.A[tag[i - 1]][tag[i]] += 1
        for line in text3:
            if line == '\n':
                continue
            line = re.sub('[0-9]*[-][0-9]*[-][0-9]{3}[-][0-9]{3}', '', line)
            word, tag = self.tag_line(line)

            for i in range(len(tag)):
                self.state_num[tag[i]] += 1
                self.B[tag[i]][word[i]] = self.B[tag[i]].get(word[i], 0) + 1  # 发射概率
                if i > 0:  # 转移概率
                    self.A[tag[i - 1]][tag[i]] += 1
        ##更新参数
        for state in states:
            self.pi[state] = MIN if self.pi[state] == 0 else log(self.pi[state]/self.line_num)
            for temp_state in states:
                self.A[state][temp_state] = MIN if self.A[state][temp_state] == 0 else log(self.A[state][temp_state]/self.state_num[state])
            for word in self.B[state].keys():
                self.B[state][word] = log(self.B[state][word] / self.state_num[state])
        self.write_res(res_path)

if __name__=="__main__":
    train=HMMTRAIN()
    text_path='./dataset/199801_seg&pos.txt'
    text_path2 = './dataset/199802.txt'
    text_path3='./dataset/name.txt'
    text='你/ 好/ 你好/ '
    # Hmm=HMM('./util/hmm_par.pkl')
    # print(Hmm.word_seg(['你', '好', '世', '界']))
    train.tag_text(text_path,'./util/hmm_par.pkl',text_path2,text_path3)
    # Hmm=HMM('./output/hmm_par.pkl')
    # Hmm.hmm('./dataset/199801_sent.txt','./output/hmm_seg.txt')
    # print(Hmm.parse_line(['迈向', '充满', '希望','的']))

