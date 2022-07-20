import requests
from bs4 import BeautifulSoup


def ekstraksi_data():
    """
    Tanggal: 18 Juli 2022, 
    Waktu: 09:54:24 WIB
    Magnitudo: 4.4
    Kedalaman: 10 km
    Lokasi: LAT = 4.91 - LON = 129.62

    Pusat Gempa: Pusat gempa berada di laut 52 km BaratDaya Banda
    Dirasakan (Skala MMI): III Banda
    """
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
    return result


def tampilkan_data(result):
    print('Gempa Berdasarkan BMKG')
    print(f"Tanggal, {result['tanggal']}")
    print(f"Waktu, {result['waktu']}")
    print(f"Magnitudo {result['magnitudo']}")
    print(f"Kedalaman {result['kedalaman']}")
    print(
        f"Koordinat LS = {result['koordinat']['lat']} BT = {result['koordinat']['lon']}")
    print(f"{result['lokasi']}")
    print(f"{result['dirasakan']}")

if __name__ == '__main__':
    result = ekstraksi_data()
    tampilkan_data(result)