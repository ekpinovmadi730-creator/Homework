# print("fdfg")
#2
def change_text(s):
     words=s.split()
     result=[]
     digits="1234567890"
     for w in words:
         has_digit=False
         for ch in w:
             if ch in  digits:
                 has_digit=True
                 break
         if not has_digit and len(w) % 2== 0:
             result.append(w[::-1])
     return " ".join(result)
text ="hello test12 eifhvbfilwvhlriv ervhuirv"
print(change_text(text))
#5
def compress_text(text):
    if text =="":
        return ""
    r=""
    c=1
    for i in range(1, len(text)):
        if text[i].lower()==text[i-1].lower():
            c+= 1
        else:
            if c==1:
                r+= text[i-1]
            else:
                r+=text[i-1]+str(c)
            c=1
    if c==1:
        r+=text[-1]
    else:
        r+=text[-1]+str(c)
    return r
text="aaabbc"
print(compress_text(text))
#9
def alternate_case_blocks(text, n):
    result=""
    for i in range(0, len(text), n):
        block = text[i:i+n]
        if (i // n)%2== 0:
            result += block.upper()
        else:
            result += block.lower()
    return result
print(alternate_case_blocks("helloworld", 2))

# 1
def analyze_text(text):
    text = text.lower()
    clean = ""
    for ch in text:
        if 'a' <= ch <= 'z':
            clean += ch
        else:
            clean += " "
    vowels = "aeiouy"
    count_vowels = 0
    used_vowels = ""
    for v in vowels:
        if v in clean:
            used_vowels += v
            count_vowels += 1
    words=clean.split()
    result_words = ""
    added = []
    for w in words:
        if len(w) >= 5 and w[0] == w[-1]:
            if w not in added:
                added.append(w)
                result_words += w + " "
    return count_vowels, result_words.strip()
text = "level, radar! apple 123456 refer hello"
print(analyze_text(text))
#3
def top_k_words(t, k):
    t = t.lower()
    c =""
    a = "abcdefghijklmnopqrstuvwxyzәіңғүұқөһ "
    for ch in t:
        if ch in a:
            c +=ch
        else:
            c += " "
    words=c.split()
    u=[]
    n=[]
    for word in words:
        if word not in u:
            u.append(word)
            n.append(1)
        else:
            i=u.index(word)
            n[i] += 1
    for i in range(len(u)):
        for j in range(i + 1, len(u)):
            if n[j]>n[i]:
                n[i],n[j]=n[j], n[i]
                u[i], u[j]=u[j],u[i]
            elif n[j]==n[i] and u[j]<u[i]:
                u[i],u[j]= u[j],u[i]
                n[i], n[j] =n[j],n[i]
    if k >len(u):
        k =len(u)
    r=[]
    for i in range(k):
        r.append(u[i])
    return r
text="apple banana apple orange banana apple"
k=2
#4
def change_words(text):
    w=text.split()
    r=[]
    for s in w:
        big= 0
        for ch in s:
            if ch ==ch.upper() and ch !=ch.lower():
                big+= 1
        if big== 1:
            if s[0]!= s[0].upper():
                if s[-1]!= s[-1].upper():
                    r.append(s.lower())
    return " ".join(r)
text = "heLlo HellO hEllo HELLO teSt Әлем кІтап"
print(change_words(text))
#7
def palindrome_words(text):
    clean = ""
    for ch in text.lower():
        if ('a' <= ch <= 'z') or ch == " ":
            clean += ch
        else:
            clean += " "
    words = clean.split()
    pals = []
    for w in words:
        if len(w) >= 3:
            rev = ""
            for i in range(len(w)-1,-1,-1):
                rev +=w[i]
            if w == rev and w not in pals:
                pals.append()
    for i in range(len(pals)):
        for j in range(i + 1, len(pals)):
            if (len(pals[j]) > len(pals[i]) or
                (len(pals[j]) == len(pals[i]) and pals[j] < pals[i])):
                pals[i], pals[j] = pals[j], pals[i]
    return pals
#11
def common_unique_chars(s1, s2):
    result=""
    for ch in s1:
        if ch==" " or ('0' <=ch<= '9'):
            continue
        if ch in s2 and ch not in result:
            result+=ch
    return result

#13
def replace_every_nth(text, n, char):
    result=""
    index=0
    words = text.split(" ")
    for word in words:
        if len(word)<3:
            result +=word
            index +=len(word)
        else:
            new_word =""
            for ch in word:
                index +=1
                if '0' <=ch<='9':
                    new_word +=ch
                elif index % n==0:
                    new_word +=char
                else:
                    new_word +=ch
            result +=new_word
        result +=" "
        index += 1
    return result[:-1]
#16
def transform_list(nums):
    result=[]
    for num in nums:
        if num<0:
            continue
        if num%2==0:
            result.append(num * num)
        elif num>10:
            s=0
            temp=num
            while temp >0:
                digit =temp%10
                s +=digit
                temp= temp//10
            result.append(s)
        else:
            result.append(num)
    return result
#18
def flatten_and_filter(lst):
    numbers=[]
    def get_numbers(sublist):
        for item in sublist:
            if type(item)==list:
                get_numbers(item)
            else:
                if type(item)==int:
                    numbers.append(item)
    get_numbers(lst)
    result=[]
    for num in numbers:
        if num>0:
            if num%4!=0:
                if len(str(num))>1:
                    result.append(num)
    result.sort()
    return result
lst=[1,[12,-5,[33,8]],[44,[25,3]],16]
print(flatten_and_filter(lst))
#20
def max_subarray_sum(nums, k):
    best=None
    i=0
    while i<=len(nums)-k:
        s=0
        ok=True
        j=i
        while j<i+k:
            if nums[j]<=0:
                ok=False
            s +=nums[j]
            j +=1
        if ok==True:
            if best== None or s>best:
                best= s
        i +=1
    return best
#22
def group_by_parity_and_sort(nums):
    even = []
    odd = []
    for x in nums:
        if x % 2 == 0:
            even.append(x)
        else:
            odd.append(x)
    sorted_even = []
    while len(even) > 0:
        m = even[0]
        for x in even:
            if x < m:
                m = x
        sorted_even.append(m)
        even.remove(m)
    sorted_odd=[]
    while len(odd) > 0:
        m = odd[0]
        for x in odd:
            if x<m:
                m=x
        sorted_odd.append(m)
        odd.remove(m)
    return sorted_even+sorted_odd
#24
def longest_increasing_sublist(nums):
    if len(nums)==0:
        return []
    best_start=0
    best_len=1
    cur_start=0
    cur_len=1
    for i in range(1,len(nums)):
        if nums[i]>nums[i-1]:
            cur_len+=1
        else:
            if cur_len>best_len:
                best_len=cur_len
                best_start=cur_start
            cur_start=i
            cur_len=1
    if cur_len>best_len:
        best_len=cur_len
        best_start=cur_start
    return nums[best_start:best_start+best_len]
#26
def remove_duplicates_keep_last(nums):
    result=[]
    for i in range(len(nums)):
        is_duplicate=False
        for j in range(i+1,len(nums)):
            if nums[i]==nums[j]:
                is_duplicate=True
                break
        if not is_duplicate:
            result.append(nums[i])
    return result
#28
def moving_average(nums,k):
    result=[]
    for i in range(len(nums)-k+1):
        sum_window=0
        has_negative=False
        for j in range(i,i+k):
            if nums[j]<0:
                has_negative=True
            sum_window +=nums[j]
        if not has_negative:
            avg=sum_window/k
            result.append(avg)
    return result
def analyze_strings_list(words):
    result=[]
    for word in words:
        has_digit=False
        for ch in word:
            if ch >='0' and ch<='9':
                has_digit=True
                break
        if has_digit:
            continue
        if len(word)%2==0:
            new_word=""
            for i in range(len(word)-1,-1,-1):
                new_word=word[i]
        else:
            new_word = word.upper()
        if new_word not in result:
            result.append(new_word)
    return result
#6
func = lambda text: list(filter(
    lambda w: len(w) >= 4
    and len(set(w)) == len(w)
    and len(set(w) - set("0123456789")) == len(set(w)),
    text.split()
))
#8
def change_text(text):
    result=[]
    digits="0123456789"
    vowels="aeiouy"
    for w in text.split():
        digit_found=False
        for d in digits:
            if d in w:
                digit_found=True
                break
        if digit_found:
            result.append(w)
        elif w[0].lower() in vowels:
            result.append("VOWEL")
        else:
            result.append("CONSONANT")
    return " ".join(result)
text="apple banana 123code orange tiger"
print(change_text(text))
#10
def string(t):
    words=t.split()
    d="0123456789"
    count=0
    for w in words:
        has_digit=False
        for ch in w:
            if ch in d:
                has_digit=True
                break
        if has_digit and w[0] not in d and len(w) >= 5:
            count+=1
    return count
print(string("abc12 1abc2 ab1234 abcde a1b2c3"))
#12
def string(text):
    words=text.split()
    result=[]
    for w in words :
        if w!=w[::-1] and len(w)>=3 and w[0]==w[-1]:
            result.append(w)
    return result
#31
def invert_unique(d):
    result={}
    for key,value in d.items():
        if value not in result:
            result[value]=[]
        if key not in result[value]:
            result[value].append(key)
    return result
#14
def string(text):
    words=text.split()
    result=[]
    vowels="aeiuoy"
    for w in words:
        if len(set(w.lower()))>3:
            vowel_list=[]
        for ch in w.lower():
            if ch in vowels:
                    vowel_list.append(ch)
            if len(vowel_list)== len(set(vowel_list)):
                result.append(w)
    return ",".join(result)
    #  result=""
    # for w in result_words:
    #     result +=w+","
    # if result !="":
    #     result=result[:-1]
    # return result
#17
def process_numbers(nums):
    result = []
    for x in nums:
        temp = abs(x)
        digits = 0
        if temp == 0:
            digits = 1
        else:
            while temp > 0:
                digits += 1
                temp //= 10
        if (x % 3 == 0 or x % 5 == 0) and x % 15 != 0 and digits % 2 == 1:
            result.append(x * x)
    return result
#19
def same_even(a, b):
    result = []
    for i in range(len(a)):
        if a[i] == b[i] and a[i] % 2 == 0:
            result.append(a[i])
    return result
#27
process=lambda lst:sorted(lst,key=lambda x:(-len(x),x))[:5]
words=["apple","hi","banana","car","apricot","dog","zebra"]
result=process(words)
print(result)
#25
process=lambda data: [sum(lst) / len(lst)
    for lst in data
    if len(lst) >= 3 and sum(lst) % 2 == 0]
#21
def process(lst):
    result = []
    for s in lst:
        only_letters =True
        for ch in s:
            if not (('a'<=ch<='z')or('A'<=ch<= 'Z')):
                only_letters=False
                break
        if only_letters and len(s)>4 and len(set(s))==len(s):
            result.append(s.upper())
    return result
#33
def merge_dicts_sum(d1, d2):
    result = {}
    for key in d1:
        result[key] = d1[key]
    for key in d2:
        if key in result:
            result[key] += d2[key]
        else:
            result[key] = d2[key]
    return result
d1 = {"a": 5, "b": 3, "c": 10}
d2 = {"b": 7, "c": 2, "d": 8}
print(merge_dicts_sum(d1, d2))
#34
def filter_sets(sets_list):
    result = []
    for s in sets_list:
        if len(s) <= 3:
            continue
        has_even = False
        has_negative = False
        for num in s:
            if num < 0:
                has_negative = True
            if num % 2 == 0:
                has_even = True
        if not has_negative and has_even:
            result.append(s)
    return result
sets_list = [
    {1, 2, 3, 4},
    {1, 3, 5, 7},
    {2, 4, 6, 8},
    {-1, 2, 3, 4},
    {10, 11, 12, 13}]
print(filter_sets(sets_list))
#32
filter_set = lambda s: set(
    filter(
        lambda x: x > sum(s)/len(s) and x % 2 != 0 and x % 5 != 0,
    s))
nums = {3, 7, 10, 11, 15, 18, 21}
print(filter_set(nums))
#35
top5_keys = lambda d: [k for k, v in sorted(d.items(), key=lambda x: (-x[1], x[0]))[:5]]
data = {
    "apple": 10,
    "banana": 7,
    "cherry": 10,
    "date": 5,
    "fig": 7,
    "grape": 12,
    "kiwi": 7}
print(top5_keys(data))
