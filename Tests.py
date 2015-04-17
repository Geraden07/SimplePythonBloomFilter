#!/usr/bin/python
import unittest
from SimplePythonBloomFilter import BloomFilter

class TestBloomFilter(unittest.TestCase):
	def test_calculate_space( self ):
		"""Test math against known values verified by Wolfram Alpha"""
		space = BloomFilter.calculate_space( 1000, 0.05 )
		self.assertTrue( space == 6236 )
		
		space = BloomFilter.calculate_space( 1000, 0.005 )
		self.assertTrue( space == 11028 )

		space = BloomFilter.calculate_space( 1000, 0.001 )
		self.assertTrue( space == 14378 )

		space = BloomFilter.calculate_space( 2000, 0.05 )
		self.assertTrue( space == 12471 )

		space = BloomFilter.calculate_space( 2000, 0.005 )
		self.assertTrue( space == 22056 )

		space = BloomFilter.calculate_space( 2000, 0.001 )
		self.assertTrue( space == 28756 )

		space = BloomFilter.calculate_space( 3000, 0.05 )
		self.assertTrue( space == 18706 )

		space = BloomFilter.calculate_space( 3000, 0.005 )
		self.assertTrue( space == 33084 )
		
		space = BloomFilter.calculate_space( 3000, 0.001 )
		self.assertTrue( space == 43133 )

	def test_calculate_hash_count( self ):
		"""Test math against known values verified by Wolfram Alpha."""
		hash_count = BloomFilter.calculate_hash_count( 1000, 10000 )
		self.assertTrue( hash_count == 7 )
		
		hash_count = BloomFilter.calculate_hash_count( 1000, 20000 )
		self.assertTrue( hash_count == 14 )
		
		hash_count = BloomFilter.calculate_hash_count( 1000, 30000 )
		self.assertTrue( hash_count == 21 )
		
		hash_count = BloomFilter.calculate_hash_count( 2000, 10000 )
		self.assertTrue( hash_count == 3 )
		
		hash_count = BloomFilter.calculate_hash_count( 2000, 20000 )
		self.assertTrue( hash_count == 7 )
		
		hash_count = BloomFilter.calculate_hash_count( 2000, 30000 )
		self.assertTrue( hash_count == 10 )
		
		hash_count = BloomFilter.calculate_hash_count( 3000, 10000 )
		self.assertTrue( hash_count == 2 )
		
		hash_count = BloomFilter.calculate_hash_count( 3000, 20000 )
		self.assertTrue( hash_count == 5 )
		
		hash_count = BloomFilter.calculate_hash_count( 3000, 30000 )
		self.assertTrue( hash_count == 7 )

	def test_default_hashfn( self ):
		"""Test that hashfn returned is callable, that it can take two
		arguments, and that the response can be passed to the function
		long() without raising errors."""
		hashfn = BloomFilter.default_hashfn()
		self.assertTrue( callable( hashfn ) )
		self.assertTrue( long( hashfn( "test", 0) ) )

	
if __name__ == '__main__':
	unittest.main()
