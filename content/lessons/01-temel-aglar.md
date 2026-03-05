# Modül 1.1: Ağ Temellerine Giriş

Siber güvenliği anlamak için öncelikle korumaya çalıştığımız ağların nasıl çalıştığını bilmemiz gerekir. Bu derste temel ağ kavramlarını öğreneceğiz.

## IP Adresi Nedir?

IP (Internet Protocol) adresi, ağa bağlı her cihazın sahip olduğu eşsiz tanımlayıcıdır.

- **IPv4:** Örn: `192.168.1.1` (4 bloktan oluşur)
- **IPv6:** Örn: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`

## TCP ve UDP

Verilerin ağ üzerinde taşınması için kullanılan iki ana protokoldür.

| Özellik | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) |
|---------|------------------------------------|---------------------------------|
| Bağlantı | Bağlantı yönelimli (Connection-oriented) | Bağlantısız (Connectionless) |
| Güvenilirlik| Yüksek (Veri ulaşımı garantilidir) | Düşük (Veri kaybı olabilir) |
| Hız | Daha yavaş | Çok hızlı |
| Kullanım | Web (HTTP), E-posta, Dosya Transferi | Canlı yayın, Online oyunlar, DNS |

## DNS (Domain Name System)

DNS, internetin telefon rehberidir. İnsanların okuyabildiği alan adlarını (örn: `google.com`) bilgisayarların anlayabildiği IP adreslerine (örn: `142.250.217.110`) çevirir.

```bash
# Bir alan adının IP adresini bulmak için nslookup komutu kullanılır
nslookup google.com
```

## HTTP ve HTTPS

Web tarayıcınız ile web sunucusu arasındaki iletişimi sağlayan protokoldür.

- **HTTP (Port 80):** Veriler düz metin olarak iletilir. Araya giren biri okuyabilir (Güvensiz).
- **HTTPS (Port 443):** Veriler şifrelenerek iletilir (Güvenli).

> **Güvenlik Notu:** Hassas verilerinizi (şifre, kredi kartı) asla HTTPS olmayan bir sitede girmeyin.
