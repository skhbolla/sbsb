class Solution:
    def bruteforce(self, a, n):
        '''
        Bruteforce approach
    
        The most naive way to approach this problem is by considering 
        every single subarray possible and finding out which has the:
        maximum benefit;
        
        Time complexity - O(n^3)
        Space complexity - O(1)
        '''
        
        ones_before_flip = a.count(1)
        
        #We initialize the max tracking variable to this so that if no better answer
        #exists, we can simply return the number of 1s before flip..
        #Which is exactly what the question asks :
        # ("You can possibly make zero operations to get the answer")
        max_possible_ones_after_flip = a.count(1) 
        
        for i in range(0, n):
            for j in range(i, n):
                subarray = a[i:j+1]
                
                #Calculate 'gain' for chosen subarray.. Gain can be negative
                #i.e choosing that subarray worsens the 1 count
                gain = sum(1 if x == 0 else -1 for x in subarray)
                
            max_possible_ones_after_flip = max(max_possible_ones_after_flip , ones_before_flip + gain)
        
        return max_possible_ones_after_flip
        
    
    def kadane(self, a, n):
        '''
        The point of kadane is that , if the local gain ever becomes negative,
        there is no point trying to extend the subarray.. Instead start fresh
        
        TC : O(n)
        SC : O(1)
        '''
        
        ones_before_flip = a.count(1)
        max_gain = 0
        gain = 0
        
        for i in a:
            if i == 0:
                gain += 1
            else:
                gain -= 1
                
            max_gain = max(max_gain, gain)
            
            if gain < 0:
                gain = 0
                
        return max_gain + ones_before_flip
        
    
    def maxOnes(self, a, n):
        #return self.bruteforce(a, n)
        return self.kadane(a, n)
        
