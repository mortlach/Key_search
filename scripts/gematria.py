#!/usr/bin/env python
# simple gematria encoding

class gematria():
    def __init__(self):
        self.latin_fragments = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I',
                                'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'ING',
                                'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
        self.bigram = ['TH', 'EO', 'NG', 'OE', 'AE', 'IA', 'IO', 'EA']
        self.trgram = 'ING'

        self.rune_pos_f = {}
        self.rune_pos_r = {}
        f = 0
        r = 28
        for rune in self.latin_fragments:
            self.rune_pos_r[rune] = r
            self.rune_pos_f[rune] = f
            f += 1
            r -= 1
        self.rune_pos_f["NG"] = self.rune_pos_f["ING"]
        self.rune_pos_f["Z"] = self.rune_pos_f["S"]
        self.rune_pos_f["IO"] = self.rune_pos_f["IA"]
        self.rune_pos_f["K"] = self.rune_pos_f["C"]
        self.rune_pos_f["V"] = self.rune_pos_f["U"]

        self.rune_pos_r["NG"] = self.rune_pos_r["ING"]
        self.rune_pos_r["Z"] = self.rune_pos_r["S"]
        self.rune_pos_r["IO"] = self.rune_pos_r["IA"]
        self.rune_pos_r["K"] = self.rune_pos_r["C"]
        self.rune_pos_r["V"] = self.rune_pos_r["U"]

    def word_to_pos_f(self,word):
        r = []
        for rune in self.translate_to_gematria(word):
            r.append(self.rune_pos_f[rune])
        return r
    def word_to_pos_r(self,word):
        r = []
        for rune in self.translate_to_gematria(word):
            r.append(self.rune_pos_r[rune])
        return r

    def phrase_to_pos_f(self,phrase):
        r = []
        for word in phrase.split( ):
            r.append(self.word_to_pos_f(word))
        return r
    def phrase_to_pos_r(self, phrase):
        r = []
        for word in phrase.split( ):
            r.append(self.word_to_pos_r(word))
        return r

    def translate_to_gematria(self, word):  # thanks to 'solvers
        res = []
        skip = 0
        WORD = word.upper()
        WORD = WORD.replace("QU", "KW")
        for i, val in enumerate(WORD):
            if skip:
                skip -= 1
                continue
            if WORD[i:i + 3] == self.trgram:
                res.append(self.trgram)
                skip += 2
                continue
            if WORD[i:i + 2] in self.bigram:
                res.append(WORD[i:i + 2])
                skip += 1
                continue
            res.append(val)
        return res