import os, sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import hdbscan

import umap

sys.path.append('../')
from basicDrawing import *

class UmapAnalysis():
    def __init__(self, resdir):
        self.xtrain = np.load('%s/../pre/x_train.npy'%(resdir))
        self.xtest = np.load('%s/../pre/x_test.npy'%(resdir))
        
        npydir='%s/npy'%resdir
        self.xrec=np.load('%s/rec.npy'%(npydir))
        self.xlat=np.load('%s/lat.npy'%(npydir))
        self.xrec_test=np.load('%s/rec_test.npy'%(npydir))
        self.xlat_test=np.load('%s/lat_test.npy'%(npydir))
        
        self.save_dir='%s/umap'%resdir
        if_not_make(self.save_dir)
    
    def umap_embedding(self, data, save=None):
        reducer = umap.UMAP(random_state=42)
        reducer.fit(data)
        umaped = reducer.transform(data)
        assert(np.all(umaped == reducer.embedding_))
        print(umaped.shape)
        
        if save!=None:
            np.save('%s/umaped'%self.save_dir, umaped )
        return umaped

    def kmeans_clustering(self, data, n_cluster, save=None):
   
        clusterer = KMeans(init="k-means++", n_clusters=n_cluster, random_state=0, max_iter = 5)
        clusterer.fit(data)
        labels = clusterer.labels_
        print(labels.shape)
     
        if save!=None:
            np.save('%s/labels_%i'%(self.save_dir, n_cluster) ,labels)
        return labels
    
    def hdbscan_clustering(self, data, n_cluster, save=None):
   
        clusterer = hdbscan.HDBSCAN(min_cluster_size=n_cluster, gen_min_span_tree=True)
        labels=clusterer.fit(data)
        print(labels.shape)
     
        if save!=None:
            np.save('%s/labels_%i'%(self.save_dir, n_cluster) ,labels)
        return labels

    def plot_projection(self, data, labels='yellowgreen', figsize=(12,8), save=None):
            
        plt.figure(figsize=figsize)
        plt.scatter(data[:, 0], data[:, 1], c= labels, alpha=0.8, cmap='rainbow', marker='.')
        if type(labels)!=str:
            n_cluster = max(labels)+1
            plt.colorbar(boundaries=np.arange(n_cluster+1)-0.5).set_ticks(np.arange(n_cluster))
            plt.title('UMAP projection of the Latent space', fontsize=24);
        
            if save!=None:
                plt.savefig('%s/project_%i'%(self.save_dir, n_cluster))
        else: 
            if save!=None:
                plt.savefig('%s/project'%(self.save_dir))
        plt.show()
