# EX_1

# x = int(input("x: "))
# y = float(input("y: "))
# z = float(input("z: "))


# EX_2
# F(m,n) = n!*m!/(n+m)!
#
# m = int(input("sir pls enter m: "))
# n = int(input("sir pls enter n: "))
#
# def fac(k):
#     if k == 0:
#         return 1
#     return fac(k-1) * k
#
# if m > 0 and n > 0:
#     def function(m, n):
#         F = (fac(n)*fac(m))/fac(n+m)
#         return F
#     print(str("F(m,n) = ") + str(function(m,n)))

# EX_3
#
# import random
#
# def Perestanovka(x,y):
#     for i in range(len(x)):
#         k = random.choice(x)
#         y = y + k
#     return(y)
#
# for i in range(4):
#     x = str(input("sir pls enter word - x: "))
#     y = ""
#     y = Perestanovka(x,y)
#     if x == y:
#         print(str("word - y: ") + x)
#     else:
#         print("слів не утворено за умовою")

# EX_5
# def swap (arr, i, j):
#     arr [i], arr [j] = arr [j], arr [i]
#
# def bubble_sort (arr):
#     i = len (arr)
#     while i> 1:
#         for j in range (i - 1):
#             if arr [j] < arr [j + 1]:
#                 swap (arr, j, j + 1)
#         i -= 1
#     return arr
#
# arr_1 = [1, 2, 43, 8, 3, 7]
# arr_2 = [1, 0, 9, 5, 3, 8, 4, 6, 2]
#
# print(bubble_sort(arr_1))
# print(bubble_sort(arr_2))

