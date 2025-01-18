# import matplotlib.pyplot as plt # type: ignore
# import numpy as np # type: ignore
# file = open("file.txt", 'w')
# data = input("Enter a sentence : ")
# file.write(data)
# file.close()
# file = open("file.txt", 'r')
# text = file.readline()
# file.close()
# text = text.lower()
# textDict = {}
# wordFrequency={}
# for txt in text:    
#     if txt == ' ':
#         continue
#     if txt in textDict.keys():
#         textDict[txt]+=1
#     else:
#         textDict[txt]=1
# wordFrequency = dict(
#     sorted(
#         textDict.items(),
#         key=lambda x: x[1],
#         reverse=True)
#     )
# rank = []
# frequency = []
# init = 0

# for freq in wordFrequency.values():
#     init+=1
#     rank.append(init)
#     frequency.append(freq)
# i = 0
# print("231030228")
# for word in wordFrequency:
#     print(f'{word} -> f = {frequency[i]} , r = {rank[i]}')
#     i += 1
# slope, intercept = np.polyfit(np.log(rank), np.log(frequency), 1)
# print("slope : " , slope)
# print("intercept : ", intercept)
# plt.loglog(rank,frequency)
# plt.xlabel('log(r)')
# plt.ylabel('log(f)')
# plt.title("Zipf's law 231030228")
# plt.show()


import inspect
def print_function_docs(func):
    print("abs(number)->number")
    print(func.__doc__)

# Sample function: abs
print("231030228")
print_function_docs(abs)

