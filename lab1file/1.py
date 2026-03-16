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
def top_k_words(text, k):
    text = text.lower()
    c =""
    a = "abcdefghijklmnopqrstuvwxyzәіңғүұқөһ "
    for ch in text:
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
print(top_k_words(text,k))

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
#30
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
#36
def deep_sum(d):
    total = 0
    for value in d.values():
        if isinstance(value, int) or isinstance(value, float):
            total += value
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, int) or isinstance(item, float):
                    total += item
                elif isinstance(item, dict):
                    total += deep_sum(item)
                elif isinstance(item, list):
                    for x in item:
                        if isinstance(x, int) or isinstance(x, float):
                            total += x
        elif isinstance(value, dict):
            total += deep_sum(value)
    return total
data = {
    "a": 5,
    "b": [1, 2, 3],
    "c": {
        "d": 4,
        "e": [5, 6]
    },
    "f": {
        "g": {
            "h": 10
        }
    }
}
print(deep_sum(data))
#37
f = lambda a, b: {x for x in (a ^ b) if x % 2 == 0}
a = {1, 2, 3, 4, 6}
b = {3, 4, 5, 6, 8}
print(f(a, b))
#38
def sort_dict_by_value_length(d):
    items = []
    for key in d:
        items.append((key, d[key]))
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            v1 = items[i][1]
            v2 = items[j][1]
            if len(v1) > len(v2) or (len(v1) == len(v2) and items[i][0] > items[j][0]):
                items[i], items[j] = items[j], items[i]
    return items
d = {
    "apple": "red",
    "banana": "yellow",
    "kiwi": "green",
    "pear": "ripe"
}
print(sort_dict_by_value_length(d))
#39
def common_elements_all(sets_list):
    if not sets_list:
        return set()
    result = sets_list[0].copy()
    for s in sets_list:
        new_result = set()
        for x in result:
            if x in s:
                new_result.add(x)
        result = new_result
    return result
sets_list = [
    {1, 2, 3, 4},
    {2, 3, 5},
    {0, 2, 3, 8}
]
print(common_elements_all(sets_list))
#40
transform = lambda d: {
    k: sorted([x for x in v if x % 2 != 0])
    for k, v in d.items()
    if any(x % 2 != 0 for x in v)
}
data = {
    "a": [1, 2, 3, 4],
    "b": [2, 4, 6],
    "c": [5, 7, 8],
    "d": [10]
}
print(transform(data))
#41
def group_by_length(words):
    result = {}
    for word in words:
        length = len(word)
        if length not in result:
            result[length] = []
        if word not in result[length]:
            result[length].append(word)
    return result
words = ["cat", "dog", "apple", "car", "dog", "pear", "hi"]
print(group_by_length(words))
#42
filter_strings = lambda s: {
    x for x in s
    if x.isalpha() and len(x) > 4 and len(set(x)) == len(x)
}
data = {"apple", "world", "hello", "abcde", "python", "aabbc", "12345"}
print(filter_strings(data))
#43
def invert_dict_strict(d):
    counts = {}
    result = {}
    for key in d:
        value = d[key]
        if value not in counts:
            counts[value] = 1
        else:
            counts[value] += 1
    for key in d:
        value = d[key]
        if counts[value] == 1:
            result[value] = key
    return result
d = {
    "a": 1,
    "b": 2,
    "c": 1,
    "d": 3
}
print(invert_dict_strict(d))
#44
def top_k_frequent(nums, k):
    freq = {}
    for n in nums:
        if n not in freq:
            freq[n] = 1
        else:
            freq[n] += 1
    items = []
    for n in freq:
        items.append((n, freq[n]))
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i][1] < items[j][1] or \
               (items[i][1] == items[j][1] and items[i][0] > items[j][0]):
                items[i], items[j] = items[j], items[i]
    result = set()
    for i in range(min(k, len(items))):
        result.add(items[i][0])
    return result
nums = [1,1,1,2,2,3,3,4]
k = 2
print(top_k_frequent(nums, k))
#45
filter_dict = lambda d: {
    k: v for k, v in d.items()
    if v >= sum(d.values())/len(d) and v % 2 != 0
}
data = {
    "a": 3,
    "b": 10,
    "c": 7,
    "d": 4,
    "e": 9
}
print(filter_dict(data))
#46
def update_counts(d, items):
    for item in items:
        if item in d:
            d[item] += 1
        else:
            d[item] = 1
    return d
d = {"apple": 2, "banana": 1}
items = ["apple", "orange", "banana", "apple"]

print(update_counts(d, items))
#47
f = lambda a, b, c: (a & b) - c
a = {1,2,3,4,5}
b = {3,4,5,6}
c = {4}
print(f(a,b,c))
#48
def sort_dict_by_value_sum(d):
    items = []

    # считаем суммы
    for key in d:
        total = 0
        for x in d[key]:
            total += x
        items.append((key, total))

    # сортировка через цикл
    for i in range(len(items)):
        for j in range(i + 1, len(items)):

            if items[i][1] < items[j][1] or \
               (items[i][1] == items[j][1] and items[i][0] > items[j][0]):

                items[i], items[j] = items[j], items[i]

    return items
d = {
    "a": [1,2,3],
    "b": [4],
    "c": [1,1,1,1],
    "d": [2,2]
}

print(sort_dict_by_value_sum(d))
#49
def filter_by_digit_sum(nums):
    result = set()

    for n in nums:
        digit_sum = 0
        temp = abs(n)

        while temp > 0:
            digit_sum += temp % 10
            temp //= 10

        if digit_sum % 2 == 0 and n % 2 != 0:
            result.add(n)

    return result
nums = {13, 24, 35, 41, 52}

print(filter_by_digit_sum(nums))
#50
f = lambda d: sorted(d.keys(), key=lambda k: (d[k], len(k)))[:3]
data = {
    "apple": 5,
    "kiwi": 2,
    "banana": 5,
    "fig": 2,
    "pear": 3
}
print(f(data))
#51
def count_leaf_values(d):
    count = 0
    for key in d:
        value = d[key]
        if isinstance(value, dict):
            count += count_leaf_values(value)
        elif isinstance(value, list):
            count += len(value)
        else:
            count += 1
    return count
data = {
    "a": 5,
    "b": [1, 2, 3],
    "c": {
        "d": 7,
        "e": [4, 5]
    }
}
print(count_leaf_values(data))
#52
f = lambda a, b: {x for x in a if x > sum(b)/len(b) and x not in b}
a = {1, 3, 5, 7, 9}
b = {2, 4, 6}
print(f(a, b))
#53
def group_by_last_letter(words):
    result = {}
    for word in words:
        last = word[-1]
        if last not in result:
            result[last] = []
        if word not in result[last]:
            result[last].append(word)
    return result
words = ["apple", "cake", "table", "orange", "cake", "blue"]
print(group_by_last_letter(words))
#54
def union_of_filtered_sets(sets_list):
    result = set()
    for s in sets_list:
        for x in s:
            if x > 10 and x % 2 != 0:
                result.add(x)
    return result
sets_list = [
    {5, 11, 12, 15},
    {9, 13, 18},
    {7, 21, 22}
]
print(union_of_filtered_sets(sets_list))
#55
f = lambda d: {
    k: __import__("math").prod([x for x in v if x > 0])
    for k, v in d.items()
    if any(x > 0 for x in v)
}
data = {
    "a": [1, -2, 3],
    "b": [-1, -5],
    "c": [2, 4, -3],
    "d": [0, -2, 5]
}
print(f(data))
#56
def remove_elements_with_common_digits(s):
    digit_count = {}

    # считаем в скольких числах встречается каждая цифра
    for num in s:
        digits = set(str(abs(num)))
        for d in digits:
            if d not in digit_count:
                digit_count[d] = 1
            else:
                digit_count[d] += 1

    result = set()

    # оставляем только числа с уникальными цифрами
    for num in s:
        digits = set(str(abs(num)))
        unique = True

        for d in digits:
            if digit_count[d] > 1:
                unique = False
                break

        if unique:
            result.add(num)

    return result
nums = {12, 34, 56, 27}
print(remove_elements_with_common_digits(nums))
#57
is_prime = lambda n: n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))
f = lambda d: {k: v for k, v in d.items() if len(k) % 2 != 0 and is_prime(v)}
data = {
    "a": 2,
    "bb": 3,
    "cat": 4,
    "dog": 5,
    "hello": 7
}
print(f(data))
#58
def sorted_unique_chars(strings):
    chars = set()

    # собираем уникальные символы
    for s in strings:
        for ch in s:
            if not ch.isdigit() and ch != " ":
                chars.add(ch)

    chars_list = list(chars)

    # сортировка через цикл
    for i in range(len(chars_list)):
        for j in range(i + 1, len(chars_list)):
            if chars_list[i] > chars_list[j]:
                chars_list[i], chars_list[j] = chars_list[j], chars_list[i]

    return chars_list
strings = ["hello 123", "world 45", "python"]

print(sorted_unique_chars(strings))
#59
f = lambda d: sorted(d.keys(), key=lambda k: (d[k] % 10, k))
data = {
    "apple": 23,
    "banana": 17,
    "cat": 45,
    "dog": 12
}

print(f(data))
#60
def partition_by_sum_parity(s):
    even_set = set()
    odd_set = set()
    for num in s:
        digit_sum = 0
        temp = abs(num)
        while temp > 0:
            digit_sum += temp % 10
            temp //= 10

        if digit_sum % 2 == 0:
            even_set.add(num)
        else:
            odd_set.add(num)

    return (even_set, odd_set)
nums = {13, 24, 35, 41, 52}

print(partition_by_sum_parity(nums))
#2
def analyze_students(data):
    vowels = set("aeiouyAEIOUY")
    result_students = []
    global_word_counts = {}
    all_vowels = set()
    for student in data:
        name = student.get("name", "")
        if any(ch.isdigit() for ch in name):
            continue
        clean_name = name.title()
        processed_grades = []
        for grade in student.get("grades", []):
            if grade <= 0:
                continue
            if grade % 2 == 1 and grade < 10:
                digit_sum = sum(int(d) for d in str(abs(grade)))
                processed_grades.append(digit_sum)
            elif grade % 2 == 0 and grade >= 10:
                processed_grades.append(grade ** 2)
            else:
                processed_grades.append(grade)
        comments = student.get("comments", [])
        joined_comments = " ".join(comments)
        cleaned_text = ""
        for ch in joined_comments:
            if ch.isalpha() or ch.isspace():
                cleaned_text += ch
            else:
                cleaned_text += " "
        words = cleaned_text.lower().split()
        unique_words = []
        seen_words = set()
        for word in words:
            if len(word) >= 4 and word != word[::-1] and word not in seen_words:
                unique_words.append(word)
                seen_words.add(word)
        student_vowels = set()
        for word in unique_words:
            for ch in word:
                if ch in vowels:
                    student_vowels.add(ch.lower())
        all_vowels.update(student_vowels)
        unique_for_student = set(unique_words)
        for word in unique_for_student:
            global_word_counts[word] = global_word_counts.get(word, 0) + 1
        result_students.append({
            "name": clean_name,
            "processed_grades": processed_grades
        })
    filtered_word_counts = dict(
        filter(lambda item: item[1] >= 2, global_word_counts.items())
    )
    sorted_word_counts = dict(
        sorted(filtered_word_counts.items(), key=lambda item: (-item[1], item[0]))
    )
    students_with_avg = []
    for student in result_students:
        grades = student["processed_grades"]
        if grades:
            avg = sum(grades) / len(grades)
        else:
            avg = 0
        students_with_avg.append((student["name"], avg))
    students_with_avg.sort(key=lambda x: (-x[1], x[0]))
    students_by_avg = [name for name, avg in students_with_avg]
    students_by_name_length = {}
    for student in result_students:
        name = student["name"]
        length = len(name)
        if length not in students_by_name_length:
            students_by_name_length[length] = []
        if name not in students_by_name_length[length]:
            students_by_name_length[length].append(name)
    return {
        "students": result_students,
        "word_counts": sorted_word_counts,
        "all_vowels": all_vowels,
        "students_by_avg": students_by_avg,
        "students_by_name_length": students_by_name_length
    }
#1
def analyze_students(data):
    vowels = set("aeiouAEIOU")
    students_result = []
    global_word_counts = {}
    all_vowels = set()
    for student in data:
        name = student["name"]
        if any(ch.isdigit() for ch in name):
            continue
        clean_name = name.title()
        processed_grades = []
        for grade in student["grades"]:
            if grade <= 0:
                continue
            elif grade % 2 == 1 and grade < 10:
                digit_sum = sum(int(d) for d in str(grade))
                processed_grades.append(digit_sum)
            elif grade % 2 == 0 and grade >= 10:
                processed_grades.append(grade ** 2)
            else:
                processed_grades.append(grade)
        joined_comments = " ".join(student["comments"])
        cleaned_text = ""
        for ch in joined_comments:
            if ch.isalpha() or ch.isspace():
                cleaned_text += ch.lower()
            else:
                cleaned_text += " "
        words = cleaned_text.split()
        unique_words = []
        seen = set()
        for word in words:
            if len(word) >= 4 and word != word[::-1] and word not in seen:
                unique_words.append(word)
                seen.add(word)
        student_vowels = set()
        for word in unique_words:
            for ch in word:
                if ch in vowels:
                    student_vowels.add(ch.lower())
        all_vowels.update(student_vowels)
        for word in set(unique_words):
            global_word_counts[word] = global_word_counts.get(word, 0) + 1
        students_result.append({
            "name": clean_name,
            "processed_grades": processed_grades
        })
    filtered_word_counts = dict(
        filter(lambda item: item[1] >= 2, global_word_counts.items())
    )

    sorted_word_counts = dict(
        sorted(filtered_word_counts.items(), key=lambda item: (-item[1], item[0]))
    )
    students_with_avg = []
    for student in students_result:
        grades = student["processed_grades"]
        avg = sum(grades) / len(grades) if grades else 0
        students_with_avg.append((student["name"], avg))

    students_with_avg.sort(key=lambda x: (-x[1], x[0]))
    students_by_avg = [name for name, avg in students_with_avg]

    students_by_name_length = {}
    for student in students_result:
        name = student["name"]
        length = len(name)

        if length not in students_by_name_length:
            students_by_name_length[length] = []

        if name not in students_by_name_length[length]:
            students_by_name_length[length].append(name)

    return {
        "students": students_result,
        "word_counts": sorted_word_counts,
        "all_vowels": all_vowels,
        "students_by_avg": students_by_avg,
        "students_by_name_length": students_by_name_length
    }
