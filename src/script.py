"""Video senaryosu: anlatim satirlari + sahne listesi.

Her sahne: id, fn (sahne cizim fonksiyonu), lines (anlatim), istege bagli parametreler.
Satir basinda "q:" olan satirlar alinti sesiyle okunur.
'say' TTS'e giden metin, 'sub' altyazi metni (genelde ayni).
"""

TITLE = "Halife Döneminde Romalılara Karşı Savaşan Bir Arap Askeri Olsaydın Ne Olurdu?"

# (sahne_id, fonksiyon, [satirlar], ekstra)
SHOTS = [
    # ------------------------------------------------------------ GIRIS
    ("s01", "hook_plain", [
        "Yıl altı yüz otuz altı. Ağustosun kavurucu sıcağında, Yermük Nehri'nin kıyısındasın.",
        "Karşında göz alabildiğine uzanan bir ordu var. Parlayan miğferler, demir zırhlar ve haçlı sancaklar.",
        "Bunlar Romalılar. Dünyanın en güçlü imparatorluğunun askerleri.",
    ], dict(music="intro", lead=0.8)),
    ("s02", "hook_items", [
        "Senin elinde ise bir mızrak, deriden bir kalkan ve bir avuç hurma var.",
    ], {}),
    ("s03", "hook_question", [
        "Peki, Halife döneminde Romalılara karşı savaşan bir Arap askeri olsaydın, hayatın nasıl olurdu?",
        "Ve en önemlisi... hayatta kalabilir miydin?",
    ], {}),
    ("s04", "title_card", [], dict(dur=4.6)),

    # ------------------------------------------------------------ BOLUM 1
    ("s05", "chapter", [], dict(dur=3.2, num=1, title="ÇÖLDE DOĞMAK", sub="Hicaz, 7. yüzyılın başları",
                                music="desert")),
    ("s06", "camp_intro", [
        "Hikayemiz birkaç yıl önce başlıyor. Adın Zeyd olsun.",
        "Arap Yarımadası'nda, Hicaz çöllerinde, kıl çadırlarda yaşayan bir kabilenin oğlusun.",
    ], {}),
    ("s07", "daily_life", [
        "Hayatın sade ama sert. Gün doğmadan develeri sağarsın, gün boyu sürüyü otlatırsın.",
        "Gece de ateşin başında, yaşlıların anlattığı şiirleri ve kahramanlık hikayelerini dinlersin.",
    ], {}),
    ("s08", "well_vs_gold", [
        "Çölde bir kuyunun yerini bilmek, altının yerini bilmekten çok daha değerlidir.",
    ], {}),
    ("s09", "unity_map", [
        "Çocukluğunda kabileler arasında kan davaları ve yağmalar hiç eksik olmazdı.",
        "Ama artık her şey değişmişti. Peygamber Efendimizin vefatından sonra Arap kabileleri, ilk kez tek bir devletin, Medine'deki Halife'nin çatısı altında birleşmişti.",
    ], {}),
    ("s10", "messengers", [
        "Ve altı yüz otuz üç yılının sonunda, Halife Ebu Bekir'in elçileri senin kabilenin çadırlarına da geldi.",
        "Kuzeye, Şam diyarına, Romalılara karşı büyük bir sefer başlıyordu.",
    ], {}),

    # ------------------------------------------------------------ BOLUM 2
    ("s11", "chapter", [], dict(dur=3.2, num=2, title="ORDUYA KATILMAK", sub="Herkes kendi silahını getirir",
                                music="desert2")),
    ("s12", "farewell", [
        "Babanın gözleri dolu, annenin elleri titriyor. Ama sen kararını verdin.",
        "Kabilenin diğer gençleriyle birlikte yola çıkıyorsun.",
    ], {}),
    ("s13", "equipment", [
        "Peki yanına ne alıyorsun? Unutma, bu ordunun bir üniforması yok. Herkes kendi silahını kendisi getirir.",
        "Bir kılıç, belki de dedenden kalma. Uzun bir mızrak. Deve derisinden bir kalkan. Şanslıysan bir yay ve oklar.",
        "Başına sardığın sarık ise seni kavurucu güneşten korur.",
    ], {}),
    ("s14", "armor_price", [
        "Zincir zırh mı? O ancak zenginlerin harcı. İyi bir zırh, bir sürü deve eder.",
    ], {}),
    ("s15", "rations", [
        "Azığın da basit: hurma, arpa unu, kurutulmuş et ve deri bir kırbada su.",
    ], {}),
    ("s16", "loot_shares", [
        "Bir de çok önemli bir hesap var: ganimet.",
        "Savaşta ele geçirilen malın beşte biri devletin hazinesine, yani Beytülmal'e gider. Kalanı askerler arasında paylaşılır.",
        "Ama dikkat: Atlıysan üç pay alırsın, yayaysan sadece bir pay. Çünkü atın da bir payı vardır.",
        "Senin atın yok. Yani şimdilik tek bir pay.",
    ], {}),

    # ------------------------------------------------------------ BOLUM 3
    ("s17", "chapter", [], dict(dur=3.2, num=3, title="ŞAM YOLU", sub="634", music="march")),
    ("s18", "orders", [
        "Ordu yola çıkmadan önce, Halife Ebu Bekir'in komutanlara verdiği emirler askerlere okunur:",
        "q:Hıyanet etmeyin. Ganimetten çalmayın. Ölülere işkence etmeyin.",
        "q:Çocuklara, kadınlara ve yaşlılara dokunmayın. Meyve ağaçlarını kesmeyin, hurmalıkları yakmayın.",
        "q:Manastırlarda kendini ibadete adamış insanlar göreceksiniz. Onları kendi hallerine bırakın.",
        "Bu kurallar, o dönemin savaş anlayışına göre oldukça sıra dışıydı.",
    ], {}),
    ("s19", "march", [
        "Medine'den kuzeye, Şam'a doğru haftalarca sürecek bir yürüyüş başlıyor.",
        "Gündüz güneş taşları kızdırıyor, gece ise çöl buz gibi oluyor.",
    ], {}),
    ("s20", "halid_map", [
        "Bu sırada ordunun en efsanevi komutanı da yoldaydı: Halid bin Velid.",
        "Irak'ta Sasanilere karşı savaşırken, Halife'nin emriyle Suriye'ye çağrıldı.",
    ], {}),
    ("s21", "desert_crossing", [
        "Halid, kimsenin geçmeye cesaret edemediği susuz bir çölü sadece birkaç günde aştı.",
        "Rivayete göre yola çıkmadan önce develere bolca su içirdiler. Yol boyunca bu develer, adeta yürüyen birer su deposu oldu.",
        "Halid Suriye'ye vardığında, Romalılar şaşkına dönmüştü.",
    ], {}),

    # ------------------------------------------------------------ BOLUM 4
    ("s22", "chapter", [], dict(dur=3.2, num=4, title="KARŞINDAKİ DÜŞMAN", sub="Roma İmparatorluğu",
                                music="tension")),
    ("s23", "byzantine_name", [
        "Peki karşındaki düşman kim? Biz bugün onlara Bizans diyoruz.",
        "Ama bu isim, yüzlerce yıl sonra Avrupalı tarihçiler tarafından verildi. Onlar kendilerine Romalı derdi. Araplar da onlara Rum derdi.",
    ], {}),
    ("s24", "roman_vs_zeyd", [
        "Romalı asker senden çok farklıydı. Maaşlı ve eğitimli bir profesyoneldi. Demir zırhlar, miğferler, büyük kalkanlar.",
        "Ve en korkuncu: katafraktlar. Hem atlının hem de atın zırhla kaplandığı ağır süvariler.",
    ], {}),
    ("s25", "heraclius_tired", [
        "Ama İmparator Herakleios'un da büyük bir sorunu vardı.",
        "İmparatorluk, Sasanilerle tam yirmi altı yıl süren bir savaştan yeni çıkmıştı. Hazine boştu, askerler yorgundu ve halk vergilerden bıkmıştı.",
    ], {}),
    ("s26", "ghassanids", [
        "Üstelik Romalıların safında Hristiyan Araplar da vardı: Gassaniler.",
        "Yani bazen karşında, senin dilini konuşan, senin gibi giyinen insanlar olacaktı.",
    ], {}),
    ("s27", "first_battles", [
        "Altı yüz otuz dört yazında ilk büyük çarpışma Ecnadeyn'de yaşanır. Ardından Şam kuşatılır ve şehir teslim olur.",
        "Fahl'da bir zafer daha gelir.",
    ], {}),
    ("s28", "heraclius_gathers", [
        "Ama Herakleios boş durmuyordu. Antakya'da, imparatorluğun dört bir yanından asker topladı:",
        "Ermeniler, Slavlar, Gassani Araplar ve Romalı süvariler. Devasa bir ordu güneye doğru yürümeye başladı.",
    ], {}),
    ("s29", "retreat_jizya", [
        "Müslüman komutanlar zor bir karar aldı: Humus'u ve Şam'ı boşaltıp geri çekilmek.",
        "Ve burada tarihe geçen bir olay yaşandı. Ebu Ubeyde, Humus halkından aldığı cizye vergisini geri ödedi.",
        "q:Sizi koruyamıyorsak, bu parayı almaya hakkımız yok.",
        "Kaynaklara göre Humus halkı, Müslümanların adaletini eski yönetimden daha çok sevdiklerini söyleyerek, şehrin kapılarını Romalılara kapattı.",
    ], {}),

    # ------------------------------------------------------------ BOLUM 5
    ("s30", "chapter", [], dict(dur=3.4, num=5, title="YERMÜK: ALTI GÜN", sub="Ağustos 636", music="battle_pre")),
    ("s31", "yarmouk_map", [
        "Ve sonunda iki ordu, Yermük Nehri'nin yakınında, derin vadilerle çevrili bir ovada karşı karşıya geldi.",
        "Sayılar kaynaktan kaynağa değişiyor. Ama kesin olan bir şey var: Romalılar sizden kat kat kalabalıktı.",
        "Siz belki otuz bin kişiydiniz. Onlar ise belki yüz bin.",
    ], {}),
    ("s32", "halid_command", [
        "Ordunun başkomutanı Ebu Ubeyde bin Cerrah'tı. Ama savaş meydanındaki yönetimi Halid bin Velid'e bıraktı.",
        "Halid orduyu otuz altı birliğe böldü ve süvarilerden hızlı bir yedek kuvvet kurdu.",
    ], {}),
    ("s33", "camp_women", [
        "Senin yanında sadece askerler yok. Kadınlar ve çocuklar da ordugahta, arka saflarda bekliyor.",
        "Onların varlığı sana tek bir şey söylüyor: Geri kaçacak bir yer yok.",
    ], {}),
    ("s34", "day1_duels", [
        "Savaş tam altı gün sürecek.",
        "İlk gün, iki ordunun ortasında teke tek dövüşler yapılır. İki taraftan da en cesur savaşçılar meydana çıkar.",
        "Kılıçlar çarpışır, kan kuma karışır.",
    ], dict(music="battle")),
    ("s35", "day2_dawn", [
        "İkinci gün, Romalılar şafak vakti, siz sabah namazındayken saldırır.",
        "Sağ kanat dağılır. Askerler geriye, ordugaha doğru kaçmaya başlar.",
    ], {}),
    ("s36", "women_push", [
        "İşte o anda inanılmaz bir şey olur.",
        "Ordugahtaki kadınlar, ellerinde çadır direkleri ve taşlarla kaçan erkeklerin önüne çıkar. Onları utandırarak yeniden savaşa gönderirler.",
    ], {}),
    ("s37", "day3_chaos", [
        "Üçüncü gün saldırılar devam eder. Toz, çığlıklar, yaralılar...",
    ], {}),
    ("s38", "day4_arrows", [
        "Ve dördüncü gün. Tarihçilerin, gözlerin kaybedildiği gün dediği gün.",
        "Ermeni okçuların yağdırdığı oklarla, yüzlerce Müslüman askeri gözünü kaybeder.",
    ], {}),
    ("s39", "ikrima", [
        "Aynı gün İkrime bin Ebu Cehil, dört yüz adamıyla ölümüne savaşmaya yemin eder.",
        "Romalıların hücumunu durdururlar. Ama neredeyse hiçbiri geri dönmez.",
    ], {}),
    ("s40", "zeyd_wounded", [
        "Ya sen? Omzuna bir ok saplanmış, kalkanın paramparça. Ama hala ayaktasın.",
    ], dict(music="heartbeat")),
    ("s41", "day5_truce", [
        "Beşinci gün sessiz geçer. Romalı komutan Vahan ateşkes ister.",
        "Halid'in cevabı kısa olur:",
        "q:Bu işi bir an önce bitirmek için acelemiz var!",
    ], dict(music="battle_pre")),
    ("s42", "day6_cavalry", [
        "Ve altıncı gün. Halid süvarileriyle saldırıp Roma süvarilerini piyadelerden koparır.",
    ], dict(music="battle")),
    ("s43", "bridge_night", [
        "Bir gece önce gizlice gönderilen Dırar bin Ezver ve beş yüz süvari, vadideki tek köprüyü ele geçirmiştir.",
        "Romalıların kaçış yolu artık kapanmıştır.",
    ], {}),
    ("s44", "sandstorm_ravine", [
        "Üstelik rivayete göre o gün, güçlü bir kum fırtınası Romalıların yüzüne doğru eser.",
        "Sıkışan Roma piyadeleri vadinin uçurumlarına doğru itilir. Binlercesi uçurumdan düşer.",
    ], {}),
    ("s45", "silent_evening", [
        "Akşam olduğunda Yermük'ün kıyısı sessizdir.",
        "Dünyanın en güçlü ordularından biri, artık yoktur.",
    ], dict(music="aftermath")),

    # ------------------------------------------------------------ BOLUM 6
    ("s46", "chapter", [], dict(dur=3.2, num=6, title="ZAFERDEN SONRA", sub="636 - 638", music="triumph")),
    ("s47", "casualties", [
        "Zaferin bedeli ağırdı. Kaynaklara göre Müslümanlardan yaklaşık üç bin kişi şehit düştü. Romalıların kaybı ise on binlerceydi.",
    ], {}),
    ("s48", "zeyd_loot", [
        "Sen yaşıyorsun. Omzundaki yara iyileşecek, ama izi ömür boyu kalacak.",
        "Payına düşen ganimet ise bir Roma zırhı, bir kılıç ve birkaç gümüş sikke. Hayatında ilk kez bu kadar zengin oldun.",
    ], {}),
    ("s49", "heraclius_farewell", [
        "Antakya'daki İmparator Herakleios, yenilgi haberini alınca Suriye'yi terk eder.",
        "Rivayete göre son kez dönüp arkasına bakar ve şöyle der:",
        "q:Elveda Suriye! Düşmana ne güzel bir ülke bırakıyorum.",
    ], dict(music="sad")),
    ("s50", "jerusalem_siege", [
        "Sıra Kudüs'e gelir. Şehir kuşatılır. Ama Patrik Sofronyus bir şart koyar:",
        "Şehrin anahtarlarını sadece Halife'nin kendisine teslim edecektir.",
    ], dict(music="desert")),
    ("s51", "omar_journey", [
        "Halife Ömer, Medine'den yola çıkar. Yanında sadece bir hizmetkar ve tek bir deve vardır.",
        "Yol boyunca deveye sırayla binerler.",
    ], {}),
    ("s52", "omar_arrives", [
        "Kudüs'e vardıklarında sıra hizmetkardadır.",
        "Ve sen, dünyanın en büyük devletlerinden birinin hükümdarını, devenin yularını tutup yürürken görürsün. Hizmetkarı ise devenin üstündedir.",
    ], {}),
    ("s53", "church", [
        "Ömer, şehir halkına canlarının, mallarının ve kiliselerinin güvencesini veren bir ahitname verir.",
        "Namaz vakti geldiğinde kilisede namaz kılmayı reddeder. Çünkü şöyle der:",
        "q:Burada namaz kılarsam, ileride Müslümanlar burayı camiye çevirmek isteyebilir.",
    ], {}),

    # ------------------------------------------------------------ BOLUM 7
    ("s54", "chapter", [], dict(dur=3.2, num=7, title="SESSİZ DÜŞMAN: VEBA", sub="Amvas, 638", music="plague")),
    ("s55", "plague", [
        "Ama seni savaştan çok daha korkunç bir düşman bekliyordu.",
        "Altı yüz otuz sekiz yılında, Amvas'ta bir veba salgını başlar.",
    ], {}),
    ("s56", "omar_qadar", [
        "Halife Ömer, Suriye'ye gelirken salgını duyar ve geri dönmeye karar verir. Ebu Ubeyde ona sorar:",
        "q:Allah'ın kaderinden mi kaçıyorsun?",
        "Ömer'in cevabı tarihe geçer:",
        "q:Evet. Allah'ın kaderinden, yine Allah'ın kaderine kaçıyoruz.",
    ], {}),
    ("s57", "plague_toll", [
        "Salgında yirmi beş bin kişi hayatını kaybeder. Aralarında komutanın Ebu Ubeyde de vardır.",
        "Savaştan sağ çıkan birçok arkadaşın, bu sessiz düşmana yenilir.",
    ], {}),
    ("s58", "zeyd_sick", [
        "Eğer şanslıysan, günlerce ateşler içinde yattıktan sonra iyileşirsin.",
    ], {}),

    # ------------------------------------------------------------ BOLUM 8
    ("s59", "chapter", [], dict(dur=3.2, num=8, title="BİR ASKERİN SONU", sub="Divan, atâ ve yeni ufuklar",
                                music="desert2")),
    ("s60", "divan", [
        "Salgından sonra hayat yeniden düzene girer. Halife Ömer bir ilke imza atar: Divan.",
        "Bütün askerlerin adlarının yazıldığı büyük bir kayıt defteri. Artık senin adın da deftere yazılıdır ve her yıl devletten düzenli bir maaş alırsın. Buna ata denir.",
    ], {}),
    ("s61", "land_rule", [
        "Ama Halife'nin bir kuralı daha vardır: Askerler fethedilen toprakları kendilerine çiftlik yapamaz.",
        "Onlar asker olarak kalacak, topraklar ise yerli halkın elinde işlenmeye devam edecektir.",
    ], {}),
    ("s62", "future_paths", [
        "Belki Şam'da evlenip bir aile kurarsın. Belki Amr bin As'ın ordusuyla Mısır'a gidersin.",
        "Ya da Anadolu'nun karlı dağlarına yapılan akınlara katılırsın.",
    ], {}),
    ("s63", "constantinople", [
        "Ve kim bilir, belki yıllar sonra, yaşlı bir asker olarak Ebu Eyyub el-Ensari ile birlikte Konstantinopolis surlarına kadar gidersin.",
    ], dict(music="epic_end")),
    ("s64", "eyup", [
        "Ebu Eyyub o surların dibinde vefat edecek ve oraya defnedilecekti.",
        "Yaklaşık sekiz yüz yıl sonra, bin dört yüz elli üçte, Fatih Sultan Mehmet'in hocası Akşemseddin onun kabrini bulacaktı. Orası bugünkü Eyüp Sultan'dır.",
    ], {}),
    ("s65", "recap", [
        "Hicaz çöllerinde deve otlatan bir çocuk olarak başlayan hayatın, böylece tarihin en büyük dönüşümlerinden birine tanıklık etmiş olurdu.",
    ], {}),
    ("s66", "outro", [
        "Peki sen olsaydın? Atlı bir süvari mi olurdun, bir okçu mu, yoksa çadır direğiyle kaçanları geri çeviren cesur kadınlardan biri mi?",
        "Cevabını yorumlara yaz. Zaman Kırığı'na abone olmayı ve bildirimleri açmayı unutma. Bir sonraki videoda görüşmek üzere!",
    ], dict(music="outro", tail=3.0)),
]

# Altyazida farkli yazilmasi gerekenler (TTS icin sadelestirilmis -> dogru imla)
SUB_FIX = {
    "Hikayemiz": "Hikâyemiz", "hikayelerini": "hikâyelerini", "ordugahta": "ordugâhta", "ordugaha": "ordugâha",
    "Ordugahtaki": "Ordugâhtaki", "hala ayaktasın": "hâlâ ayaktasın", "hizmetkar": "hizmetkâr",
    "hizmetkardadır": "hizmetkârdadır", "Hizmetkarı": "Hizmetkârı", "Buna ata denir": "Buna atâ denir",
    "altı yüz otuz altı": "636", "altı yüz otuz üç": "633", "altı yüz otuz dört": "634", "altı yüz otuz sekiz": "638",
    "bin dört yüz elli üçte": "1453'te", "yirmi altı": "26", "otuz bin": "30 bin", "yüz bin": "100 bin",
    "otuz altı": "36", "dört yüz": "400", "beş yüz": "500", "üç bin": "3 bin", "yirmi beş bin": "25 bin",
    "sekiz yüz": "800",
}

# Bolum basliklari (YouTube bolumleri icin)
CHAPTERS = {
    "s01": "Giriş", "s05": "Çölde Doğmak", "s11": "Orduya Katılmak", "s17": "Şam Yolu",
    "s22": "Karşındaki Düşman: Romalılar", "s30": "Yermük: Altı Gün", "s46": "Zaferden Sonra",
    "s54": "Sessiz Düşman: Veba", "s59": "Bir Askerin Sonu",
}
