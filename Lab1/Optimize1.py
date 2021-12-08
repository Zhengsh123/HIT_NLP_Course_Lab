#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 21:41
# @Author  : ZSH
from math import log
import pickle
from utils import writeTime
import time
import re
class SimpleDIc():
    """
    本类型构建一个简单的词典，实现添加和计算频率功能
    存储的是词对应出现的次数，可计算词出现的次数
    """
    def __init__(self):
        self.d = {}
        self.total = 0.0
        self.none = 0

    def found(self, key):
        return key in self.d

    def sum(self):
        return self.total

    def get(self, key):
        if not self.found(key):
            return False, self.none
        return True, self.d[key]

    def get_freq(self, key):
        return float(self.get(key)[1]) / self.total

    def items(self):
        return self.d.keys()

    def add(self, key, value):
        self.total += value
        if not self.found(key):
            self.d[key] = value
        else:
            self.d[key] += value

class model():
    """
    构建一个二阶HMM分词模型
    """
    def __init__(self):
        self.Uni = SimpleDIc()
        self.Bi = SimpleDIc()
        self.Tri = SimpleDIc()
        self.lambda1 = 0.0
        self.lambda2 = 0.0
        self.lambda3 = 0.0
        self.status = ('b', 'm', 'e', 's')

    def div(self, v1, v2):
        if v2 == 0:
            return 0
        return float(v1) / v2
    def model_train(self, data):
        for sentence in data:

            self.Bi.add((('', 'BOS'), ('', 'BOS')), 1)
            self.Uni.add(('', 'BOS'), 2)
            current = [('', 'BOS'), ('', 'BOS')]
            for word, tag in sentence:
                current.append((word, tag))
                self.Tri.add(tuple(current), 1)
                self.Bi.add(tuple(current[1:]), 1)
                self.Uni.add((word, tag), 1)

                current.pop(0)
        temp_lambda_1,temp_lambda_2,temp_lambda_3 = 0.0,0.0,0.0

        samp = sorted(self.Tri.items(), key=lambda x: self.Tri.get(x)[1])

        for current in samp:##可以查看报告，这一部分就是lambda的计算
            temp3 = self.div(self.Tri.get(current)[1] - 1, self.Bi.get(current[:2])[1] - 1)
            temp2 = self.div(self.Bi.get(current[1:])[1] - 1, self.Uni.get(current[1])[1] - 1)
            temp1 = self.div(self.Uni.get(current[2])[1] - 1, self.Uni.sum() - 1)

            if temp3 >= temp1 and temp3 >= temp2:
                temp_lambda_3 += self.Tri.get(current)[1]
            elif temp2 >= temp1 and temp2 >= temp3:
                temp_lambda_2 += self.Tri.get(current)[1]
            else:
                temp_lambda_1 += self.Tri.get(current)[1]

        self.lambda1 = self.div(temp_lambda_1, temp_lambda_1 + temp_lambda_2 + temp_lambda_3)
        self.lambda2 = self.div(temp_lambda_2, temp_lambda_1 + temp_lambda_2 + temp_lambda_3)
        self.lambda3 = self.div(temp_lambda_3, temp_lambda_1 + temp_lambda_2 + temp_lambda_3)

    def cal_log(self, char1, char2, char3):
        Uni = self.lambda1 * self.Uni.get_freq(char3)
        Bi = self.div(self.lambda2 * self.Bi.get((char2, char3))[1], self.Uni.get(char2)[1])
        Tri = self.div(self.lambda3 * self.Tri.get((char1, char2, char3))[1], self.Bi.get((char1, char2))[1])
        if Uni + Bi + Tri == 0:
            return float('-inf')
        return log(Uni + Bi + Tri)

    def tag_line(self, data):
        current = [((('', 'BOS'), ('', 'BOS')), 0.0, [])]
        for ch in data:
            stage = {}
            not_exist = True
            for state in self.status:
                if self.Uni.get_freq((ch, state)) != 0:
                    not_exist = False
                    break
            if not_exist:
                for state in self.status:
                    for pre_word in current:
                        stage[(pre_word[0][1], (ch, state))] = (pre_word[1], pre_word[2] + [state])
                current = list(map(lambda x: (x[0], x[1][0], x[1][1]),stage.items()))
                continue
            for state in self.status:
                for pre_word in current:
                    current_temp=self.cal_log(pre_word[0][0], pre_word[0][1], (ch, state))
                    temp_p = pre_word[1] + current_temp
                    if (not (pre_word[0][1],(ch, state)) in stage) or temp_p > stage[(pre_word[0][1],(ch, state))][0]:
                        stage[(pre_word[0][1], (ch, state))] = (temp_p, pre_word[2] + [state])
            current = list(map(lambda x: (x[0], x[1][0], x[1][1]), stage.items()))

        temp=zip(data, max(current, key=lambda x: x[1])[2])

        return temp

    def save(self,save_path):
        with open(save_path, "wb") as f:
            pickle.dump(self.lambda1, f)
            pickle.dump(self.lambda2, f)
            pickle.dump(self.lambda3, f)
            pickle.dump(self.Uni, f)
            pickle.dump(self.Bi, f)
            pickle.dump(self.Tri, f)
        f.close()
    def load(self,load_path):
        with open(load_path, "rb") as f:
            self.lambda1=pickle.load(f)
            self.lambda2=pickle.load(f)
            self.lambda3=pickle.load(f)
            self.Uni=pickle.load(f)
            self.Bi=pickle.load(f)
            self.Tri = pickle.load(f)
        f.close()


class SEG():
    def __init__(self):
        self.tag=model()
    def train(self,file_path1,save_path):
        with open(file_path1,'r',encoding='utf-8')as f:
            fr=f.readlines()
        data = []
        for i in fr:
            line = i.strip()
            if not line:
                continue
            tmp = map(lambda x: x.split('/'), line.split())
            data.append(tmp)
        f.close()
        self.tag.model_train(data)
        self.tag.save(save_path)
    def load(self,load_path):
        self.tag.load(load_path)
    def seg(self,sentence):
        ret = self.tag.tag_line(sentence)
        res = ''
        for tup in ret:
            if tup[1] == 'e':
                yield res + tup[0]
                res = ''
            elif tup[1] == 'b' or tup[1] == 's':
                if res:
                    yield res
                res = tup[0]
            else:
                res += tup[0]
        if res:
            yield res

def generateBMES(lines,save_path):
    '''
    为文本生成BEMS划分的划分，并存储
    :param lines:文本
    :param save_path:划分结果需要保存的地址
    :return:生成文件
    '''
    bmse_list=[]
    for line in lines:
        word_list=[]
        bmes=[]
        if len(line)==0:
            continue
        line = re.sub('[0-9]*[-][0-9]*[-][0-9]{3}[-][0-9]{3}', '', line)
        words=line.strip().split()
        for word in words:
            if word==" ":
                continue
            full_word=(word.strip().split('/'))#词和对应的词性
            if len(full_word[0])==0 or len(full_word[1])==0:
                continue
            temp=full_word
            if full_word[0][0]=='[' and len(full_word[0])>1:
                full_word=(full_word[0][1:],temp[1])
            word_list.append(full_word[0])
        if len(word_list)==0:
            continue
        for word in word_list:
            # 给每一个字符加上对应标志
            length=len(word)
            if length==1:
                bmes.append(word+'/s')
            else:
                bmes.append(word[0]+'/b')
                for j in range(1,length):
                    if j==length-1:
                        bmes.append(word[j]+'/e')
                    else:
                        bmes.append(word[j]+'/m')
        temp_str=bmes[0]
        for j in range(1,len(bmes)):
            temp_str+=' '+bmes[j]
        bmse_list.append(temp_str)
    with open(save_path,'a+',encoding='utf-8')as fw:
        for temp in bmse_list:
            fw.write(temp+'\n')
    fw.close()
def Seg_no_train(text_path,save_path,res_path):
    """
    直接读取预训练的参数，不再训练直接分词
    :param text_path: 需要分词的文本的地址
    :param save_path: 参数保存的地址
    :param res_path: 分词结果需要保存的地址
    :return:
    """
    seg = SEG()
    seg.load(save_path)
    print("finish load parameter")
    with open(text_path, 'r', encoding='gbk')as fr:
        lines = fr.readlines()
    textsize = len(lines)
    print("begin seg")
    fw = open(res_path, 'w')
    for i in range(textsize):
        sen = lines[i].strip()
        if len(sen) == 0:
            fw.write("\n")
            continue
        ##处理开始的时间
        sentence_seg=[]
        sentence=writeTime(sen,sentence_seg)
        head_time = ''
        if len(sentence_seg) != 0:
            head_time = sentence_seg[0]
        res=''
        if head_time!='':
            res=head_time+"/ " + "/ ".join(seg.seg(sentence)) + "/ " + "\n"
        fw.write(res)
        if (i % 1000 == 0):
            print(time.time())
    fw.close()
def Seg_with_train(text_path,train_path1,train_path2,train_path3,save_path,save_path2,res_path):
    """
    重新进行训练并分词
    :param text_path: 需要分词的文件
    :param train_path1: 训练集1
    :param train_path2: 训练集2
    :param train_path3: 训练集3
    :param save_path: BMES划分结果保存地址
    :param save_path2: 参数保存地址
    :param res_path: 分词结果保存地址
    :return:
    """
    with open(save_path,'w',encoding='utf-8')as fw:
        fw.write('')
    fw.close()
    with open(train_path1, 'r', encoding='gbk')as f:
        lines=f.readlines()
    f.close()
    generateBMES(lines,save_path)
    with open(train_path2, 'r', encoding='gbk')as f:
        lines=f.readlines()
    f.close()
    generateBMES(lines,save_path)
    with open(train_path3, 'r', encoding='gbk')as f:
        lines=f.readlines()
    f.close()
    generateBMES(lines,save_path)

    print('finish BEMS')
    seg = SEG()
    print("seg train")
    seg.train(save_path,save_path2)
    print("finish train")
    Seg_no_train(text_path,save_path2,res_path)

if __name__=='__main__':
    train_path1= './dataset/199801_seg&pos.txt'
    train_path2='./dataset/199802.txt'
    train_path3='./dataset/name.txt'
    save_path='./util/BMSE.txt'
    text_path='./dataset/test.txt'
    save_path2='./util/segTrain.pkl'
    res_path='./test.txt'

    # Seg_no_train(text_path,save_path2,res_path)

    Seg_with_train(text_path,train_path1,train_path2,train_path3,save_path,save_path2,res_path)