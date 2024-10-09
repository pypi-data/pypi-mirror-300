import requests
from bs4 import BeautifulSoup
"""
Method = fungsi
filed/atribute = variable
constructor = method yang dipanggil pertama kali saat object diciptakan. gunakan untuk mendeklarasikan semua variabel
pada class ini
"""

class Bencana :
    def __init__(self, url, Description):
        self.Description = Description
        self.result = None
        self.url = url
    def tampilkan_keterangan(self):
        print(self.Description)

    def scraping_data(self):
        print('Not yet implemented')
    def tampilkan_data(self):
        print('Not yet implemented')
    def run(self):
        self.scraping_data()
        self.tampilkan_data()

class deteksibanjir(Bencana):
    def __init__(self, url):
        super(deteksibanjir, self).__init__(url,
                                            'Not yet Implementation, but it should return last flood '
                                            'in Indonesia')
    def tampilkan_keterangan(self):
        print(f'UNDER CONTRUCTION {self.Description}')

class deteksigempa(Bencana):
    def __init__(self, url):
        super(deteksigempa, self).__init__(url, 'To get lastest information eathquake from BMKG.go.id')

    def scraping_data(self):
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
            content = requests.get(self.url)
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
            self.result = hasil
        else:
            return None

    def tampilkan_data(self):
        if self.result is None:
            print("Tidak bisa menemukan data gempa terkini")

        print('Gempa Terkahir Berdasarkan BMKG')
        print(f"Tanggal {self.result['Tanggal']}")
        print(f"Waktu {self.result['Waktu']}")
        print(f"Magnitudo {self.result['Magnitudo']}")
        print(f"Kedalaman {self.result['Kedalaman']}")
        print(f"Lokasi {self.result['Lokasi']}")
        print(f"Koordinat: LS={self.result['Koordinat']['LS']}, BT={self.result['Koordinat']['BT']}")
        print(f"Dirasakan {self.result['Dirasakan']}")

    def run(self):
        self.scraping_data()
        self.tampilkan_data()



if __name__ == '__main__':
    gempa_di_indonesia = deteksigempa('https://bmkg.go.id')
    gempa_di_indonesia.tampilkan_keterangan()
    gempa_di_indonesia.run()

    banjir_di_indonesia = deteksibanjir('Not yet')
    banjir_di_indonesia.tampilkan_keterangan()
    banjir_di_indonesia.run()

    daftar_bencana = [gempa_di_indonesia, banjir_di_indonesia]
    print('\nSemua bencana yang ada')
    for bencana in daftar_bencana:
        bencana.tampilkan_keterangan()


    # gempa_di_indonesia.ekstraksi_data()
    # gempa_di_indonesia.tampilkan_data()