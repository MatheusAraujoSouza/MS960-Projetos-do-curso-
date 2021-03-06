import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

################################################################################################
#Funções
def estimateGaussian(X):
    
    m = X.shape[0]
    
    sum_ = np.sum(X,axis=0)
    mu = 1/m *sum_
    
    sigma = 1/m * ((X - mu).T)@(X - mu)    
    return mu,sigma

def multivariateGaussian(X, mu, Sigma):
       
    k = len(mu)
    
    X = X - mu.T
    p = 1/((2*np.pi)**(k/2)*(np.linalg.det(Sigma)**0.5))* np.exp(-0.5* np.sum(X @ np.linalg.pinv(Sigma) * X,axis=1))
    return p

def selectThreshold(yval, pval):
    best_epi = 0
    best_F1 = 0
    
    stepsize = (max(pval) -min(pval))/1000
    epi_range = np.arange(pval.min(),pval.max(),stepsize)
    for epi in epi_range:
        predictions = (pval<epi)[:,np.newaxis]
        tp = np.sum(predictions[yval==1]==1)
        fp = np.sum(predictions[yval==0]==1)
        fn = np.sum(predictions[yval==1]==0)
        
        # compute precision, recall and F1
        prec = tp/(tp+fp)
        rec = tp/(tp+fn)
        
        F1 = (2*prec*rec)/(prec+rec)
        
        if F1 > best_F1:
            best_F1 =F1
            best_epi = epi
        
    return best_epi, best_F1
################################################################################################
#Leitura dos dados
mat = loadmat("dado1.mat")
X = mat["X"]
Xval = mat["Xval"]
yval = mat["yval"]

#Cálculo da média e da matriz de covariâncias da matriz X
mu, Sigma = estimateGaussian(X)

#Retorna o valor z da gaussiana nos pontos pertencentes à matriz X
p = multivariateGaussian(X, mu, Sigma)

#Cálculo do valor da variância nos pontos do conjunto de validação Xval
pval = multivariateGaussian(Xval, mu, Sigma)

#Cálculo dos valores de epsilon e F1
epsilon, F1 = selectThreshold(yval, pval)

#Determina os pontos anômalos
Xanomaly = X[p<epsilon, :]

#Plota todos os pontos e circula as anomalias
plt.scatter(X[:,0],X[:,1],marker="x")
plt.scatter(Xanomaly[:,0],Xanomaly[:,1],marker="o", s = 100, edgecolors='r', facecolors='none')
plt.xlim(0,30)
plt.ylim(0,30)
plt.xlabel("Latência (ms)")
plt.ylabel("Taxa de transferência (mb/s)")
            
