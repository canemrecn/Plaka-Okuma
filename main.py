import cv2
#OpenCV kütüphanesini içeri aktarır. Bu kütüphane görüntü işleme ve video analizi için kullanılır.
import numpy as np
#NumPy kütüphanesini içeri aktarır. Bu kütüphane çok boyutlu diziler ve matematiksel işlemler için kullanılır.
from PIL import Image
#PIL kütüphanesinden Image sınıfını içeri aktarır. Bu sınıf, görüntüleri açmak, işlemek ve kaydetmek için kullanılır.
import PIL.Image
# PIL kütüphanesinden Image sınıfını içeri aktarır.
import pytesseract
#pytesseract kütüphanesini içeri aktarır. Bu kütüphane, optik karakter tanıma (OCR) işlemleri yapmak için kullanılır.
import sys
#sys kütüphanesini içeri aktarır. Bu kütüphane, sistemle ilgili bilgilere erişmek için kullanılır.
if sys.platform == 'win32':
    deltax = 0
    deltay = 0
    FONTADI = 'verdana.ttf'
else:
    deltax = 50
    deltay = 105
    FONTADI = 'FreeSerif.ttf'
#Bu kod satırları, işletim sisteminin tespit edilerek, değişkenlere başlangıç değerleri atar.
# İşletim sistemi Windows ise deltax ve deltay değerleri sıfır olarak ayarlanır ve FONTADI
# değişkenine 'verdana.ttf' değeri atanır. Eğer işletim sistemi Windows değilse, deltax ve
# deltay değerleri 50 ve 105 olarak ayarlanır, FONTADI değişkenine ise 'FreeSerif.ttf' değeri atanır.
#Bu kod bloğu, işletim sistemiyle ilgili ayarları belirlemek için kullanılır.
def dpi_kontrol(dosya_adres):
    imaj = Image.open(dosya_adres)
    gen, yuks = imaj.size
    carpan = min(1, float(1024.0 / gen))
    size = int(carpan * gen), int(carpan * yuks)
    yeni_imaj = imaj.resize(size, Image.ANTIALIAS)
    gecici_dosyaad = 'resimler/gecici.png'
    yeni_imaj.save(gecici_dosyaad, dpi=(300, 300))
    return gecici_dosyaad
#Bu fonksiyon, verilen dosya adresindeki görüntünün DPI (Nokta Başına İnç) değerini kontrol eder.
# Görüntüyü açar, genişlik ve yükseklik değerlerini alır ve bir ölçek faktörü hesaplar. Bu ölçek
# faktörü, görüntünün 1024 pikselden daha büyük olup olmadığını kontrol eder ve gerektiğinde
# boyutunu yeniden ölçeklendirir. Son olarak, yeniden boyutlandırılmış görüntüyü belirli bir
# DPI değeriyle kaydeder ve geçici bir dosya yolunu döndürür.
def ana():
    dosyaad = dpi_kontrol('resimler/plaka014.jpg')
    kare = cv2.imread(dosyaad)
    cv2.imshow('kare', kare)
    cv2.moveWindow('kare', deltax,deltay)
    gri = cv2.cvtColor(kare,cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gri, 7)
    cv2.imshow('blur', blur)
    cv2.moveWindow('blur',deltax,deltay+kare.shape[0])
    _, sb = cv2.threshold(gri,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    cv2.imshow('sb', sb)
    cv2.moveWindow('sb',deltax,deltay+kare.shape[0]*2)
    cv2.imwrite('resimler/plgecici.png', kare)
    if sys.platform == 'win32':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    else:
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    output = pytesseract.image_to_string(PIL.Image.open('resimler/plgecici.png'), lang='eng')
    print(output[1:-1])
    cv2.waitKey()
    cv2.destroyAllWindows()
ana()
#dpi_kontrol() fonksiyonunu kullanarak 'resimler/plaka014.jpg' dosyasının DPI'sını kontrol eder ve
# geçici bir dosya adı (dosyaad) alır.
#cv2.imread() ile dosyaad dosyasını okur ve kare adlı değişkene atar.
#cv2.imshow('kare', kare) ile kare görüntüsünü ekranda gösterir.
#cv2.moveWindow('kare', deltax, deltay) ile kare penceresinin konumunu ayarlar.
#cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY) ile kare görüntüsünü BGR renk formatından gri tonlamaya
# dönüştürür ve gri adlı değişkene atar.
#cv2.medianBlur(gri, 7) ile gri görüntüsüne median bulanıklık filtresi uygular ve blur adlı değişkene
# atar.
#cv2.imshow('blur', blur) ile blur görüntüsünü ekranda gösterir.
#cv2.moveWindow('blur', deltax, deltay + kare.shape[0]) ile blur penceresinin konumunu ayarlar.
#cv2.threshold(gri, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) ile gri görüntüsünde eşikleme
# işlemi uygular ve ters ikili eşiklenmiş görüntüyü (sb)
#cv2.imshow('sb', sb) ile sb görüntüsünü ekranda gösterir.
#cv2.moveWindow('sb', deltax, deltay + kare.shape[0] * 2) ile sb penceresinin konumunu ayarlar.
#cv2.imwrite('resimler/plgecici.png', kare) ile kare görüntüsünü 'resimler/plgecici.png' dosyasına
# kaydeder.
#İşletim sistemi kontrolü yaparak Tesseract OCR motorunun komut yolunu belirler. Eğer işletim sistemi
# 'win32' ise, Tesseract'in Windows konumunu belirler, aksi takdirde diğer işletim sistemleri için
# uygun komut yolunu atar.
#pytesseract.image_to_string(PIL.Image.open('resimler/plgecici.png'), lang='eng') ile
# 'resimler/plgecici.png' dosyasındaki görüntüyü Tesseract OCR kullanarak metne dönüştürür.
#print(output[1:-1]) ile metni ekrana yazdırır. output değişkeninin başındaki ve sonundaki boşluk
# karakterlerini atlayarak metni yazdırır.
#cv2.waitKey() ile herhangi bir tuşa basılmasını bekler.
#cv2.destroyAllWindows() ile tüm açık pencereleri kapatır ve belleği temizler.
#Son olarak, ana() fonksiyonunu çağırarak işlemlerin gerçekleştirilmesini sağlar.