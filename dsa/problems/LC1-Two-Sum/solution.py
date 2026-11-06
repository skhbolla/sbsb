class Solution:

    def bruteforce_approach(self, nums: List[int], target: int) -> List[int]:
        '''
        Time complexity - O(n^2)
        Space complexity - O(1)
        '''
        for i in range(0,len(nums)):
            for j in range(i+1, len(nums)): #i+1 because we can not use same element twice
                if nums[i]+nums[j] == target:
                    return [i,j] #The question guarentees a solution, so no other return needed.

    def sorting_approach(self, nums: List[int], target: int) -> List[int]:
        '''
        THE SORTING & TWO-POINTER CONVERGENCE
        
        1. THE PREPARATION:
        Since sorting rearranges the array, we first create a list of pairs:
        (value, original_index). This ensures that even when the 'value' moves,
        its 'identity' (index) stays attached to it.
        Example: [4, 7, 1] becomes [(4, 0), (7, 1), (1, 2)]
        
        2. THE TRANSFORMATION:
        We sort the list based on the values.
        Sorted: [(1, 2), (4, 0), (7, 1)]
        
        3. THE TWO-POINTER BRIDGE:
        We place a 'Left' pointer at the start and a 'Right' pointer at the end.
        This creates a "Monotonic Search Space" where moving a pointer has a 
        predictable result on the sum.
        '''
        
        # Attach original indices to the values
        # Format: [(val1, idx1), (val2, idx2), ...]
        indexed_nums = []
        for i, v in enumerate(nums):
            indexed_nums.append((v, i))
            
        # Sort by the value (the first element of the tuple)
        # Time Complexity: O(n log n)
        indexed_nums.sort()

        

        left = 0
        right = len(nums) - 1
        
        # 4. THE CONVERGENCE:
        while left < right:
            current_sum = indexed_nums[left][0] + indexed_nums[right][0]
            
            if current_sum == target:
                # We found the values! Return their original indices.
                return [indexed_nums[left][1], indexed_nums[right][1]]
            
            elif current_sum < target:
                # THE INTUITION: Our sum is too "light." 
                # Since the array is sorted, the only way to get a larger sum 
                # is to move the Left pointer to a larger value.
                left += 1
                
            else:
                # THE INTUITION: Our sum is too "heavy."
                # We must move the Right pointer to a smaller value.
                right -= 1

        return []

    '''
    FINAL COMPLEXITY ANALYSIS:
    - Time: O(n log n) because the sorting step dominates the linear O(n) pointer walk.
    - Space: O(n) to store the extra list of (value, index) tuples.

    PATTERN LABELING: 
    This is the 'Two-Pointer' pattern. 
    Trigger: Use this when you need to find a pair in a range and the data is 
    (or can be) sorted, allowing you to "shrink" the search space from both ends.
    '''

    def twopass_hashtable_approach(self, nums: List[int], target: int) -> List[int]:
        '''
        Two pass Hashtable approach 

        The Bottleneck with bruteforce approach is as follows:
            For every chosen 'i' we repeatedly travel over the array to find a 'j' 
            that suits our need (i.e adds up to target)

            Can linearize this search ?
            Yes , use a hashmap to for O(1) lookup

        Realize that the question explicitly states that only one possible answer exists.
        So for any given value 'x', there can only be one value 'y' that adds up to target.
        i.e., for a given value 'x', its complement will not have a duplicate.
        
        We use a list of indices here to handle the "Self-Match" scenario.
        Example: nums = [4, 7, 1, 4], target = 8.
        
        If we used a simple dictionary like {value: index}, the second '4' at 
        index 3 would overwrite the first '4' at index 0. 
        When we later search for the complement of 4 (which is 8 - 4 = 4), 
        we lose the ability to see both distinct positions (0 and 3) 
        at the same time. Storing them in a list [0, 3] preserves all coordinates 
        in our "Memory" before we start the search.

        Time complexity - O(n) #Two passes over input array
        Space complexity - O(n) #Hashtable
        '''

        ht = {}

        #Iterate over the array and create a hash table
        for idx, val in enumerate(nums):
            if val not in ht:
                ht[val] = [idx]
            else:
                ht[val].append(idx)

        #Iterate over the array and try to find sum complement
        for idx, val in enumerate(nums):
            if target-val in ht:
                for i in ht[target-val]: #Iterate over the list of indices
                    if idx != i: #make sure that we are not using the same element twice
                        return [idx,i]

    def onepass_hashtable_approach(self, nums: List[int], target: int) -> List[int]:
        '''
        Single pass hashtable approach

        In the naive hashtable approach, we has 2 seperate loops for
        creating the hashtable (building) and lookups over hashtable (searching).
        
        Realization : As we walk through the array, we don't need to know
        about the entire array. We only need to know if the complement of the
        current number has appeared previously. If the complement is ahead 
        of us, we will find it later and look back. If it is behind us, 
        we find it now. 

        Time Complexity - O(n) #Single pass
        Space Complexity - O(n)
        '''
        visited = {}
        for idx, val in enumerate(nums):
            if target-val in visited:
                return [idx,visited[target-val]]
            else:
                visited[val] = idx

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # return self.bruteforce_approach(nums, target)
        # return self.sorting_approach(nums, target)
        # return self.twopass_hashtable_approach(nums, target)
        return self.onepass_hashtable_approach(nums, target)
