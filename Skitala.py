text = "GRIREAAEEALRALSNNLLITFT EWAVHPT"

curr= 0
step = 8
for x in range(len(text)):
    print(text[curr])
    curr = (curr + step )% len(text)