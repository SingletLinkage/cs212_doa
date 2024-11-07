string_x = 'aggtab'
string_y = 'gxtxayb'
x = len(string_x)
y = len(string_y)

dp = [[-1] * (y + 1) for _ in range(x + 1)]
letters = [[''] * (y + 1) for _ in range(x + 1)]

# for i in range(1, x + 1):
#     for j in range(1, y + 1):
#         if string_x[i - 1] == string_y[j - 1]:
#             dp[i][j] = 1 + dp[i - 1][j - 1]
#             letters[i][j] = letters[i - 1][j - 1] + string_x[i - 1]
#         else:
#             dp[i][j], letters[i][j] = max((dp[i][j-1], letters[i][j-1]), (dp[i-1][j], letters[i-1][j]))

# print("\nLongest Common Subsequence:", letters[x][y], "\nLength: ", dp[x][y])

def lcs(s1, s2, i, j, memo):
    global ans
    if i==0 or j==0:
        return 0
    
    if memo[i][j] != -1:
        return memo[i][j]

    if s1[i-1] == s2[j-1]:
        memo[i][j] = lcs(s1, s2, i-1, j-1, memo)
        return memo[i][j]
    else:
        memo[i][j] = max(lcs(s1, s2, i-1, j, memo), lcs(s1, s2, i, j-1, memo))
        return memo[i][j]

print(lcs(string_x, string_y, x, y, dp))
