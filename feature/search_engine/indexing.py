class inverted_index:
    def __init__(self, docs):
        '''
        @param docs: map: ind -> [obj, [text]]
        '''
        self.docs = docs
        self.inv_ind = dict() # map: term -> map: doc_ind -> list of positions
        for i in docs:
            text = docs[i][1]
            for j in range(len(text)):
                term = text[j]
                try: # check if the term key exist
                    curr = self.inv_ind[term]
                except:
                    self.inv_ind[term] = dict()

                try: # check if the doc key exist
                    self.inv_ind[term][i].append(j)
                except:
                    self.inv_ind[term][i] = [j]
