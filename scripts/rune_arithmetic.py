#!/usr/bin/env python
# basic rune arithmetic functions, mod 29
# written out so that each step can be followed for each method
import os
import gematria
import time
from  build_maps import *


'''
from the maps in build_maps.py we can build a class that has functions to encrypt/decrypt 
using the pre-computed maps instead of calculating the answers
'''
class rune_arithmetic(object):
	def __init__(self,build = None):
		self.g = gematria.gematria()
		self.k_e = 'e'
		self.wc  = '*'

		if build:
			print 'building'
			build_arithmetic_lookup_tables()
			build_iterative_arithmetic_lookup_tables()

		print 'loading'

		[[self.plus_e, self.minus_e,  self.multiply_e,self.divide_e],
		 [self.plus_d, self.minus_1_d,self.minus_2_d, self.multiply_d, self.divide_1_d,
		  self.divide_2_d]] =import_arithmetic_lookup_tables()

		[[self.itplus_e, self.itminus_e,  self.itmultiply_e,self.itdivide_e],
		 [self.itplus_d, self.itminus_1_d,self.itminus_2_d, self.itmultiply_d, self.itdivide_1_d,
		  self.itdivide_2_d]] =import_iterative_arithmetic_lookup_tables()

		self.encrypt_type = ['plus_encrypt',    'minus_1_encrypt', 'minus_2_encrypt',
							 'multiply_encrypt','divide_1_encrypt','divide_2_encrypt']
		self.decrypt_type = ['plus_decrypt',    'minus_1_decrypt', 'minus_2_decrypt',
							 'multiply_decrypt','divide_1_decrypt','divide_2_decrypt']
		self.decrypt_type_pm = ['plus_decrypt',    'minus_1_decrypt', 'minus_2_decrypt']
		self.decrypt_type_md = ['multiply_decrypt','divide_1_decrypt','divide_2_decrypt']


		self.itencrypt_type = ['itplus_encrypt',    'itminus_1_encrypt', 'itminus_2_encrypt',
							 'itmultiply_encrypt','itdivide_1_encrypt','itdivide_2_encrypt']
		self.itdecrypt_type = ['itplus_decrypt',    'itminus_1_decrypt', 'itminus_2_decrypt',
							 'itmultiply_decrypt','itdivide_1_decrypt','itdivide_2_decrypt']

		self.itdecrypt_type_pm = ['itplus_decrypt',    'itminus_1_decrypt', 'itminus_2_decrypt']
		self.itdecrypt_type_md = ['itmultiply_decrypt','itdivide_1_decrypt','itdivide_2_decrypt']


		self.encrypt_func = [self.plus_encrypt,    self.minus_1_encrypt, self.minus_2_encrypt,
							 self.multiply_encrypt,self.divide_1_encrypt,self.divide_2_encrypt]

		self.decrypt_func_pm = [self.plus_decrypt,    self.minus_1_decrypt, self.minus_2_decrypt]
		self.decrypt_func_md = [self.multiply_decrypt,self.divide_1_decrypt,self.divide_2_decrypt]

		self.itencrypt_func = [self.itplus_encrypt,    self.itminus_1_encrypt, self.itminus_2_encrypt,
							 self.itmultiply_encrypt,self.itdivide_1_encrypt,self.itdivide_2_encrypt]
		self.itdecrypt_func_pm = [self.itplus_decrypt, self.itminus_1_decrypt,
								  self.itminus_2_decrypt]
		self.itdecrypt_func_md = [self.itmultiply_decrypt,self.itdivide_1_decrypt,
								  self.itdivide_2_decrypt]

		self.encrypt_func = [self.plus_encrypt,    self.minus_1_encrypt, self.minus_2_encrypt,
							 self.multiply_encrypt,self.divide_1_encrypt,self.divide_2_encrypt]
		self.decrypt_func = [self.plus_decrypt,    self.minus_1_decrypt, self.minus_2_decrypt,
							 self.multiply_decrypt,self.divide_1_decrypt,self.divide_2_decrypt]

		self.itencrypt_func = [self.itplus_encrypt,    self.itminus_1_encrypt, self.itminus_2_encrypt,
							 self.itmultiply_encrypt,self.itdivide_1_encrypt,self.itdivide_2_encrypt]
		self.itdecrypt_func = [self.itplus_decrypt,    self.itminus_1_decrypt, self.itminus_2_decrypt,
							 self.itmultiply_decrypt,self.itdivide_1_decrypt,self.itdivide_2_decrypt]


	def plus_encrypt(self,message_rune,key_rune):
		return self.plus_e.get(to_dict_key(message_rune, key_rune),self.k_e)
	def minus_1_encrypt(self,message_rune,key_rune):
		return self.minus_e.get(to_dict_key(message_rune, key_rune),self.k_e)
	def minus_2_encrypt(self,message_rune,key_rune):
		return self.minus_e.get(to_dict_key(key_rune,message_rune),self.k_e)
	def multiply_encrypt(self,message_rune,key_rune):
		return self.multiply_e.get(to_dict_key(message_rune, key_rune),self.k_e)
	def divide_1_encrypt(self,message_rune,key_rune):
		return self.divide_e.get(to_dict_key(message_rune, key_rune),self.k_e)
	def divide_2_encrypt(self,message_rune,key_rune):
		return self.divide_e.get(to_dict_key(key_rune,message_rune),self.k_e)
	def plus_decrypt(self,message_rune,key_rune):
		return self.plus_d.get(to_dict_key(message_rune, key_rune),self.k_e)
	def minus_1_decrypt(self,message_rune,key_rune):
		return self.minus_1_d.get(to_dict_key(message_rune, key_rune),self.k_e)
	def minus_2_decrypt(self,message_rune,key_rune):
		return self.minus_2_d.get(to_dict_key(key_rune,message_rune),self.k_e)
	def multiply_decrypt(self,message_rune,key_rune):
		return self.multiply_d.get(to_dict_key(message_rune, key_rune),self.k_e)
	def divide_1_decrypt(self,message_rune,key_rune):
		return self.divide_1_d.get(to_dict_key(message_rune, key_rune),self.k_e)
	def divide_2_decrypt(self,message_rune,key_rune):
		return self.divide_2_d.get(to_dict_key(key_rune,message_rune),self.k_e)

	'''
	Functions to enocde
	'''
	def itplus_encrypt(self, message_rune, key_rune, it_rune):
		return self.itplus_e.get(to_dict_key(message_rune, key_rune, it_rune),self.k_e)
	def itminus_1_encrypt(self, message_rune, key_rune, it_rune):
		return self.itminus_e.get(to_dict_key(message_rune, key_rune, it_rune),self.k_e)
	def itminus_2_encrypt(self, message_rune, key_rune, it_rune):
		return self.itminus_e.get(to_dict_key(key_rune, message_rune, it_rune),self.k_e)
	def itmultiply_encrypt(self, message_rune, key_rune, it_rune):
		return self.itmultiply_e.get(to_dict_key(message_rune, key_rune, it_rune),self.k_e)
	def itdivide_1_encrypt(self, message_rune, key_rune, it_rune):
		return self.itdivide_e.get(to_dict_key(message_rune, key_rune, it_rune),self.k_e)
	def itdivide_2_encrypt(self, message_rune, key_rune, it_rune):
		return self.itdivide_e.get(to_dict_key(key_rune, message_rune, it_rune),self.k_e)
	'''
	Functions to decrypt
	'''
	def itplus_decrypt(self, message_rune, it_rune, cipher_rune):
		return self.itplus_d.get(to_dict_key(message_rune, it_rune, cipher_rune),self.k_e)
	def itminus_1_decrypt(self, message_rune, it_rune, cipher_rune):
		return self.itminus_1_d.get(to_dict_key(message_rune, it_rune, cipher_rune),self.k_e)
	def itminus_2_decrypt(self, message_rune, it_rune, cipher_rune):
		return self.itminus_2_d.get(to_dict_key(message_rune, it_rune, cipher_rune),self.k_e)
	def itmultiply_decrypt(self, message_rune, it_rune, cipher_rune):
		return self.itmultiply_d.get(to_dict_key(message_rune, it_rune, cipher_rune),self.k_e)
	def itdivide_1_decrypt(self, message_rune, it_rune, cipher_rune):
		return self.itdivide_1_d.get(to_dict_key(message_rune, it_rune, cipher_rune),self.k_e)
	def itdivide_2_decrypt(self, message_rune, it_rune, cipher_rune):
		return self.itdivide_2_d.get(to_dict_key(message_rune, it_rune, cipher_rune),self.k_e)

	def encrypt_f(self, plaintext, key, method):
		cipher_text = []
		for p, k in zip(plaintext, key):
			cipher_text.append(method(p, k))
		return cipher_text

	def encrypt(self, plaintext, key):
		ans = []
		for method in self.encrypt_func:
			ans.append( self.encrypt_f(plaintext, key, method) )
		return ans

	def decrypt(self, plaintext, ciphertext):
		ans = []
		for method in self.decrypt_func:
			key = []
			for p, c in zip(plaintext, ciphertext):
				key.append( method(p, c))
			ans.append(key )
		return ans

	def decrypt_pm(self, plaintext, ciphertext):
		ans = []
		for method in self.decrypt_func_pm:
			key = []
			for p, c in zip(plaintext, ciphertext):
				key.append( method(p, c))
			ans.append(key )
		return ans

	def decrypt_md(self, plaintext, ciphertext):
		ans = []
		for method in self.decrypt_func_md:
			key = []
			for p, c in zip(plaintext, ciphertext):
				key.append( method(p, c))
			ans.append(key )
		return ans

	def it_enc(self, message, key, off0, f):
		r = []
		i = 0
		while i < len(message):
			if i == 0:
				if key[0] == 'e':
					r.append(off0)
				else:
					r.append(f(message[0], key[0], off0))
			else:
				if key[i] == 'e':
					r.append(r[-1])
				else:
					r.append(f(message[i], key[i], r[-1]))
			i += 1
		return r

	def it_dec(self, message, cipher, off0, f):
		r = []
		i = 0
		while i < len(message):
			if i == 0:
				r.append(f(message[0], off0, cipher[0]))
			else:
				r.append(f(message[i], cipher[i - 1], cipher[i]))
			i += 1
		return r

	def itencrypt(self, message, key, off0):
		ans = []
		for method in self.itencrypt_func:
			ans.append(self.it_enc(message, key, off0, method))
		return ans

	def itdecrypt(self, message, ciphertext, off0):
		ans = []
		for method in self.itdecrypt_func:
			ans.append(self.it_dec(message, ciphertext, off0, method))
		return ans

	def itdecrypt_pm(self, message, ciphertext, off0):
		ans = []
		for method in self.itdecrypt_func_pm:
			ans.append(self.it_dec(message, ciphertext, off0, method))
		return ans

	def itdecrypt_md(self, message, ciphertext, off0):
		ans = []
		for method in self.itdecrypt_func_md:
			ans.append(self.it_dec(message, ciphertext, off0, method))
		return ans

	def list_match(self, m, n):
		'''
			test if two lists are the same, given wildcards * and e
		'''
		for m1, n1 in zip(m,n):
			if should_skip(m1,n1):
				pass
			elif m1 != n1:
				return False
		return True

	def write(self, key, pre_string ,file):
		'''
			write key and string to file, also shift key so first rune is 0
			to help with looking for sequences
		:param key:
		:param pre_string:
		:param file:
		:return:
		'''
		k_str = ' '.join([str(c) for c in key])
		k = []
		if isinstance(key[0], int):
			for v in key:
				if isinstance(v, str):
					k.append(v)
				elif isinstance(v, int):
					k.append(mod29(v - key[0]))
		else:
			k = key
		k_0 = ' '.join([str(c) for c in k])
		a = pre_string + ',\t ' + k_str + ',\t ' + k_0
		#print a
		file.write(a)
		file.write('\n')

	def get_pm_keys_for_crib(self,crib_with_count, ct, file_pm, itfile_pm):
		'''
			plus minus functions are quick as they are 'shift-independant'

		:param crib_with_count:
		:param ct:
		:param file_pm:
		:param itfile_pm:
		:return:
		'''
		# ct as string to write to file
		ct_s = ' '.join([str(c) for c in ct])
		# expect dat to be n-gram crib with count and dictionary type (M)
		crib = crib_with_count.split( )[0:-2]
		crib =  ' '.join(crib)
		# crib in gematria position
		m_f = [y for x in self.g.phrase_to_pos_f(crib) for y in x][0:len(ct)]
		m_r = [y for x in self.g.phrase_to_pos_r(crib) for y in x][0:len(ct)]
		# crib gem. position as string to write to file
		m_f_s = ' '.join([str(c) for c in m_f])
		m_r_s = ' '.join([str(c) for c in m_r])
		# part fo string to write to file
		sf = crib_with_count + ", m_f = " + m_f_s + ", ct = " + ct_s + ", "
		sr = crib_with_count + ", m_r = " + m_r_s + ", ct = " + ct_s + ", "

		# plus and minus methods require only 1 gematria shift
		keys_f = self.decrypt_pm(m_f, ct)
		keys_r = self.decrypt_pm(m_r, ct)
		itkeys_f = self.itdecrypt_pm(m_f, ct, 0)
		itkeys_r = self.itdecrypt_pm(m_r, ct, 0)

		for i, key in enumerate(keys_f):
			self.write(key, sf + self.decrypt_type_pm[i], file_pm)
		for i, key in enumerate(keys_r):
			self.write(key, sr + self.decrypt_type_pm[i], file_pm)
		for i, key in enumerate(itkeys_f):
			self.write(key, sf + self.itdecrypt_type_pm[i], itfile_pm)
		for i, key in enumerate(itkeys_r):
			self.write(key, sf + self.itdecrypt_type_pm[i], itfile_pm)

	def get_md_keys_for_crib(self,crib_with_count, ct, file_md, itfile_md):
		'''
			multiply and divide (md) give different answers depending on the shift, so apply all
			shifts. There are probably more ways that the text can be shifted

		:param crib_with_count:
		:param ct:
		:param file_md:
		:param itfile_md:
		:return:
		'''
		# ct as string to write to file
		ct_s = ' '.join([str(c) for c in ct])
		# expect dat to be n-gram crib with count and dictionary type (M)
		crib = crib_with_count.split( )[0:-2]
		crib =  ' '.join(crib)

		# for multiply /divide the shift effects the key in a non-trivial way
		for shift in range(0, 29):
			# crib in gematria position
			m_f = mod29L([y + shift for x in self.g.phrase_to_pos_f(crib) for y in x][0:len(ct)])
			m_r = mod29L([y + shift for x in self.g.phrase_to_pos_r(crib) for y in x][0:len(ct)])

			keys_f = self.decrypt_md(m_f, ct)
			keys_r = self.decrypt_md(m_r, ct)
			itkeys_f = self.itdecrypt_md(m_f, ct, 0)
			itkeys_r = self.itdecrypt_md(m_r, ct, 0)

			m_f_s = ' '.join([str(c) for c in m_f])
			m_r_s = ' '.join([str(c) for c in m_r])
			shift_s = str(shift)

			sf=crib_with_count+", Shift " + shift_s + ", m_f = " + m_f_s +  ", ct = " + ct_s+", "
			sr=crib_with_count+", Shift " + shift_s + ", m_r = " + m_r_s + ", ct = "+ ct_s+ ", "

			for i, key in enumerate(keys_f):
				self.write(key, sf + self.decrypt_type_md[i], file_md)
			for i, key in enumerate(keys_r):
				self.write(key, sr + self.decrypt_type_md[i], file_md)
			for i, key in enumerate(itkeys_f):
				self.write(key, sf + self.itdecrypt_type_md[i], itfile_md)
			for i, key in enumerate(itkeys_r):
				self.write(key, sr + self.itdecrypt_type_md[i], itfile_md)

	def get_pm_keys(self, ct_f, ct_r, file_suffix, crib_file):
		'''
			get keys for plus minus functions
		:param ct_f:
		:param ct_r:
		:param file_suffix:
		:param crib_file:
		:return:
		'''
		print file_suffix
		# get cribs
		cribs = []
		with open(crib_file, 'r') as f:
			for line in f:
				cribs.append(line)
		# file names to export data
		file_f_pm   = 'ctf_pm' + file_suffix
		file_r_pm   = 'ctr_pm' + file_suffix
		itfile_f_pm = 'ctr_itpm' + file_suffix
		itfile_r_pm = 'ctf_itpm' + file_suffix

		self.del_f(file_f_pm  )
		self.del_f(file_r_pm  )
		self.del_f(itfile_f_pm)
		self.del_f(itfile_r_pm)
		# iterate over each crib for the cipher-text decoded with forward gematria
		with open(file_f_pm, 'a') as f_pm:
			with open(itfile_f_pm, 'a') as itf_pm:
				for crib in cribs:
					self.get_pm_keys_for_crib(crib.rstrip(), ct_f,  file_pm = f_pm, itfile_pm =
					itf_pm)
		# iterate over each crib for the cipher-text decoded with reverse gematria
		with open(file_r_pm, 'a') as r_pm:
			with open(itfile_r_pm, 'a') as itr_pm:
				for crib in cribs:
					self.get_pm_keys_for_crib(crib.rstrip(), ct_r,  file_pm = r_pm, itfile_pm =
					itr_pm)

	def get_md_keys(self, ct_f, ct_r, file_suffix, crib_file):
		'''
					get keys for multiply divide functions, this takes awhile, so print some timings
		:param ct_f:
		:param ct_r:
		:param file_suffix:
		:param crib_file:
		:return:
		'''
		start = time.time()
		print file_suffix
		print 'Getting cribs'
		cribs = []
		with open(crib_file, 'r') as f:
			for line in f:
				cribs.append(line)

		# file names
		file_f_md   = 'ctf_md' + file_suffix
		file_r_md   = 'ctr_md' + file_suffix
		itfile_f_md = 'ctf_itmd' + file_suffix
		itfile_r_md = 'ctr_itmd' + file_suffix

		self.del_f(file_f_md  )
		self.del_f(file_r_md  )
		self.del_f(itfile_f_md)
		self.del_f(itfile_r_md)

		now1 = time.time()
		print('Time  = ', now1 - start)
		print
		print 'Getting get_keys_for_crib ct_f '
		# iterate over each crib for the cipher-text decoded with forward gematria
		with open(file_f_md, 'a') as f_md:
			with open(itfile_f_md, 'a') as itf_md:
				for crib in cribs:
					self.get_md_keys_for_crib(crib.rstrip(), ct_f,file_md = f_md, itfile_md = itf_md)
		now2 = time.time()
		print('Time  = ', now2 - now1)
		print
		print 'Getting get_keys_for_crib ct_r '
		# iterate over each crib for the cipher-text decoded with reverse gematria
		with open(file_r_md, 'a') as r_md:
			with open(itfile_r_md, 'a') as itr_md:
				for crib in cribs:
					self.get_md_keys_for_crib(crib.rstrip(), ct_r, file_md = r_md, itfile_md = itr_md)
		now3 = time.time()
		print('Total Time  = ', now3 - now2)
		print
		print('FIN Total Time  = ',time.time() - start)

	def del_f(self,f):
		'''
			delete a file
		:param f:
		:return:
		'''
		try:
			os.remove(f)
		except OSError:
			pass
