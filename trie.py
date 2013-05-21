def gen_alphabet():
    """ Generator for alphabet characters. """
    for x in list(xrange(ord('a'),ord('z')+1)):
        yield chr(x)

class trienode:
    """ Nodes for prefix and postfix tries. 'exists' flag denotes if complete word terminates with it. """
    def __init__(self, pre = True, exists = True):
        self.branches = {}
        self.exists = exists
        self.pre = pre

    def add_branch(self, char, pre, exists = True):
        self.branches[char] = trienode(pre, exists)

    def grow(self, wordset):
        self.branches.clear()

        if self.pre:
            def sub_set(s,p):
                return set([x[1:] for x in s if x and x[0] == p])
                # re.match('^'+p+'.*',x)
        else:
            def sub_set(s,p):
                return set([x[:-1] for x in s if x and x[-1] == p])

        for letter in gen_alphabet():
            p = sub_set(wordset,letter)
            if p:
                # '' in p means the set contained a word which has been spelled
                self.add_branch(letter,self.pre,'' in p)
                self.branches[letter].grow(p)

    def check(self,word):
        """ If word is reachable from this node, return resulting node. """
        if self.pre:
            def sub_word(chars):
                if re.match('^'+chars+'.*',word):
                    return word[len(chars):]
                else:
                    return None
        else:
            def sub_word(chars):
                if re.match('^.*'+chars+'$',word):
                    return word[:-len(chars)]
                else:
                    return None

        if word == '':
            return self
        for chars in self.branches.keys():
            res =  sub_word(chars)
            if res:
                return self.branches[chars].check(res)
            elif res == '':
                return self.branches[chars]
        return None

    def get_words(self, chars = None):
        """ Return all existing words derived from this node, with prefix chars.
        """
        if not self.branches.keys():
            return ['']

        if self.pre:
            def apre(word,letter):
                return letter + word
        else:
            def apre(word,letter):
                return word + letter

        if chars:
            sub = self.check(chars)
            if sub:
                return [apre(x,chars) for x in sub.get_words()]
            else:
                return []

        # If this node marks an existing word, pass back empty string to parent
        # nodes to rebuild this word separately from any derived compound words
        if self.exists:
            selfwordmarker = ['']
        else:
            selfwordmarker = []

        return  [word for sublist in \
                   [[apre(word,key) for word in self.branches[key].get_words()]\
                   for key in self.branches.keys()]\
                for word in sublist] + selfwordmarker

    def __repr__(self):
        if self.exists:
            xst = 'Is a word.  '
        else:
            xst = 'Non-word. '
        if self.pre:
            cpnd= 'Put at the end to build: '
        else:
            cpnd= 'Put in front to build: '
        return xst+'\n'+cpnd+str(self.branches.keys())
