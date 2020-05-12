'''
# ---------------------------------------------------------------- 
# cs 446 Search Engine P3
#
# filename: run.py
# Functionality: Inverted Index (read input -> do sth -> write output)
# Author: Yunfei Luo
# Start date: EST Feb.20th.2020
# Last update: EST Feb.20th.2020
# ----------------------------------------------------------------
'''

import sys
import time
import gzip
import json
#import numpy as np
import src.class_lib as cl

# read file (with dependencies on gzip)
def readgz(filename):
    with gzip.open(filename, "r+") as f:
        data = f.read().decode("utf-8")
    return data

# write file
def writeFile(filename, arr):
    cont = ''
    for a in arr:
        cont += str(a) + '\n'
    with open(filename, 'w+') as f:
        f.write(cont)

# write file in TREC form
def to_TREC(i, res, tag, docs):
    '''
    @param res: map: sceneId -> score
    '''
    out = ''
    rank = 1
    for scene in res:
        curr = 'Q' + str(i) # 1st col
        curr += ' skip'# 2nd col
        curr += ' ' + docs[scene]['sceneId'] # 3rd col
        curr += ' ' + str(rank) # 4th col
        curr += ' ' + str(res[scene]) # 5th
        curr += ' ' + tag # 6th
        curr += '\n'
        out += curr
        rank += 1
    return out

# main driver
if __name__ == '__main__':
    filename = None
    try:
        filename = sys.argv[1] # command line argument
    except:
        filename = 'shakespeare-scenes.json.gz'

    # read then parse the file
    print('Reading files...')
    docs = readgz(filename) # documents
    docs = json.loads(docs)['corpus'] # list of play, each is a dictionary

    # split the text by spaces, str -> array of str
    for play in docs:
        play['text'] = [i for i in play['text'].split(' ') if len(i) > 0]

    # build inverted index
    print('Building inverted index...')
    inv_ind = cl.inv_ind(docs) # create inverted index object
    inv_ind.build()

    ##############  programming project 4  ######################
    Qs = ['the king queen royalty', 'servant guard soldier', 'hope dream sleep', 'ghost spirit', 'fool jester player', 'to be or not to be']
    BM25 = cl.BM25(k1=1.1, k2=10, b=0.6, inv_ind = inv_ind.ind, docs=docs)
    QL = cl.Query_Likelihood(mu=1000, inv_ind = inv_ind.ind, docs=docs)

    print('Query with BM25 and QL...')
    start = time.time()
    acc_bm25 = ''
    acc_ql = ''
    for i in range(len(Qs)):
        res = BM25.queries(Qs[i])
        acc_bm25 += to_TREC(i + 1, res, 'jjfoley-bm25', docs)

        res = QL.queries(Qs[i])
        acc_ql += to_TREC(i + 1, res, 'jjfoley-ql', docs)
    end = time.time()
    print("Query time: " + str(end - start) + ' s')

    print('Write result from bm25 to file...')
    with open('bm25.trecrun', 'w+') as f:
        f.write(acc_bm25)
    with open('ql.trecrun', 'w+') as f:
        f.write(acc_ql)
    
    judg = ''
    res_bm25 = BM25.queries(Qs[4])
    res_ql = QL.queries(Qs[4])
    i = 0
    for j in res_bm25:
        if i >= 10:
            break
        judg += docs[j]['sceneId'] + ' \n'
        i += 1
    i = 0
    for j in res_ql:
        if i >= 10:
            break
        judg += docs[j]['sceneId'] + ' \n'
        i += 1
    with open('judgments.txt', 'w+') as f:
        f.write(judg)

    # print('For report questions...')
    # res = QL.queries('setting the scene')
    # res = to_TREC(0, res, 'jjfoley-try', docs).split('\n')
    # for line in res:
    #     print(line)


##############  programming project 3  #######################
    # # term-based queries
    # start = time.time()
    # #plays = inv_ind.query_term(["verona", "rome", 'italy'], "sceneId")
    # #plays = inv_ind.helper0("thee", "thou", 'you', "sceneId")
    # plays = inv_ind.query_phrase("a rose by any other name".split(' '), "sceneId")
    # end = time.time()
    # print('Time used for query: ' + str(end - start) + ' s')

    # writeFile('phrase1.txt', plays)

    # #print(inv_ind.comp_scene('shortest'))
    # #print(inv_ind.comp_scene('avg'))
    # # print(inv_ind.comp_play('shortest'))
    # # print(inv_ind.comp_play('longest'))
    
    # # inv_ind.helper1(['thee', 'thou'])
    # inv_ind.helper1(['you'])
