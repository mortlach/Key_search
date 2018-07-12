#!/usr/bin/env python
# basic rune arithmetic functions, mod 29
# written out so that each step can be followed for each method
from memoize import Memoize
import os
import pickle

# mod 29
@Memoize
def mod29(k):
	if isinstance(k,int):
		return k % 29
	return k

def mod29L(list):
	a = []
	for item in list:
		a.append(mod29(item))
	return a

# arithmetic functions
@Memoize
def plus_m29(rune1, rune2):
	return mod29(rune1 + rune2)

@Memoize
def minus_m29(rune1, rune2):
	return mod29(rune1 - rune2)

@Memoize
def multiply_m29(rune1, rune2):
	return mod29(rune1 * rune2)

@Memoize
def divide_mod29(rune1, rune2):
	''' for a prime modulus p
		y = pow(x, p-2, p)
	'''
	return mod29(rune1 * pow(rune2, 27, 29))


'''
	We can create encryption/decryption dictiionaries. In Python dictionaries can't have lists as 
	keys so we convert the first two runes in each list to a unique string  
'''
@Memoize
def to_dict_key(rune_1, rune_2, rune_3 = ''):
		if rune_3 == '':
			return str(rune_1) + '_' + str(rune_2)
		return str(rune_1) + '_' + str(rune_2) + '_' + str(rune_3)
'''
    some functions don't give well-formed  answers (i.e divide by zero) so we have some wildcards
'''
@Memoize
def is_wildcard(r):
	if r == 'e':
		return True
	elif r == '*':
		return True
	return False
@Memoize
def should_skip(m, n):
	if is_wildcard(m):
		return True
	if is_wildcard(n):
		return True
	return False
'''
	Detalied explanation of generating the maps to encrypt / decrypt runes
'''
def build_arithmetic_lookup_tables():
	'''
		_enc_data are lusts showing how each plaintext-rune (r1) and a key-rune (r2) combine to
		give a cipher text rune. These lists are used to generate encryption / decryption maps
	'''
	plus_enc_data     = []
	multiply_enc_data = []
	minus_enc_data    = []
	divide_enc_data   = []
	print 'making encryption data'
	for r1 in range(0,29):
		for r2 in range(0, 29):
			multiply_enc_data.append( [r1, r2 , multiply_m29(r1,r2)])
			divide_enc_data.append(   [r1, r2 , divide_mod29(r1,r2)])
			minus_enc_data.append(    [r1, r2 , minus_m29(   r1,r2)])
			plus_enc_data.append(     [r1, r2 , plus_m29(    r1,r2)])
	'''
		First we use these lists to to create lists of decryption data. re-arrange the order 
		of the data to give lists of plaintext rune and cipher rune  
		as minus and divide are not associative there are two lists for those operations, 
		one for each combination of 
			message - rune and cipher - rune 
			message / rune and cipher / rune
	'''
	print 'making decryption data'
	plus_dec_data     = [ [x[0],x[2],x[1]] for x in plus_enc_data    ]
	multiply_dec_data = [ [x[0],x[2],x[1]] for x in multiply_enc_data]
	minus_1_dec_data  = [ [x[0],x[2],x[1]] for x in minus_enc_data   ]
	minus_2_dec_data  = [ [x[1],x[2],x[0]] for x in minus_enc_data   ]
	divide_1_dec_data = [ [x[0],x[2],x[1]] for x in divide_enc_data  ]
	divide_2_dec_data = [ [x[1],x[2],x[0]] for x in divide_enc_data  ]
	'''
		now build the encryption dictionaries from the above data
	'''
	print 'making encryption maps'
	plus_enc     = {}
	multiply_enc = {}
	minus_enc    = {}
	divide_enc   = {}
	for i in plus_enc_data:
		key = to_dict_key(i[0],i[1])
		plus_enc[key] = i[2]

	for i in multiply_enc_data:
		key = to_dict_key(i[0],i[1])
		multiply_enc[key] = i[2]

	for i in minus_enc_data:
		key = to_dict_key(i[0],i[1])
		minus_enc[key] = i[2]

	for i in divide_enc_data:
		key = to_dict_key(i[0],i[1])
		divide_enc[key] = i[2]
	'''
		Same for decrypting
	'''
	print 'making decryption maps'
	plus_dec     = {}
	multiply_dec = {}
	minus_1_dec  = {}
	minus_2_dec  = {}
	divide_1_dec = {}
	divide_2_dec = {}
	for i in plus_dec_data:
		key = to_dict_key(i[0],i[1])
		plus_dec[key] = i[2]
	for i in minus_1_dec_data:
		key = to_dict_key(i[0],i[1])
		minus_1_dec[key] = i[2]
	for i in minus_2_dec_data:
		key = to_dict_key(i[0],i[1])
		minus_2_dec[key] = i[2]
	'''
		For multiply and divide there are combinations (involving zero) where any key rune 
		applied to the plaintext-rune gives the same cipher rune (and vice-versa)
		we use a wildcard character for these
	'''
	wc = '*'
	for i in multiply_dec_data:
		key = to_dict_key(i[0],i[1])
		if (i[0] == 0):
			multiply_dec[key] = wc
		else:
			multiply_dec[key] = i[2]
	for i in divide_1_dec_data:
		key = to_dict_key(i[0],i[1])
		if (i[0] == 0):
			divide_1_dec[key] = wc
		else:
			divide_1_dec[key] = i[2]
	for i in divide_2_dec_data:
		key = to_dict_key(i[0],i[1])
		if (i[0] == 0):
			divide_2_dec[key] = wc
		else:
			divide_2_dec[key] = i[2]
	print 'saving maps'
	encode_maps = [plus_enc, minus_enc, multiply_enc, divide_enc]
	decode_maps = [plus_dec, minus_1_dec, minus_2_dec, multiply_dec, divide_1_dec,divide_2_dec]
	script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
	encode_file = os.path.join(script_dir, "data/arithmetic_encode.pkl")
	with open(encode_file , 'wb') as f:
		pickle.dump(encode_maps, f)
	decode_file = os.path.join(script_dir, "data/arithmetic_decode.pkl")
	with open(decode_file , 'wb') as f:
		pickle.dump(decode_maps, f)

def import_arithmetic_lookup_tables():
	'''
		load in pre-computed tables of the above
	'''
	print 'loading maps'
	script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
	encode_file = os.path.join(script_dir, "data/arithmetic_encode.pkl")
	with open(encode_file, 'rb') as f:
		encode_maps = pickle.load(f)
	decode_file = os.path.join(script_dir, "data/arithmetic_decode.pkl")
	with open(decode_file, 'rb') as f:
		decode_maps = pickle.load(f)
	return [encode_maps, decode_maps]

##
## Iterative functions,
##
'''
    for recursive (iterative) schemes we add an extra rune,
    cipher[i] = encrypt(plaintext[i], key[i]) + cipher[i-1]
    where encrypt is 'any' function of two runes
'''
@Memoize
def itplus_m29(rune1, rune2, rune3):
	return mod29(rune1 + rune2 + rune3)
@Memoize
def itminus_m29(rune1, rune2,rune3):
	return mod29(rune1 - rune2 + rune3)
@Memoize
def itmultiply_m29(rune1, rune2,rune3):
	return mod29(rune1 * rune2 + rune3)
@Memoize
def itdivide_m29(rune1, rune2, rune3):
	''' for a prime modulus p
		y = pow(x, p-2, p)
	'''
	return mod29(rune1 * pow(rune2, 27, 29) + rune3)
'''
	Detalied explanation of generating the maps to encrypt / decrypt runes
'''
def build_iterative_arithmetic_lookup_tables():
	'''
		encryption data, all possible combinations
	'''
	itplus_enc_data     = []
	itmultiply_enc_data = []
	itminus_enc_data    = []
	itdivide_enc_data   = []
	print 'making iterative encryption data'
	for r1 in range(0,29):
		for r2 in range(0, 29):
			for r3 in range(0, 29):
				itmultiply_enc_data.append( [r1, r2 , r3, itmultiply_m29(r1,r2,r3)])
				itdivide_enc_data.append(   [r1, r2 , r3, itdivide_m29(  r1,r2,r3)])
				itminus_enc_data.append(    [r1, r2 , r3, itminus_m29(   r1,r2,r3)])
				itplus_enc_data.append(     [r1, r2 , r3, itplus_m29(    r1,r2,r3)])

	'''
	We can use these lists  to create a map of message-rune,it-rune,cipher-rune to key
	'''
	'''
	shows how a plaintext rune and a key rune give each cipher text rune 
	as minus and divide are not associative there are two maps, 
	one for each combination of message-rune,it-rune, and cipher-rune 
	'''
	print 'generating iterative decryption data'
	itplus_dec_data     = [ [x[0],x[2],x[3],x[1]] for x in itplus_enc_data    ]
	itmultiply_dec_data = [ [x[0],x[2],x[3],x[1]] for x in itmultiply_enc_data]
	itminus_1_dec_data  = [ [x[0],x[2],x[3],x[1]] for x in itminus_enc_data   ]
	itdivide_2_dec_data = [ [x[1],x[2],x[3],x[0]] for x in itdivide_enc_data  ]
	itminus_2_dec_data  = [ [x[1],x[2],x[3],x[0]] for x in itminus_enc_data   ]
	itdivide_1_dec_data = [ [x[0],x[2],x[3],x[1]] for x in itdivide_enc_data  ]
	'''
	Encryption maps (dictionary)
	we can now create a decryption dictiionary,
	in Python dictionaries can't have lists as 
	keys so we convert the first two runes in each list to a string  using to_dict_key
	'''
	itplus_enc     = {}
	itmultiply_enc = {}
	itminus_enc    = {}
	itdivide_enc   = {}
	print 'making iterative encryption maps'
	for i in itplus_enc_data:
		key = to_dict_key(i[0],i[1],i[2])
		itplus_enc[key] = i[3]
	for i in itmultiply_enc_data:
		key = to_dict_key(i[0],i[1],i[2])
		itmultiply_enc[key] = i[3]
	for i in itminus_enc_data:
		key = to_dict_key(i[0],i[1],i[2])
		itminus_enc[key] = i[3]
	for i in itdivide_enc_data:
		key = to_dict_key(i[0],i[1],i[2])
		itdivide_enc[key] = i[3]
	'''
	Same for decrypting
	'''
	print 'making iterative ecryption maps'
	itplus_dec     = {}
	itmultiply_dec = {}
	itminus_1_dec    = {}
	itminus_2_dec    = {}
	itdivide_1_dec  = {}
	itdivide_2_dec  = {}
	for i in itplus_dec_data:
		key = to_dict_key(i[0],i[1],i[2])
		itplus_dec[key] = i[3]
	for i in itminus_1_dec_data:
		key = to_dict_key(i[0],i[1],i[2])
		itminus_1_dec[key] = i[3]
	for i in itminus_2_dec_data:
		key = to_dict_key(i[0],i[1],i[2])
		itminus_2_dec[key] = i[3]
	'''
		For multiply and divide there are combinations (involving zero) where any key rune 
		applied to the plaintext-rune and iterative rune gives the same cipher rune (and vice-versa)
		we use a wildcard character for these
	'''
	wc = '*'
	for i in itmultiply_dec_data:
		key = to_dict_key(i[0],i[1],i[2])
		if (i[0] == 0):
			itmultiply_dec[key] = wc
		else:
			itmultiply_dec[key] = i[3]
	for i in itdivide_1_dec_data:
		key = to_dict_key(i[0],i[1],i[2])
		if (i[0] == 0):
			itdivide_1_dec[key] = wc
		else:
			itdivide_1_dec[key] = i[3]
	for i in itdivide_2_dec_data:
		key = to_dict_key(i[0],i[1],i[2])
		if (i[0] == 0):
			itdivide_2_dec[key] = wc
		else:
			itdivide_2_dec[key] = i[3]
	print 'saving maps'
	encode_maps = [itplus_enc, itminus_enc, itmultiply_enc, itdivide_enc]
	decode_maps = [itplus_dec, itminus_1_dec, itminus_2_dec, itmultiply_dec, itdivide_1_dec,itdivide_2_dec]
	script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
	encode_file = os.path.join(script_dir, "data/iterative_arithmetic_encode.pkl")
	with open(encode_file , 'wb') as f:
		pickle.dump(encode_maps, f)
	decode_file = os.path.join(script_dir, "data/iterative_arithmetic_decode.pkl")
	with open(decode_file , 'wb') as f:
		pickle.dump(decode_maps, f)

def import_iterative_arithmetic_lookup_tables():
	'''
		load in pre-computed tables of the above
	'''
	print 'loading maps'
	script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
	encode_file = os.path.join(script_dir, "data/iterative_arithmetic_encode.pkl")
	with open(encode_file, 'rb') as f:
		encode_maps = pickle.load(f)
	decode_file = os.path.join(script_dir, "data/iterative_arithmetic_decode.pkl")
	with open(decode_file, 'rb') as f:
		decode_maps = pickle.load(f)
	return [encode_maps, decode_maps]
'''
from these maps we can build a class that has functions functions to encrypt/decrypt using the 
pre-computed  dictionries instead of calculating the answers
'''