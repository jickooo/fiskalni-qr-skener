# 🧾 Fiskalni QR Skener

> Python desktop aplikacija za skeniranje QR kodova sa fiskalnih računa putem web kamere ili telefona povezanog preko DroidCam-a, uz automatsko otvaranje stranice za proveru ispravnosti računa.

<p align="left">
  <img src="https://img.shields.io/badge/python-3.x-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/opencv-computer%20vision-green?style=for-the-badge&logo=opencv" />
  <img src="https://img.shields.io/badge/qr-scan-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/platform-windows-lightgrey?style=for-the-badge" />
  <img src="https://img.shields.io/badge/status-active-success?style=for-the-badge" />
</p>

---

## 📌 O projektu

**Fiskalni QR Skener** je Python alat za očitavanje QR kodova sa fiskalnih računa i automatsko otvaranje zvanične stranice za proveru validnosti računa.

Aplikacija radi sa:

- 📷 običnom web kamerom
- 📱 telefonom povezanom kao kamera preko **DroidCam**
- 💻 računarom na kome se skeniranje obrađuje i otvara rezultat u browseru

Nakon uspešnog skeniranja QR koda, aplikacija:

- prepoznaje URL sa računa
- proverava da li vodi ka odgovarajućoj stranici za validaciju
- automatski otvara link u browseru
- omogućava dalji pregled, štampu ili čuvanje stranice kao PDF

---

## ✨ Glavne funkcionalnosti

- 📷 Skeniranje QR kodova u realnom vremenu
- 📱 Podrška za telefon kao kameru preko **DroidCam**
- 🔍 Napredno očitavanje kroz **20 različitih metoda obrade slike**
- 🌐 Automatsko otvaranje stranice za proveru računa
- 💾 Čuvanje kadrova i uspešno obrađenih slika
- 🔁 Sprečavanje duplog otvaranja istog QR koda
- ⚙️ Ručno podešavanje osvetljenja
- 🟩 Vizuelni okvir za lakše centriranje QR koda
- 🧾 Pogodno za fiskalne račune sa QR kodom za proveru ispravnosti

---

## 🧠 Kako radi

Aplikacija koristi kameru priključenu na računar i prikazuje live prikaz.

Kada korisnik pritisne `SPACE`:

1. trenutni kadar se zamrzava
2. generiše se 20 različitih verzija slike
3. svaka verzija se testira na prisustvo QR koda
4. ako se pronađe validan QR kod:
   - ispisuje se URL
   - čuva se uspešna verzija slike
   - otvara se stranica u browseru

Ako QR nije uspešno očitan, aplikacija predlaže dodatne korake kao što su bolje osvetljenje, bliža pozicija ili ručno čuvanje kadra.

---

## 📱 Korišćenje telefona preko DroidCam

Aplikacija može koristiti telefon kao kameru preko **DroidCam**, što je korisno kada telefon ima bolju kameru od laptop/web kamere.

### Potrebno:

- instaliran **DroidCam** na telefonu
- instaliran **DroidCam Client** na računaru
- telefon i računar povezani preko USB-a ili Wi-Fi mreže

### Kako koristiti:

1. Poveži telefon i računar preko **DroidCam**
2. Pokreni DroidCam na telefonu i računaru
3. Proveri da je telefon prepoznat kao kamera na sistemu
4. Pokreni Python aplikaciju
5. Aplikacija koristi kameru dostupnu preko `cv2.VideoCapture(0)`

Ako DroidCam nije prepoznat kao glavna kamera, možda će biti potrebno promeniti indeks kamere u kodu:

```python
cap = cv2.VideoCapture(0)
