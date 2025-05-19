# **Yüksel-İlhan Alanyalı Fen Lisesi** TÜBİTAK 4006-B Bilim Fuarı Projesi kaynak kodu

## **"Bilgisayarla görme ve Yapay zekâ ile insan ayırt edebilen modern güvenlik kamerası sistemi"**

### TÜBİTAK 4006-B Projesinin Özeti ve Yöntemi:
>Kamera sistemi, görünrüleri açık kaynak yapay zeka modelleriyle işleyerek obje tanımlaması yapar. Eğer bir insan 10 saniyeden fazla tespit edilirse, sistem kullanıcıya uyarı gönderir. Sistem iki ana bileşenden oluşur: Kamera Düzeneği (ESP32-CAM ve OV260 kamera) ve İşleme Merkezi (Raspberry Pi 5). Kamera verileri İşleme Merkezi’ne iletilir; burada işlenip SD karta kaydedilir ve şüpheli durumlar kullanıcıya bildirilir. Kamera modülü için Estetik ve koruma amacıyla 3D yazıcıdan üretilmiş parçalar kullanılmıştır. Fakat Raspberry Pi5’in soğutma gereksinimlerini karşılamak için original üretim kabı kullanılmıştır Bu sistem, hareket algılama yerine yapay zeka temelli görüntü işleme ile yanlış negatifleri azaltmayı hedefler.

>Projemizde işleme merkezi için farklı yapay zeka işleme kapasitesine sahip modüllerinin yapay zeka performanslarını inceledik ve düşük maaliyetli ve kullanım kolaylığı sebebiyle Raspberry Pi 5’I seçtik. Kamera modülü için ise kompakt tasarımı, kullanım kolaylığı ve düşük maaliyetli olması sebebiyle ESP32CAM geliştirme kardını seçtik. İşleme Merkezi’nin soğutma ihtiyaçlarını karşılamak için Raspberry Pi 5’in orijinal içinde fan monteli kabını kullandık. Kamera Modülü için 3 boyutlu yazıcıdan PLA filament ile CAD program ile tasarladığımız kabı bastırdık. Daha sonra ESP32Cam’in webserver özelliği ile Raspberry Pi5’e kamera verisi iletmesini sağladık. Raspberry Pi 5’te Python kodu ile OpenCV kütüphanesi ile ESP32CAM’in kamera verilerine erişen, sonra bu verileri Google’ın geliştirdiği açık kaynaklı Mediapipe yapay zeka modelleri ile işleyen ve elde edilen sonuçları Raspberry Pi’ın dahili SD kart’ına kaydeden, uyarı şartlarını(10> saniye boyunca insan algılama) karşıladığı durumda MQTT protokolü ile kullanıcıların telefonlarındaki uygulamalar aracılıyla bildirim gönderebilen bir program yazdık. Bu program test ettik ve sonuçları kaydettik. Kamera Sistemi’nin görüntü güncelleme aralığılını saniyede 10 kare olacak şekilde ayarladık. 

### Geliştiren Öğrenciler

- Erdem ÖZTÜRK
- Yağız Adem ALMALI

## Özellikler

- [x] Küçük boyutlu ve Wi-Fi özelliği bulunan ESP32CAM geliştirme kartı ile görüntü alınması ve HTTP protokolü ile yayın yapılması
- [x] Raspberry Pi'ın donanımı üzerinde Google'ın geliştirdiği ve eğittiği açık kaynaklı Mediapipe **MobileNetV2** yapay zeka modeli sayesinde gömülü sistemlerde yapay zeka ile insan tanımlama
- [x] Uyarı durumunu[^1] karşıladığında MQTT protokolü ve bu protokolü uygulayan **mosquitto** ve **paho-mqtt** açık kaynaklı yazılımları sayesinde `alert/person_detected` konusuna abone olan cihazlara (PC,Telefon,Tablet vb) uyarı gönderilmesi

### Gelecekte yapılabilinecek iyileştirmeler

- [ ] Görüntülerin ve tespit verilerinin RPİ5'ın MicroSD kardına kaydedilmesi
- [ ] RPİ 5'te yerleşik bulunan Ethernet portu ile ev içindeki bir NAS sunucusuna bağlanıp uzun vadede kamera görüntüleri depolama ihtiyacının giderilmesi
- [ ] Telefonlar ve bilgisayarlar için MQTT sinyali alabilen amaca özel uygulamalar geliştirilmesi


[^1]:Bir insanın 10 saniye boyunca yapay zeka tarafından tanımlanması.

## Projenin kodu

### Bu kaynak kodu iki kısımdan oluşmaktadır:
1. **İşleme merkezi(*Raspberry Pi 5*) kodu** Yapay zeka ile Kamera Modülü'nden gelen HTTP video yayını OpenCV2 ile çeker ve Mediapipe modelleri ile işleyip uyarı durumunda MQTT protokolü ile uyarı mesajı gönderir.
2. **Kamera Modülü(*ESP32CAM*) kodu** yerleşik OV260 kamera ile görüntüyü alıp HTTP protokolü ile canlı yayın açar.

### Raspberry Pi 5 kodu kurulumu

1. Gereksinimler
    - Python 3.10
    - pip
    - venv
    - mosquitto
2. mosquitto için gerekli config ve password dosyası ile mosquitto systemd servisini başlat
3. Gerekli Kütüphaneleri yükle
    ```
    pip install mediapipe
    pip install paho-mqtt
    
    ```
4. Ana kodu çalıştır ``python main2.py``

### Bu projenin iletişim ve yapay zeka içeren kısımlarında aşağıdaki açık kaynak python kütüphaneleri kullanılmıştır.

[![GitHub Release](https://img.shields.io/github/v/release/google-ai-edge/mediapipe?label=mediapipe&link=https%3A%2F%2Fgithub.com%2Fgoogle-ai-edge%2Fmediapipe)](https://github.com/google-ai-edge/mediapipe)
[![GitHub Release](https://img.shields.io/github/v/release/eclipse-paho/paho.mqtt.python?label=paho-mqtt&link=https%3A%2F%2Fgithub.com%2Feclipse-paho%2Fpaho.mqtt.python)](https://github.com/eclipse-paho/paho.mqtt.python)
[![GitHub Release](https://img.shields.io/github/v/release/opencv/opencv-python?label=opencv-python)](https://github.com/opencv/opencv-python)