import cv2
import numpy as np
from pyzbar.pyzbar import decode
import webbrowser
import os
import time
from datetime import datetime
import warnings

# Isključi pyzbar warning-e
warnings.filterwarnings('ignore')
os.environ['ZBAR_CFG_ENABLE'] = '0'  # Pokušaj da isključiš debug output


# ---------------------------------------------------------
#  PODEŠAVANJE
# ---------------------------------------------------------
desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
folder_za_cuvanje = os.path.join(desktop_path, "Skenirani_Racuni")
os.makedirs(folder_za_cuvanje, exist_ok=True)


# ---------------------------------------------------------
#  EKSTREMNA OBRADA - 20 RAZLIČITIH METODA
# ---------------------------------------------------------
def generiši_20_verzija(frame: np.ndarray):
    """Generiše 20 različitih verzija slike za maksimalnu šansu detekcije"""
    
    verzije = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # --- VERZIJA 1-3: Različiti threshold nivoi ---
    for thresh in [100, 127, 150]:
        _, binary = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
        verzije.append(('threshold_' + str(thresh), binary))
    
    # --- VERZIJA 4-6: Adaptive threshold sa različitim blokovima ---
    for block_size in [31, 51, 71]:
        adapt = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, block_size, 11)
        verzije.append((f'adaptive_{block_size}', adapt))
    
    # --- VERZIJA 7-8: CLAHE sa različitim pojačanjima ---
    for clip in [2.0, 4.0]:
        clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        verzije.append((f'clahe_{clip}', enhanced))
    
    # --- VERZIJA 9-10: Otsu threshold ---
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    verzije.append(('otsu_normal', otsu))
    verzije.append(('otsu_inverted', cv2.bitwise_not(otsu)))
    
    # --- VERZIJA 11-12: Upscaling + obrada ---
    upscaled = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    _, up_binary = cv2.threshold(upscaled, 127, 255, cv2.THRESH_BINARY)
    verzije.append(('upscaled_2x', up_binary))
    
    upscaled3 = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    _, up3_binary = cv2.threshold(upscaled3, 127, 255, cv2.THRESH_BINARY)
    verzije.append(('upscaled_3x', up3_binary))
    
    # --- VERZIJA 13: Normalizacija ---
    normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    verzije.append(('normalized', normalized))
    
    # --- VERZIJA 14-15: Kontrast boost ---
    for alpha in [1.5, 2.5]:
        contrasted = cv2.convertScaleAbs(gray, alpha=alpha, beta=-50)
        verzije.append((f'contrast_{alpha}', contrasted))
    
    # --- VERZIJA 16: Denoising ---
    denoised = cv2.fastNlMeansDenoising(gray, None, h=10)
    verzije.append(('denoised', denoised))
    
    # --- VERZIJA 17: Bilateral filter ---
    bilateral = cv2.bilateralFilter(gray, 9, 75, 75)
    verzije.append(('bilateral', bilateral))
    
    # --- VERZIJA 18: Median blur ---
    median = cv2.medianBlur(gray, 5)
    verzije.append(('median', median))
    
    # --- VERZIJA 19: Morphological gradient ---
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morph = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
    verzije.append(('morphological', morph))
    
    # --- VERZIJA 20: Original color (bez obrade) ---
    verzije.append(('original_color', frame))
    
    return verzije


def skeniraj_sve_verzije(verzije, show_progress=True):
    """Pokušava da pročita QR kod iz svih verzija"""
    
    total = len(verzije)
    
    for idx, (naziv, img) in enumerate(verzije):
        if show_progress:
            print(f"  [{idx+1}/{total}] Testiram: {naziv}...", end='\r')
        
        try:
            # Probaj sa pyzbar
            decoded = decode(img, symbols=[0])  # 0 = QR-CODE samo
            
            if decoded:
                data = decoded[0].data.decode('utf-8')
                print(f"\n  ✓✓✓ PRONAĐEN! Metoda: {naziv}")
                return {
                    'success': True,
                    'metoda': naziv,
                    'data': data,
                    'image': img
                }
        except Exception as e:
            pass
    
    print("\n  ✗ Nijedna verzija nije uspela")
    return {'success': False}


# ---------------------------------------------------------
#  INTERAKTIVNI REŽIM SA MANUELNIM KADROM
# ---------------------------------------------------------
def interaktivni_skener():
    
    cap = cv2.VideoCapture(0)
    
    # Postavi najvišu rezoluciju
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    
    # Pojačaj osvetljenje i kontrast
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 170)
    cap.set(cv2.CAP_PROP_CONTRAST, 60)
    cap.set(cv2.CAP_PROP_SATURATION, 40)
    cap.set(cv2.CAP_PROP_GAIN, 50)
    
    used_codes = []
    
    print("\n" + "="*70)
    print("  NAPREDNI QR SKENER - 20 METODA OBRADE")
    print("="*70)
    print("\n  📋 VAŽNE INSTRUKCIJE:")
    print("  ┌─────────────────────────────────────────────────────────────┐")
    print("  │ 1. QR kod mora biti RAVNO ispred kamere (bez nagiba)       │")
    print("  │ 2. Rastojanje: 10-20cm od kamere                            │")
    print("  │ 3. JAKO VAŽNO: Dobro osvetljenje (idealno dnevna svetlost)  │")
    print("  │ 4. Sačekaj 2-3 sekunde da se slika stabilizuje             │")
    print("  │ 5. QR kod treba da zauzme bar 30% ekrana                    │")
    print("  └─────────────────────────────────────────────────────────────┘")
    print("\n  ⌨️  Kontrole:")
    print("     SPACE - Zamrzni i skeniraj (20 metoda)")
    print("     s     - Sačuvaj trenutni kadar kao PNG")
    print("     b     - Pojačaj brightness")
    print("     d     - Smanji brightness")
    print("     q     - Izlaz")
    print("="*70 + "\n")
    
    brightness = 170
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Greška: Ne mogu da čitam sa kamere!")
            break
        
        h, w = frame.shape[:2]
        
        # Crtaj centralni kvadrat (vodič)
        margin_x, margin_y = w//4, h//4
        cv2.rectangle(frame, 
                     (margin_x, margin_y), 
                     (w - margin_x, h - margin_y),
                     (0, 255, 0), 3)
        
        # Crtaj linije za fini centriranje
        cv2.line(frame, (w//2, margin_y), (w//2, h - margin_y), (0, 255, 0), 1)
        cv2.line(frame, (margin_x, h//2), (w - margin_x, h//2), (0, 255, 0), 1)
        
        # Info tekst
        cv2.putText(frame, "Centriraj QR kod ovde", 
                   (margin_x + 20, margin_y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.putText(frame, f"Brightness: {brightness} | Pritisni SPACE za sken", 
                   (10, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.putText(frame, f"Skenirano racuna: {len(used_codes)}", 
                   (10, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        cv2.imshow('QR Skener', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        
        elif key == ord('b'):
            brightness = min(255, brightness + 10)
            cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
            print(f"[BRIGHTNESS] Postavljeno na {brightness}")
        
        elif key == ord('d'):
            brightness = max(0, brightness - 10)
            cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
            print(f"[BRIGHTNESS] Postavljeno na {brightness}")
        
        elif key == ord('s'):
            # Sačuvaj kadar
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(folder_za_cuvanje, f"KADAR_{timestamp}.png")
            cv2.imwrite(path, frame)
            print(f"\n[SAVED] Kadar sačuvan: {path}")
            print("  → Upload na https://zxing.org/w/decode za test\n")
        
        elif key == ord(' '):  # SPACE - glavna funkcija
            print("\n" + "="*70)
            print("  🔍 ZAPOČINJEM DUBINSKU ANALIZU...")
            print("="*70)
            
            # Sačuvaj kadar za analizu
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            freeze_path = os.path.join(folder_za_cuvanje, f"FREEZE_{timestamp}.png")
            cv2.imwrite(freeze_path, frame)
            print(f"  📸 Kadar sačuvan: {freeze_path}")
            
            # Generiši sve verzije
            print(f"  ⚙️  Generišem 20 verzija obrade...")
            verzije = generiši_20_verzija(frame)
            
            # Skeniraj sve
            print(f"  🔎 Skeniram sve verzije...")
            rezultat = skeniraj_sve_verzije(verzije, show_progress=True)
            
            if rezultat['success']:
                data = rezultat['data']
                
                if "purs.gov.rs" in data:
                    print(f"\n  {'='*66}")
                    print(f"  ✓✓✓ RAČUN USPEŠNO PROČITAN!")
                    print(f"  {'='*66}")
                    print(f"  URL: {data}")
                    print(f"  Metoda koja je uspela: {rezultat['metoda']}")
                    print(f"  {'='*66}\n")
                    
                    # Sačuvaj uspešnu verziju
                    success_path = os.path.join(
                        folder_za_cuvanje, 
                        f"SUCCESS_{rezultat['metoda']}_{timestamp}.png"
                    )
                    cv2.imwrite(success_path, rezultat['image'])
                    print(f"  💾 Uspešna verzija sačuvana: {success_path}\n")
                    
                    if data not in used_codes:
                        webbrowser.open(data)
                        used_codes.append(data)
                        print('\a')  # Beep
                        time.sleep(2)
                else:
                    print(f"\n  ⚠️  Pronađen QR ali NIJE purs.gov.rs:")
                    print(f"     {data}\n")
            else:
                print(f"\n  {'='*66}")
                print(f"  ❌ QR KOD NIJE DETEKTOVAN")
                print(f"  {'='*66}")
                print(f"  🔧 Pokušaj sledeće:")
                print(f"     • Pojačaj osvetljenje (idi pod lampu)")
                print(f"     • Pritisni 'b' za brightness ++")
                print(f"     • QR bliže kameri (ali ne previše)")
                print(f"     • Drži račun/telefon potpuno RAVNO")
                print(f"     • Proveri je li QR kod fizički čitljiv (oštećen?)")
                print(f"  {'='*66}\n")
                print(f"  💡 TIP: Pritisni 's' da sačuvaš kadar, pa probaj:")
                print(f"     https://zxing.org/w/decode")
                print(f"  {'='*66}\n")
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n{'='*70}")
    print(f"  📊 ZAVRŠENO")
    print(f"  Ukupno skeniranih računa: {len(used_codes)}")
    print(f"  Svi kadri sačuvani u: {folder_za_cuvanje}")
    print(f"{'='*70}\n")


# ---------------------------------------------------------
if __name__ == "__main__":
    interaktivni_skener()