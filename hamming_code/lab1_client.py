import socket
import pickle
import random

def string_formating(input_str, word_length):
    binary_str = ''.join([bin(ord(i))[2:].zfill(8) for i in input_str])
    words_list = ['']
    leng = len(binary_str)
    zeros = bin(word_length - leng%word_length) if leng%word_length!=0 else bin(0)
    for i in range(0, word_length - len(zeros) + 2):
        words_list[0] += '0'
    for i in range(2, len(zeros)):
        words_list[0] += zeros[i]
    for i in range(0, leng, word_length):
        words_list.append('')
        for j in range(i, i + min(word_length, leng-i)):
            words_list[i//word_length + 1] += binary_str[j]
    end = leng//word_length+1 if leng%word_length!=0 else leng//word_length
    while len(words_list[end]) < word_length:
        words_list[end] += '0'
    return words_list

def add_bits(str):
    i = 1
    j = 0
    ans = []
    while i <= len(str):
        ans.append(0)
        for k in range(i-1):
            if j+k >= len(str):
                break
            ans.append(ord(str[j+k]) - ord('0'))
        j += i-1
        i *= 2
    return ans


def hamming_code(binary_list):
    sz = len(binary_list)
    coded_list = []
    for _ in range(sz):
        coded_list.append(add_bits(binary_list[_]))
        i = 1
        leng = len(coded_list[_])
        while(i <= leng):
            cnt = 0
            j = i-1
            while j <= leng:
                for a in range(j, min(j+i, leng)):
                    cnt += coded_list[_][a]
                j += 2*i
            coded_list[_][i-1] = cnt % 2
            i *= 2
    return coded_list

def add_mistakes(n, coded_list):
    mistake_num = []
    for word in coded_list:
        p = random.random()
        if p > 0.57:
            mistake_num.append([0])
            continue
        cnt = 0
        idx = -1
        for i in range(len(word)):
            p = random.random()
            if p < 0.38 and cnt < n:
                word[i] = 0 if word[i] else 1
                cnt += 1
        if cnt == 1:
            mistake_num.append([1, idx])
        else:
            mistake_num.append([cnt])
    return mistake_num

word_length = 66
localhost = '127.0.0.1'
port = 6436
sock = socket.socket()
sock.connect((localhost, port))
while True:
    with open('message.txt', 'r', encoding='utf-8') as file:
        message = file.read().replace('\n', '')
    binary_str = string_formating(message, word_length)
    coded_list = hamming_code(binary_str)
    print()
    print('Введите количество ошибок')
    mistakes_cnt = int(input())
    mistakes_list = add_mistakes(mistakes_cnt, coded_list)
    correct = 0
    one_mistake = 0
    plural_mistake = 0
    for l in mistakes_list:
        if l[0] == 0:
            correct += 1
        elif l[0] == 1:
            one_mistake += 1
        else:
            plural_mistake += 1
    print()
    print('Описание передаваемого сообщения:')
    print('Слов без ошибок - ', correct)
    print('Слов с одной ошибкой - ', one_mistake)
    print('Слов с более, чем одной ошибкой - ', plural_mistake)
    sock.send(pickle.dumps(coded_list))
    respond = b""
    while True:
        data = sock.recv(1024)
        respond += data
        if len(data) < 1024:
            break
    new_list = pickle.loads(respond)
    correct = 0
    one_mistake = 0
    plural_mistake = 0
    for l in new_list:
        if l[0] == 0:
            correct += 1
        elif l[0] == 1:
            one_mistake += 1
        else:
            plural_mistake += 1
    print()
    print('Описание полученного сервером сообщения:')
    print('Слов без ошибок - ', correct)
    print('Слов с одной ошибкой - ', one_mistake)
    print('Слов с более, чем одной ошибкой - ', plural_mistake)
    print()
sock.close()