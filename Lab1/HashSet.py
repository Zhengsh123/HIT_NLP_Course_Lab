"""
本文件用于定义一个HashSet，冲突用链表法解决
"""
#定义链表节点
class Node:
    def __init__(self,word=None):
        self.word=word
        self.next=None
    def add(self,next):
        self.next=next
#定义哈希表
class HashSet:
    def __init__(self,length):
        """
        初始化哈希表
        :param length:哈希表长度
        """
        self.length =length
        self.hashSet=[]
        self.nullNode=Node("")
        for i in range(self.length):
            self.hashSet.append(self.nullNode)

    ##哈希函数
    def __hash(self,word):
        """
        哈希散列函数
        :param word:需要散列的词
        :return:
        """
        word_hash=0
        for char in word:
            char_hash=ord(char)*6143
            word_hash=word_hash+char_hash
        return int((word_hash & 0x7FFFFFFF))

    ##冲突的时候构建链表
    def add(self,word):
        """
        向散列表中添加元素，发生冲突时采用链表法
        :param word:需要添加的元素
        :return:
        """
        index = hash(word) % self.length
        newNode = Node(word)
        if self.hashSet[index] == self.nullNode:
            self.hashSet[index] = newNode
        else:
            current = self.hashSet[index]
            # 找到最后一个词，插入最后
            while current.next is not None:
                if current.word == word:
                    return False
                current = current.next
            current.add(newNode)
        return True
    def __contains__(self, word):
        index = hash(word) % self.length
        if self.hashSet[index] == self.nullNode:
            return False
        else:
            current = self.hashSet[index]
            while current.word != word:
                current = current.next
                if (current == None or len(current.word)>len(word)):
                    return False
            return True


