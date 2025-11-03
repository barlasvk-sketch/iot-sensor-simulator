# IoT Sensör Simülatörü (MQTT Projesi)

Bu proje, bir IoT cihazının (sensör) MQTT protokolü üzerinden nasıl veri yayınladığını (publish) ve bir istemcinin (client) bu veriye nasıl abone olduğunu (subscribe) simüle eder.

Proje, donanıma ihtiyaç duymadan MQTT'nin temel mantığını anlamak için iki ayrı Python script'inden oluşur.

## Bileşenler

1.  **`sensor.py` (Yayıncı - Publisher):**
    * Sahte toprak nemi verisi (`%30` - `%80` arası) üretir.
    * Bu veriyi `JSON` formatında paketler (örn: `{"cihaz_id": "...", "nem_yuzdesi": ...}`).
    * `broker.hivemq.com` adresindeki genel MQTT broker'ına, `proje/tarla_1/toprak_nem` konusuna (topic) her 5 saniyede bir yayınlar.

2.  **`listener.py` (Abone - Subscriber):**
    * Aynı broker'a (`broker.hivemq.com`) bağlanır.
    * `proje/tarla_1/toprak_nem` konusuna abone olur.
    * Gelen tüm mesajları yakalar ve terminale yazdırır.

## Nasıl Çalıştırılır?

Bu projeyi test etmek için iki ayrı terminale ihtiyacınız vardır:

### 1. Terminal 1 (Sensör - Veri Gönderici):
```bash
python sensor.py
