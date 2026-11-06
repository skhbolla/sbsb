class Solution:

    def bruteforce(self, nums: List[int]) -> int:
        '''
        Bruteforce - Extremely naive

        This is truely naive because we have a complexity of n^3 :
        n - to run in outer loop
        n - to run the outer loop
        n - to perform the sum calculation over the chose subarray

        Time complexity - O(n^3)
        Space Complexity - O(1)
        '''

        max_sum = float('-inf')
        n = len(nums)
        for i in range(0,n):
            for j in range(i,n):
                max_sum = max(max_sum , sum(nums[i:j+1]))

        return max_sum

    def better_bruteforce(self, nums: List[int]) -> int:
        '''
        Bruteforce - Optimized bruteforce

        The problem in the previous bruteforce is:
        When we use list slicing , we are creating a shallow copy of the slice
        Since it is a shallow copy , python creates uses a contiguous block
        of k * 8 bytes in memory
            -> Where K is the length of the slice
            -> 8 bytes is the size of a pointer (reference) in 64 bit machines

        Every time your loop hits nums[i:j+1], the Python memory allocator
        requests a block of k * 8 bytes. Even though the slice is "destroyed"
        after sum() finishes, the Python Garbage Collector does not always
        return that memory to the OS immediately. It often keeps it in a
        "free list" for future allocations. This could cause a spike in RSS.
        '''

        n = len(nums)
        max_sum = float('-inf')

        for i in range(0,n):
            for j in range(i,n):
                curr_sum = 0
                for x in range(i,j+1):
                    curr_sum += nums[x]
                max_sum = max(max_sum , curr_sum)

        return max_sum

    def running_sum_approach(self, nums: List[int]) -> int:
        '''
        Approach - Running sum

        The problem with bruteforce approach is ,
        to calculate the sum(nums[i:j]) we are walking the array from i to j
        for every pair of i, j we encounter ...

        But wait, why restart the summation from scratch for every 'j'?
        If we fix 'i', the sum of the subarray ending at 'j' is just
        the sum of the subarray ending at 'j-1' plus the new element.
        By maintaining this 'running sum', we eliminate the inner-most loop
        and linearize the summation process.

        Time Complexity - O(n^2)
        Space Complexity - O(1)
        '''
        n = len(nums)
        max_sum = float('-inf')

        for i in range(0,n):
            curr_sum = 0
            for j in range(i,n):
                curr_sum += nums[j]
                max_sum = max(max_sum, curr_sum)

        return max_sum

    def prefix_array_approach(self, nums: List[int]) -> int:
        '''
        Approach - Prefix arrays

        In the previous approach we are re-calculating sums for every
        different 'i'. While Running Sum is space-efficient, it doesn't
        "store" anything. If we needed to perform multiple Range Sum Queries,
        we'd be stuck walking the sub-array every single time.

        By using a Prefix Array, we precompute the cumulative sum from the origin
        for every index. We can find sum(nums[i:j]) = pa[j] - pa[i-1].

        So , we trade O(n) space to linearize our summation 'walk' into a O(1) query.

        *** [!IMPORTANT] Low-Level Trade-offs: ***
        Is this actually "better" than the Running Sum approach?
            Answer is a resounding **NO**

        This approach still uses the same outer 'i' loop and inner 'j' loop,
        but swaps the addition operations inside the inner loop with subtraction operations.
        Hence, the time complexity remains same.

        In a real-world scenario, this approach is technically "*worse*" for a
        Maximum Subarray problem because of the O(n) memory tax.

        By allocating a second large array (pa), we increase the risk of Cache Misses
        as the CPU has to fetch data from different segments of RAM.

        Running Sum (O(1) space) on the other hand wins on raw hardware performance because
        the CPU has to keep track of just one number (the running sum) in a single register.

        Time Complexity - O(n^2)
        Space Complexity - O(n)
        '''

        n = len(nums)

        # Construct prefix array
        pa = []

        run_sum = 0
        for i in range(0,n):
            run_sum += nums[i]
            pa.append(run_sum)

        # Main logic
        max_sum = float('-inf')

        for i in range(0, n):
            for j in range(i, n):
                # This entire conditional stuff feels janky to me
                # I much prefer creating my prefix sum array with a
                # extra zero in the front..
                # That will remove the necessity of having to do this..
                if i == 0:
                    curr_sum = pa[j]
                else:
                    # Note: Python's pa[-1] would access the end of the list,
                    # which is why we need this boundary check to maintain
                    # the identity property of the summation.
                    curr_sum = pa[j] - pa[i-1]

                max_sum = max(max_sum, curr_sum)

        return max_sum

    def better_prefix_array_approach(self, nums: List[int]) -> int:
        '''
        This is the same approach as previous , but
        with a slightly different way of implementing out prefix sum array

        By choosing to have the first element of prefix sum array as 0,
        we can remove the janky if conditions inside the main logic..

        Time complexity - O(n^2)
        Space complexity - O(n)
        '''

        n = len(nums)

        # Construct the prefix sum array
        pa = [0] * (n+1) #n+1 because we dedicate the 0th index for a dummy zero

        for i in range(0, n):
            pa[i+1] = pa[i] + nums[i]


        # Main Logic
        max_sum = float('-inf')

        for i in range(0, n):
            for j in range(i, n):
                curr_sum = pa[j+1] - pa[i]
                max_sum = max(max_sum, curr_sum)

        return max_sum

    def optimal(self, nums: List[int]) -> int:
        '''
        Kadane's algorithm

        The main idea behing this approach is that , 
        if at any point the current sum of the sub array becomes negative,
        it becomes a debt... so it is better to start a new subarray instead..
        '''
        max_sum = float('-inf')
        curr_sum = 0

        for x in nums:
            curr_sum += x

            max_sum = max(max_sum, curr_sum)

            if curr_sum < 0:
                curr_sum = 0 #Resetting the subarray

        return max_sum



    def maxSubArray(self, nums: List[int]) -> int:
        # return self.bruteforce(nums)
        # return self.better_bruteforce(nums)
        # return self.running_sum_approach(nums)
        # return self.prefix_array_approach(nums)
        # return self.better_prefix_array_approach(nums)
        return self.optimal(nums)
