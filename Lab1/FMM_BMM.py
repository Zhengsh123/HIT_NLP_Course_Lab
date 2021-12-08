from utils import *

def FMM(text_path,dic_path,seg_path):
    """
    FMM分词
    :param text_path:需要分词文本存储地址
    :param dic_path:词典所在文本地址
    :param seg_path:分词结果需要写入的文本位置
    :return:输出分词结果文件
    """
    text_list = readText(text_path)
    dic, max_len = readDic(dic_path)
    text_len=len(text_list)
    with open(seg_path,'w',encoding='gbk')as fw:
        for i in range(text_len):
            temp_list = []
            temp_text = writeTime(text_list[i], temp_list)
            while len(temp_text) > 0:
                match_word = temp_text[0:min(len(temp_text),max_len)]
                while match_word not in dic:
                    if len(match_word) == 1:#当前词没有匹配上
                        break
                    match_word = match_word[0:len(match_word) - 1]
                temp_list.append(match_word+'/ ')
                temp_text = temp_text[len(match_word):]
            fw.write(''.join(temp_list)+'\n')

def BMM(text_path,dic_path,seg_path):
    """
       BMM分词
        :param text_path:需要分词文本存储地址
        :param dic_path:词典所在文本地址
        :param seg_path:分词结果需要写入的文本位置
        :return:输出分词结果文件
        """
    text_list = readText(text_path)
    dic, max_len = readDic(dic_path)
    text_len=len(text_list)
    with open(seg_path,'w',encoding='gbk')as fw:
        for i in range(text_len):
            temp_list = []
            temp_text = writeTime(text_list[i], temp_list)
            while len(temp_text) > 0:
                match_word = temp_text[len(temp_text) - min(max_len, len(temp_text)):]
                while match_word not in dic:
                    if len(match_word) == 1:#词典中没有匹配得上的词
                        break
                    match_word = match_word[1:]
                temp_list.insert(1, match_word+'/ ')#BMM注意插入分词结果的顺序
                temp_text = temp_text[:len(temp_text) - len(match_word)]
            fw.write(''.join(temp_list)+'\n')

