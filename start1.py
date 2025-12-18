# import datetime


# def calc(x):                                                                 ## Age calculator
#     hozirgi_yil = datetime.datetime.now().year
#     if type(x) is not int:
#         return "Please enter data not string"
#     else:
#         calced = hozirgi_yil-x
#         print(f"You're, {calced}")
    
# calc(2006)

    
    
    
# def someword(n)                                                              ## Prints first letter
#     if type(n) != str:
#         print("Only string required")
            
#     else:
#         print(n[0])
# someword("Python")




# def reverse_word(s):                                                         ## Reverses the given word
#     if type(s) is not str:
#         print("Only string is acceptable!")
#     else:
#         print(s[::-2])
# reverse_word("Python")




# def first_test(d):                                                           ## Print only "Python"
#     if type(d) is not str:
#         print("I can't see any string")
#     else:
#         print(d[7:14])
# first_test("I love Python Programming")




# kocha = "Bog'bon"                                                            ## Custom
# mahalla = "Sog'bon"
# tuman = "Bodomzor"
# viloyat = "Samarqand"
# print(kocha + " ko'chasi, \n"  + mahalla +
#       " mahallasi, \n" + tuman + " tumani, \n" + viloyat + "viloyati")




# kocha = str(input("Ko'changiz nomini kiriting-> "))                          ## Custom
# mahalla = str(input("Mahallangiz nomini kiriting-> "))
# tuman = str(input("Tumaningiz nomini kiriting-> "))
# viloyat = str(input("Viloyatingiz nomini kiriting-> "))
# print("\n")
# print("Siz ")
# print(kocha + " ko'chasi, \n"  + mahalla +
#       " mahallasi, \n" + tuman + " tumani, \n" + viloyat
#       + " viloyatida yashar ekansiz!")




# kocha = str(input("Ko'changiz nomini kiriting-> "))                          ## Custom # Method using
# mahalla = str(input("Mahallangiz nomini kiriting-> "))
# tuman = str(input("Tumaningiz nomini kiriting-> "))
# viloyat = str(input("Viloyatingiz nomini kiriting-> "))
# Manzil = f"{kocha}  ko'chasi,\n{mahalla} mahallasi,\n{tuman} tumani,\n{viloyat} viloyati"
# print(Manzil.upper())




# ismlar = []                                                                  ## Custom
# ismlar.append("Abror")
# ismlar.append("Najmiddin")
# ismlar.append("Sohib")
# print(ismlar)
# print(f"{ismlar[0]}, bugun choyxona bormi?")
# print(f"{ismlar[1]}, bugun choyxona bor ekan.")
# print(f"{ismlar[2]}, bugun choyxonaga kelgin!")




# def calc(a, b):
#     return (a + b)
# calc(10, 5)




# def ismlarimiz(ismlar):
#     print(ismlar)
# ismlarimiz("Abdusamad")
# ismlarimiz()




# def whosbetter(a, b):
#     if a > b:
#         print("A is better!")
#     elif a < b:
#         print("B is better!")
#     else:
#         print("They are equal or no number provided!")
# whosbetter(5, 6)
    
    
    

# def vowelsep(word):
#     vowels = "AaOoUuIiEe"
#     vowel_list = []
#     if not isinstance(word, str):
#         print("No numbers!!!")
#     else:
#         for i in word:
#             if i in vowels:
#                 vowel_list.append(i)
#         print(vowel_list)
# vowelsep("PythonProgramming")
# vowelsep(122)




# total_balance = 0

# def deposit(a):
#     global total_balance
#     if not isinstance(a, str):
#         total_balance += a
#     else:
#         print("Only numbers allowed!")
# def withdraw(b):
#     global total_balance
#     if not isinstance(b, str):
#         total_balance -= b
#     else:
#         print("Only numbers allowed!")
# def show_balance():
#     print(total_balance)
    
# deposit(1000)
# withdraw(500)
# show_balance()




# class Solution:                                                              ## LeetCode 1 Sol
#     def twoSum(self, nums: List[int], target: int) -> List[int]:
#         for h in range(len(nums)):
#             for l in range(h + 1, len(nums)):
#                 if nums[h] + nums[l] == target:
#                     return [h, l]




# class Solution:
    # def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    #     total1 = 0
    #     total2 = 0
    #     p1, p2 = l1, l2                                                      ## LeetCode 2 Sol
    #     multiplier = 1
    #     while p1 or p2:
    #         val1 = p1.val if p1 else 0
    #         val2 = p2.val if p2 else 0
    #         total1 += val1 * multiplier
    #         total2 += val2 * multiplier
    #         multiplier *= 10
    #         if p1:
    #             p1 = p1.next
    #         if p2:
    #             p2 = p2.next
    #     total_sum = total1 + total2
    #     dummy = ListNode(0)
    #     current = dummy
    #     if total_sum == 0:
    #         return ListNode(0)
    #     while total_sum > 0:
    #         digit = total_sum % 10
    #         current.next = ListNode(digit)
    #         current = current.next
    #         total_sum //= 10
    #     return dummy.next




# counts = {}                                                                  ## LeetCode 169 Sol
# nums_lenght = len(nums)
# half_nums_length = nums_lenght // 2

# for item in nums:
#     if item in counts:
#         counts[item] += 1
#     else:
#         counts[item] = 1
# for result_item in counts:
#     if counts[result_item] > half_nums_length:
#         return result_item



# def Solution(nums, target):                                                  ## LeetCode 35 Sol

#     for i in range(len(nums)):
#         if nums[i] <= target:
#             print(i)
#             break
# Solution(nums = [1, 4, 5, 7, 8] , target = 9)




# def removeDuplicates(nums):                                                  ## LeetCode 26 Sol
#     i = 0
#     for j in range(1, len(nums)):
#         if nums[j] != nums[i]:
#             i += 1
#             nums[i] = nums[j]
#     return i + 1
        
# nums = [0,0,1,1,2,2,2,3,4,4]
# print(removeDuplicates(nums))
# print(nums)




# class Solution:
#     def moveZeroes(self, nums: List[int]) -> None:                           ## LeetCode 283 Sol
#         zero_count = 0
#         for i in nums:
#             if i == 0:
#                 zero_count += 1
            
#         while 0 in nums:
#             nums.remove(0)
            
#         for _ in range(zero_count):
#             nums.append(0)
#         return nums




# def solution(x):                                                             ## LeetCode 9 Sol
#     str_ver = str(x)
#     if str_ver == str_ver[::-1]:
#         return True
#     else:
#         return False
# print(solution(17671))




# def Solution(nums):                                                          ## LeetCode 136 Sol
#     x = 0
#     for num in nums:
#         x = x ^ num
#     print(x)
# Solution([1,2,1,3,2])




# class Solution:                                                              ## LeetCode 1929 Sol
#     def getConcatenation(self, nums: List[int]) -> List[int]:
#         ans = []
#         for smth in nums:
#             ans.append(smth)
#         ans += nums
#         return ans




# def Solution(word1, word2):                                                  ## LeetCode 1768 Sol
#     merged_one = ""
#     for k in range(max(len(word1), len(word2))):
#         if k < len(word1):
#             merged_one += word1[k]
#         if k < len(word2):
#             merged_one += word2[k]
#     print(merged_one)
# Solution("13579", "2468")




# class Solution:
#     def containsDuplicate(self, nums: List[int]) -> bool:                    ## LeetCode 217 Sol
#         seen_number = set()
#         for xD in nums:
#             if xD in seen_number:
#                 return True
#             seen_number.add(xD)
#         return False




# class Solution:                                                              ## LeetCode 242 Sol
#     def isAnagram(self, s: str, t: str) -> bool:
#         if sorted(s) == sorted(t):
#             return True
#         else:
#             return False




# class Solution:                                                              ## LeetCode 49 Sol
#     def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
#         output = {}
#         for word in strs:
#             that_key = ''.join(sorted(word))
#             if that_key not in output:
#                 output[that_key] = []
#             output[that_key].append(word)
#         output2 = list(output.values())
#         return output2




# def topKFrequent(nums, k):                                                   ## LeetCode 347 Sol
#     freq_nums = {}
#     for num in nums:
#         if num in freq_nums:
#             freq_nums[num] += 1
#         else:
#             freq_nums[num] = 1
#     sorted_nums = sorted(freq_nums.items(), key=lambda x: x[1], reverse=True)
#     final = [key for key, value in sorted_nums[:k]]
#     print(final)
    
# topKFrequent([5,5,5,8,8,8,8,5,2,2,2,3,3], 2)




# class Solution:                                                              ## LeetCode 344 Sol
#     def reverseString(self, s: List[str]) -> None:
#         left, right = 0, len(s) - 1
#         while left < right:
#             s[left], s[right] = s[right], s[left]
#             left += 1
#             right -= 1




# juft_sonlar = 0
# some_array = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# i = 0
# while i < len(some_array):
#     if some_array[i] % 2 == 0:
#         juft_sonlar += 1
#     i += 1

# print(juft_sonlar)




# some_array = [2, 1, 3, 4, 5, 6, 7, 8, 9]
# element = 0
# biggest_one = some_array[0]

# while element < len(some_array):
#     if some_array[element] > biggest_one:
#         biggest_one = some_array[element]
#     else:
#         element += 1
# print(biggest_one)




# class Solution:                                                              ## LeetCode Sol 167
#     def twoSum(self, numbers: List[int], target: int) -> List[int]:
#         right = 0
#         left = len(numbers) -1
#         while right <= left:
#             s = numbers[right] + numbers[left]
            
#             if s == target:
#                 return [right + 1, left + 1]
#             elif s < target:
#                 right += 1
#             else:
#                 left -= 1




# class Solution:                                                              ## LeetCode Sol 412
#     def fizzBuzz(self, n: int) -> List[str]:
#         answer = []
#         for i in range(1, n+1):
#             if i % 3 == 0 and i % 5 == 0:
#                 answer.append("FizzBuzz")
#             elif i % 3 == 0:
#                 answer.append("Fizz")
#             elif i % 5 == 0:
#                 answer.append("Buzz")
#             else:
#                 answer.append(str(i))
#         return answer




# from collections import Counter, defaultdict

# def frequencySort(s):
#     count = Counter(s)
#     buckets = defaultdict(list)
    
#     for char, cnt in count.items():
#         buckets[cnt].append(char)
         
#     final = ""
    
#     for i in range(len(s), 0, -1):
#         for c in buckets[i]:
#             final += c * i
#     print(final)
    
# frequencySort("tree")




# def smth(a, b):
#     try:
#         x = a / b
#         return x 
    
#     except ZeroDivisionError:
#         return ("Cannot devide by 0!")
#     except TypeError:
#         return ("Type is incorrect!")
    
# smth(7, 0)


# def somedef(fruits, indecies):
#     try:
#         print(fruits[indecies])
#     except IndexError:
#         print("No such index!")
#     except TypeError:
#         print("Type error raised hand!")
    
    
    
# somedef(['apple', 'lemon', 'melon', 'avacado'], 9)




















































































































































































    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    










