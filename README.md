# SimplePythonBloomFilter v0.0.1
This is a simple implementation of a Bloom filter using Python.

## Basics About the Data Structure and Theory
A Bloom filter is a data structure that can test whether an element is LIKELY in a predefined set of elements, or DEFINITELY not. False positives (ie: being told an element IS in the set when it is not) are always a possibility but the probability of them occuring can be controlled by tuning the construction parameters of the Bloom array.

For a further explaination of the basics of Bloom filters, Curtis Lassam gave a talk at PyCon 2015 that does a very good job explaining. The talk is available on YouTube here:

https://www.youtube.com/watch?v=IGwNQfjLTp0&t=5m45s

##Basic Usage
A straight-forward example:
```python
from SimplePythonBloomFilter import BloomFilter

bfilter = BloomFilter(1000, 0.001)

bfilter.add("string element")

# The following will evaluate to true
"string element" in bfilter

# The following will LIKELY be false
"another string" in bfilter
```

The above filter is initiated with the values 1000 and 0.001. This means that the object returned is a Bloom filter that will have a probability of one in one thousand (0.001) of returning a false positive when there are 1000 elements in the filter. As the number of elements increases, the probability of false positives will increase. As the filter starts to fill up, the probability of false positives will grow exponentially until it reaches 1 (always) for a full filter.

Resizing and removing from the filter are not possible.

##Use Benefits and Scalability
Why might we want to use a Bloom filter instead of just always searching our data directly?
Well sometimes searching other data structures can be very poor performance:
- Hashtables, for example, are very good for inserting, retrieving, deleting, etc. in constant time. Searching through all possible values is comparitively expensive in terms of processing time.
- Linked Lists are another good example. The worst case scenario for a search is if the item we are looking for doesn't exist in our list. We must search all the way through until the end of the Linked List in order to determine this.
- Data that has a high ratio of misses to hits.
- Network resources are often very expensive, in terms of response time, for retrieving information.

In all the above cases, it can be a big performance benefit if we can have a data structure that can return in constant time whether a desired element is even present before we make our search call. We won't mind having a small probability of false positives inherient to Bloom filters because then we just end up searching for something that isn't there and returning nothing anyway. By controlling that probability of false positives and keeping it very low, we can ensure nearly all of our search calls that would result in misses are never done.

We are not, however, able to STORE any data in the Bloom filter. The filter only keeps track of IF something has likely been seen before or if it has definitely not been. This allows us to keep the memory footprint of the filter incredibly small. To have a filter that can remember 4 million elements and only return false positives at a rate of 1 in 1000 (or 0.001), the memory required would be just over 7MB.

Comparatively, if we were to attempt to instead STORE 4 million elements each of a mere 1 KB in length, the resulting memory footprint would require 4 GB. This is why Bloom filters can only tell us if something has been seen before, but it cannot return to us the actual object.

##Performance
Technically speaking, a Bloom filter is simply a bit array where 1s represent a hit and 0s represent a miss. When an element is added to the filter, it is hashed with different algorithms a certain number of times (determined by some magic math that impacts the false positive probability) and then those hashes are used as different indexes to store 1s.

Cryptographic hash functions, especially modern ones such as BCrypt, are often designed specifically to be slow in order to deter password crackers. Non-cryptographic hash functions, such as Murmur and City, are instead designed to be very quick.

This implementation by default uses Python's builtin `hashlib` module and the MD5 hash function contained therein, but it is highly recommended to instead supply your own. Faster hash functions will increase performance of the filter. <a href="https://github.com/flier/pyfasthash">PyHash</a> is a great third-party module for non-cryptographic hash functions.

To supply a hash function for the BloomFilter to use you simply pass the callable reference to the constructor as such:
```python
from pyhash import Murmur3_x64_128 as murmur

murmur_hash_function = murmur()
bfilter = BloomFilter(1000, 0.001, murmur_hash_function)
```

In order to pass a function in this way it must follow 3 criteria:
- it is a reference to a `callable()` function or object
- it can take 2 arguments, where the first is a string to be hashed and the second is a salt or seed value that will vary the result by a large and varying amount (ie avalanching)
- it returns a value on which python's `long()` function can be called

Note in the code example above, we first must call the murmur constructor and then pass reference to the returned callable object into our constructor.

##Dependencies
This module has been specifically designed to rely on as few third-party modules as possible. At this time, the only required third-party dependency is on <a href="https://github.com/ilanschnell/bitarray">bitarray</a> which can be installed with:

`pip install bitarray`

<a href="https://github.com/flier/pyfasthash">PyHash</a> is a great third-party module for fast non-cryptographic hashes, however it is not depended upon in anyway.

##Performance Data and Metrics
Coming soon.
