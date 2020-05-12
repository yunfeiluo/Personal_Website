class preprocess:
    '''
    tokenize, stopwords removel, stemming
    '''
    def __init__(self, stopwords, json_file):
        # stored
        self.text = dict() # map: ind -> [obj, [text]]

        # fetch all the documents
        self.ind = 0
        def dfs(item):
            self.text[self.ind] = [item, list()]
            self.ind += 1
            if len(item["docs"]) == 0:
                return
            for sub_item in item["docs"]:
                dfs(sub_item)

        for key in json_file:
            for item in json_file[key]:
                dfs(item)

        self.stopwords = dict() # map: words -> bool
        for word in stopwords:
            self.stopwords[word] = True

    # remove the dot '.' in the string, return string
    def removeD(self, word):
        res = list()
        lw = len(word)
        phrase = ''
        curr = ''
        sl = 0
        for i in range(lw):
            if word[i] != '.':
                curr += word[i]
                sl += 1
            else:
                if sl == 1:
                    sl = 0
                    phrase += curr
                    curr = ''
                    continue
                else:
                    res.extend([phrase, curr] if len(phrase) >= 1 else [curr])
                    curr = ''
                    phrase = ''
        if len(phrase) >= 1:
            res.append(phrase)
        if len(curr) >= 1:
            res.append(curr)
        return res

    def tokenize(self, lines):
        words = list()
        # split by space
        for line in lines:
            word = ''
            for c in line:
                if c.isalpha():
                    word += c.lower()
                elif c.isdigit() or c == '.':
                    word += c
                else:
                    if len(word) >= 1:
                        words.extend(self.removeD(word))
                    word = ''
        return words
    
    def stopword_removel(self):
        for i in self.text:
            words = list()
            for word in self.text[i][1]:
                try:
                    curr = self.stopwords[word]
                except:
                    words.append(word)
            self.text[i][1] = words

    
    def pre_process(self):
        for i in self.text:
            lines = list()
            path = self.text[i][0]["path"]
            try:
                with open(path[:len(path) - 3] + 'txt', 'r') as f:
                    lines = f.read()
                    lines = lines.split('\n')
                    lines.pop()
            except:
                continue

            words = self.tokenize(lines)
            self.text[i][1] = words
        return self
    
    def stemming(self):
        from nltk.stem.snowball import SnowballStemmer
        stemmer = SnowballStemmer("english")
        for i in self.text:
            words = self.text[i][1]
            for i in range(len(words)):
                words[i] = stemmer.stem(words[i])
        return self