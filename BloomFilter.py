from BitHash import BitHash as BH
from BitVector import BitVector as BV
import math

class BloomFilter(object):
    
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        
        #use equation to calculate the number of bits needed to avoid
        #more false positives than the maximum allowed
        phi = 1-(maxFalsePositive)**(1/numHashes)
        return math.ceil((numHashes)/(1-phi**(1/numKeys)))
        
    
    # Creates a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes are be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        
        #keep track of the number of keys, hashes, and the maximum false positive
        #rate
        self.__numKeys = numKeys
        self.__numHashes = numHashes
        self.__maxFalsePos = maxFalsePositive
        
        #use the __bitsNeeded()  method to calculate how many bits long the 
        #bit vector should be
        self.__N=self.__bitsNeeded(self.__numKeys, self.__numHashes,\
                                   self.__maxFalsePos)
        
        #initialize a bit vector of the needed size
        self.__bitVector = BV(size=(self.__N))
        
        #keep track of how many bits are set to 1
        self.__numBits=0
    
  
    def insert(self, key):
        
        #start seed should be zero
        seed = 0
        for i in range(self.__numHashes):
            
            #upon hashing, store the result of the hash to be used as
            #the next seed
            seed = BH(key, seed)
            
            #find what index to use based on the size of the bit vector
            index = seed%self.__N
            
            #if the index isn't already a 1, set it to be 1, and increment
            #the count of the number of bits we've set
            if self.__bitVector[index]!=1:
                self.__bitVector[index]=1
                self.__numBits+=1
        
    
    def find(self, key):
        
        #start seed should be zero
        seed = 0
        for i in range(self.__numHashes):
            
            #each time we hash, use the previous hash as the seed - 
            #this simulates using multiple hash functions
            seed = BH(key, seed)
            
            #if we did not find that the index where we should find this key
            #was set to 1, tell the client
            if not self.__bitVector[seed%self.__N]:
                return False
        
        #if we made it here, then we found the key in the Bloom Filter
        return True
            
       
    def falsePositiveRate(self):
        
        #calculate the false positive rate based on the number of bits
        #that are initialized
        phi = (self.__N - self.__numBits)/(self.__N)
        return (1-phi)**self.__numHashes

    def numBitsSet(self):
        return self.__numBits


def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter
    BF = BloomFilter(numKeys, numHashes, maxFalse)
    f = open("wordlist.txt")
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    for i in range(numKeys):
        BF.insert(f.readline().strip())
        
    f.close()

    print('Estimated False Positive:', BF.falsePositiveRate())
    
    f = open("wordlist.txt")
    
    missing = 0

    for i in range(numKeys):
        if not BF.find(f.readline().strip()): missing+=1

    print("Missing", missing, "words")
    

    accidentallyFound = 0
    for i in range(numKeys):
        if BF.find(f.readline().strip()): accidentallyFound+=1
    
    f.close()
    
    print('Percent False Positive:', accidentallyFound/numKeys)
    
if __name__ == '__main__':
    __main()       

