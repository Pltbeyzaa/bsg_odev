# Avalanche-RNG: Hash Tabanlı Güvenli Sayı Üretimi

## 📋 Giriş

Bu proje, **Bilgi Sistemleri Güvenliği** dersi kapsamında geliştirilmiş özgün bir **Rastgele Sayı Üreteci (RNG - Random Number Generator)** algoritmasıdır. Proje, standart Python kütüphanelerindeki rastgele sayı üreteçleri yerine, kriptografik hash fonksiyonlarının güvenlik özelliklerinden yararlanan modern bir yaklaşım sunmaktadır.

**Amaç:** SHA-256 özet fonksiyonunun **Çığ Etkisi (Avalanche Effect)** özelliğini kullanarak, tahmin edilebilirliği minimize eden ve kriptografik olarak güçlü bir sayı üretim mekanizması tasarlamaktır.

---

## 🔄 Algoritma Mantığı (Adım Adım)

Algoritma, **Hash Chain (Hash Zinciri)** yapısı üzerine kurulmuştur. İşleyiş süreci şu adımlardan oluşur:

1. **Başlangıç Durumu (Initialization):**
   - Kullanıcı tarafından belirlenen seed string ile sistem zamanı birleştirilir
   - Bu birleşim, algoritmanın ilk durumunu (state) oluşturur
   - Her çalıştırmada farklı bir başlangıç değeri garantilenir

2. **Hash İşlemi (Hashing):**
   - Mevcut state değeri ile bir sayaç (counter) birleştirilir
   - Bu veri **SHA-256** hash fonksiyonuna girdi olarak verilir
   - Hash fonksiyonu, 256-bit (64 hex karakter) uzunluğunda bir çıktı üretir

3. **Tamsayıya Dönüşüm (Integer Conversion):**
   - Hash çıktısının ilk 8 hex karakteri alınır
   - Bu hex değer, 16 tabanından 10 tabanına çevrilerek bir tamsayıya dönüştürülür
   - Bu işlem, rastgele sayı üretimi için ham değeri sağlar

4. **Hash Zinciri Güncellemesi (Chain Update):**
   - Üretilen hash değerinin tamamı, yeni state olarak atanır
   - Bu sayede her iterasyonda tamamen farklı bir durum oluşur
   - Sayaç (counter) bir artırılarak bir sonraki iterasyona hazırlanılır

5. **Aralık Normalizasyonu (Range Normalization):**
   - Ham tamsayı değeri, kullanıcının istediği aralığa (min-max) modülo işlemi ile sığdırılır
   - Sonuç, belirtilen aralık içinde rastgele bir sayı olarak döndürülür

### 🔗 Hash Chain Yapısı

Algoritmanın temel gücü, **Hash Chain** yapısından gelmektedir. Her üretilen sayı, bir önceki hash değerine bağlıdır ve bu bağımlılık, deterministik olmayan bir zincir oluşturur:

```
Seed + Time → [SHA-256] → Hash₁ → Int₁
                              ↓
                         Hash₁ + Counter → [SHA-256] → Hash₂ → Int₂
                                                              ↓
                                                         Hash₂ + Counter → [SHA-256] → Hash₃ → Int₃
```

---

## 🛡️ Neden Bu Algoritma Seçildi? (Teknik Savunma)

### 1. Çığ Etkisi (Avalanche Effect)

**Çığ Etkisi**, kriptografik hash fonksiyonlarının en önemli özelliklerinden biridir. Bu özellik şu anlama gelir:

> **Girdideki 1 bitlik değişim, çıktının yaklaşık %50'sini değiştirir.**

**Güvenlik Açısından Önemi:**
- **Tahmin Edilemezlik:** Girdideki en küçük değişiklik bile tamamen farklı bir çıktı üretir
- **Korelasyon Yokluğu:** Ardışık sayılar arasında matematiksel bir ilişki kurulamaz
- **Entropi Korunumu:** Her hash işlemi, yüksek entropi seviyesini korur

**Örnek Senaryo:**
```
Girdi₁: "Hello" → Hash: a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e
Girdi₂: "Hellp" → Hash: 8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4
                    ↑ (Sadece 1 karakter farkı)
                    ↓
            Çıktılar tamamen farklı! (64 karakterden ~32'si değişti)
```

### 2. Lineer Olmayan Yapı (Non-Linear Structure)

Geleneksel RNG algoritmaları (örneğin **LCG - Linear Congruential Generator**) lineer formüller kullanır:

```
LCG: Xₙ₊₁ = (a × Xₙ + c) mod m
```

Bu tür algoritmalar:
- ❌ **Tersine çevrilebilir:** Önceki değerler tahmin edilebilir
- ❌ **Periyodik:** Belirli bir süre sonra tekrar eder
- ❌ **Korelasyonlu:** Ardışık değerler arasında matematiksel ilişki vardır

**Hash Tabanlı Yaklaşım:**
- ✅ **Tek Yönlü (One-Way):** Hash'ten orijinal veriyi geri elde etmek hesaplama açısından imkansızdır
- ✅ **Kaotik:** Deterministik görünse de, küçük değişiklikler büyük farklılıklar yaratır
- ✅ **Korelasyonsuz:** Ardışık çıktılar arasında öngörülebilir bir ilişki yoktur

### 3. Kriptografik Güç

SHA-256, **NIST (National Institute of Standards and Technology)** tarafından onaylanmış bir kriptografik hash fonksiyonudur. Bu durum:
- Güvenlik standartlarına uygunluğu garanti eder
- Kriptanaliz saldırılarına karşı direnç sağlar
- Endüstriyel uygulamalarda yaygın kullanımı vardır

---

## 🚀 Kurulum ve Kullanım

### Gereksinimler

Bu proje, yalnızca Python standart kütüphanelerini kullanmaktadır:
- `hashlib` (SHA-256 için)
- `time` (Zaman tabanlı seed için)

**Python Sürümü:** Python 3.6 veya üzeri

### Kurulum

Projeyi klonlayın veya `sayı_uret.py` dosyasını indirin:

```bash
# Proje dizinine gidin
cd Beyza_Sayı_Üretme

# Python dosyasını çalıştırın
python sayı_uret.py
```

### Kullanım Örneği

```python
from sayı_uret import HashTabanliRNG

# RNG nesnesi oluştur (isteğe bağlı seed belirle)
rng = HashTabanliRNG(seed_str="OzelTohumDegeri")

# Belirli bir aralıkta rastgele sayı üret
sayi = rng.randint(0, 100)
print(f"Üretilen sayı: {sayi}")

# Birden fazla sayı üret
for i in range(10):
    sayi = rng.randint(1, 50)
    print(f"{i+1}. sayı: {sayi}")
```

### Çıktı Örneği

```
SHA-256 Tabanlı Güvenli RNG (The Avalanche):
--------------------------------------------------
1. Sayı: 42    (Kaynak Hash: a591a6d40b...)
2. Sayı: 17    (Kaynak Hash: 8f43434664...)
3. Sayı: 89    (Kaynak Hash: 2c65bf0bcd...)
--------------------------------------------------
```

---

## 📊 Algoritma Akış Diyagramı

```
┌─────────────────────────────────────────────────────────────┐
│                    AVALANCHE-RNG AKIŞI                       │
└─────────────────────────────────────────────────────────────┘

    [Başlangıç]
         │
         ├─→ Seed String + System Time
         │
         ↓
    ┌─────────────────┐
    │  Initial State  │
    └─────────────────┘
         │
         ├─→ State + Counter
         │
         ↓
    ┌─────────────────┐
    │   SHA-256 Hash  │  ◄─── Çığ Etkisi Aktif
    │   Fonksiyonu    │
    └─────────────────┘
         │
         ├─→ 256-bit Hash (64 hex karakter)
         │
         ↓
    ┌─────────────────┐
    │ Hex → Integer   │  ◄─── İlk 8 karakter
    │   Dönüşümü      │
    └─────────────────┘
         │
         ├─→ Ham Tamsayı Değeri
         │
         ↓
    ┌─────────────────┐
    │  Modülo İşlemi  │  ◄─── Aralık Normalizasyonu
    │  (min, max)     │
    └─────────────────┘
         │
         ├─→ Rastgele Sayı
         │
         ↓
    ┌─────────────────┐
    │  State Update   │  ◄─── Hash Chain Güncellemesi
    │  (Hash → State) │
    └─────────────────┘
         │
         ├─→ Counter++
         │
         └─→ [Sonraki İterasyon]
```

---

## 🔬 Teknik Detaylar

### Hash Fonksiyonu: SHA-256

- **Çıktı Boyutu:** 256 bit (32 byte, 64 hex karakter)
- **Girdi Boyutu:** Sınırsız (bu projede state + counter)
- **Güvenlik Seviyesi:** Kriptografik olarak güvenli
- **Hız:** Modern işlemcilerde yüksek performans

### Entropi Kaynağı

1. **Kullanıcı Seed'i:** Belirlenebilir ancak özelleştirilebilir
2. **Sistem Zamanı:** Her çalıştırmada farklı başlangıç değeri
3. **Hash Chain:** Her iterasyonda yeni entropi üretimi

### Deterministik vs. Rastgelelik

- **Deterministik:** Aynı seed ve aynı sırada çağrılırsa aynı sonuçlar üretilir
- **Rastgelelik:** Farklı seed'ler veya farklı zamanlarda tamamen farklı sonuçlar
- **Pratik Kullanım:** Güvenlik uygulamaları için uygun (seed gizli tutulmalıdır)

---

## 📚 Referanslar ve Kavramlar

- **SHA-256:** Secure Hash Algorithm 256-bit
- **Avalanche Effect:** Çığ Etkisi - Girdideki küçük değişikliğin çıktıda büyük değişiklik yaratması
- **Hash Chain:** Hash Zinciri - Her hash'in bir önceki hash'e bağlı olduğu yapı
- **Entropy:** Entropi - Rastgelelik veya belirsizlik ölçüsü
- **One-Way Function:** Tek yönlü fonksiyon - Geri döndürülemez matematiksel işlem

---

## 👤 Geliştirici Notları

Bu proje, **Bilgi Sistemleri Güvenliği** dersi kapsamında, kriptografik hash fonksiyonlarının pratik uygulamalarını göstermek amacıyla geliştirilmiştir. Algoritma, eğitimsel amaçlıdır ve gerçek dünya uygulamalarında ek güvenlik önlemleri (seed yönetimi, sıfırlama mekanizmaları vb.) gerekebilir.

---

## 📝 Lisans

Bu proje eğitim amaçlıdır ve açık kaynak kodludur.

---

**Not:** Bu README dosyası, projenin teknik detaylarını ve güvenlik özelliklerini açıklamak için hazırlanmıştır. Sorularınız veya önerileriniz için lütfen iletişime geçin.

