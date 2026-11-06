class Solution:

    def bruteforce(self, height: List[int]) -> int:
        '''
        The most naive way of solving this is by calculating
        the water stored by all possible containers and returning the
        maximum possible water.
        '''
        n = len(height)
        max_water = 0
        for i in range(0, n):
            for j in range(i+1, n):
                contained_water = (j-i) * min(height[i], height[j])
                max_water = max(max_water, contained_water)
        return max_water

    def two_pointers(self, height: List[int]) -> int:

        '''
        Start with the widest container and move inward, 
        trading width for the potential of finding more height.
        '''
 
        l = 0
        r = len(height)-1
        max_water = 0

        while(l < r):
            # 1. Record the area of the current widest possible container for these two sides
            contained_water = (r-l) * min(height[l], height[r])
            max_water = max(max_water, contained_water)

            #2. Try a narrower container in hopes of finding 
            # a height taller than our current bottleneck 
            if height[l] < height[r]:
                l = l + 1
            else:
            #Note: This else block includes the case where heights are equal.
                r = r - 1

        return max_water


    def maxArea(self, height: List[int]) -> int:
        # return self.bruteforce(height)
        return self.two_pointers(height)