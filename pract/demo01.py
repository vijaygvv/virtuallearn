# print("-------12345-------")



# op = [i for i in range(1, 101)]
# print(op)

# #or

# print([i for i in range(1, 101)])











# def my_generator(n):
#     value = 0
#     while value < n:
#         yield value
#         value += 1

# for value in my_generator(1000):
#     print(value)







# a = "gggrraaagggg"
# op = ""
# cnt = 0

# temp_var = a[0]
# for i in a:
#     if i == temp_var:
#         cnt +=1
#     else:
#         op += str(cnt)+temp_var
#         temp_var = i
#         cnt = 1
# op += str(cnt)+temp_var

# print(op)







# cnt = 0
# temp_var = ""

# for j in range(len(a),-1):
#     if a[a] == a[j+1]:
#         cnt += 1
#         temp_var = 



# 28-0-0-8=20***170/170
# 30-0-0-8=22***185/187
# 31-0-0-10=21***175/179
# 30-0-0-8=22***183/187
# 31-1-0-9=21***166/187
# 31-(2+3)-9=17***170/187
# 28-0-0-8=20***170/170
# 31-0-1-8=22***167/187

i = [170,185,175,183,166,170,170,167]
j = [ 170,187,179,187,187,187,170,187 ]

print(sum(i)/sum(j))


