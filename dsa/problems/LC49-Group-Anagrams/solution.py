class Solution:

    def bruteforce1(self, strs: List[str]) -> List[List[str]]:
        '''
        For every string i , compare it with every other string j
        If i , j are anagrams (check by sorting) .. 
            group them and mark them as grouped
        
        But why mark them ??
        Take for example : ["eat","tea","tan","ate","nat","bat"]

        When i is at eat , then j loops over until end of array , 
        we get the grouping as [eat, tea, ate]
        If we dont mark tea and ate as grouped , 
        then when i reaches tea , it produces another grouping [tea, ate]
        '''

        """
            TIME COMPLEXITY: O(N^2 * K log K)
            - SEARCH SPACE: The implementation utilizes a nested iteration structure to partition 
            the input set S. While the 'grouped' bitmask prunes unnecessary iterations, the worst-case 
            scenario (where no anagrams exist) requires checking every unique pair (i, j), 
            approximating N*(N-1)/2 comparisons, or O(N^2).
            - TRANSFORMATION COST: Within each valid inner loop, 'sorted(strs[i])' and 'sorted(strs[j])' 
            are invoked. For a maximum string length K, sorting typically follows a Timsort 
            mechanism with O(K log K) complexity. 
            - RESULTANT: The total temporal bound is the product of the quadratic selection process 
            and the log-linear transformation cost: O(N^2 * K log K).

            SPACE COMPLEXITY: O(N * K)
            - OUTPUT SPACE: The result structure stores every character of the input precisely once 
            within a nested list architecture. With N strings of length K, the space required 
            for 'sol' is O(N * K).
            - AUXILIARY STATE: 
                1. 'grouped' array: O(N) space to track processed indices.
                2. Sorting overhead: 'sorted()' in Python creates a new list of characters, requiring 
                O(K) temporary space per comparison.
            - TOTAL FOOTPRINT: Dominated by the output storage, maintaining O(N * K).
        """

        """
        LOW-LEVEL IMPLEMENTATION INTRICACIES (REAL-WORLD PERFORMANCE ANALYSIS):

        1) ANCHOR RE-SORTING & REDUNDANT TRANSFORM COST
        ------------------------------------------------
        The dominant inefficiency is that 'sorted(strs[i])' is executed inside the
        inner 'j' loop. This means the anchor string at index 'i' is re-sorted
        (N - i - 1) times. Since sorting is O(K log K), the same deterministic
        transformation is redundantly recomputed repeatedly.

        At the CPU level:
        - Timsort performs multiple comparisons and branching operations.
        - Sorting is branch-heavy and difficult for the branch predictor.
        - The repeated transformation prevents instruction cache reuse benefits.

        This causes a large constant-factor multiplier on top of the already
        quadratic comparison space.


        2) HEAP ALLOCATION & TEMPORARY OBJECT CHURN
        --------------------------------------------
        Python strings are immutable. Therefore:

            sorted(strs[i])

        creates:
            - A new list object
            - K new references (pointers to 1-character strings)
            - Temporary iterator machinery

        Because this happens O(N^2) times in the worst case,
        it generates a massive number of short-lived heap allocations.

        Consequences:
        - Increased pressure on Python's memory allocator.
        - Frequent deallocation of temporary lists.
        - Higher GC (garbage collection) activity.
        - CPU cycles wasted managing reference counts.

        This allocation churn often dominates wall-clock time more than the
        theoretical complexity suggests.


        3) POINTER CHASING & POOR DATA LOCALITY
        -----------------------------------------
        'strs' is a list of object references (pointers).
        Each access to 'strs[j]' requires:

            Load pointer from list
            Dereference pointer to string object
            Access string internals

        The string objects themselves are not guaranteed to be contiguous in memory.
        This creates pointer chasing behavior.

        Effects:
        - Increased L1/L2 cache misses
        - Pipeline stalls waiting on memory
        - Poor spatial locality

        Quadratic scanning worsens this because the same memory regions are
        revisited non-sequentially.


        4) BRANCH MIS-PREDICTION COST
        ------------------------------
        The inner loop contains multiple conditional branches:

            if grouped[j] == 1: continue
            if sorted(strs[i]) == sorted(strs[j]):

        Branch predictors perform best with stable patterns.
        In this algorithm:

        - grouped[j] distribution is input dependent.
        - Anagram matches are irregular and unpredictable.
        - Sorting itself contains multiple comparison branches.

        This results in:
        - Frequent branch mispredictions
        - Pipeline flushes
        - Lost speculative execution work

        Sorting particularly amplifies this cost.


        5) CONTROL FLOW OVERHEAD REMAINS QUADRATIC
        --------------------------------------------
        Even if character comparisons were free,
        the nested iteration alone performs roughly:

            N*(N-1)/2 loop iterations

        Each iteration incurs:
        - Index arithmetic
        - Bounds checks
        - Branch evaluation
        - Python bytecode dispatch

        In CPython, every loop iteration executes multiple bytecode instructions.
        The interpreter dispatch overhead compounds quadratically.


        6) INTERPRETER DISPATCH COST (CPython SPECIFIC)
        ------------------------------------------------
        This implementation runs entirely in Python bytecode.

        For every loop iteration:
        - Python evaluates bytecode instructions.
        - Reference counts are updated.
        - Dynamic type checks are performed.

        Unlike a compiled language, this overhead is non-trivial.
        Thus the quadratic structure multiplies interpreter overhead,
        not just algorithmic operations.


        7) INEFFICIENT EQUIVALENCE CLASS CONSTRUCTION
        ----------------------------------------------
        The 'grouped' bitmask prevents duplicate groups,
        but it does not reduce the comparison search space sufficiently.

        Worst case (no anagrams):
        - Every pair is still examined.
        - grouped[j] check becomes mostly false.
        - Control flow cost remains near maximal.

        Thus, although logically correct, the partitioning mechanism
        does not structurally reduce computational work.


        ------------------------------------------------
        SUMMARY OF REAL-WORLD BOTTLENECKS:

        The slowdown is not caused by a single factor,
        but by the multiplicative interaction of:

            - Quadratic iteration space
            - Repeated O(K log K) sorting
            - Heavy heap allocations
            - Poor cache locality (pointer chasing)
            - Branch misprediction penalties
            - CPython interpreter overhead

        Together, these effects make the implementation
        dramatically slower in practice than the asymptotic
        notation alone suggests.
        """

        n = len(strs)
        sol = []
        grouped = [0]*n #Acts as our grouping tracker

        for i in range(0, n):
            if grouped[i] == 1 : continue #If already grouped, skip
            grouped[i] = 1
            group = [strs[i]]
            for j in range(i+1, n):
                if grouped[j] == 1 : continue #If already grouped, skip
                if sorted(strs[i]) == sorted(strs[j]):
                    group.append(strs[j])
                    grouped[j] = 1
            sol.append(group)
        return sol

    def bruteforce2(self, strs: List[str]) -> List[List[str]]:
        '''
        In bruteforce 1 , for a given i we are repeatedly checking the 
        sorted(i) ... This is totally unnecessary , instead calculate once
        and keep it stored.

        The time and space complexities remain the same as above
        TC : O(N² * K log K)
        SC : O(N * K)
        '''
        n = len(strs)
        sol = []
        grouped = [0]*n

        for i in range(0, n):
            if grouped[i] == 1 : continue #Skip already grouped strings
            grouped[i] = 1
            x = sorted(strs[i])  #Our slight optimization
            group = [strs[i]]
            for j in range(i+1, n):
                if grouped[j] == 1 : continue #Skip already grouped strings
                if sorted(strs[j]) == x:
                    group.append(strs[j])
                    grouped[j] = 1
            sol.append(group)
        
        return sol
    
    def bruteforce3(self, strs: List[str]) -> List[List[str]]:
        '''
        In the previous approach , we realized that we are repeatedly
        sorting the 'i' string for every possible 'j'

        Similarly we are also re sorting the j string for every possible i
        So , we can create a auxilary array that holds the sorted versions 
        of each string.

        TC : O((N² * K) + (N * K log K)) ==> O(N² * K)
        SC : O(N * K + N) ==> O(N * K) 
        '''

        sorted_strs = [sorted(i) for i in strs]

        n = len(strs)
        sol = []
        grouped = [0] * n

        for i in range(0, n):
            if grouped[i] == 1 : continue
            grouped[i] = 1
            group = [strs[i]]
            sorted_i = sorted_strs[i] #Assigning to local variable to avoid repeated array fetches
            for j in range(i+1, n):
                if grouped[j] == 1: continue
                if sorted_i == sorted_strs[j] :
                    group.append(strs[j])
                    grouped[j] = 1
            sol.append(group)

        return sol
    
    def freq_maps(self, strs: List[str]) -> List[List[str]]:
        '''
        For two strings to be anagrams , we know that their character frequency maps
        need to be same.

        Since the input constraints specify that all characters will be 
        lower case english alphabets, we can simply create freq maps of size 26 
        for each string in the input array ..
        
        This will bring down our pre-computation time complexity from
        O(n * k log k) to O(n * k)

        The space complexity will also go down because now we are creating
        constant sized freq maps instead of storing sorted strings of same size,
        the SC goes down from O(n * k) to O(n * 26) ==> O(n)
        '''

        freq_mappings = []
        for s in strs:
            x = [0] * 26
            for c in s:
                x[ord(c) - ord('a')] += 1
            freq_mappings.append(x)


        n = len(strs)
        sol = []
        grouped = [0] * n

        for i in range(0, n):
            if grouped[i] == 1 : continue
            grouped[i] = 1
            group = [strs[i]]
            freq_map_i = freq_mappings[i] #Assigning to local variable to avoid repeated array fetches
            for j in range(i+1, n):
                if grouped[j] == 1: continue
                if freq_map_i == freq_mappings[j] :
                    group.append(strs[j])
                    grouped[j] = 1
            sol.append(group)

        return sol

    def optimal(self, strs: List[str]) -> List[List[str]]:
        '''
        We were successful in bringing down the time complexity of the 
        precomputation , but the bottleneck still remains the 
        quadratic grouping. Can we somehow get this down ??

        The issue right now is for each 'i' , we are doing forward lookups,
        instead can we group them together in a linear scan 
        (think grouping using hashmaps) ? If hashmaps , what can we use as
        the key ?

        The frequency maps of the strings will be the canonical form , so we 
        can use them as the keys for hashmap. 

        So basically we are constructing a hashmap using the canonical 
        versions of each string (freq map) as the key. Then the 
        precomputation is O(n * k), and grouping becomes 
        O(n * 1) ==> O(n). Then to return the solution ,we need to loop
        over the hashmap and construct lists out of it.. This will again 
        be a O(n) operation since every string in input array will go inside
         the hashmap. Therefore , 
         
        TC = O((n * k) + (n * 1) + n) ==> O(n * k)
        SC = O(n * 28  +  n * k ) ==> O(n * k + n) ==> O(n * k)
        '''

        #Loop over input strings, calculate freq maps and use 
        # them as keys for the hashmap.
        hm = defaultdict(list)

        base = ord('a')  #Minor optimization to remove repetative calls to ord
        for s in strs:
            freq = [0] * 26
            for c in s:
                freq[ord(c) - base] += 1

            key = tuple(freq) # Use the freq_map as the key.
                            # Since lists in python are mutable,
                            # they cannot be used as keys for a dict
                            # So , we cast to immutable tuple
            
            hm[key].append(s)

        # Now construct the final output lists
        return [i for i in hm.values()]

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # return self.bruteforce1(strs)
        # return self.bruteforce2(strs)
        # return self.bruteforce3(strs)
        # return self.freq_maps(strs)
        return self.optimal(strs)
