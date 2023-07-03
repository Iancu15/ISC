1. crypto-attack

Uitandu-ma la fisier am observat ca generatorul va fi mereu 2 si vad ca
cheia publica este int(pow(g, my_priv, p)). Dupa cere cheia mea publica si
calculeaza cheia shared ca int(pow(yours, my_priv, p)). Intre cheia publica
si shared observ ca singura diferenta e intre g si yours, asa ca daca pun
cheia mea publica sa fie egala cu generatorul(=2), atunci cheia shared va
fi egala cu cheia publica si o voi sti. Apelez functia si dau cheia publica
2 si salvez cheia publica(=cheia shared) si flag-ul criptat si encodat.

Fac un script de python(attack.py), unde decodez flag-ul si calculez cheia
de criptare folosind cheia shared pe care o am. Decriptez folosind cheia
de criptare/decriptare flag-ul decodat si il printez.

Am vazut ca merge pe local, asa ca fac acelasi lucru pe valorile de pe remote.
Apelez la remote folosind comanda nc isc2023.1337.cx 11008.

2. linux-acl

Am facut ssh folosind cheia din folder: ssh janitor@isc2023.1337.cx -i id_rsa.
Pentru ca ssh-ul sa mearga a trebuit sa schimb permisiunile pentru cheie cat
sa aiba doar owner-ul.

In terminalul deschis m-am uitat dupa fisiere cu setuid-ul setat folosind comanda
find / -perm -u=s -type f 2>/dev/null. Am gasit 2 mai interesante si anume th3CEO
si robotsudo. Inspectand fisierele si permisiunile am ajuns la concluzia ca trebuie
sa folosesc robotsudo cumva sa apelez th3CEO. Ruland comanda strings pe robotsudo
am aflat ca are un fisier de configurare, insa pe acesta nu il puteam modifica.

Ruland ltrace pe robotsudo am aflat ca citeste fisierul de configurare si il compara
cu "allow janitor [comanda data de mine]" folosind strncmp pe 43 de caractere. Vad
ca in fisierul de configurare executabilul la care am allow (vacuum-control), toata
linia are fix 43 de caractere. Lucru ce inseamna ca pot appendui orice la path-ul
lui vacuum-control si va putea fi executat. Deci un fisier cu denumirea vacuuum-controlXXX
in acelasi director cu vacuum-control va putea fi executat si cum e creat de mine pot
sa pune orice si anume si path-ul la th3CEO sa il execut.

Totusi pare ca imi zice ca n-am acces de la fisier asa ca trebuie sa fac ceva si la asta.
Dau strings pe el si vad ca are un flag la /etc/X11/not_for_your_eyes/.zaflag (nu il pot citi).
Insa mai important a fost ca avea un sir de caractere ciudat 662a6d08664c68d30306f35361357bf7
ca o cheie. Dupa diverse incercari am descoperit ca pot da cheia respectiva ca parametru,
astfel da un mesaj ca sunt janitor. Daca apelez din vacuuum-controlXXX, am acces total si
primesc flagul.

3. binary-exploit

Intai am deschis programul in ghidra si m-am uitat sa vad ce functii sunt si cam ce ar trebui sa
fac. Am vazut o functie win care avea un puts ce zicea "bravo ai aflat flagul" si am zis ca trebuie
sa ajung cumva acolo din main sau loop. Din main dupa incercari repetate n-am reusit, asa ca mi-am
indreptat atentia catre loop. Vad ca are un while care merge la infinit cat timp primeste un integer
prin scanf si stocheaza valoarea intr-un vector local_b8 la o pozitie specificata de o variabila uVar5.
Vad ca uVar5 creste constant, asa ca pot da integers de X ori ca sa suprascriu primele X valori incepand
cu adresa local_b8.

Pentru a nu sta sa introduc date manual si datorita lipsei de manevrabilitate a introducerii inputului
manual am decis sa folosesc pwntools. Revenind la problema, cum local_b8 e ultima variabila locala
si are dimensiunea 42 am decis sa introduc 42 de integers in while sa ajung la finalul variabilelor locale.
La inceput de functie loop s-a dat push pe stiva la registrii ebp, edi, esi si ebx asa ca am mai introdus
4 integers sa sar peste ei. Am luat adresa de la func win in hexa din ghira si am transformat-o folosind un site in
integer-ul echivalent pentru a putea sa mai adaug dupa el si parametrul functiei win pe care trebuia sa-l
suprascriu sa fie echivalent cu lucky_number pentru a primii flag-ul.

Lucky number se schimba la inceput de main pe baza timestamp-ului (secunde de la epoch - 1970) care e dat
ca seed la srand si se foloseste a doua rulare de rand() pentru acesta. Problema e ca bibliotecile
fiecarui limbaj isi implementeaza random-ul diferit(PRG diferit de ex.) si asta inseamna ca random.random()
din python nu dadea aceleasi valori cu rand() din C(cel putin mie imi dadea diferit) pe acelasi seed.
Asa ca ce am facut a fost sa scriu partea de calculare a lucky number-ului in C, sa compilez codul C
si sa rulez executabilul cu subprocess in python. Lucky number-ul il printez in C si capturez stdout-ul
in python.

Sidenote, cand intreaba "Continue [Y/N]" zic nu pentru ca pe branch-ul de yes se schimba lucky number-ul.