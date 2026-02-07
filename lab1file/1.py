print("fdfg")
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
    if text == "":
        return ""
    r= ""
    c= 1
    for i in range(1, len(text)):
        if text[i].lower() == text[i-1].lower():
            c+= 1
        else:
            if c== 1:
                r+= text[i-1]
            else:
                r+= text[i-1] + str(c)
            c = 1
    if c == 1:
        r += text[-1]
    else:
        r += text[-1] + str(c)
    return r
#9
def alternate_case_blocks(text, n):
    result = ""
    for i in range(0, len(text), n):
        block = text[i:i+n]
        if (i // n) % 2 == 0:
            result += block.upper()
        else:
            result += block.lower()
    return result
#1
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
    words = clean.split()
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
    c = ""
    a = "abcdefghijklmnopqrstuvwxyzәіңғүұқөһ "
    for ch in t:
        if ch in a:
            c += ch
        else:
          c += " "
    w = c.split()
    u = []
    n = []
    for x in w:
        if x not in u:
            u.append(x)
            n.append(1)
        else:
            i = u.index(x)
            n[i] += 1
    for i in range(len(u)):
        for j in range(i + 1, len(u)):
            if n[j] > n[i]:
                n[i], n[j] = n[j], n[i]
                u[i], u[j] = u[j], u[i]
            elif n[j] == n[i] and u[j] < u[i]:
                u[i], u[j] = u[j], u[i]
                n[i], n[j] = n[j], n[i]
    if k > len(u):
        k = len(u)
    r = []
    for i in range(k):
        r.append(u[i])
    return r
#4
def change_words(text):
    w= text.split()
    r=[]
    for s in w:
        big= 0
        for ch in s:
            if ch == ch.upper() and ch != ch.lower():
                big= big+ 1
        if big== 1:
            if s[0] != s[0].upper():
                if s[-1] != s[-1].upper():
                    r.append(s.lower())
    return " ".join(r)
text = "heLlo HellO hEllo HELLO teSt Әлем кІтап"
print(change_words(text))
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
def replace_every_nth(text, n, char):
    result=""
    i=0
    length=len(text)
    while i<length:
        ch=text[i]
        if ('a' <= ch<= 'z') or ('A' <= ch <= 'Z'):
            word=""
            start=i
            while i< length and (('a' <= text[i] <= 'z') or ('A' <= text[i] <= 'Z')):
                word+=text[i]
                i+=1
            if len(word)<3:
                result+=word
            else:
                for j in range(len(word)):
                    if (j+1)%n==0:
                        result+=char
                    else:
                        result +=word[j]
        else:
            result +=ch
            i +=1
    return result
#13
def replace_every_nth(text, n, char):
    result=""
    index=0
    words = text.split(" ")
    for word in words:
        if len(word)<3:
            result +=word
            index += len(word)
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
            continue
        if num%2==0:
            result.append(num * num)
        elif num>10:
            s=0
            temp =num
            while temp >0:
                digit =temp%10
                s +=digit
                temp= temp//10
            result.append(s)
        else:
            result.append(num)
    return result