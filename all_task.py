import math
import socket
import time
import sys
import string
import base64
import zlib

while 1:
    task = int(input("Enter your task\n"))
    if 1 <= task <= 4:
        break

def solve1(txt):
    n1, n2 = txt.split(' / ')
    return round(math.sqrt(int(n1)) * int(n2), 2)

def solve2(txt):
    return str(base64.b64decode(txt).decode('utf-8'))

def solve3(txt):
    rot13 = str.maketrans( 
    "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", 
    "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
    return str.translate(txt, rot13)

def solve4(txt):
    return zlib.decompress(base64.b64decode(txt)).decode('utf-8')

server = 'irc.hackerzvoice.net'
port = 6667
channel = '#root-me_challenge'
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))
irc.setblocking(False)
botnick = 'hungnk1112k'
message = 'hello'
time.sleep(1)
irc.send("USER {0} {0} {0}: {1}\r\n".format(botnick, message).encode('utf-8'))
time.sleep(1)
irc.send("NICK {}\n".format(botnick).encode('utf-8'))
time.sleep(1)
irc.send("JOIN {}\n".format(channel).encode('utf-8'))

sent_private_msg = False
sent_result = False

while 1:
    text = ''
    time.sleep(0.1)
    try:
        text = irc.recv(2040).decode('utf-8')
        if text:
            print(text)
    except Exception:
        pass
    
    if 'BANNED' in text:
        print('sleep for 30 seconds')
        timer = 0
        while timer < 31:
            print(timer)
            time.sleep(1)
            timer += 1
        sent_private_msg = False
        sent_result = False
        text = 'End of /NAMES list.'
    if 'PING' in text:
        msg = 'PONG {} \r\n'.format(text.split()[1])
        irc.send(msg.encode('utf-8'))
    if text.strip().endswith('End of /NAMES list.') and not sent_private_msg: # haven't sent private message yet
        # :irc.hackerzvoice.net 366 qiwoehrwqero123 #root-me_challenge :End of /NAMES list.
        print('send message')
        msg = 'PRIVMSG candy : !ep{}\r\n'.format(task)
        irc.send(msg.encode('utf-8'))
        sent_private_msg = True
    if ':Candy!Candy@root-me.org' in text and sent_private_msg and not sent_result: # sent private message but not result
        print('send result')
        result = locals()['solve{}'.format(task)](text.strip().split(':')[-1])
        msg = 'PRIVMSG candy : !ep{} -rep {}\r\n'.format(task, result)
        print(result)
        irc.send(msg.encode('utf-8'))
        print(msg)
        sent_result = True
        continue
    if text != '' and sent_private_msg and sent_result:
        print('send quit')
        msg = 'QUIT :Bye!\r\n'
        irc.send(msg.encode('utf-8'))
        irc.close()
        sys.exit('End')
