open_secrets = open('/Users/yarik/Documents/ITMO_1/Computer architecture and OS/text.txt', 'r')
stroka = ''
for word in open_secrets.read().split():
    stroka += chr(int(word))

print(stroka)