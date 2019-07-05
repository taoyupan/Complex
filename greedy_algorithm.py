'图顶点着色的贪婪盒覆盖算法'
import numpy as np
import random

class Greed:
    def __init__(self,B):
        self.B = B   # 网络的距离矩阵
        self.max_box = int(np.max(self.B))+1   # 覆盖网络的最大盒子直径

    def greed(self):
        n = len(self.B)
        L_boxs = list(range(1,self.max_box+1))  # 所有盒子的直径
        nodes = [i for i in range(n)]
        random.shuffle(nodes)
        random_node_id = nodes
        node_id_index = np.argsort(random_node_id)
        C = np.zeros([n,self.max_box])
        for i in range(self.max_box):
            C[:,i] = [j for j in range(1,n+1)]
        C[node_id_index[0],:] = 0    # 把节点id为0的顶点着色为颜色0
        colors = list(C[:,0]).copy()
        for L_box in L_boxs:
            for i in range(1,n):
                index1 = node_id_index[i]
                set_ = []
                for j in range(i):
                    index2 = node_id_index[j]
                    if self.B[index1,index2] >= L_box:
                        set_.append(C[index2,L_box-1])
                if set_:
                    C[index1, L_box - 1] = min(set(colors).difference(set(set_)))
                else:
                    C[index1, L_box - 1] = min(C[:,L_box - 1])
        return C

    def counter_box(self,C):
        n = C.shape[1]
        res = []
        for i in range(n):
            res.append(len(set(C[:,i])))
        return res









