# (points, reference_point): Fungsi untuk mencari titik terdekat dari kumpulan titik.
#ANGEL
def haversine(longitude1, latitude1, longitude2, latitude2):
    R = 6371  # Radius bumi dalam kilometer
    pi = 3.141592653589793

    # Konversi derajat ke radian
    dlong = (longitude2 - longitude1) * (pi / 180.0)
    dlat = (latitude2 - latitude1) * (pi / 180.0)
    
    a = ( (dlat / 2) ** 2 + 
          ( (pi / 180.0) * latitude1 ) * ( (pi / 180.0) * latitude2 ) * 
          (dlong / 2) ** 2 )
    c = 2 * ( (a ** 0.5) )
    
    return R * c

def titik_terdekat(titik_pusat, kumpulan_titik):
    longitude_pusat, latitude_pusat = titik_pusat
    titik_terdekat = None
    jarak_terdekat = float('inf')
    
    for nama_kota, titik in kumpulan_titik:
        longitude_titik, latitude_titik = titik
        jarak_sekarang = haversine(longitude_pusat, latitude_pusat, longitude_titik, latitude_titik)
        if jarak_sekarang < jarak_terdekat:
            jarak_terdekat = jarak_sekarang
            titik_terdekat = (nama_kota, titik)
            
    return titik_terdekat
