n = 8
prices = [1, 5, 8, 9, 10, 17, 17, 20]

best = [0]*(n+1)
cuts = [0]*(n+1)

for j in range(1, n+1):
    temp = [prices[i-1] + best[j-i] for i in range(1, j+1)]
    best[j] = max(temp)
    cuts[j] = temp.index(best[j])+1

# print(best[1:], cuts[1:])
temp = n
ans = []
while temp > 0:
    ans.append(cuts[temp])
    temp = temp - cuts[temp]

print(ans, sum(ans))
