'离散粒子群算法求网络的盒覆盖问题'
import numpy as np
import random
from greedy_algorithm import Greed
import matplotlib.pyplot as plt
class DpsoBc():
    def __init__(self,A,B,L_b,pop=30,W=0.67,c1=1.44,c2=1.44,G = 100):
        self.A = A  # A 为网络的距离矩阵
        self.B = B   # B 为网络的邻接矩阵
        self.L_b = L_b-1  # 盒子的直径
        self.pop = pop
        self.W = W
        self.c1 , self.c2 = c1 , c2
        self.G = G
        self.n = len(self.A)

    def main(self):
        X = np.zeros([self.pop,self.n])
        g = Greed(self.A)
        for i in range(self.pop):
            X[i,:] = g.greed()[:,self.L_b]  # 初始化种群
        V = np.zeros([self.pop,self.n])
        for i in range(self.pop):
            for j in range(self.n):
                V[i,j] = random.randint(0,1)  # 初始化速度
        pg_best = X[self.pop-1,:]    # 先假设种群全局最佳粒子为种群的最后一个粒子
        p_best = np.zeros([self.pop,self.n])
        for i in range(self.pop):
            p_best[i,:] = X[i,:]  # 个体历史最优
            if len(set(X[i,:])) < len(set(pg_best)):
                pg_best = X[i,:]  # 当前全局最优
        X_new = np.zeros([self.pop,self.n])
        V_new = np.zeros([self.pop,self.n])
        each_generation_bestfit_value = []
        for t in range(self.G):
            for i in range(self.pop):
                V_new[i,:] = self.Sig(self.W * V[i,:]
                                  + self.c1 * random.uniform(0,1) * self.Xor(p_best[i,:],X[i,:])
                                  + self.c2 * random.uniform(0,1) * self.Xor(pg_best,X[i,:]))
                for j in range(self.n):
                    if V_new[i,j] == 0:
                        X_new[i,j] = X[i,j]
                    else:
                        x_j = X[i,j]
                        X_new[i,j] = x_j
                        N , B = list(X[i,:]) , list(X[i,:])
                        while B:
                            index1 = random.randint(0,len(B)-1)
                            x_k = B.pop(index1)
                            if x_k == x_j:
                                continue
                            ID , L = [] , []
                            for index , value in enumerate(N):
                                if x_k == value:
                                    ID.append(index)
                                    L.append(value)
                            count = 0
                            for k in ID:
                                if self.A[k,j] >= self.L_b+1:
                                    break
                                else:
                                    count += 1
                            if count == len(ID):
                                X_new[i,j] = L[0]
                                break
                            else:
                                continue
            for i in range(self.pop):
                # 更新个体历史最佳位置
                if len(set(X_new[i,:])) < len(set(p_best[i,:])):
                    p_best[i,:] = X_new[i,:]
                else:
                    p_best[i,:] = X[i,:]
                # 更新全局最佳
                if len(set(X_new[i,:])) < len(set(pg_best)):
                    pg_best = X_new[i,:]
            X = X_new
            V = V_new
            each_generation_bestfit_value.append(len(set(pg_best)))
        return pg_best, each_generation_bestfit_value

    def Sig(self,X):
        V = []
        for i in range(len(X)):
            if random.uniform(0,1) < self.Sigmoid(X[i]):
                V.append(1)
            else:
                V.append(0)
        return np.array(V)

    def Sigmoid(self,x):
        return 1/(1+np.exp(-x))

    def Xor(self,X,Y):
        n = len(X)
        y = []
        for i in range(n):
            if X[i] == Y[i]:
                y.append(0)
            else:
                y.append(1)
        return np.array(y)

    def plot_dpsobc(self):
        value = self.main()[1]
        x = self.G
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['font.family'] = 'sans-serif'
        plt.xlabel('DPSOBC迭代的次数')
        plt.ylabel('每代所求的盒子个数')
        plt.plot(list(range(x)),value)
        plt.show()
















