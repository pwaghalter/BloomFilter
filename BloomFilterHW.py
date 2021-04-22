from BitHash import BitHash as BH
from BitVector import BitVector as BV
import math

class BloomFilter(object):
    # Return the estimated number of bits needed (N in the slides) in a Bloom 
    # Filter that will store numKeys (n in the slides) keys, using numHashes 
    # (d in the slides) hash functions, and that will have a
    # false positive rate of maxFalsePositive (P in the slides).
    # See the slides for the math needed to do this.  
    # You use Equation B to get the desired phi from P and d
    # You then use Equation D to get the needed N from d, phi, and n
    # N is the value to return from bitsNeeded
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        
        #use equation to calculate the number of bits needed to avoid
        #more false positives than the maximum allowed
        phi = 1-(maxFalsePositive)**(1/numHashes)
        return math.ceil((numHashes)/(1-phi**(1/numKeys)))
        
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed
        # In addition to the BitVector, might you need any other attributes?
        
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
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    # See the "Bloom Filter details" slide for how insert works.
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
        
    
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.
    # See the "Bloom Filter details" slide for how find works.
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
            
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # measuring the proportion of false positives that are actually encountered.
    # In other words, you use equation A to give you P from d and phi. 
    # What is phi in this case? it is the ACTUAL measured current proportion 
    # of bits in the bit vector that are still zero. 
    def falsePositiveRate(self):
        
        #calculate the false positive rate based on the number of bits
        #that are initialized
        phi = (self.__N - self.__numBits)/(self.__N)
        return (1-phi)**self.__numHashes
         
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.
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
    
    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.
    print('Estimated False Positive:', BF.falsePositiveRate())
    
    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter. Don't close the input file of words since
    # in the next step we want to read the next numKeys words from the file. 
    f = open("wordlist.txt")
    
    missing = 0

    for i in range(numKeys):
        if not BF.find(f.readline().strip()): missing+=1

    print("Missing", missing, "words")
    

    
    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    accidentallyFound = 0
    for i in range(numKeys):
        if BF.find(f.readline().strip()): accidentallyFound+=1
    
    f.close()
    
    # Print out the percentage rate of false positives.
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE
    print('Percent False Positive:', accidentallyFound/numKeys)
    
if __name__ == '__main__':
    __main()       

