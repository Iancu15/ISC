with open('otp.txt', 'rb') as f:
    enc = f.read()
    
f_out = open("otp_dec.txt", 'w')

for byte in range(256):
	dec = ""
	for ch in enc:
		dec_ch = chr(int(ch) ^ byte)
		dec += dec_ch
	
	f_out.write(dec + '\n')
		
