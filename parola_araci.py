#!/usr/bin/env python3
"""Parola Aracı

Komut satırından rastgele parola üretir ve parolanın ne kadar güçlü
olduğunu tahmin eder. Sadece Python'un kendi modüllerini kullanır,
internete bağlanmaz ve hiçbir şeyi dosyaya kaydetmez.
"""

import argparse
import getpass
import math
import secrets
import string
import sys

MIN_UZUNLUK = 4
MAX_UZUNLUK = 128

# Ekranda birbirine benzeyen karakterler (büyük i, küçük L, bir, büyük o, sıfır...)
BENZER_KARAKTERLER = set("Il1O0o")

# En çok kullanılan parolalardan kısa bir örnek. Tam liste değil.
YAYGIN_PAROLALAR = {
    "123456", "12345678", "123456789", "1234567890", "password", "parola",
    "sifre", "şifre", "qwerty", "qwerty123", "111111", "000000", "abc123",
    "iloveyou", "admin", "letmein", "welcome", "password1", "123123",
    "1q2w3e4r", "q1w2e3r4", "football", "monkey", "dragon", "master",
}


def karakter_gruplari(kucuk=True, buyuk=True, rakam=True, sembol=True,
                      benzerleri_cikar=False):
    """Seçilen türlere göre karakter gruplarının listesini döndürür."""
    gruplar = []
    if kucuk:
        gruplar.append(string.ascii_lowercase)
    if buyuk:
        gruplar.append(string.ascii_uppercase)
    if rakam:
        gruplar.append(string.digits)
    if sembol:
        gruplar.append(string.punctuation)

    if benzerleri_cikar:
        gruplar = ["".join(c for c in g if c not in BENZER_KARAKTERLER)
                   for g in gruplar]
    return gruplar


def parola_uret(uzunluk=16, kucuk=True, buyuk=True, rakam=True, sembol=True,
                benzerleri_cikar=False):
    """Rastgele bir parola üretir.

    Seçilen her türden (küçük harf, rakam vs.) en az bir karakter girer.
    """
    if not MIN_UZUNLUK <= uzunluk <= MAX_UZUNLUK:
        raise ValueError(
            f"Uzunluk {MIN_UZUNLUK} ile {MAX_UZUNLUK} arasında olmalı."
        )

    gruplar = karakter_gruplari(kucuk, buyuk, rakam, sembol, benzerleri_cikar)
    if not gruplar:
        raise ValueError("En az bir karakter türü seçmelisin.")
    if uzunluk < len(gruplar):
        raise ValueError("Uzunluk, seçilen tür sayısından az olamaz.")

    # Önce her türden bir karakter al, kalanı bütün havuzdan doldur.
    karakterler = [secrets.choice(g) for g in gruplar]
    havuz = "".join(gruplar)
    while len(karakterler) < uzunluk:
        karakterler.append(secrets.choice(havuz))

    # İlk alınanlar hep başta kalmasın diye karıştır.
    secrets.SystemRandom().shuffle(karakterler)
    return "".join(karakterler)


def havuz_boyutu(parola):
    """Parolada kullanılan karakter türlerine bakıp havuz boyutunu tahmin eder."""
    boyut = 0
    if any(c in string.ascii_lowercase for c in parola):
        boyut += 26
    if any(c in string.ascii_uppercase for c in parola):
        boyut += 26
    if any(c in string.digits for c in parola):
        boyut += 10
    if any(c in string.punctuation for c in parola):
        boyut += len(string.punctuation)
    if any(c not in string.printable for c in parola):
        boyut += 32  # ç, ğ, ı, ö, ş, ü gibi harfler için kabaca bir değer
    return boyut


def entropi_hesapla(parola):
    """Parolanın tahmini entropisini bit olarak verir."""
    boyut = havuz_boyutu(parola)
    if boyut == 0:
        return 0.0
    return len(parola) * math.log2(boyut)


def guc_degerlendir(parola):
    """(entropi, etiket, uyarılar) üçlüsünü döndürür."""
    uyarilar = []
    entropi = entropi_hesapla(parola)

    if parola.lower() in YAYGIN_PAROLALAR:
        return 0.0, "Çok zayıf", ["Bu, en sık kullanılan parolalardan biri."]

    if len(parola) < 12:
        uyarilar.append("12 karakterden kısa. Daha uzun bir parola seç.")
    if len(set(parola)) <= len(parola) // 2:
        uyarilar.append("Aynı karakterler çok tekrar ediyor.")
    if parola.isdigit():
        uyarilar.append("Sadece rakamlardan oluşuyor.")
    if parola.isalpha():
        uyarilar.append("Sadece harflerden oluşuyor.")

    # abc, 123, cba, 321 gibi ardışık dizilere bak
    for i in range(len(parola) - 2):
        a, b, c = ord(parola[i]), ord(parola[i + 1]), ord(parola[i + 2])
        if (b - a == 1 and c - b == 1) or (a - b == 1 and b - c == 1):
            uyarilar.append("Ardışık karakterler var (abc, 123 gibi).")
            break

    # Tahmin edilmesi kolay kalıplar varsa puanı biraz kır
    if uyarilar:
        entropi *= 0.75

    if entropi < 28:
        etiket = "Çok zayıf"
    elif entropi < 36:
        etiket = "Zayıf"
    elif entropi < 60:
        etiket = "Orta"
    elif entropi < 80:
        etiket = "Güçlü"
    else:
        etiket = "Çok güçlü"
    return entropi, etiket, uyarilar


def komut_uret(args):
    try:
        for _ in range(args.adet):
            print(parola_uret(
                uzunluk=args.uzunluk,
                kucuk=not args.kucuk_yok,
                buyuk=not args.buyuk_yok,
                rakam=not args.rakam_yok,
                sembol=not args.sembol_yok,
                benzerleri_cikar=args.benzerleri_cikar,
            ))
    except ValueError as hata:
        print(f"Hata: {hata}", file=sys.stderr)
        return 1
    return 0


def komut_kontrol(args):
    # Parolayı komut satırına yazdırmıyoruz, çünkü terminal geçmişinde
    # kalır. getpass yazarken ekranda göstermez.
    parola = getpass.getpass("Kontrol edilecek parolayı yaz (ekranda görünmez): ")
    if not parola:
        print("Hata: Boş parola girdin.", file=sys.stderr)
        return 1

    entropi, etiket, uyarilar = guc_degerlendir(parola)
    print(f"Uzunluk : {len(parola)} karakter")
    print(f"Entropi : yaklaşık {entropi:.1f} bit")
    print(f"Güç     : {etiket}")
    for uyari in uyarilar:
        print(f"  - {uyari}")
    return 0


ORNEKLER = """\
örnekler:
  python parola_araci.py uret                    16 karakterlik 1 parola
  python parola_araci.py uret -u 24 -n 5         24 karakterlik 5 parola
  python parola_araci.py uret --sembol-yok       sembolsüz parola
  python parola_araci.py kontrol                 yazdığın parolanın gücünü ölçer
"""


def arguman_ayristirici():
    ap = argparse.ArgumentParser(
        prog="parola_araci",
        description=("Rastgele ve güvenli parola üretir, istersen kendi "
                     "parolanın ne kadar güçlü olduğunu da söyler."),
        epilog=ORNEKLER,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    alt = ap.add_subparsers(
        dest="komut", required=True, metavar="komut",
        help="uret: yeni parola üret | kontrol: parola gücünü ölç",
    )

    u = alt.add_parser(
        "uret",
        help="yeni parola üret",
        description="Rastgele parola üretir. Hiçbir ayar vermezsen 16 karakterlik, "
                    "harf + rakam + sembol içeren bir parola yazdırır.",
        epilog=ORNEKLER,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    u.add_argument("-u", "--uzunluk", type=int, default=16, metavar="SAYI",
                   help=f"parola kaç karakter olsun ({MIN_UZUNLUK}-{MAX_UZUNLUK}, "
                        "varsayılan: 16)")
    u.add_argument("-n", "--adet", type=int, default=1, metavar="SAYI",
                   help="kaç tane parola üretilsin (varsayılan: 1)")
    u.add_argument("--kucuk-yok", action="store_true",
                   help="küçük harf (a-z) kullanma")
    u.add_argument("--buyuk-yok", action="store_true",
                   help="büyük harf (A-Z) kullanma")
    u.add_argument("--rakam-yok", action="store_true",
                   help="rakam (0-9) kullanma")
    u.add_argument("--sembol-yok", action="store_true",
                   help="sembol (!, @, # gibi) kullanma")
    u.add_argument("--benzerleri-cikar", action="store_true",
                   help="birbirine benzeyen karakterleri (I, l, 1, O, 0, o) çıkar")
    u.set_defaults(islev=komut_uret)

    k = alt.add_parser(
        "kontrol",
        help="parola gücünü ölç",
        description="Yazdığın parolanın gücünü tahmin eder. Parola ekranda "
                    "görünmez ve hiçbir yere kaydedilmez.",
    )
    k.set_defaults(islev=komut_kontrol)
    return ap


def main(argv=None):
    args = arguman_ayristirici().parse_args(argv)
    return args.islev(args)


if __name__ == "__main__":
    sys.exit(main())
