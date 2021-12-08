"""
这一文件主要是方便查验代码，partX对应于要求中的3.x，在main函数中解除该行注释即可
"""
from creatDic import *
from FMM_BMM import *
from score import *
from Fast_FMM import *
from LM_Bi import *
from Optimize1 import *
from HMM import *
from LM_Bi_without_OOV import *
import time
def Part1():
    data_path = './dataset/199801_seg&pos.txt'
    output_path = ('./output/dic.txt')
    dic = get_dic(data_path)
    write_dic(dic, output_path)
    print('Dictionary creation completed ')

def Part2(text_path = './dataset/199801_sent.txt',
    dic_path = './output/dic.txt',
    fmm_seg_path = './output/seg_FMM.txt',
    bmm_seg_path = './output/seg_BMM.txt'):
    """
    这一段代码测试不是用额外手段的FMM和BMM，不建议运行，耗时很长
    :return:
    """
    BMM(text_path,dic_path,bmm_seg_path)
    print('bmm is ok')
    FMM(text_path, dic_path, fmm_seg_path)
    print('fmm is ok')

def Part3(standard_path='./dataset/199801_seg&pos.txt',FMM_seg_path='./output/seg_FMM.txt',BMM_seg_path='./output/seg_BMM.txt'
          ,result_path='./output/score.txt'):
    BMM_precision,BMM_recall,BMM_F=calc(standard_path,BMM_seg_path)
    FMM_precision,FMM_recall,FMM_F=calc(standard_path,FMM_seg_path)
    result='FMM准确率：\t'+str(FMM_precision)+'\n'
    result += 'FMM召回率：\t' + str(FMM_recall)+ '\n'
    result += 'FMM F值：\t' + str(FMM_F) + '\n\n'
    result += 'BMM准确率：\t' + str(BMM_precision) + '\n'
    result += 'BMM召回率：\t' + str(BMM_recall) + '\n'
    result += 'BMM F值：\t' + str(BMM_F) + '\n\n'
    with open(result_path,'w')as fw:
        fw.write(result)
    fw.close()

def Part4(dic_path='./output/dic.txt',text_path='./dataset/199801_sent.txt',time_path='./output/TimeCost.txt'):
    """
    优化机械匹配速度(FMM)
    :param dic_path:词典地址
    :param text_path:需要分词的文本的地址
    :param time_path:算法消耗时间需要写入的地址
    :return:
    """
    time_binary_search=BinarySearchFMM(dic_path,text_path)
    time_hash= HashFMM(dic_path, text_path)
    # time_bmm=HashBMM(dic_path,text_path)
    result='二分查找时间：\t'+str(time_binary_search)+'s\n'
    result+= '哈希查找时间：\t' + str(time_hash) + 's\n'
    with open(time_path,'a+')as fw:
        fw.write(result)
    fw.close()

def Part5_No_OOV(text_path='./dataset/test.txt',dic_path='./util/LM_dic.txt',
          dic2_path='./util/Bi_dic.txt',res_path='./output/seg_LM.txt'):
    """
    实现二元文法，没有未登录词处理
    :param text_path:需要分词的文件的地址
    :param dic_path: 一元文法词典所在地址，注意不要修改
    :param dic2_path:二元文法词典所在地址，注意不要修改
    :param res_path:结果要写入的地址
    :return:
    """
    seg = Bi_seg_without_OOV(text_path, dic_path, dic2_path)
    writeRes(seg, res_path)

def Part5(text_path='./dataset/test.txt',dic_path='./util/LM_dic.txt',
          dic2_path='./util/Bi_dic.txt',res_path='./output/seg_Bigram_OOV.txt'):
    """
    实现二元文法+未登录词处理,HMM参数已经训练完成，建议不要重新训练
    :param text_path:需要分词的文件的地址
    :param dic_path: 一元文法词典所在地址，注意不要修改
    :param dic2_path:二元文法词典所在地址，注意不要修改
    :param res_path:结果要写入的地址
    :return:
    """
    ##如果要重新训练HMM参数，把注释去除，但是请不要修改注释中的地址，谢谢
    # train_path = './dataset/199801_seg&pos.txt'
    # train_path2 = './dataset/199802.txt'
    # train_path3='./dataset/name.txt'
    # train = HMMTRAIN()
    # train.tag_text(train_path, './util/hmm_par.pkl', train_path2,train_path3)
    # print('HMM train finish')
    seg = Bi_seg(text_path, dic_path, dic2_path)
    writeRes(seg, res_path)

def Part6(text_path='./dataset/test.txt',model_save_path='./util/segTrain.pkl',res_path='./output/seg_Optimize.txt'):
    """
    最终优化结果的运行函数，所有的参数已经训练完成，不建议重新训练，直接读取训练结果即可
    注意：本部分分词时间较长，大约为10min，请耐心等待，谢谢;
    注意：本函数中出现的地址建议不要修改，谢谢
    :param text_path: 需要分词的文件的地址
    :param model_save_path: 模型参数存储的地址
    :param res_path: 分词结果需要写入的地址
    :return:
    """
    Seg_no_train(text_path,model_save_path,res_path)
    #如果想重新训练，将下面这一部分去除注释，上一行注释运行即可，注意不要修改地址
    # train_path1 = './dataset/199801_seg&pos.txt'
    # train_path2 = './dataset/199802.txt'
    # train_path3='./dataset/name.txt'
    # save_path = './util/BMSE.txt'
    # text_path = './dataset/test.txt'
    # save_path2 = './util/segTrain.pkl'
    # Seg_with_train(text_path,train_path1,train_path2,train_path3,save_path,save_path2,res_path)
if __name__=="__main__":

    ##这一部分作为代码测试部分，由于本次提交只涉及3.5,3.6，因此不再展示之前的部分

    text_path = './dataset/test.txt' ##如果要改测试文件请修改这一条路径，建议使用utf-8格式


    standart_path = './dataset/test_standard.txt'  # 测试集对应的标准分词文件地址，txt格式，建议使用utf-8格式文件
    Bi_res_path = './output/seg_LM.txt' ##二元文法分词无未登录词版本将会写入这个文件，utf-8格式
    Bi_res_path_OOV='./output/seg_Bigram_OOV.txt'##二元文法分词有未登录词版本将会写入这个文件，utf-8格式
    optimize_res_path = './output/seg_Optimize.txt'##二元文法分词将会写入这个文件，utf-8格式

    ##以下路径请不要修改，谢谢
    ##以下路径请不要修改，谢谢
    dic_path = './util/LM_dic.txt'
    dic2_path = './util/Bi_dic.txt'
    model_save_path='./util/segTrain.pkl'

    # Part5_No_OOV(text_path,dic_path,dic2_path,Bi_res_path)##这一行运行没有未登录词的二元文法
    # Part5(text_path,dic_path,dic2_path,Bi_res_path_OOV)##这一行运行二元文法+未登录词处理
    Part6(text_path,model_save_path,optimize_res_path)##这一行运行最终的优化算法

    # ##如果想要测试分词效果，请使用如下代码
    #
    # p,r,f=calc(standart_path, optimize_res_path)
    # with open('./output/temp_score.txt','a+')as fw:
    #     current_time=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
    #     fw.write(str(current_time)+'\t准确率：'+str(p)+'\t召回率：'+str(r)+'\t F值：'+str(f)+'\n')
    # fw.close()


