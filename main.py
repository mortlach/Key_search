#!/usr/bin/env python
# basic rune arithmetic on cribs for the first 6 runes of each red rune section start
from scripts.rune_arithmetic import rune_arithmetic
import time


# this class does all the work
# pass build = True to build all the encryption / decryption maps
# these are then saved and need to be built again
cipher = rune_arithmetic(build = False)
#
# INPUT DATA FOR DECRYPTING
#
# output file suffixes
suffix = ['_ct1_8_5.txt', '_ct2_2_11.txt', '_ct4_4_1_4.txt', '_ct5_2_4.txt', '_ct6_4_8.txt',
          '_ct7_4_5.txt', '_ct8_4_2.txt', '_ct9_2_6.txt', '_ct10_3_12.txt', '_ct11_2_8.txt',
          '_ct12_3_5.txt', '_ct14_3_5.txt', '_ct15_1_8.txt']
#
# files with all cribs (with unique first 6 runes) for desired word lengths (given in file name)
crib_file = ['./red_rune_cribs/cut_to_6/ct1_8_5_M_cut6.txt',
             './red_rune_cribs/cut_to_6/ct2_2_11_M_cut6.txt',
             './red_rune_cribs/cut_to_6/ct4_4_1_4_M_cut6.txt',
             './red_rune_cribs/cut_to_6/ct5_2_4_M_cut6.txt',
             './red_rune_cribs/cut_to_6/ct6_4_8_M_cut6.txt',
             './red_rune_cribs/cut_to_6/ct7_4_5_M_cut6.txt',
             './red_rune_cribs/cut_to_6/ct8_4_2_M_cut6.txt',
             './red_rune_cribs/cut_to_6/ct9_2_6_M_cut6.txt',
             './red_rune_cribs/cut_to_6/ct10_3_12_M_cut6.txt',
             './red_rune_cribs/cut_to_6/ct11_2_8_M_cut6.txt',
             './red_rune_cribs/cut_to_6/ct12_3_5_M_cut6.txt',
             './red_rune_cribs/cut_to_6/ct14_3_5_M_cut6.txt',
             './red_rune_cribs/cut_to_6/ct15_1_8_M_cut6.txt']
#
# forward and reverse gematria encoded cipher text (red runes, apart from the single 3 rune words)
allct = [[[15,8,18,3,6,19,27,0,15,26,18,21,5],[13,20,10,25,22,9,1,28,13,2,10,7,23]],
[[20,11,12,8,21,5,2,16,25,11,16,14,8,16,1,22],[8,17,16,20,7,23,26,12,3,17,12,14,20,12,27,6]],
[[24,16,14,17,19,6,27,15,17,14,12],[4,12,14,11,9,22,1,13,11,14,16]],
[[23,3,22,16,2,25],[5,25,6,12,26,3]],
[[14,10,14,19,1,14,19,5,2,13,3,17],[14,18,14,9,27,14,9,23,26,15,25,11]],
[[0,1,20,19,24,28,26,22,24],[28,27,8,9,4,0,2,6,4]],
[[20,1,21,9,5,1,17,9,16,0,21],[8,27,7,19,23,27,11,19,12,28,7]],
[[1,24,7,21,6,14,23,6,10,17,10,12,16,17,10,26],[27,4,21,7,22,14,5,22,18,11,18,16,12,11,18,2]],
[[19,13,26,20,15,3,24,25,8,20,18,12,10,19,20,20,15,5,13],[9,15,2,8,13,25,4,3,20,8,10,16,18,9,8,8,13,23,15]],
[[23,12,14,5,0,10,24,7,8,6],[5,16,14,23,28,18,4,21,20,22]],
[[21,2,12,10,0,5,22,12],[7,26,16,18,28,23,6,16]],
[[0,9,19,26,6,23,25,8],[28,19,9,2,22,5,3,20]],
[[24,19,21,23,27,2,14,10,19],[4,9,7,5,1,26,14,18,9]]]
#
# loop over each data-set, find plus/minus keys, write all data to files
start = time.time()
for i in range(0,len(suffix)):
    [ct_f, ct_r] = allct[i]
    cipher.get_pm_keys(ct_f = ct_f[0:6] , ct_r = ct_r[0:6], file_suffix = suffix[i],
                       crib_file= crib_file[i] )
print('Plus/minus keys, FIN, Total Time  = ', time.time() - start)

#
# # loop over each data-set, find multiply/divide keys, write all data to files
# # this one takes a while (we include all shifts of gematria ... !
# start = time.time()
# for i in range(0,len(suffix)):
#     [ct_f, ct_r] = allct[i]
#     cipher.get_md_keys(ct_f = ct_f[0:6] , ct_r = ct_r[0:6], file_suffix = suffix[i],
#                        crib_file= crib_file[i] )
# print('Multiply/Divided keys, FIN, Total Time  = ', time.time() - start)

