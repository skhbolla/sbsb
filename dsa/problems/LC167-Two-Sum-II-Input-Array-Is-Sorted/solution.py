class Solution:
    def bruteforce(self, numbers: List[int], target: int) -> List[int]:
        '''
        Ignore the ordering , try every possible pair
        Time Complexity - O(n ^ 2)
        Space Complexity - O(1)
        '''
        for i in range(0,len(numbers)):
            for j in range(i+1, len(numbers)):
                if numbers[i] + numbers[j] == target:
                    return [i+1, j+1]

    def hashmap_two_pass(self, numbers: List[int], target: int) -> List[int]:
        '''
        For every 'i' , we are repeatedly iterating over the array
        to find it's complement.. This is costing us quadratic time.

        Instead we can create a hashmap to reduce this "search" complexity
        into a simple O(1) lookup

        Time Complexity - O(N) two passes over input array
        Space Complexity - O(N) to create lookup table
        '''

        #Construct the lookup hashmap
        lookup = {}
        for i in range(0, len(numbers)):
            if numbers[i] not in lookup:
                lookup[numbers[i]] = [i]
            else:
                lookup[numbers[i]].append(i)

        #Iterate over array to check if complement exists
        for idx, val in enumerate(numbers):
            complement = target - val
            if complement in lookup:
                for i in lookup[complement]:
                    # Because the problem guarantees exactly one solution,
                    #'lookup[complement]' will contain at most 2 indices
                    # which happens only if complement + complement == target.
                    # i.e, if 'complement == val', there are exactly two occurrences in 'lookup'.
                    # If 'complement != val', there is exactly one occurrence in 'lookup'.
                    # This makes the inner loop runs at most twice, maintaining O(1) inner complexity.
                    if idx != i:
                        return [idx+1, i+1]

    def hashmap_one_pass(self, numbers: List[int], target: int) -> List[int]:
        '''
        In the two pass approach , we dedicated an entire iteration
        over the full array just to create the lookups.

        But we already know that the ordering does not matter. So why
        bother precomputing a lookup , just so we can do forward lookups..?

        Why not create the hashmap whilst checking for the complement
        in already visited items ??
        '''

        lookup = {}
        for idx, val in enumerate(numbers):
            complement = target - val
            if complement in lookup:
                # Note: No loop is needed over lookup[complement] because:
                # 1. 'One solution' guarantee: If val != complement, 
                #complement appears only once (Guarenteed by the question).
                # 2. Implementation logic: If val == complement, we return the first index 
                #    (already in lookup) and the current index before the second one is ever 
                #    added to the map. Thus, lookup[complement] always has exactly one element.
                return [lookup[complement][0]+1, idx+1]
            if val not in lookup:
                lookup[val] = [idx]
            else:
                lookup[val].append(idx)

    def binary_search(self, numbers: List[int], target: int) -> List[int]:
        '''
        Since we know that the array is already in non-descending order..
        For a given value at index i , calculate complement as target - val
        and perform binary search over array[i+1] to array[n]

        This reduces our quadratic time search to a logarithmic search.

        Time complexity - O(n log n)
        Space complexity - O(1)
        '''

        for i in range(len(numbers)):
            l, r = i + 1, len(numbers) - 1
            tmp = target - numbers[i]
            while l <= r:
                mid = l + (r - l)//2
                if numbers[mid] == tmp:
                    return [i + 1, mid + 1]
                elif numbers[mid] < tmp:
                    l = mid + 1
                else:
                    r = mid - 1

    def two_pointers(self, numbers: List[int], target: int) -> List[int]:
        '''
        We know that the array is already sorted .. So initialize 
        two pointers at either end of the array.

        Move both pointers inward such that the sum of two pointer values
        moves closer to target.

        i.e if target > (l + r) ; move r to the left
        or if target < (l + r) ; move l to the right
        or if target = (l + r) ; we found the solution

        Since the question guarentees atleast (and exactly) one solution,
        this approach is extremely safe..
        '''

        l = 0
        r = len(numbers) - 1
        while(True):
            if numbers[l] + numbers[r] == target:
                return [l+1, r+1]
            elif numbers[l] + numbers[r] > target:
                r = r-1
            else:
                l = l+1
            #Note that we are not writing any break statements
            #inside the infinite while loop. This is usually very unsafe
            #but the question guarentees a solution exists. So the loop 
            #will break out through the return statement


    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        # return self.bruteforce(numbers, target)
        # return self.hashmap_two_pass(numbers, target)
        # return self.hashmap_one_pass(numbers, target)
        # return self.binary_search(numbers, target)
        return self.two_pointers(numbers, target)
