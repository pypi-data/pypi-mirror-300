import requests
from bs4 import BeautifulSoup
from docutils.nodes import description
from urllib3 import request

Description = "To get lastest information eathquake from BMKG.go.id"

def ekstraksi_data():
    """
    Tanggal : 21 September 2024
    Waktu : 06:26:20 WIB
    Magnitudo : 4.8
    Kedalaman : 22 km
    Lokasi : LS=8.57 BT=115.32
    Pusat gempa : berada di darat 3 km baratdaya Gianyar
    Dirasakan : (Skala MMI): IV Gianyar, III Badung, III Denpasar, III Tabanan, III Karangasem, III Bangli, II Buleleng, II Mataram, II Lombok Barat
    :return:
    """
    try:
        content = requests.get('https://bmkg.go.id')
    except Exception:
        return None
    if content.status_code == 200:
        # print(content.text)
        soup = BeautifulSoup(content.text, 'html.parser')

        result = soup.find('span', {'class': 'waktu'})
        Waktu = result.text.split(',') [1]
        Tanggal = result.text.split(',')[0]

        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')
        i = 0
        Magnitudo = None
        LS = None
        BT = None
        Dirasakan = None

        for res in result:
            if i ==1:
                Magnitudo = res.text
            elif i == 2:
                Kedalaman = res.text
            elif i == 3:
                Koordinat = res.text.split(' - ')
                LS = Koordinat[0]
                BT = Koordinat[1]
            elif i == 4:
                Lokasi = res.text
            elif i == 5:
                Dirasakan = res.text
            i = i + 1
        # Magnitudo = 0

        hasil = dict()
        hasil['Tanggal'] = Tanggal
        hasil['Waktu'] = Waktu
        hasil['Magnitudo'] = Magnitudo
        hasil['Kedalaman'] = Kedalaman
        hasil['Lokasi'] = Lokasi
        hasil['Koordinat'] = {'LS': LS, 'BT': BT}
        hasil['Dirasakan'] = Dirasakan
        return hasil
    else:
        return None

def tampilkan_data(result):
    print('Gempa Terkahir Berdasarkan BMKG')
    print(f"Tanggal {result['Tanggal']}")
    print(f"Waktu {result['Waktu']}")
    print(f"Magnitudo {result['Magnitudo']}")
    print(f"Kedalaman {result['Kedalaman']}")
    print(f"Lokasi {result['Lokasi']}")
    print(f"Koordinat: LS={result['Koordinat']['LS']}, BT={result['Koordinat']['BT']}")
    print(f"Dirasakan {result['Dirasakan']}")

if __name__ == '__main__':
    print('Description', Description)
    result = ekstraksi_data()
    tampilkan_data(result)