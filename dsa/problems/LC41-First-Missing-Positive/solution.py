class Solution:
    def bruteforce(self, nums: List[int]) -> int:
        ''' The honest way of doing this is by
        starting from i = 1 and checking if i is in the array

        If the first missing positive is 'k' , then the time complexity
        will be O(k*n) where n is len of array
        '''

        ''' TC - O(k*n) where k is the first missing positive
        SC - O(1)
        '''
        i = 1
        while True:
            if i not in nums:
                break
            else:
                i = i+1
        return i

    def first_optimization(self, nums: List[int]) -> int:
        '''
        The pigeon hole approach:
        If 'n' is the length of the array, the first missing positive
        MUST be in the range [1, n+1].

        We only need to probe from 1 to n. If all those exist,
            n+1 will be the default answer.
        This bounds our search space and proves that values > n are irrelevant.

        Hence instead of running a True while loop , we can iterate i = 1 to n
        Although this makes no difference in code performance 
            (because the point where loop breaks remains the same) ,
        it's still important to realize that pigeon hole principle is in effect
        '''

        '''
        TC - O(n^2)
        SC - O(1)
        '''
        n = len(nums)
        for i in range(1, n + 1):
            if i not in nums:
                return i

        # Default fallback if 1..n are all present
        return n + 1

    def second_optimization(self, nums: List[int]) -> int:
        ''' Hashmap - UnOptimized
        Inner loop's 'Search over the array' is costing quadratic time.
        We use a hashmap to reduce lookup to O(1).
        Following our search space logic, we only probe up to n.
        '''
        '''
        TC - O(n)
        SC - O(n)
        '''
        hm = {}

        # 1. Frequency Mapping: O(n)
        for i in nums:
            hm[i] = hm.get(i, 0) + 1

        # 2. Probing the bounded range [1, n]: O(n)
        n = len(nums)
        for i in range(1, n + 1):
            if i not in hm:
                return i

        return n + 1

    def third_optimization(self, nums: List[int]) -> int:
        '''
        Refining the Hashmap:
        Since our search space is strictly [1, n], we can ignore
        any input value x <= 0 or x > n.

        By storing anything value outside this search space in the hashmap we 
            are wasting both time and space..

        So , what if we use a simple if condition to check if condition 
            before pushing to hashmap ?
        I pondered over the implications here... 
        Doing this conditional check introduces branching into our code,
        and since our input is an unsorted array , it will be a random mix 
            of positive and negative numbers...
        So the CPU might suffer branch misprediction penalties ...

        Doing this optimization does not change the asymptotic complexities :
        TC will still be O(n + n) => O(n) &
        SC will still be O(n) .. because in worst case, 
            all values in input array will be in the search space.

        Verdict : This Optimization might not change the Asymptotic Complexity,
            but makes a positive difference in Real-world Performance.

        Here's why :
        1. Time - Even though the conditional statement might introduce 
            CPU branching mis-prediction penalties;
            the cost of said penalty is far lower than the cost of hashing, 
                handling potential hash collisions,resizing the hashmap's 
                underlying array(amortized),allocating memory for the new entry
        2. Space - Even though the worst case scenario is still O(n) , 
                in most cases , by ignoring the values outside our search space
                we bring down the Resident Set Size (RSS).
                ( A side benefit is that less dense hashmaps will have fewer 
                    hash collisions , hence faster lookups closer to true O(1))
        '''

        n = len(nums)
        hm = {}

        for i in nums:
            # Ignore anything outside our "Interest Set" [1, n]
            if 1 <= i <= n:
                hm[i] = 1

        for i in range(1, n + 1):
            if i not in hm:
                return i

        return n + 1

    def optimal(self, nums: List[int]) -> int:
        ''' Cyclic Sort approach
        The array itself becomes the hashmap.
        We place every value x in the range [1, n] at index x-1 (It's rightful
                home).
        Any value outside [1, n] is ignored and left as "noise".
        If index i does not hold value i+1 after sorting, i+1 is missing.
        '''

        '''
        TC - O(n) (Amortized: each swap places one element correctly)
        SC - O(1)
        '''
        n = len(nums)

        # First pass - Cyclic Swap
        for i in range(n):
            # While the current value belongs in our [1, n] range
            # AND it is not already in its rightful home...
            # AND the home it wants to go to doesn't already have the correct
            # value, if we dont do this.... duplicates in the input array will
            # cause an infinite loop.
            while 1 <= nums[i] <= n and nums[i] != nums[nums[i] - 1]:
                # Swap it to its rightful home (nums[i] - 1)
                target = nums[i] - 1
                nums[i], nums[target] = nums[target], nums[i]

        # Second pass - Find the first gap
        for idx, val in enumerate(nums):
            # The first index that doesn't "match" its value
            if val != idx + 1:
                return idx + 1

        # Final fallback: The array was a perfect permutation of [1, n]
        return n + 1

    def firstMissingPositive(self, nums: List[int]) -> int:
        return self.optimal(nums)
