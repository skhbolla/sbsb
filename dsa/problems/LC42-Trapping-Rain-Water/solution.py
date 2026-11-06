class Solution:
    def trap(self, height: List[int]) -> int:
        return self.maxArrays(height)


    def maxArrays(self, height):
        trapped = 0
        # Construct the left max array
        lmax = []
        currmax = float('-inf')
        for i in height:
            if i > currmax:
                currmax = i
            lmax.append(currmax)
        # Construct the right max array
        rmax = [0] * len(height)
        currmax = float('-inf')
        for i in range(len(height)-1 , -1 , -1):
            if(height[i] > currmax):
                currmax = height[i]
            rmax[i] = currmax
        print(f"Leftmax array = {lmax}")
        print(f"Right max array = {rmax}")
        # Calculate the water at each index using left max and right max
        for i in range(0,len(height)):
            water = min(lmax[i] , rmax[i]) - height[i]
            trapped = trapped + water if water > 0 else trapped

        return trapped

    def bruteforce(self, height):
        trapped = 0
        for i in range(0,len(height)):
            left_max = max(height[0:i+1])
            right_max = max(height[i::])
            print(f"For index {i} the left & right max are {left_max} {right_max}")
            water = min(left_max , right_max) - height[i]
            print(f"Water at index {i} is {water}")
            trapped = trapped + water if water > 0 else trapped
        return trapped
