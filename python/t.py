def outer():
    x = 4068

    def inner():
        nonlocal x
        x += 1
        print(f"value of x is: {x}")

    return inner, inner


f1, f2 = outer()

f1()
f2()

# print(outer.__closure__)
# print(f.__closure__)
#
# print(f.__code__)
# print(f.__code__.co_code)
# print(f.__code__.co_freevars)
#
# print(dir(f.__code__))
