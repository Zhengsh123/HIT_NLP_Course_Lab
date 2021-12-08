'''
本文件主要功能是生成3.1中的字典构建
输入文件： 199801_seg&pos.txt
输出： dic.txt（自己形成的分词词典）
'''
import re
def get_dic(data_path):
    """
    生成词典
    :param data_path:输入数据集的path
    :return: 词典
    """
    dic = {}
    with open(data_path)as f:
        lines = f.readlines()
        for line in lines:
            line=line.strip()
            ##去空行
            if line=="":
                continue
            #去时间
            whole_line_word=line.split(' ')[1:]
            for word in whole_line_word:
                word_tag=tuple(word.strip().split('/'))
                #遇到空缺，跳过
                if len(word_tag[0])==0 or len(word_tag[1])==0:
                    continue
                #去除一部分前面有[的词
                if word_tag[0][0]=='[':
                    word_tag=(word_tag[0][1:],word_tag[1])
                # 去除一部分后面有]的词
                if word_tag[0][-1]==']':
                    word_tag=(word_tag[0][0:-1],word_tag[1])
                # #去掉一些太长的人名
                # if len(word_tag[0])>10 and word_tag[1]=='nr':
                #     continue
                #去掉一些量词和英文长词
                punc='０１２３４５６７８９ＡＢＣＤＥＦＫＩＮＬＧＳＨＪＲＴＸＭＹＰＯＶａｂｅｍｎｈｏ'
                word0 = re.sub(r'[{}]+'.format(punc), "", word_tag[0])
                if len(word0) == 0 or len(word0) != len(word_tag[0]):
                    continue
                if word_tag in dic.keys():
                    dic[word_tag]+=1
                else:
                    dic[word_tag]=1
    dic = sorted(dic.items(), key=lambda e: len(e[0][0]), reverse=False)
    return dic
def get_LMdic(data_path):
    """
    生成词典
    :param data_path:输入数据集的path
    :return: 词典
    """
    dic = {}
    with open(data_path)as f:
        lines = f.readlines()
        for line in lines:
            line=line.strip()
            ##去空行
            if line=="":
                continue
            #去时间
            whole_line_word=line.split(' ')[1:]
            for word in whole_line_word:
                word_tag=tuple(word.strip().split('/'))
                #遇到空缺，跳过
                if len(word_tag[0])==0 or len(word_tag[1])==0:
                    continue
                #去除一部分前面有[的词
                if word_tag[0][0]=='[':
                    word_tag=(word_tag[0][1:],word_tag[1])
                # 去除一部分后面有]的词
                if word_tag[0][-1]==']':
                    word_tag=(word_tag[0][0:-1],word_tag[1])
                if word_tag in dic.keys():
                    dic[word_tag]+=1
                else:
                    dic[word_tag]=1
    dic = sorted(dic.items(), key=lambda e: len(e[0][0]), reverse=False)
    return dic
def getBigramDic(data_path):
    """
    生成适合于二元文法的词典
    :param data_path:原始数据地址
    :return:词典
    """
    dic=dict()
    with open(data_path,'r')as f:
        text=f.readlines()
    f.close()

    for line in text:
        temp_list=[]
        line = line.strip()
        ##去空行
        if line == "":
            continue
        # 去时间
        whole_line_word = line.split(' ')[1:]
        for word in whole_line_word:
            word_tag = tuple(word.strip().split('/'))
            # 遇到空缺，跳过
            if len(word_tag[0]) == 0 or len(word_tag[1]) == 0:
                continue
            # 去除一部分前面有[的词
            if word_tag[0][0] == '[':
                word_tag = (word_tag[0][1:], word_tag[1])
            # 去除一部分后面有]的词
            if word_tag[0][-1] == ']':
                word_tag = (word_tag[0][0:-1], word_tag[1])
            if len(word_tag[0]) > 10 and word_tag[1] == 'nr':
                continue
            temp_list.append(word_tag[0])
        #加入句首和句尾标志
        temp_list.append("<EOS>")
        temp_list.insert(0,'<BOS>')
        for j in range(len(temp_list)-1):
            pair=(temp_list[j],temp_list[j+1])
            if pair in dic:
                dic[pair]+=1
            else:
                dic[pair]=1
    dic=sorted(dic.items(), key=lambda e: e[0][0], reverse = False)
    return dic

def write_dic(dic,write_path):
    """
    将得到的字典写入文件
    :param dic: 字典,注意本实验中需要写入的字典形式都是(tuple(,),int)
    :param write_path:需要写入的地址
    :return:
    """
    with open(write_path,'w')as fw:
        for word in dic:
            fw.write(word[0][0]+'\t'+word[0][1]+'\t'+str(word[1])+'\n')
    fw.close()

if __name__=="__main__":
    data_path='./dataset/Bi_train.txt'
    output_path=('./util/Bidic.txt')
    dic=getBigramDic(data_path)
    write_dic(dic,output_path)