class Solution:

    def sorting_approach(self, nums: List[int]) -> int:
        '''
        A trivial solution to this problem would be by sorting the array 
        and finding the longest consecutive element sequence.

        T.C = Sort the array O(N log N) + iterate over sorted array O(N)
            ==> O(N log N + N) ==> O(N log N)
        
        S.C = In place sort used , so no auxilary space O(1)

        '''
        nums.sort() #O(n log n) -> Tim Sort

        if len(nums) == 0 : return 0

        max_length = 1 #For a non empty array this can never be less than 1.
        count = 1
        for i in range(1, len(nums)):
            if nums[i] == nums[i-1] + 1 : count += 1
            elif nums[i] == nums[i-1] : continue
            else : count = 1
            if count > max_length : max_length = count

        return max_length


    def longestConsecutive(self, nums: List[int]) -> int:
        return self.sorting_approach(nums)
