import sys

class Solution:
    def counterpart(self, x):
        if x == ')' : return '('
        elif x == '}' : return '{'
        elif x == ']' : return '['
        else : sys.exit()

    def bruteforce(self, s: str) -> bool:
        '''
        Keep removing valid pairs from the string until no more pairs left
        If string empty , valid
        otherwise invalid
        '''
        while '()' in s or '[]' in s or '{}' in s:
            s = s.replace('()' , '')
            s = s.replace('[]' , '')
            s = s.replace('{}' , '')
        return s == ''

    def stack_approach(self, s: str) -> bool:
        stack = []

        for i in s:
            if i == '(' or i == '{' or i == '[':
                stack.append(i)
            else:
                if stack == []:
                    return False
                #Function call instead of simple if else 
                #conditions is admittedly worse for performance , 
                #but the code looks cleaner
                cp = self.counterpart(i) 
                popped = stack.pop()
                if cp != popped:
                    return False
        return stack == []

    def pythonic_stack_approach(self, s: str) -> bool:
        # 1. Map closing brackets to their opening counterparts
        # This replaces the 'counterpart()' function call
        mapping = {")": "(", "}": "{", "]": "["}
        stack = []

        for char in s:
            # 2. If char is a key in our map, it's a CLOSING bracket
            if char in mapping:
                # 3. Pop if stack exists, else use a 'dummy' value that won't match
                top_element = stack.pop() if stack else '#'
                
                # 4. Parity check
                if mapping[char] != top_element:
                    return False
            else:
                # 5. It's an opening bracket, push to stack
                stack.append(char)

        # 6. Final check: Is the stack empty?
        return not stack


    def isValid(self, s: str) -> bool:
        # return self.bruteforce(s)
        # return self.stack_approach(s)
        return self.pythonic_stack_approach(s)
