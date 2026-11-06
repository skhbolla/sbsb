class Solution:
    def bruteforce_approach(self, s: str, t: str) -> bool:
        '''
        The most naive way of doing this is by interating
        over the first string , and for each character find out
        if the same character exists in second string.. If yes , "mark" it a
        'used'.

        If at any point , the second string does not have
        the needed char unused , return False
        By the end all chars in second string should be used, otherwise False.
        '''

        used_mask = [0]*len(t)
        for c in s:
            found_flag = 0
            for i in range(0,len(t)):
                if t[i] == c and used_mask[i] == 0:
                    used_mask[i] = 1
                    found_flag = 1
                    break
            if found_flag != 1:
                return False
        
        for i in used_mask:
            if i != 1:
                return False
        return True



    def sorting_approach(self, s: str, t: str) -> bool:
        '''
        The idea behind this approach is that the 
        sorted versions of both strings must be same.
        
        Time Complexity - O()
        Space Complexity - (n) #Python strings are immutable , inplace sort not possible
        '''
        return sorted(s) == sorted(t)
    
    def hashmap_approach(self, s: str, t: str) -> bool:
        '''
        Two strings are considered anagrams if they consist of 
        identical characters, and each character appears the 
        same number of times in both strings
        i.e same character frequency distribution
        '''

        if len(s) != len(t): #Optimization - If lens are not same, not anagrams
            return False

        #hashtable to create a frequency distribution of first string
        ht = {}
        for i in s:
            if i in ht:
                ht[i] += 1
            else:
                ht[i] = 1

        #Iterate over second string and decrement corresponding ht mapping
        for i in t:
            if i in ht and ht[i] > 0:
                ht[i] -= 1
            else:
                return False

        return True
    
    def counter_approach(self, s: str, t: str) -> bool:
        '''
        Counter is a subclass of dict. It is mainly used to 
        count the frequency of elements.. This property lends itself
        very well to this problem..

        Why is Counter(s) often faster than a manual dict counting loop,
        even though Counter is a subclass of dict?

        Although Counter inherits from dict and uses the same underlying
        hash table implementation, the performance difference does NOT
        come from the data structure itself.

        The key difference is WHERE the counting loop executes:

        - In a manual dict approach, the iteration over the string happens
        in Python bytecode. Each iteration incurs interpreter overhead,
        method lookups, function calls (e.g., dict.get), reference counting,
        and multiple hash table operations.

        - In Counter(s), the iterable is processed inside optimized C code
        within CPython's implementation of Counter.update(). The loop,
        hash lookups, and updates are performed in tight C-level loops,
        avoiding Python interpreter overhead.

        C-level loops are significantly faster than Python-level loops due to:
            - No bytecode dispatch
            - Fewer indirections
            - Better cache locality
            - Reduced function call overhead

        Thus, Counter is not faster because it is a different data structure,
        but because its counting logic executes in C rather than Python.

        Important:
        If you manually increment a Counter inside a Python loop
        (e.g., for ch in s: c[ch] += 1), there is no performance advantage
        for the increment logic (compared to raw python dicts), 
        this is because the loop is again executed in Python space.
        '''

        return Counter(s) == Counter(t)

    def isAnagram(self, s: str, t: str) -> bool:
        # return self.bruteforce_approach(s, t)
        # return self.sorting_approach(s, t)
        # return self.hashmap_approach(s, t)
        return self.counter_approach(s, t)
