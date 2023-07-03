with open('manchester.txt') as f:
    text = f.read()

decoded_text = ""
for x in range(0, len(text), 2):
	ch = text[x]
	decoded_text += ch

print(decoded_text)
