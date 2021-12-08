## 各部分相关代码
注：所有的输出文件都在./output中
0.所有的代码测试可以在Test_my_code.py中完成，其中函数PartX对应实验指导中3.X的要求，每一部分的测试要求在注释中均详细注明，包括可以修改的地址与不能修改的地址。

1.生成词典：createDic.py中实现生成词典

2.无优化FMM与BMM：FMM_BMM.py

3.评分函数：score.py

4.优化FMM：Fast_FMM.py，其中实现了二分查找与哈希查找，HashSet.py文件自定义了一个哈希表的类

5.二元文法实现：LM_Bi_without_OOV.py实现的是未加入未登录词的二元文法，

LM_Bi.py是加入了未登录词处理的二元文法，测试方式详情可见Test_my_code.py中Part5部分注释。其中HMM.py是为了支持未登录词做出的HMM，单纯使用HMM分词效果不佳

6.最终优化版本：Optimize1.py：实现了一定的优化，运行方式可见est_my_code.py中Part6部分注释。这一部分分词时间较长，在笔记本上测试大约需要8-15分钟，麻烦耐心等待，谢谢。



输出文件解释：

1.util文件夹中存储一些模型的参数，例如HMM的参数，建议不要移动

2.output文件夹中存储所有的分词结果，对于3.5和3.6小节，seg_LM.txt是没有未登录词的二元文法结果；seg_Bigram_OOV.txt是加上未登录词的二元文法的结果；seg_Optimize.txt是进一步优化之后的分词结果。

3.如果分词结果评判要使用本实验实现的函数来做，代码操作详见Test_my_code.py最下面部分。输出将在./output/temp_score.txt，输出格式为当前时间，准确率，召回率，F值。



**./dataset/test.txt**是我自己找的测试集，**与训练集并不重合**，而与之对应的**./dataset/test_standard.txt**是其对应的标准划分。如果要替换测试集参考代码中的注释，改变路径即可
