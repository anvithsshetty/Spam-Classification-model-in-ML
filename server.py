import socket
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np



def decrypt(str,key,key2):
    s = list(str)

    for j in range(len(key)):
        low = 0
        x = 0
        i = 0
        l = int(key[len(key)-1-j])
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

    for i in range(len(str)):
        if s[i]==' ':
            continue
        else:
            s[i] = chr(ord(s[i]) - key2)

    return ''.join(s)







key = '2561'
key2=3

df = pd.read_csv('spam.csv')
x_train = df['EmailText']
y = df['Label']
y_train = y.replace(['ham','spam'],[1,0])

cv = TfidfVectorizer(min_df=1)
x_traincv = cv.fit_transform(x_train.values.astype('U'))
mnb = MultinomialNB()
mnb.fit(x_traincv,y_train)

s = socket.socket()
print('Socket created')
s.bind(('localhost',9999))
s.listen(3)
print('Waiting for connections')
c,addr = s.accept()
print("Connected with ",addr)
while True:
    str = c.recv(1024).decode()
    str = decrypt(str,key,key2)
    print(str)
    if str=='quit':
        c.close()
        exit(0)
    str=[str]
    anvi = cv.transform(str)
    res = mnb.predict(anvi)
    if res[0]==1:
        c.send(bytes("HAM",'utf-8'))
    else:
        c.send(bytes("SPAM", 'utf-8'))
