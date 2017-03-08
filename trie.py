"""
    Text Trie (prefix and postfix) class for string storage. Provides a set of strings with optimized storage and lookup.

    Trie storage optimizes lookup times after adding words to the trie by combining common substrings, then performing a (singlei- or multi-) character-level comparison scan with the member in question.
"""

import re

# TODO implement path compression
class Trie:
    """ Nodes for prefix and postfix tries. 'is_word' flag denotes if complete word terminates with it. """
    def __init__(self, pre = True, is_word = False):
        self.branches = {}
        self.is_word = is_word
        self.pre = pre

        if self.pre:
            def sub_set(wordset,letter):
                return set([word[1:] for word in wordset if word and word[0] == letter])
        else:
            def sub_set(wordset,letter):
                return set([word[:-1] for word in wordset if word and word[-1] == letter])

        self.sub_set = sub_set

    def _add_branch(self, char, is_word):
        self.branches[char] = Trie(self.pre, is_word)

    def _gen_alphabet(self):
        """ Generator for alphabet characters. """
        for x in list(xrange(ord('a'),ord('z')+1)):
            yield chr(x)

    def insert(self,wordset):
        """ Add a single word or an iterable of text strings """
        if isinstance(wordset,basestring):
            wordset = [wordset]
        for letter in self._gen_alphabet():
            p = self.sub_set(wordset,letter)
            if p:
                if not self.branches.has_key(letter):
                    # '' in p means the set contained a word which has been spelled
                    self._add_branch(letter,'' in p)
                self.branches[letter].insert(p)

    def check(self,word):
        """ If word is reachable from this trie, return resulting trie. """
        if self.pre:
            def sub_word(chars):
                if re.match('^'+chars+'.*',word):
                    return word[len(chars):]
                else:
                    return False
        else:
            def sub_word(chars):
                if re.match('^.*'+chars+'$',word):
                    return word[:-len(chars)]
                else:
                    return False

        if word == '':
            return True
        for chars in self.branches.keys():
            res =  sub_word(chars)
            if res:
                return self.branches[chars].check(res)
            elif res == '':
                return True
        return False

    def get_words(self, chars = None):
        """ Return all existing words derived from this trie with prefix chars """
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

        # If this trie marks an existing word, pass back empty string to parent
        # tries to rebuild this word separately from any derived compound words
        if self.is_word:
            selfwordmarker = ['']
        else:
            selfwordmarker = []

        return  [word for sublist in \
                   [[apre(word,key) for word in self.branches[key].get_words()]\
                   for key in self.branches.keys()]\
                for word in sublist] + selfwordmarker

    def __repr__(self):
        if self.is_word:
            xst = 'Is a word.  '
        else:
            xst = 'Non-word. '
        if self.pre:
            cpnd= 'Put at the end to build: '
        else:
            cpnd= 'Put in front to build: '
        return xst+'\n'+cpnd+str(self.branches.keys())
