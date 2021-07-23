import socket


def encrypt(str,key,key2):
    s = list(str)

    for i in range(len(s)):
        if s[i]==' ':
            continue
        else:
            s[i]=chr(ord(s[i])+key2)
    print('after key1:',''.join(s))

    for j in range(len(key)):
        low = 0
        x = 0
        i = 0
        l = int(key[j])
        high = len(s) - 1
        while low < high:
            if x == l:
                #print(low)
                i = (i + 1) % (len(key))
                l = int(key[i])
                x = 0
                low += 1
                high -= 1
                continue
            temp = s[low]
            s[low] = s[high]
            s[high] = temp
            x += 1
            high -= 1
            low += 1

    return ''.join(s)






c = socket.socket()

key1 = '2561'
key2 = 3

c.connect(('localhost',9999))
while True:
    str = input("ENTER MESSAGE  :")
    if str=='quit':
        break
    str = encrypt(str,key1,key2)
    print(str)

    c.send(bytes(str,'utf-8'))

    print(c.recv(1024).decode())