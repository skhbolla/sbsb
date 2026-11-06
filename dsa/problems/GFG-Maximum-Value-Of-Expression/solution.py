#User function Template for python3

class Solution:
    def bruteforce(self, arr: list[int]) -> int:
        '''The most naive way of solving this is 
        by looking at every possible pair of i,j and calculating the expression'''
        n = len(arr)
        sol = 0
        for i in range(0,n):
            for j in range(0,n):
                expr = abs(arr[i] - arr[j]) + abs(i - j)
                if expr > sol:
                    sol = expr
                    
        return sol
        
    def first_optimization(self, arr: list[int]) -> int:
        '''Realize that, for a pair of chosen i and j
        the value of expression stays the same
        for both (i,j) and (j,i).
        So we are making a lot of unnecessary repeated calculations.
        Instead of running the inner loop from 0 to n ; let's run it 
        from i to n. This will ensure that we dont perform 
        the above mentioned symmetric calculations.'''
        n = len(arr)
        sol = 0
        for i in range(0,n):
            for j in range(i,n):
                expr = abs(arr[i] - arr[j]) + abs(i-j)
                if expr > sol:
                    sol = expr
                    
        return sol
        
    def second_optimization(self, arr : list[int]) -> int:
        '''This is a very minor optimization , but
        important observation nonetheless.
        When i=j , the value of expression will be 0.
        Since the expression is in absolute terms , the result will 
        always be positive i.e greater than or equal to zero.
        
        Hence the cases where i=j can be safely ignored because 
        some other case will definitely produce zero or higher result.
        
        Code wise this can be acheived by running the inner loop from 
        i+1 to n instead of i to n (So i will never equal to j)'''
        
        n = len(arr)
        sol = 0
        for i in range(0, n):
            for j in range(i+1, n):
                expr = abs(arr[i] - arr[j]) + abs(i - j)
                if expr > sol:
                    sol = expr
        return sol
        
    def third_optimization(self, arr : list[int]) -> int:
        ''' From the second optimization , we realize that 
        j will always be greater than i
        So the expression collapses into : 
        |arr[i] - arr[j]| + (j - i)
        
        Why ??
        Since the term (i-j) is guarenteed to be negative ,
        |i-j| will be the negative counterpart of the same
        i.e -(i-j) => (j-i)
        '''
        
        '''Remember that the time complexity is still quadratic (n^2) ,
        this optimization does not achieve much in terms of time complexity,
        but we were able to get rid of a absolute term.
        '''
        
        n = len(arr)
        sol = 0
        for i in range(0, n):
            for j in range(i+1, n):
                expr = abs(arr[i] - arr[j]) + (j-i)
                if expr > sol:
                    sol = expr
        return sol
        
    def fourth_optimization(self, arr : list[int]) -> int:
        ''' In the previous optimization, we were successful in
        removing the absolute bars for one of the terms..
        If we can remove the absolute bars from the other term too,
        we will be able to completely de-couple i and j terms...
        
        This will linearize the expression therefore our time complexity too...
        
        The term |arr[i] - arr[j]| only has two possible cases:
        arr[i] - arr[j] and arr[j] - arr[i]
        
        Therefore the possible cases of our expression become:
        (arr[i] - arr[j]) + (j - i)
        (arr[j] - arr[i]) + (j - i)
        
        Decouple and rewrite as :
        (arr[i] - i) + (j - arr[j])
        (arr[j] + j) - (arr[i] + i) 
        
        Rewrite again as :
        (arr[i] - i) - (arr[j] - j)
        (arr[j] + j) - (arr[i] + i) 
        
        So the question was to find the maximum of the expression,
        the solution is simply the maximum of above two terms
        
        solution = MAX ( (arr[i] - i) - (arr[j] - j) ,
                         (arr[j] + j) - (arr[i] + i) )
        
        
        To simplify let's just call :
        f1(x) = arr[x] - x 
        f2(x) = arr[x] + x
        
        The the solution becomes,
        
        solution = MAX ( (max f1 - min f1) ,
                         (max f2 - min f2) )
        '''
        
        '''
        Extremely important to note:
        
        Even though this is now O(n) time , we are using two arrays to store 
        f1 and f2 values respectively at each index i.e space = O(n)
        
        '''
        
        
        f1 = [] #Store the value of f1 for each index
        f2 = [] #Store the value of f2 for each index
        
        n = len(arr)
        
        for x in range(0, n):
            f1.append(arr[x] - x)
            f2.append(arr[x] + x)
            
        return max( ( max(f1) - min(f1) ) , 
                    ( max(f2) - min(f2) ) 
                )
        
        
    def optimal(self, arr : list[int]) -> int:
        '''
        In the above optimization , we were using arrays to maintain the f1 , f2
        values at each index. This meant that we used two extra arrays of same size as the input
        Hence the space complexity is O(n)
        
        Also , we pass over the input array only once , but we pass over the f1 , f2 arrays too,
        to caluculate the min and max of each respective array..
        
        Realize that we only ever cared about the min and max ... 
        What is the point of maintaing f1 and f2 arrays...
        Instead just maintain the max and min of f1 and f2 respectively
        '''
        
        n = len(arr)
        
        if(n < 2): 
            # The constraints specify that size will never be 0,
            # But it can be 1
            # I've chosen to handle both cases either way
            return 0 
        
        maxf1 = maxf2 = arr[0] - 0
        minf1 = minf2 = arr[0] + 0 

        for x in range(0, n):
            f1 = arr[x] - x
            f2 = arr[x] + x
            
            if f1 > maxf1 : maxf1 = f1
            if f1 < minf1 : minf1 = f1
            if f2 > maxf2 : maxf2 = f2
            if f2 < minf2 : minf2 = f2
        
        return max( (maxf1 - minf1) , (maxf2 - minf2) )
        
    
    def maxValueOfExpression(self, arr):
        return self.optimal(arr)
    
