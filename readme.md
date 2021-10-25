# INFORMATII ADITIONALE
sistemul de operare: macOS Big Sur Version 11.6

# INSTALAREA

Pentru a instala Python 3 pe macOS:
```
brew install python3
```

Pentru a verifica daca python3 s-a instalat cu succes:
```
python3 --version
```

Ar trebui sa afiseze versiunea instalata.

Pentru a instala Selenium, numpy, opencv, ~~pyautogui~~ pillow si pyaudio, trebuie mai intai sa instalam pip - sistemul de management al librariilor pentru python:
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

aceste doua linii vor descarca scriptul de instalare a pip pe calculator si apoi il va rula in python3.

Pentru a instala librariile necesare:
```
pip install selenium
pip install opencv-python

brew install portaudio

pip install pillow
pip install PyAudio
```

Pentru a instala pyaudio, e nevoie de instalat mai intai portaudio:
```
brew install portaudio
pip install pyaudio
```

In cazul macOS pe chipurile M1, vor aparea probleme cu libraria portaudio.h din fisierele portaudio. Pentru a evita aceasta problema, e nevoie de instalat pyaudio cu 3 optiuni aditionale:

```
pip install --global-option='build_ext' --global-option='-I/opt/homebrew/Cellar/portaudio/19.7.0/include' --global-option='-L/opt/homebrew/Cellar/portaudio/19.7.0/lib' pyaudio
```

daca eroarea persista, verificati unde e instalata libraria portaudio.h cu comanda
```
find / -name "portaudio.h"
```

si modificati optiunea 2 si 3 astfel incat caile spre include si lib sa coincida cu locatia portaudio.h


## Selenium Python API

Pentru a folosi selenium, va fi nevoie de un driver de browser. Eu am folosit Chrome Driver, prealabil avand Google Chrome instalat.

Chromedriver poate fi instalat cu homebrew. Dupa instalare, e nevoie de ridicat carantina:
```
brew install chromedriver
which chromedriver
xattr -d com.apple.quarantine /calea/spre/chromedriver
```

Daca prima metoda nu merge, incercati urmatoarea:

E nevoie de instalat o versiune compatibila cu browserul Google Chrome instalat pe calculator. Pentru a verifica versiunea browserului: apasati pe trei puncte de sus-dreapta a ferestrei browserului => Settings => About Chrome.

De pe https://sites.google.com/chromium.org/driver/downloads descarcati versiunea respectiva de ChromeDriver, tinand cont si de sistema de operare.

Dezarhivati driverul si mutati-l intr-un folder convenabil.

Incercati mai intai sa deschideti manual chromedriver executandu-l in terminal sau cu dublu click. Cel mai probabil, macOS nu va va permite sa rulati executabilul din moment ce nu il poate verifica. Avand incredere oarba in Chrome, trebuie sa ridicam executabilul de sub carantina pentru a-l putea rula. Mai intai, ca sa obtineti calea spre executabil, rulati:
```
which chromedriver
```
Apoi ridicati carantina folosind calea optinuta
```
xattr -d com.apple.quarantine /calea/spre/chromedriver
```

Daca nici asta nu merge, instalati chromedriver cu homebrew si ridicati-i carantina:
```
brew install chromedriver
which chromedriver
xattr -d com.apple.quarantine /calea/spre/chromedriver
```

## Utilizare

Apelati din terminal 

```
python main.py
```

Acest script va deschide o fereastra de Google Chrome, va accesa youtube.com, va scrie in caseta de cautare un cuvant aleatoriu si il va acesa. Apoi, va alege un video oarecare din cele propuse si il va accesa. Cand videoul se va porni, va incepe inregistrarea desktopului dumneavoastra si a sunetului microfonului. Dupa 10 secunde, inregistrarea se va opri, se va salva cu denumirea output_timpul_si_data_inregistrarii_cuvantul_aleatoriu_cautat.mov in acelasi folder unde se afla si scriptul main.

Pentru a alege un timp anume de inregistrare, adaugati timpul in secunde ca primul argument la apelare

```
python main.py 60
```

Pentru a alege un cuvant anumit care sa fie cautat, adaugati cuvantul ca al doilea argument la apelare

```
python main.py 60 hello
```