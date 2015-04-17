#!/usr/bin/python
# Author: Steven B.
# 2015-04-16
# Released under license GPLv3
# https://www.gnu.org/licenses/gpl-3.0.html

# Built-in python modules
from __future__ import division
from math import ceil
from math import log
from math import e
from hashlib import md5

# 3rd party modules
from bitarray import bitarray # https://pypi.python.org/pypi/bitarray/

class BloomFilter( object ):
	"""
		This is a simple implementation of a Bloom filter designed specifically to be able
		to swap in any hash function that follows a given signature (see comments below).

		The design goals of this class are to be highly performant, independant of any given
		hash function, and as light weight and with as few dependencies as possible.

		All rates and probability representations are as a ratio of 1. IE: 0.001 represents
		a rate of one in one thousand

		The default of this implementation uses the md5 hash function provided by the built-in
		hashlib python module in order to avoid more dependencies on 3rd party modules. It is VERY
		HIGHLY RECOMMENDED to instead use a hash function provided by a module like PyHash such 
		as Murmur3 or City. Cryptographic hashes such as those provided by PyCrypto are generally
		undesireable as they are not designed for speed in the same way as non-cryptographic
		hash functions are.

		To learn about the basic principles of a Bloom filter, watch this talk from PyCon 2015
		https://www.youtube.com/watch?v=IGwNQfjLTp0&t=5m45s
	"""

	# Instance members
	# __element_count	# Keeps track of number of elements that have been added to the bitarray
	# __bitarray_size	# The total number of bits in the bitarray
	# __bitarray			# The actual bitarray object
	# __hash_count		# The number of times a given element is hashed and entered into the bitarray
	# __hashfn			# The function that has signature hashfn(element, seed) and returns a long

	def __init__( self, capacity, error_rate = 0.001, hashfn = None ):
		# Constructor
		self.__element_count = 0
		self.__bitarray_size = BloomFilter.calculate_space( capacity, error_rate )
		self.__bitarray = bitarray( self.__bitarray_size )
		self.__bitarray.setall(False)
		self.__hash_count = BloomFilter.calculate_hash_count( capacity, self.__bitarray_size )
		if hashfn == None:
			self.__hashfn = BloomFilter.default_hashfn()
		else:
			self.__hashfn = hashfn

	def __contains__( self, element ):
		# Method to be able to use Python's "in" operator
		for x in range(self.__hash_count):
			index = self.__hashfn( str( element ), str( x ) ) % self.__bitarray_size
			if self.__bitarray[index] == False:
				return False
		return True

	def add( self, element ):
		"""Adds a string element to the filter."""
		for x in range(self.__hash_count):
			index = self.__hashfn( str( element ), str( x ) ) % self.__bitarray_size
			self.__bitarray[index] = True
		self.__element_count += 1

	def fp_rate( self ):
		"""Returns the probability as a ratio of 1 of a false positive being returned."""
		m = self.__bitarray_size
		k = self.__hash_count
		n = self.__element_count
		return pow( 1 - pow( e,  ( -k * n / m ) ), k )

	def count( self ):
		"""Returns the count of elements that have been added to the filter."""
		return self.__element_count

	@staticmethod
	def calculate_space( capacity, error_rate ):
		"""A static method that calculates the size of the bit array needed for a filter with given
		capacity and error rate."""
		return int( ceil( ( capacity * log( error_rate ) / log( 1 / pow( 2, log( 2 ) ) ) ) ) )

	@staticmethod
	def calculate_hash_count( capacity, space ):
		"""A static method that calculates the number of different hash values to store in the
		filter for a new element."""
		return int( round( log( 2 ) * space / capacity ) )

	@staticmethod
	def default_hashfn():
		"""Creates and returns a reference to a hashfn that meets the necessary signature and is
		based on the haslib.md5() hash function. It is HIGHLY desireable to provide a different
		hash function such as one based on Murmur3 or City. See the 3rd party module PyHash.
		Any hash function supplied in place of this must return a value of type long."""
		def hashfn( element, seed ):
			m = md5()
			m.update( str( element ) + str( seed ) )
			return long( ''.join( format( ord( x ), 'b' ) for x in m.digest() ), 2 )
		return hashfn
