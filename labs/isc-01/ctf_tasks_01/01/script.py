from base64 import *

with open('b64.txt') as f:
    text = f.read()

while ((str(text)).find('FLAG') == -1):
	text = b64decode(text)

print(text.decode())
