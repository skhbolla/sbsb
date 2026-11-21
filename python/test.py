# def runner(a):
#     a("srikanth")
#
# runner(lambda x: print(x))

# x  = 3
# for i in range(0,5):
#     print(i)
#     if i == x:
#         break
#
# try:
#     print(5/0)
# except:
#     print("Divsion by 0 encountered")
# finally:
#     print("finally")
#
# print("Test")

# class Rectangle:
#     height = 10
#     width = 10
#
#     def dimensions(self):
#         print(self.height, self.width)
#
# r = Rectangle()
# r.dimensions()
#
# Rectangle.dimensions(r)
#
# print(dir(Rectangle))
#
# print(dir(object))
# print(object.__mro__)
#
# print(Rectangle.__mro__)
#
# class Shape:
#     def details(self):
#         print("Hi , I am a shape")
#
# class Rectangle(Shape):
#     def details(self):
#         print("Hi , I am a Rectangle")
#
# r = Rectangle()
# print(Rectangle.__mro__)

# class Test:
#     def __init__(self, a):
#         self.a = a
#
#     def change_a(self, a):
#         self.a = a
#
# t = Test(1)
# print(t.a)
# print(id(t))
# print(id(t.a))
# t.change_a(2)
# print(t.a)
# print(id(t))
# print(id(t.a))
#

# import sys
# a = 31234575
# b = 4
# print(sys.getrefcount(a))
# t = (a,b)
# print(sys.getrefcount(a))
# print(t)
# print(id(t))
# a= 5
# print(sys.getrefcount(t[0]))
# print(t)
# print(id(t))


def func(x):
    '''
    Test doc
    '''
    print("Hello" , x)
    print(locals())

print(type(func).__mro__)


class Test:
    def test():
        print("hello")

t = Test()

print(type(type(t)).__mro__)
