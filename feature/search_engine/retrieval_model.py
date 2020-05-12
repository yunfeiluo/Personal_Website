import math

class Query_Likelihood:
    def __init__(self, mu, inv_ind, docs):
        '''
        @param mu: parameter for QL algorithm
        @param inv_ind: the inverted list, in the form map: [term -> map: (docId -> positions)]
        @param docs: the collected document, in the form array[dict(doc)]
        '''
        self.mu = mu
        self.inv_ind = inv_ind
        self.docs = docs
        self.C = len(docs)
        self.scenes = dict() # map: doc_id -> score
        for i in range(len(self.docs)):
            self.scenes[i] = -1
    
    # lambda self, arr(tuple): dict
    def rebuild_dict(self, list_):
        dict_ = dict()
        for l in list_:
            dict_[l[0]] = l[1]
        return dict_

    # queries alg, return map: docId -> score
    def queries(self, queries):
        # TODO
        words = queries.split(' ')
        for scene in self.scenes:
            score = 0
            D = len(self.docs[scene]['text'])
            for word in words:
                fi = None
                try:
                    fi = len(self.inv_ind[word][scene])
                except:
                    fi = 0
                cqi = sum([len(self.inv_ind[word][i]) for i in self.inv_ind[word]])
                score += math.log((fi + self.mu * (cqi / self.C)) / (D + self.mu))
            self.scenes[scene] = score
        self.scenes = self.rebuild_dict(reversed(sorted(self.scenes.items(), key = lambda x:x[1])))
        return self.scenes

class BM25:
    def __init__(self, k1, k2, b, inv_ind, docs):
        '''
        @param k1, k2, b: parameters for BM25 algorithm
        @param inv_ind: the inverted list, in the form map: [term -> map: (docId -> positions)]
        @param docs: the collected document, in the form array[dict(doc)]
        '''
        self.k1 = k1
        self.k2 = k2
        self.b = b
        self.inv_ind = inv_ind
        self.docs = docs
        self.N = len(docs)
        self.avdl = 0
        self.scenes = dict() # map: doc_id -> score
        for i in range(self.N):
            self.scenes[i] = -1
            self.avdl += len(docs[i]['text'])
        self.avdl /= self.N
    
    # lambda self, arr(tuple): dict
    def rebuild_dict(self, list_):
        dict_ = dict()
        for l in list_:
            dict_[l[0]] = l[1]
        return dict_
    
    # queries alg, return map: docId -> score
    def queries(self, queries):
        qf = dict()
        for term in queries.split(' '):
            try:
                qf[term] += 1
            except:
                qf[term] = 1
        for scene in self.scenes:
            K = self.k1 * ((1 - self.b) + self.b * (len(self.docs[scene]['text']) / self.avdl))
            score = 0
            for q in qf:
                ni = 0
                fi = 0
                try:
                    ni = len(self.inv_ind[q])
                except:
                    ni = 0
                try:
                    fi = len(self.inv_ind[q][scene])
                except:
                    fi = 0
                out = math.log(1 / ((ni + 0.5) / (self.N - ni + 0.5)))
                out *= ((self.k1 + 1) * fi) / (K + fi)
                out *= ((self.k2 + 1) * qf[q]) / (self.k2 + qf[q])
                score += out
            self.scenes[scene] = score
        self.scenes = self.rebuild_dict(reversed(sorted(self.scenes.items(), key = lambda x:x[1])))
        return self.scenes