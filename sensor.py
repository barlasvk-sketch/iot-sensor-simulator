# -----------------------------------------------------------------
# ADIM 1: ALET ÇANTAMIZDAN (KÜTÜPHANELERDEN) ALETLERİ ÇIKARMAK
# -----------------------------------------------------------------
import paho.mqtt.client as mqtt
import time
import random
import json

# -----------------------------------------------------------------
# ADIM 2: GEREKLİ AYARLARI YAPMAK (RADYO KULESİ VE FREKANS)
# -----------------------------------------------------------------

# Hangi radyo kulesine (Broker) bağlanacağız? 
# broker.hivemq.com -> Ücretsiz ve çalışan yeni kulemiz
BROKER_ADRESI = "broker.hivemq.com"
# Kuleyle hangi kapıdan (Port) konuşacağız? MQTT için standart kapı 1883'tür.
BROKER_PORT = 1883

# Hangi frekanstan (Topic) yayın yapacağız? 
MQTT_KONUSU = "proje/tarla_1/toprak_nem"

# Kaç saniyede bir radyo anonsu (veri) yapacağız?
GONDERIM_ARALIGI = 5 

# -----------------------------------------------------------------
# ADIM 3: İŞİMİZİ KOLAYLAŞTIRACAK KÜÇÜK GÖREVLER (FONKSİYONLAR) YAZMAK
# -----------------------------------------------------------------

# --- Sahte Sensör Fonksiyonu ---
def get_simulated_soil_moisture():
    """
    Sanki bir sensörden okunuyormuş gibi %30.0 ile %80.0 arası
    rastgele bir toprak nemi değeri (sayısı) üretir.
    """
    nem = random.uniform(30.0, 80.0)
    return round(nem, 1)

# --- Bağlantı Alarmı Fonksiyonu ---
def on_connect(client, userdata, flags, rc):
    """
    Broker'a başarıyla bağlandığımızda bu fonksiyon çalışır.
    """
    if rc == 0:
        print(f"Radyo Kulesine ({BROKER_ADRESI}) başarıyla bağlanıldı.")
        print(f"Yayın yapılacak frekans (topic): {MQTT_KONUSU}")
    else:
        print(f"Bağlantı hatası! Hata kodu: {rc}")

# -----------------------------------------------------------------
# ADIM 4: ANA PROGRAM (TÜM OLAYIN DÖNDÜĞÜ YER)
# -----------------------------------------------------------------
def main():
    
    # 1. Radyo DJ'imizi (Client) oluşturalım.
    client_id = f"sensor_cihazi_{random.randint(0, 1000)}" 
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)

    # 2. DJ'e alarmı (on_connect fonksiyonunu) kuralım.
    client.on_connect = on_connect

    # 3. DJ'e kuleye (Broker) bağlanma emri verelim.
    try:
        client.connect(BROKER_ADRESI, BROKER_PORT, 60) 
    except Exception as e:
        print(f"Kuleye bağlanılamadı: {e}")
        return 

    # 4. DJ'in arka planda kuleyi dinlemesini başlat.
    client.loop_start()

    print("Yayın (veri gönderimi) başlıyor... (Durdurmak için Ctrl+C)")
    
    try:
        # 5. SONSUZ DÖNGÜ
        while True:
            
            # 5a. Sahte sensörden veriyi oku.
            nem_verisi = get_simulated_soil_moisture() 

            # 5b. Veriyi Kargo Paketine (JSON) Koy.
            veri_paketi = {
                "cihaz_id": "tarla_sensor_01", 
                "timestamp": int(time.time()), 
                "nem_yuzdesi": nem_verisi      
            }
            
            # 5c. Koliyi Bantla (JSON String'e Çevir).
            payload = json.dumps(veri_paketi)

            # 5d. YAYINLA! (Anonsu Yap!)
            client.publish(MQTT_KONUSU, payload)
            
            print(f"'{MQTT_KONUSU}' frekansına veri gönderildi -> {payload}")

            # 5e. Bekle.
            time.sleep(GONDERIM_ARALIGI)

    except KeyboardInterrupt:
        print("\nYayın durduruluyor...")
    finally:
        # 6. DJ'in arka plan dinlemesini durdur
        client.loop_stop()
        # 7. DJ'in kuleyle bağlantısını saygıyla kes
        client.disconnect()
        print("Radyo kulesi bağlantısı kapatıldı. Hoşçakal.")

# -----------------------------------------------------------------
# ADIM 5: PROGRAMI BAŞLATMAK İÇİN TETİKLEYİCİ
# -----------------------------------------------------------------
if __name__ == "__main__":
    main()