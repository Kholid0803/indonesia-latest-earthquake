import requests
from bs4 import BeautifulSoup


class GempaTerkini:
    def __init__(self):
        self.description = 'To get the latest earthquake in Indonesia from BMKG.go.id'
        self.result = None

    def ekstraksi_data(self):

        try:
            content = requests.get('https://bmkg.go.id')
        except Exception:
            return None
        if content.status_code == 200:
            soup = BeautifulSoup(content.text, 'html.parser')
            webResult = soup.find('span', {'class': 'waktu'})
            webResult = webResult.text.split(', ')
            time = webResult[1]
            date = webResult[0]

            webResult = soup.find(
                'div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
            webResult = webResult.findChildren('li')
            i = 0
            magnitude = None
            lat = None
            lon = None
            depth = None
            location = None
            feel = None
            for res in webResult:
                if i == 1:
                    magnitude = res.text
                elif i == 2:
                    depth = res.text
                elif i == 3:
                    coordinate = res.text.split(' - ')
                    lat = coordinate[0]
                    lon = coordinate[1]
                elif i == 4:
                    location = res.text
                elif i == 5:
                    feel = res.text
                i = i + 1

        result = dict()
        result['tanggal'] = date
        result['waktu'] = time
        result['magnitudo'] = magnitude
        result['kedalaman'] = depth
        result['koordinat'] = {'lat': lat, 'lon': lon}
        result['lokasi'] = location
        result['dirasakan'] = feel
        self.result = result

    def tampilkan_data(self):
        print('Gempa Berdasarkan BMKG')
        print(f"Tanggal, {self.result['tanggal']}")
        print(f"Waktu, {self.result['waktu']}")
        print(f"Magnitudo {self.result['magnitudo']}")
        print(f"Kedalaman {self.result['kedalaman']}")
        print(
            f"Koordinat LS = {self.result['koordinat']['lat']} BT = {self.result['koordinat']['lon']}")
        print(f"{self.result['lokasi']}")
        print(f"{self.result['dirasakan']}")

    def run(self):
        self.ekstraksi_data()
        self.tampilkan_data()


if __name__ == '__main__':
    gempa_di_indonesia = GempaTerkini()
    print('Deskripsi package', gempa_di_indonesia.description)
    gempa_di_indonesia.run()
    # gempa_di_indonesia.ekstraksi_data()
    # gempa_di_indonesia.tampilkan_data()
