import matplotlib.pyplot as plt
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
        self.C = sum([len(play['text']) for play in docs])
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

class inv_ind:
    def __init__(self, docs):
        self.docs = docs

    # lambda self, arr(tuple): dict
    def rebuild_dict(self, list_):
        dict_ = dict()
        for l in list_:
            dict_[l[0]] = l[1]
        return dict_

    # build inverted index
    def build(self):
        ind = dict() # map: [term -> map: (docId -> positions)]
        for i in range(len(self.docs)):
            for j in range(len(self.docs[i]['text'])):
                if ind.get(self.docs[i]['text'][j]) == None:
                    ind[self.docs[i]['text'][j]] = {i:[j]}
                else:
                    try:
                        ind[self.docs[i]['text'][j]][i].append(j)
                    except:
                        ind[self.docs[i]['text'][j]][i] = [j]
                # try: # map: (term -> postings)
                #     ind[self.docs[i]['text'][j]].append((i+1, j+1))
                # except:
                #     ind[self.docs[i]['text'][j]] = [(i+1, j+1)]
        self.ind = self.rebuild_dict(sorted(ind.items(), key=lambda x:x[0]))
    

############### below is mainly for p3 #########################
    # term-based queries
    def query_term(self, terms, id_):
        plays = set()
        for term in terms:
            try:
                for i in self.ind[term]:
                    if id_ != None:
                        plays.add(self.docs[i][id_])
                    else:
                        plays.add(i)
            except:
                print('term ' + term + ' does not exist.')
        return sorted(plays)

    # phrase-based queries
    def query_phrase(self, terms, id_):
        if len(terms) <= 1:
            return self.query_term(terms, id_)

        plays = set()

        try:
            for i in self.ind[terms[0]]: # i is dict of doc->positions
                for j in self.ind[terms[0]][i]: # each position in i
                    contain = True
                    for k in range(1, len(terms)):
                        try:
                            if j + k not in self.ind[terms[k]][i]:
                                contain = False
                                break
                        except:
                            contain = False
                            break
                    if contain:
                        plays.add(self.docs[i][id_])
                        break
        except:
            print('some term does not exist')
        return plays
    
    # other helper functions
    def helper0(self, term0, term1, term2, id_):
        plays = set()
        for i in self.ind[term0]:
            if self.ind[term2].get(i) != None and len(self.ind[term0][i]) > len(self.ind[term2][i]):
                plays.add(self.docs[i][id_])
        for i in self.ind[term1]:
            if self.ind[term2].get(i) != None and len(self.ind[term1][i]) > len(self.ind[term2][i]):
                plays.add(self.docs[i][id_])
        return sorted(plays)
    
    def helper1(self, terms):
        y = list()
        x = list()
        for i in range(len(self.docs)):
            curr_y = 0
            x.append(i)
            for term in terms:
                curr_y += len(self.ind[term][i]) if self.ind[term].get(i) != None else 0
            y.append(curr_y)

        plt.plot(x, y)

        # plt.ylabel('count of \'thee\' or \'thou\'')
        plt.ylabel('count of \'you\'')
        plt.xlabel('sceneNum')

        plt.show()

    def comp_scene(self, res):
        all_scene = dict()
        for doc in self.docs:
            all_scene[doc['sceneId']] = len(doc['text'])
        #print(len(all_scene) == len(self.docs))
        return sorted(all_scene.items(), key=lambda x: x[1])[0] if res == 'shortest' else sum([all_scene[i] for i in all_scene]) / len(all_scene)

    def comp_play(self, res):
        all_play = dict()
        for doc in self.docs:
            try:
                all_play[doc['playId']] += len(doc['text'])
            except:
                all_play[doc['playId']] = len(doc['text'])
        all_play = sorted(all_play.items(), key=lambda x: x[1])
        return all_play[0] if res == 'shortest' else all_play[-1]
