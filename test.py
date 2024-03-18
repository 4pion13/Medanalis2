list = ['', 1, 2, 3]
print(list[0])
for item in range(len(list)):
    if list[item] == "":
        list[item] = 0


print(list)