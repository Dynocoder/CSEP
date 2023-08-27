import re

arrStr = "['10.0', '200.00', '7.0', '400.00']"

print(arrStr)
a = re.findall("\d+.{0,1}\d+", arrStr)
print("list", a)
for i in range(0, len(a)):
    a[i] = float(a[i])

print(a)
for i in a:
    print(type(i))