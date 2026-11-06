from typing import List 

class Solution:
    def twopassbruteforce(self, nums: List[int]) -> int:
        '''
        Time complexity - O(n) to create hashmap/counter + O(n) to get max element
        Space complexity - O(n) to hold hashmap/counter
        '''
        #Maintain a counter and return most frequent element
        hm = {}
        for i in nums:
            hm[i] = hm.get(i, 0) + 1
        
        return max(hm, key = hm.get) 
        #Max takes a key arugment which is a function applied to each element
        # and the result will be used as the comparator

    def onepassbruteforce(self, nums: List[int]) -> int:
        '''
        Time Complexity - O(n) to create counter/hashmap while simulataneously tracking max
        Space Complexity - O(1) to hold counter/hashmap
        '''
        hm = {}
        maxi = maxc = 0
        for i in nums:
            hm[i] = hm.get(i, 0) + 1

            #Keep track of max
            if hm[i] > maxc:
                maxc = hm[i]
                maxi = i
        return maxi

    def boyermoore(self, nums: List[int]) -> int|None:
        '''
        Boyer-Moore Voting Algorithm

        The algorithm works by partitioning the array into disjoint blocks, 
        where each block has no majority (its count reduced to zero) except 
        potentially the final block. By the Pigeonhole Principle, if a global 
        majority exists, it must emerge as the survivor of the final 
        non-neutralized block because there are physically not enough minority 
        elements in the entire set to neutralize all instances of the majority.
        '''
        soldier_on_field = None
        count = 0

        for curr_soldier in nums:
            #Check if field is un-occupied
            if count == 0:
                #Put the soldier in arena
                soldier_on_field = curr_soldier
                count = 1
            elif curr_soldier == soldier_on_field:
                #Check if curr_soldier is in same team as soldier on field
                count += 1
            else:
                #Fight the opponent and die
                count -= 1
        
        return soldier_on_field

    def majorityElement(self, nums: List[int]) -> int|None:
        return self.boyermoore(nums)
        
