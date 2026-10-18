import string
import unittest

import parola_araci as pa


class ParolaUretTesti(unittest.TestCase):
    def test_uzunluk(self):
        for n in (4, 12, 16, 64, 128):
            self.assertEqual(len(pa.parola_uret(n)), n)

    def test_her_gruptan_en_az_bir_karakter(self):
        for _ in range(200):
            p = pa.parola_uret(8)
            self.assertTrue(any(c in string.ascii_lowercase for c in p))
            self.assertTrue(any(c in string.ascii_uppercase for c in p))
            self.assertTrue(any(c in string.digits for c in p))
            self.assertTrue(any(c in string.punctuation for c in p))

    def test_sadece_rakam(self):
        p = pa.parola_uret(10, kucuk=False, buyuk=False, sembol=False)
        self.assertTrue(p.isdigit())

    def test_benzer_karakterler_cikarilir(self):
        for _ in range(200):
            p = pa.parola_uret(32, benzerleri_cikar=True)
            self.assertFalse(set(p) & pa.BENZER_KARAKTERLER)

    def test_gecersiz_uzunluk(self):
        with self.assertRaises(ValueError):
            pa.parola_uret(3)
        with self.assertRaises(ValueError):
            pa.parola_uret(129)

    def test_grup_secilmezse_hata(self):
        with self.assertRaises(ValueError):
            pa.parola_uret(10, False, False, False, False)

    def test_parolalar_birbirinden_farkli(self):
        self.assertEqual(len({pa.parola_uret(16) for _ in range(100)}), 100)


class GucTesti(unittest.TestCase):
    def test_yaygin_parola_cok_zayif(self):
        _, etiket, _ = pa.guc_degerlendir("password")
        self.assertEqual(etiket, "Çok zayıf")

    def test_ardisik_uyarisi(self):
        _, _, uyarilar = pa.guc_degerlendir("Abcdef!9xyZ")
        self.assertTrue(any("Ardışık" in u for u in uyarilar))

    def test_uretilen_uzun_parola_guclu(self):
        _, etiket, _ = pa.guc_degerlendir(pa.parola_uret(24))
        self.assertIn(etiket, ("Güçlü", "Çok güçlü"))

    def test_entropi_uzunlukla_artar(self):
        self.assertGreater(pa.entropi_hesapla("aB3$aB3$aB3$"),
                           pa.entropi_hesapla("aB3$"))

    def test_bos_parola_entropisi_sifir(self):
        self.assertEqual(pa.entropi_hesapla(""), 0.0)


class CLITesti(unittest.TestCase):
    def test_uret_komutu(self):
        self.assertEqual(pa.main(["uret", "-u", "20", "-n", "3"]), 0)

    def test_gecersiz_uzunluk_hata_kodu(self):
        self.assertEqual(pa.main(["uret", "-u", "2"]), 1)


if __name__ == "__main__":
    unittest.main()
