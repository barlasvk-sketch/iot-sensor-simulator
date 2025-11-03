import paho.mqtt.client as mqtt

# --- AYARLAR ---
# Kulemiz aynı kule
BROKER_ADRESI = "broker.hivemq.com"
BROKER_PORT = 1883
# Dinleyeceğimiz frekans (sensor.py'deki ile AYNI OLMALI)
MQTT_KONUSU = "proje/tarla_1/toprak_nem"

# --- GÖREVLER (FONKSİYONLAR) ---

def on_connect(client, userdata, flags, rc):
    """
    Kuleye (Broker) başarıyla bağlandığımızda bu fonksiyon çalışır.
    """
    if rc == 0:
        print(f"Radyo Kulesine ({BROKER_ADRESI}) başarıyla bağlanıldı.")
        # Bağlantı başarılı olur olmaz, DİNLEMEK İSTEDİĞİMİZ FREKANSA ABONE OLUYORUZ.
        client.subscribe(MQTT_KONUSU)
        print(f"'{MQTT_KONUSU}' frekansı dinleniyor...")
    else:
        print(f"Bağlantı hatası! Hata kodu: {rc}")

def on_message(client, userdata, msg):
    """
    Bu en önemlisi! Abone olduğumuz frekansa (konuya) bir mesaj GELDİĞİNDE bu fonksiyon çalışır.
    """
    # msg.payload -> Gelen asıl veri, ama "b'{}'" formatındadır (byte string)
    # .decode('utf-8') -> Bu veriyi bizim okuyabileceğimiz normal metne çevirir.
    gelen_mesaj = msg.payload.decode('utf-8')
    
    print(f"MESAJ GELDİ! -> {gelen_mesaj}")

# --- ANA PROGRAM ---
def main():
    # 1. Dinleyici DJ'imizi (Client) oluşturalım.
    client_id = f"dinleyici_cihaz_{random.randint(0, 1000)}" # ID'si farklı olmalı
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)

    # 2. Görevleri ata
    client.on_connect = on_connect   # Bağlanınca ne yapacak?
    client.on_message = on_message   # Mesaj gelince ne yapacak?

    # 3. Kuleye bağlanmayı dene
    try:
        client.connect(BROKER_ADRESI, BROKER_PORT, 60)
    except Exception as e:
        print(f"Kuleye bağlanılamadı: {e}")
        return

    # 4. 'loop_forever()' -> Bu komut, programı sonsuza kadar çalıştırır
    # ve sürekli olarak gelen mesajları dinler. 'loop_start'tan farklıdır.
    # Bu programın tek işi dinlemek olduğu için bunu kullanıyoruz.
    print(f"{BROKER_ADRESI} adresindeki kuleye bağlanılıyor...")
    client.loop_forever()

# --- Programı Başlat ---
# (random kütüphanesini client_id için kullandık, onu da ekleyelim)
import random
if __name__ == "__main__":
    main()