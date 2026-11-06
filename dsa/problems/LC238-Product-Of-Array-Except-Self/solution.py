class Solution:
    def bruteforce(self, nums: List[int]) -> List[int]:
        '''
        The bruteforce solution is,
        for every index i , iterate from 0 to i-1 and i+1 to n,
        calculate the products and return

        T.C = For each 'i' O(N) * traverse through n-1 elements O(N)
            ==> O(N * N) ==> O(N^2)
        S.C = No auxilary space utilized except for the solution array. O(1)
        '''

        sol = []
        n = len(nums)
        for i in range(0,n):
            prod = 1
            for j in range(0,i):
                prod *= nums[j]
            for j in range(i+1, n):
                prod *= nums[j]
            sol.append(prod)

        return sol

    def divide(self, nums: List[int]) -> List[int]:
        '''
        Division method:

        This problem would be trivial if there can be no zeroes in the array.

        But since the array can contain zeroes. There are 3 cases to handle:
        No zeroes -> sol[i] will be product/arr[i]
        One Zero -> sol is all zeroes except for the index of zero element
                    (where the sol will be product of all non-zeroes).
        More than One Zero -> sol is all zeroes
        '''

        #First pass to calculate product of non zeroes and to count zeroes.
        product = 1
        zeroes = 0
        for i in nums:
            if i == 0:
                zeroes += 1
            else:
                product *= i

        #Second pass to calculate the solution array

        if zeroes == 0 : return [int(product/i) for i in nums]
        if zeroes > 1 : return [0]*len(nums)

        if zeroes == 1:
            sol = []
            for i in nums:
                if i != 0:
                    sol.append(0)
                else:
                    sol.append(product)
        return sol

    def prefix_suffix_array(self, nums: List[int]) -> List[int]:
        '''
        The problem with the bruteforce method was the recalculation 
        of products from scratch over and over..

        We know that sol[i] = product(sol[0 to i-1]) * product(sol[i+1, n])
        What if we precompute the two terms ? 

        1. First pass (0 to n) - Caclulate the prefix product array
        2. Second pass (n to 0) - Calculate the suffix product array
        3. Final pass (0 to n) - Calculate sol[i] as prefix[i] * suffix[i] 

        T.C = 3 passes over array = O(N + N + N) ==> O(N)
        S.C = 2 auxilary arrays (prefix and suffix) + 1 solution array
            ==> O(N + N + N) ==> O(N)
        '''

        #Calculate Prefix product array
        pre = []
        prd = 1
        for i in nums:
            pre.append(prd)
            prd *= i

        #Calculate Suffix product array
        suf = [None]*len(nums)
        prd = 1
        for i in range(len(nums)-1, -1, -1):
            suf[i] = prd
            prd *= nums[i]

        #Calculate solution array
        return [pre[i] * suf[i] for i in range(0, len(nums))]

    def optimal(self, nums: List[int]) -> List[int]:
        '''
        Can we achieve the same outcome as prefix+suffix approach,
        but without using any auxilary space ??

        Yes..
        For our solution array 'sol':
        First pass
            |-> for each 'i' , sol[i] = product of all preceding elements
            |-> So , basically the prefix array
            |-> Maintain running products to avoid quadratic time
        Second pass
            |-> sol[i] = sol[i] * product of all subsequent elements
            |-> Since we need subsequent elements , the only way to avoid
                quadratic time is to traverse the array in reverse
            |-> So basically the same logic as the suffic array

        By the end of the two passes , the sol array will be our result

        T.C = Two passes O(N + N) ==> O(N)
        S.C = No auxilary space except for solution array ==> O(1)
        '''

        sol = []

        #First pass
        prd = 1 #running product
        for i in nums:
            sol.append(prd)
            prd *= i

        #Second pass
        prd = 1 #running product
        for i in range(len(nums)-1, -1, -1):
            sol[i] *= prd
            prd *= nums[i]

        return sol



    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # return self.bruteforce(nums)
        # return self.divide(nums)
        # return self.prefix_suffix_array(nums)
        return self.optimal(nums)
