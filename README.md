# Parola Aracı

Terminalden rastgele parola üreten ve parolanın ne kadar güçlü olduğunu tahmin eden küçük bir Python programı.

Özellikleri:

- Dışarıdan hiçbir paket kurmaya gerek yok, sadece Python yeterli.
- İnternete bağlanmaz.
- Ürettiğin ya da kontrol ettiğin parolaları dosyaya yazmaz, saklamaz.
- Parolaları `secrets` modülüyle üretir. Bu modül işletim sisteminin güvenli rastgele sayı kaynağını kullanır.
- Parola kontrolünde parolayı komuta yazmazsın, program ayrıca sorar ve ekranda göstermez. Böylece terminal geçmişinde kalmaz.

## Gereksinimler

Python 3.8 veya daha yeni bir sürüm. Python yüklü mü diye bakmak için:

```
python --version
```

Mac veya Linux'ta bu çalışmazsa `python3 --version` dene. Aşağıdaki komutlarda `python` yerine `python3` yazman gerekebilir.

## Kullanım

Önce projenin klasörüne gir:

```
cd parola-araci
```

Parola üretmek için:

```
python parola_araci.py uret
```

Birkaç örnek daha:

```
# 24 karakterlik 5 parola
python parola_araci.py uret -u 24 -n 5

# sembolsüz parola
python parola_araci.py uret --sembol-yok

# I, l, 1, O, 0, o gibi karışan karakterler olmasın
python parola_araci.py uret --benzerleri-cikar
```

Bir parolanın gücünü ölçmek için:

```
python parola_araci.py kontrol
```

Program parolayı ister, yazarken ekranda görünmez. Sonunda uzunluğu, tahmini entropiyi ve güç seviyesini yazar.

Bütün seçenekleri görmek için:

```
python parola_araci.py --help
python parola_araci.py uret --help
```

### `uret` seçenekleri

| Seçenek | Ne yapar |
|---|---|
| `-u`, `--uzunluk` | Parola uzunluğu (4 ile 128 arası, varsayılan 16) |
| `-n`, `--adet` | Kaç parola üretileceği (varsayılan 1) |
| `--kucuk-yok` | Küçük harf kullanmaz |
| `--buyuk-yok` | Büyük harf kullanmaz |
| `--rakam-yok` | Rakam kullanmaz |
| `--sembol-yok` | Sembol kullanmaz |
| `--benzerleri-cikar` | Birbirine benzeyen karakterleri çıkarır |

## Testler

```
python -m unittest -v
```

## Bilinmesi gerekenler

- Güç ölçümü basit bir tahmindir. Sözlük saldırılarını tam olarak hesaba katmaz ve içindeki yaygın parola listesi çok kısadır.
- Parolalarını bir parola yöneticisinde sakla ve mümkünse iki adımlı doğrulamayı aç.

## Lisans

MIT
