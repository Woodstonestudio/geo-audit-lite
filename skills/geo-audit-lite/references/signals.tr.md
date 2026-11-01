# 24 temel sinyal (ücretsiz sürüm)

Tam sürümde 78 sinyal, düzeltme şablonları, müşteri bulma ve bağımsız denetçi var: woodstonestudio.com


## Yapay zekâ erişimi (alan ağırlığı 14)

### `ai.robots_search` · 5 (Kritik)
**robots.txt Google ve Bing botlarına ana sayfayı açıyor**  
Neden: Google ve Bing siteyi okuyamazsa aramada çıkmazsınız; ChatGPT ve Copilot da web aramasında büyük ölçüde Bing'i kullanır.  
Düzeltme: robots.txt'deki Googlebot / Bingbot / * için 'Disallow: /' satırını kaldırın.

### `ai.robots_ai` · 3 (Önemli)
**robots.txt AI arama botlarına izin veriyor**  
Neden: ChatGPT, Claude ve Perplexity cevap verirken kaynak sayfaları kendi arama botlarıyla okur; engelliyseniz cevapta adınız geçmez.  
Düzeltme: OAI-SearchBot, ChatGPT-User, Claude-SearchBot ve PerplexityBot'u engellemeyin. Yalnızca eğitimi kapatmak için GPTBot, ClaudeBot ve Google-Extended'ı engellemeniz yeterli.

### `ai.live_ai` · 3 (Önemli)
**AI arama botları ana sayfaya gerçekten ulaşabiliyor**  
Neden: robots.txt izin verse bile CDN veya güvenlik duvarı (ör. Cloudflare) bu botlara hata ya da doğrulama sayfası döndürebilir.  
Düzeltme: CDN/güvenlik duvarındaki bot ayarlarını kontrol edin. Cloudflare'de AI Crawl Control'de eğitim için 'Block' yerine 'Disallow AI training' seçin, arama botlarını açık bırakın.

### `ai.parity` · 3 (Önemli)
**Botlar tarayıcıyla aynı içeriği alıyor**  
Neden: Bota boş ya da farklı bir sayfa sunuluyorsa AI ve arama motorları sitenizi eksik anlatır; bazı durumlarda gizleme (cloaking) sayılır.  
Düzeltme: Bot kimliğiyle gelen isteklere de tam sayfayı sunun; önbellek/eklenti ayarlarında bot ayrımını kapatın.

### `ai.ssr` · 5 (Kritik)
**Sayfa metni sunucudan hazır geliyor (JavaScript beklemeden)**  
Neden: AI botlarının çoğu JavaScript çalıştırmaz; metin yalnızca tarayıcıda oluşuyorsa onlar için sayfa boştur.  
Düzeltme: Sunucu tarafı oluşturma (SSR) ya da statik çıktı kullanın; en azından başlık, açıklama ve ana metni HTML'de verin.

## Marka ve kimlik (alan ağırlığı 12)

### `brand.org` · 3 (Önemli)
**Kurum/işletme yapısal verisi var (Organization, LocalBusiness)**  
Neden: Bu veri AI'a ve Google'a 'bu site kimin, ne iş yapıyor, nerede' sorusunun hatasız cevabını verir; bilgi panelleri ve AI cevapları bunu kullanır.  
Düzeltme: Organization ya da işletme türünüze uygun LocalBusiness şeması ekleyin: ad, logo, adres, telefon, sosyal hesaplar.

### `brand.contact` · 3 (Önemli)
**Telefon veya e-posta sayfada görünüyor**  
Neden: Ziyaretçi de AI da 'nasıl ulaşırım' sorusunun cevabını sayfada arar.  
Düzeltme: Telefon ve e-postayı üst menüde ya da alt bilgide düz metin olarak yazın.

## İçerik ve cevaplar (alan ağırlığı 12)

### `content.h1` · 3 (Önemli)
**Sayfada tek bir H1 başlık var**  
Neden: H1 sayfanın ana konusunu söyler; hiç yoksa ya da birden fazlaysa konu bulanıklaşır.  
Düzeltme: Sayfaya ne iş yaptığınızı söyleyen tek bir H1 koyun; diğer başlıkları H2/H3 yapın.

### `content.words` · 3 (Önemli)
**Ana sayfada yeterli metin var**  
Neden: Az metinli sayfa Google ve AI için 'ne iş yaptığı belirsiz' demektir; sıralanacak ve alıntılanacak bir şey yoktur.  
Düzeltme: Ana sayfada en az 300 kelime: ne yaptığınız, kime, nerede, neden siz, sık sorulan sorular.

## Teknik SEO (alan ağırlığı 14)

### `tech.status` · 5 (Kritik)
**Ana sayfa sorunsuz açılıyor (2xx)**  
Neden: Ana sayfa hata veriyorsa ne ziyaretçi ne arama motoru sitenizi görebilir.  
Düzeltme: Barındırma ve alan adı ayarlarını kontrol edin; site düzelene kadar reklamı durdurun.

### `tech.indexable` · 5 (Kritik)
**Ana sayfa aramada gösterilebilir (noindex yok)**  
Neden: noindex etiketi Google ve Bing'e 'bu sayfayı gösterme' der; çoğu zaman yayına alırken unutulan bir ayardır.  
Düzeltme: <meta name="robots" content="noindex"> etiketini ya da X-Robots-Tag başlığını kaldırın (WordPress: Ayarlar → Okuma → 'Arama motorlarını engelle' kapalı olmalı).

### `tech.title` · 3 (Önemli)
**Sayfa başlığı var ve uygun uzunlukta**  
Neden: Başlık arama sonucunda tıklanan mavi satırdır; çok kısa veya uzunsa kesilir ya da Google kendisi yazar.  
Düzeltme: 10–60 karakterlik, ne yaptığınızı ve markanızı içeren bir başlık yazın (ör. 'Bahçeşehir Kuaför | Salon Adı').

### `tech.description` · 3 (Önemli)
**Meta açıklama var ve uygun uzunlukta**  
Neden: Arama sonucunda başlığın altındaki iki satırdır; tıklama kararını etkiler.  
Düzeltme: 50–160 karakterlik, hizmetinizi ve konumunuzu anlatan bir açıklama yazın.

### `tech.viewport` · 3 (Önemli)
**Mobil görünüm ayarı (viewport) var**  
Neden: Bu ayar yoksa telefonda sayfa küçülmüş masaüstü görünümüyle açılır; Google mobil sürümü esas alır.  
Düzeltme: <meta name="viewport" content="width=device-width, initial-scale=1"> ekleyin ve tasarımı mobilde kontrol edin.

## Hız (alan ağırlığı 14)

### `speed.perf` · 5 (Kritik)
**Mobil PageSpeed puanı 90 ve üstü**  
Neden: Telefondan gelen ziyaretçinin yarısı yavaş sayfada beklemeden çıkar; Google hızı sıralamada kullanır.  
Düzeltme: Görselleri WebP'ye çevirip boyutlandırın, kullanılmayan eklenti ve betikleri kaldırın, önbellek ve CDN kullanın.

### `speed.lcp` · 3 (Önemli)
**Ana içerik 2,5 saniyede görünüyor (LCP)**  
Neden: LCP, sayfanın en büyük öğesinin (genelde kapak görseli) ne zaman göründüğüdür; Google'ın temel kullanıcı deneyimi ölçüsüdür.  
Düzeltme: Kapak görselini küçültün ve öncelikli yükleyin (fetchpriority=high), yazı tiplerini hafifletin.

### `speed.cls` · 3 (Önemli)
**Sayfa yüklenirken kaymıyor (CLS)**  
Neden: Yükleme sırasında kayan düğmeler yanlış tıklamaya ve kızgınlığa yol açar; Google bunu ölçer.  
Düzeltme: Görsellere genişlik/yükseklik verin, reklam ve gömülü içerik için yer ayırın.

## Yapısal veri (alan ağırlığı 10)

### `schema.present` · 3 (Önemli)
**Yapısal veri (JSON-LD) var**  
Neden: Yapısal veri sayfadaki bilgiyi (işletme, hizmet, SSS, fiyat) makinelerin hatasız okuyacağı biçimde verir.  
Düzeltme: Sayfaya schema.org JSON-LD bloğu ekleyin; Google'ın Zengin Sonuç Testi ile doğrulayın.

### `schema.valid` · 3 (Önemli)
**Tüm JSON-LD blokları geçerli**  
Neden: Tek bir virgül hatası bloğun tamamen yok sayılmasına yol açar.  
Düzeltme: Blokları Zengin Sonuç Testi'nde doğrulayın; elle yazılmış blokları bir eklentiyle üretin.

## Güvenlik (alan ağırlığı 8)

### `sec.https` · 5 (Kritik)
**Site HTTPS ile açılıyor**  
Neden: HTTPS olmayan sitede tarayıcı 'Güvenli değil' yazar; ziyaretçi form doldurmaz, Google geri plana atar.  
Düzeltme: Ücretsiz SSL (Let's Encrypt ya da Cloudflare) kurun.

### `sec.redirect` · 3 (Önemli)
**http:// adresi kalıcı olarak https'e yönleniyor**  
Neden: Kalıcı (301/308) yönlendirme yoksa eski linkler güvensiz sürüme gider ve sıralama gücü taşınmaz.  
Düzeltme: Sunucuda tüm http isteklerini 301 ile https'e yönlendirin.

## İletişim ve dönüşüm (alan ağırlığı 7)

### `contact.form` · 3 (Önemli)
**İletişim veya randevu formu var**  
Neden: Ziyaretçi o an yazmak ister; e-posta adresini kopyalayıp mail atmak yerine çoğu vazgeçer.  
Düzeltme: Kısa bir form (ad, telefon, mesaj) ya da online randevu ekleyin.

### `contact.tel` · 3 (Önemli)
**Tek dokunuşla arama linki var (tel:)**  
Neden: Telefondaki ziyaretçi numarayı ezberleyip yazmak yerine dokunarak arar.  
Düzeltme: Telefon numarasını <a href="tel:+90…"> ile link yapın.

## Paylaşım (alan ağırlığı 5)

### `social.image` · 3 (Önemli)
**Paylaşım görseli (og:image) var**  
Neden: Görselsiz paylaşımlar çok daha az tıklanır.  
Düzeltme: 1200×630 bir og:image görseli ekleyin.

