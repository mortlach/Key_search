#!/usr/bin/env python
# basic key comparison, first the prime sequence
import os
import time

class key_matcher(object):
    def __init__(self):
        self.k_e = 'e'
        self.wc = '*'
        self.prime_seq = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                          73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        self.prime_seq_shifted = [x - self.prime_seq[0] for x in self.prime_seq]

        self.fib1_seq = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        self.fib1_seq_shifted = [x - self.fib1_seq[0] for x in self.fib1_seq]
        self.fib2_seq = [1, 2, 3, 5, 8, 13, 21, 34, 55]
        self.fib2_seq_shifted = [x - self.fib2_seq[0] for x in self.fib2_seq]
        self.fib3_seq = [0, 1, 1,  2, 3, 5, 8, 13, 21, 34, 55]
        self.fib3_seq_shifted = [x - self.fib3_seq[0] for x in self.fib3_seq]

    def is_wildcard(self, x):
        if x == self.k_e:
            return True
        elif x == self.wc:
            return True
        return False

    def wildcard_count(self, a_list):
        a = len([p for p in a_list if p == self.wc])
        b = len([p for p in a_list if p == self.k_e])
        return a + b

    def key_match(self, key, test):
        for i, k in enumerate(key):
            if self.is_wildcard(k):
                pass
            elif k != test[i]:
                return False
        return True

    def prime_seq_shifted_match(self, key):
        return self.key_match(key , self.prime_seq_shifted)

    def fib_seq_shifted_match(self, key):
        if self.key_match(key , self.fib1_seq_shifted):
            return True
        if self.key_match(key, self.fib2_seq_shifted):
            return True
        if self.key_match(key, self.fib3_seq_shifted):
            return True
        return False

    def get_end_key(self, string):
        a = []
        for i in string.split(',')[-1].split():
            if self.is_wildcard(i):
                a.append(i)
            else:
                a.append(int(i))
        return a

    def test_prime_seq_shifted(self, files_in, file_out):
        x = 0
        start = time.time()
        with open(file_out, 'a') as out_file:
            for file in files_in:
                print 'Checking ' + file
                with open(file , 'r') as data:
                    for line in data:
                        if self.prime_seq_shifted_match(self.get_end_key(line)):
                            print line
                            x += 1
                            out_file.write(line)
        print 'Found ' + str(x) + ' prime keys'
        print 'Took ' + str(time.time() - start)

    def test_fib_seq_shifted(self, files_in, file_out):
        x = 0
        start = time.time()
        with open(file_out, 'a') as out_file:
            for file in files_in:
                print 'Checking ' + file
                with open(file , 'r') as data:
                    for line in data:
                        if self.fib_seq_shifted_match(self.get_end_key(line)):
                            print line
                            x += 1
                            out_file.write(line)
        print 'Found ' + str(x) + ' Fibonacci keys'
        print 'Took ' + str(time.time() - start)

    def find_prime_seq_shifted(self, dir, file_out):
        files = [dir + '/' + x for x in  os.listdir(dir)]
        self.test_prime_seq_shifted(files, file_out)

    def find_fib_seq_shifted(self, dir, file_out):
        files = [dir + '/' + x for x in  os.listdir(dir)]
        self.test_fib_seq_shifted(files, file_out)


km = key_matcher()
#
# print 'Checking Plus Minus Keys'
# dir = "./pm_keys"
# x = km.find_prime_seq_shifted(dir,'prime_keys.txt')
#
#
# print 'Checking Multiply Divide Keys'
# dir = "./md_keys"
# x = km.find_prime_seq_shifted(dir,'prime_keys.txt')

print 'Looking for Fibonacci sequence'
print 'Checking Plus Minus Keys'
dir = "./pm_keys"
x = km.find_fib_seq_shifted(dir,'fib_keys.txt')

print 'Checking Multiply Divide Keys'
dir = "./md_keys"
x = km.find_fib_seq_shifted(dir,'fib_keys.txt')




# with open('prime_keys_cut.txt','a') as out:#
#     with open('prime_keys.txt','r') as f:#
#         for line in f:
#             if km.wildcard_count(km.get_end_key(line)) < 2:
#                 out.write(line)

with open('fib_keys_cut.txt','a') as out:#
    with open('fib_keys.txt','r') as f:#
        for line in f:
            if km.wildcard_count(km.get_end_key(line)) < 2:
                out.write(line)

