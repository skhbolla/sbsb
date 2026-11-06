class BruteForce:

    def __init__(self):
        self.data = []

    def push(self, val: int) -> None:
        self.data.append(val)

    def pop(self) -> None:
        self.data.pop()

    def top(self) -> int:
        return self.data[-1]

    def getMin(self) -> int:
        return min(self.data)

class TwoStacks:

    def __init__(self):
        self.valstack = []
        self.minstack = []

    def push(self, val: int) -> None:
        if not self.valstack:
            self.valstack.append(val)
            self.minstack.append(val)
        else:
            self.valstack.append(val)
            self.minstack.append(min(val, self.minstack[-1]))
            # replacing the min() method with a simple
            # if val < m: m = val 
            # would be faster at the bytecode level. 
            #But I deliberately use min() to keep code readable.

    def pop(self) -> None:
        self.valstack.pop()
        self.minstack.pop()

    def top(self) -> int:
        return self.valstack[-1]

    def getMin(self) -> int:
        return self.minstack[-1]

class OneStackTuple:

    def __init__(self):
        self.stack = []

    def push(self, val: int) -> None:
        if not self.stack:
            self.stack.append((val, val))
        else:
            m = min(val, self.stack[-1][1])
            self.stack.append((val,m))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]


class OneStackEncoding:
    def __init__(self):
        self.stack = []
        self.min_val = None

    def push(self, val: int) -> None:
        if not self.stack:
            self.stack.append(val)
            self.min_val = val
        else:
            if val < self.min_val:
                # Encode the previous min into the stack
                # The pushed value will be smaller than the new min_val
                self.stack.append(2 * val - self.min_val)
                self.min_val = val
            else:
                self.stack.append(val)

    def pop(self) -> None:
        if not self.stack:
            return
        
        top = self.stack.pop()
        
        # If the popped value is less than min_val, it's a marker
        # We must restore the previous minimum
        if top < self.min_val:
            self.min_val = 2 * self.min_val - top
        
        if not self.stack:
            self.min_val = None

    def top(self) -> int:
        top = self.stack[-1]
        # If the value in the stack is a marker (smaller than min_val),
        # it means the current min_val IS the actual top value.
        return self.min_val if top < self.min_val else top

    def getMin(self) -> int:
        return self.min_val




# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()