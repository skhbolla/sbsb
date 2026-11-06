class Solution:
    def two_pointer_approach(self, s: str) -> bool:
        '''
        Initialize two pointers , one at each end of the string/array.
        Move them towards each other ignoring non-alphanumeric characters.
        If at any point the two pointer dont point to equal case ignored
        characters , then return False

        T.C => one pass over array O(N)
        S.C => O(1) no auxilary space
        '''

        pl, pr = 0, len(s) - 1

        while(pr > pl):
            #move pl and pr until we encounter a alpha numeric char 
            while(pl < pr and not s[pl].isalnum()):
                 pl += 1
            
            while(pr > pl and not s[pr].isalnum()):
                pr -= 1

            if s[pl].lower() != s[pr].lower():
                return False

            pl += 1
            pr -= 1
            
        return True


    def isPalindrome(self, s: str) -> bool:
        return self.two_pointer_approach(s)
