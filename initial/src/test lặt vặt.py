
# Merge sort
def merge_sort(a):
    mid = len(a)//2
    if mid == 0:
        return a
    a1 = a[:mid]
    a2 = a[mid:]
    a1 = merge_sort(a1)
    a2 = merge_sort(a2)
    return merge_2_sorted_list(a1, a2)

def merge_2_sorted_list(a,b):
    ret=[]
    while len(a)!=0 or len(b)!=0:
        if len(a)!=0 and len(b)!=0:
            if a[0]<b[0]:
                ret.append(a.pop(0))
            else:
                ret.append(b.pop(0))
        elif len(a)!=0:
            ret.append(a.pop(0))
        else:
            ret.append(b.pop(0))
    return ret

merge_2_sorted_list([1,3,5],[2,4,6])
merge_sort([5,3,1,6,4,2])

# Quick sort
def quick_sort(a):
    if len(a)<=1:
        return a
    pivot = a.pop()
    g = []
    l = []
    for item in a:
        if item >pivot:
            g.append(item)
        else:
            l.append(item)
    g = quick_sort(g)
    l = quick_sort(l)
    return l + [pivot] + g

quick_sort([5,3,1,6,4,2])

#

from math import *
def countingStar(matrix):
    n = len(matrix)
    m = len(matrix[0])
    count = 0
    bo = False
    for i in range(n):
        for j in range(m):
            if matrix[i][j]==0:
                bo = re(i,j,matrix,bo)
            if bo:
                count+=1
                bo = False
    return count

def re(a,b,matrix,bo):
    n = len(matrix)
    m = len(matrix[0])
    if matrix[a][b]==0:
        matrix[a][b] = -1
        bo = True
    for i in range(n):
        for j in range(m):
            if ((abs(a-i)==1 and b==j) or (abs(b-j)==1 and a==i)) and matrix[i][j]==0:
                bo = re(i,j,matrix,bo)
    return bo

countingStar([[0], [1]])

def  longestSubStringWithoutDuplicates(string):
    string = list(string)
    subString = []
    maxLength = 0
    while len(string) > 0:
        if string[0] in subString:
            index = subString.index(string[0])
            subString = subString[index + 1:]
        subString.append(string.pop(0))
        maxLength = maxLength if maxLength > len(subString) else len(subString)
    return maxLength

print(longestSubStringWithoutDuplicates('aabbccddeee'))
