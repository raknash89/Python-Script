# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 18:29:20 2022

@author: gowrishankar.p
"""

import sys
class Solution(object):
    def wordSubsets(self, words1, words2):
        """
        :type words1: List[str]
        :type words2: List[str]
        :rtype: List[str]
        """
        arr = []
        double = False
        double = self.check(words2)
        for i in words1:
            # print('List=',i)
            for j in range(len(words2)):
                # print('Key=',words2[j])
                count = 0
                indicator = False
                match = 0 
                prev = ''
                while count < len(i):
                    if len(i) > count+1:
                        if double != True:
                            if words2[j] == i[count] and words2[j] == i[count+1]:
                                if str(i) not in arr:
                                    # print('test-1',str(i))
                                    arr.append(str(i))
                                break
                            if len(words2) != j+1 :
                                if words2[j] == i[count] and words2[j+1] == i[count+1]:
                                    if str(i) not in arr:
                                        # print('test-2',str(i))
                                        arr.append(str(i))
                                    break
                        if double == True:
                            if words2[j] in i and len(words2[j])>1:
                                if str(i) not in arr:
                                    # print('test-3',str(i))
                                    arr.append(str(i))
                                    indicator = True
                                    # print('INDC=',indicator)
                            if len(words2[j]) > 1 and indicator == False:
                                # match = 0
                                # print('inside')
                                #prev = ''
                                for each in words2[j]:
                                    # print('PREV=',i[count],prev)
                                    if prev != i[count]:
                                        if each in i[count]:
                                            match = match + 1
                                            # print('Match:: ',match)
                                            prev = i[count]
                                            break
                                        if match >= len(words2[j]):
                                            if str(i) not in arr:
                                                # print('test-4',str(i))
                                                arr.append(str(i))
                                prev = i[count]
                                    # if match > 0:
                                        # break
                                        
                    count = count+1
        return(arr)
    
    def check(self,words2):
        for j in words2:
            if len(j) > 1:
                return True
                break
                         
                    



words1 = ["amazon","apple","facebook","google","leetcode"]
words2 = ["lo","eo"]
a = Solution()
res = a.wordSubsets(words1,words2)

print(res)

# Input: words1 = ["amazon","apple","facebook","google","leetcode"], words2 = ["e","o"]
# Output: ["facebook","google","leetcode"]
# Input: words1 = ["amazon","apple","facebook","google","leetcode"], words2 = ["l","e"]
# Output: ["apple","google","leetcode"]
# Input: words1 = ["amazon","apple","facebook","google","leetcode"], words2 = ["lo","eo"]
# Output: ["google","leetcode"]
# words1 =["amazon","apple","facebook","google","leetcode"], words2 = ["ec","oc","ceo"]
# Output: ["facebook","leetcode"]


## Answer :
    
# class Solution:
# def wordSubsets(self, words1: List[str], words2: List[str]) -> List[str]:
    
#     target = {}
#     for targetWord in words2:
#         toAdd = {}
#         for letter in targetWord:
#             if letter not in toAdd:
#                 toAdd[letter] = 1
#             else:
#                 toAdd[letter] += 1
        
#         for letter, occur in toAdd.items():
#             if letter in target:
#                 target[letter] = max(occur, target[letter])
#             else:
#                 target[letter] = occur
    
#     ret = []
#     for a in words1:
#         toInclude = True
#         for key in target:
#             if a.count(key) < target[key]:
#                 toInclude = False
#                 break
#         if toInclude:
#             ret.append(a)
#     return ret