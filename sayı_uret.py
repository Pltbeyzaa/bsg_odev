import time
import hashlib

class HashTabanliRNG:
    def __init__(self, seed_str="SiberGuvenlik2025"):
        """
        SHA-256 Hash fonksiyonunun 'Avalanche Effect' (Çığ Etkisi) 
        özelliğini kullanan modern bir RNG.
        """
        # Başlangıç tohumunu ve zamanı birleştirip ilk durumu oluşturuyoruz
        baslangic = f"{seed_str}-{time.time()}"
        self.state = baslangic
        self.counter = 0

    def _get_hash_int(self):
        """
        Mevcut durumu hash'leyip tamsayıya çevirir.
        """
        # 1. Veriyi hazırla: State + Sayaç (Her seferinde değişsin diye)
        data = f"{self.state}-{self.counter}".encode('utf-8')
        
        # 2. SHA-256 uygula (Çıktı tamamen kaotik bir hex string'dir)
        hash_object = hashlib.sha256(data)
        hex_dig = hash_object.hexdigest()
        
        # 3. Hex string'in bir kısmını (ilk 8 karakter) alıp tamsayıya çevir
        # 16 tabanından 10 tabanına çeviriyoruz.
        random_int = int(hex_dig[:8], 16)
        
        # 4. State'i güncelle (Zincirleme etkisi için hash'in kendisi yeni state olur)
        self.state = hex_dig
        self.counter += 1
        
        return random_int

    def randint(self, min_val, max_val):
        """
        İstenilen aralıkta sayı üretir.
        """
        raw_val = self._get_hash_int()
        
        # Modülo işlemi ile aralığa sığdır
        aralik = max_val - min_val + 1
        return min_val + (raw_val % aralik)

# --- TEST KISMI ---

rng = HashTabanliRNG(seed_str="OdevIcinOzelTohum")

print("SHA-256 Tabanlı Güvenli RNG (The Avalanche):")
print("-" * 50)

dagilim = []
for i in range(1):
    sayi = rng.randint(0, 100)
    dagilim.append(sayi)
    # Görsel olarak ne kadar karışık olduğunu görmek için hash'in başını da yazdıralım
    print(f"{i+1}. Sayı: {sayi:<5} (Kaynak Hash: {rng.state[:10]}...)")

print("-" * 50)
print(f"Liste: {dagilim}")