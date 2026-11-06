class Solution:
    def bruteforce(self, nums: list[int]) -> list[list[int]]:
        '''
        Explore all possible triplets and return the ones that sum to 0

        Unlike 2sum problem, we are not asked to return the indices of pairs
        (indices are unique non repeating); instead we are asked to return the 
        value triplets (values are not guarenteed to be unique). So just 
        limiting the inner loops to i+1 and j+1 will not avoid duplication.

        Hence, we insert sorted triplets into a set to return only unique
        triplets. 
        '''
        sol = set()
        for i in range(0, len(nums)):
            for j in range(i+1, len(nums)):
                for k in range(j+1, len(nums)):
                    if i!= j and i != k and j != k and nums[i] + nums[j] + nums[k] == 0:
                        x = sorted([nums[i], nums[j], nums[k]])
                        sol.add(tuple(x))

        return [list(i) for i in sol]

    def sorted_bruteforce(self, nums: list[int]) -> list[list[int]]:
        '''
         By pre-sorting the array , we can improve the real world
         performance of bruteforce (although TC remains same).
        '''
        nums.sort()
        s = set()
        sol = []
        for i in range(0, len(nums)):
            for j in range(i+1, len(nums)):
                for k in range(j+1, len(nums)):
                    if nums[i] + nums[j] + nums[k] == 0:
                        s.add(tuple([nums[i], nums[j], nums[k]]))
        return [list(i) for i in s]

    def optimized_sorted_bruteforce(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        sol = []
        n = len(nums)

        for i in range(n):
            # Early Break: Smallest number > 0 means no zero sum possible
            if nums[i] > 0:
                break
            # Skip Logic: Avoid re-processing the same 'i' value
            if i > 0 and nums[i] == nums[i-1]:
                continue

            for j in range(i + 1, n):
                # Skip Logic: Avoid re-processing the same 'j' value
                if j > i + 1 and nums[j] == nums[j-1]:
                    continue

                for k in range(j + 1, n):
                    # Skip Logic: Avoid re-processing the same 'k' value
                    if k > j + 1 and nums[k] == nums[k-1]:
                        continue

                    total = nums[i] + nums[j] + nums[k]
                    if total == 0:
                        sol.append([nums[i], nums[j], nums[k]])
                    elif total > 0:
                        # Since it's sorted, if total > 0, increasing k won't help
                        break
        return sol

    def optimal(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        sol = []
        n = len(nums)

        for i in range(n):
            # Early Break and Skip Logic for 'i'
            if nums[i] > 0:
                break
            if i > 0 and nums[i] == nums[i-1]:
                continue

            # Initialize Two Pointers
            left, right = i + 1, n - 1

            while left < right:
                total = nums[i] + nums[left] + nums[right]

                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    # Match found
                    sol.append([nums[i], nums[left], nums[right]])
                    
                    # Move pointers and skip duplicate twins to avoid redundant results
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    
                    # Final shift to next unique values
                    left += 1
                    right -= 1
        return sol

    def threeSum(self, nums: list[int]) -> list[list[int]]:
        # return self.bruteforce(nums)
        # return self.sorted_bruteforce(nums)
        # return self.optimized_sorted_bruteforce(nums)
        return self.optimal(nums)
        
