class Solution:
    def bruteforce(self, nums: List[int], k: int) -> List[int]:
        '''
        The most intuitive way to do this is by counting the frequencies
        of each item in array using a hashmap, then sorting the hashmap
        by converting to an array of (item, count) pairs and using count 
        for sorting. 

        T.C => Construct hash table O(N) 
             + Convert to list O(M)
             + sort list O(M log M)
             + Extract top K elements O(k)
            
            where M is the number of unique elements.
            ==> O(N + M + M log M + K) 
            ==> O(N + M log M)

        In a truly randomized distribution where M scales with N, 
        this simplifies to O(N log N).

        S.C => Storing the hash table O(M)
             + Storing the list O(M)
             + sorting the list creates new list O(M)
             + List slicing produces new list O(K)
            
            where M is the number of unique elements.
            ==> O(M + M + M + K)
            ==> O(M + K)
        Again , in a truly randomized distribution where M scales with N, 
        this simplifies to O(N + K).
        '''
        
        # Construct the hash table to count frequencies.
        hm = {}
        for i in nums:
            if i in hm:
                hm[i] += 1
            else:
                hm[i] = 1

        # Convert the hash table to a list of (item, count) pairs
        l = list(hm.items())

        # Sort the list based on the count field
        l = sorted(l, key = lambda x : x[1], reverse=True)

        print(l)

        # Select the first k items and return
        return [i[0] for i in l[0:k]]

    def bucketsort(self, nums: List[int], k: int) -> List[int]:
        '''
        For an input array of size 'N' , the highest possible frequency
        possible is 'N' (when all elements are same).

        So , we can create a auxilary array of size 'N' , 
        where the indices act as buckets of frequency..

        i.e any elements in input array with frequency 1 go into index 1
        frequency 2 go into 1 etc..

        After we are done putting every element into buckets,
        read the array in reverse and print top k freq elements

        T.C ==> Creating hashmap O(N)
                + Flattening hashmap into bucket array O(M)
                + Returning solution by traversing buckets O(K)
            ==> O(N + M + K)
            In a truly randomized distribution where M scales with N, 
        this simplifies to O(N).

        S.C ==> Hashmap O(N)
                + Flat buckets O(N)
                + solution array O(K)
            ==> O(N + N + K)
            ==> O(N + K)
        '''
        buckets = [None] * (len(nums) + 1) 
                    # easier to do len+1 than handle 0 based indexing

        # Use a hashmap to calculate frequncies in O(N)
        hm = {}
        for num in nums:
            hm[num] = 1 + hm.get(num, 0)

        # Take the hashmap and flatten it into our buckets
        for num, count in hm.items():
            if buckets[count] == None:
                buckets[count] = [num]
            else:
                buckets[count].append(num)
        
        # Read the buckets from highest to lowest index and return k elements
        sol = []
        for i in range(len(buckets)-1, 0, -1):
            if buckets[i]: #Make sure not a None element before trying to loop
                for j in buckets[i]:
                    sol.append(j)
                    if(len(sol) == k):
                        return sol #The question guarentees that a solution exists, 
                                # so we can safely have a return in this block


    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # return self.bruteforce(nums, k)
        return self.bucketsort(nums, k)
