#(point, center_point): Fungsi untuk menghitung jarak ke titik pusat.
#RYANNN


def distance(lat, lon, lat_pusat, lon_pusat):
    """
    Menghitung jarak antara dua titik berdasarkan koordinat geografis (dalam derajat)
    menggunakan rumus Haversine tanpa menggunakan modul math.

    Parameters:
    lat (float): Latitude titik.
    lon (float): Longitude titik.
    lat_pusat (float): Latitude titik pusat.
    lon_pusat (float): Longitude titik pusat.

    Returns:
    float: Jarak dalam kilometer.
    """
    # Radius bumi dalam kilometer
    R = 6371.0

    # Konversi derajat ke radian dengan rumus pi/180
    lat_rad = lat * (3.141592653589793 / 180)
    lon_rad = lon * (3.141592653589793 / 180)
    lat_pusat_rad = lat_pusat * (3.141592653589793 / 180)
    lon_pusat_rad = lon_pusat * (3.141592653589793 / 180)

    dlat = lat_pusat_rad - lat_rad
    dlon = lon_pusat_rad - lon_rad

    a = (dlat / 2) ** 2 + (lat_rad * lat_pusat_rad) * (dlon / 2) ** 2
    c = 2 * (a ** 0.5) / ((1 - a) ** 0.5)

    # Menghitung jarak
    jarak = R * c
    return jarak
