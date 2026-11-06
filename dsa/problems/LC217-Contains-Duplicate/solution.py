class Solution:

    def sorting_approach(self, nums: List[int]) -> bool:
        '''
        Choose a in-place sorting algo with best possible time complexity..

        Time complexity - O(n logn) because python sorted() uses timsort
        Space complexity - O(1)
        '''
        nums.sort() #In place sort

        for i in range(1,len(nums)):
            if nums[i] == nums[i-1]:
                return True
        return False
    
    def hashtable_approach(self, nums: List[int]) -> bool:
        '''
        The problem is essentially asking us to keep track of occurances of element.
        If any element occurs more than once, return True

        Hash Tables are a great way to keep track of occurances because of 
        average O(1) time lookups and inserts..

        Minor optimization we made here:
        We dont need to wait until the end of list ,
        if we ever find a duplicate , terminate immeditely and return True

        Time complexity - O(n)
        Space complexity - O(n)
        '''
        ht = {} #Dictionaries in python are implemented as hash tables
        for i in nums:
            if i in ht:
                return True
            else:
                ht[i] = 1
        return False

    def set_approach(self, nums: List[int]) -> bool:
        """
        We use a `set` instead of a `dict` (hashmap) because we only need
        membership testing, not key → value associations.

        Internally, both `set` and `dict` in CPython are implemented as
        open-addressing hash tables with perturbation-based probing and
        power-of-two resizing. Therefore, the asymptotic complexity is identical:

            Time Complexity:  O(n) average
            Space Complexity: O(n)

        However, their entry layouts differ:

            dict entry:
                - cached hash
                - pointer to key
                - pointer to value

            set entry:
                - cached hash
                - pointer to key

        Because a set entry is smaller:
            1) More entries fit into the same cache line (better cache locality).
            2) Fewer memory loads are required during probing.
            3) No value pointer dereference is needed.

        In open-addressed hash tables, lookup performance is heavily influenced
        by memory access patterns rather than pure algorithmic steps. Since `set`
        has a denser memory layout, probing typically results in fewer cache misses
        and less pointer chasing.

        Thus, while Big-O time complexity remains O(n), real-world performance
        is slightly better for `set` due to improved cache behavior and reduced
        per-entry memory overhead.

        In short:
        Same asymptotic complexity, but better constant factors and memory-level
        efficiency make `set` the more appropriate and faster choice when only
        existence tracking is required.
        """

        seen = set()

        for n in nums:
            if n in seen:
                return True
            else:
                seen.add(n)
        return False

    def containsDuplicate(self, nums: List[int]) -> bool:
        # return self.sorting_approach(nums)
        # return self.hashtable_approach(nums)
        return self.set_approach(nums)
