#(points, center_point, radius): Fungsi untuk menyaring wilayah berdasarkan radius tertentu.
#FERA

def saring_radius(lat1, lon1, lat2, lon2):
    # Konversi derajat ke radian
    def to_radian(degree):
        return degree * (3.141592653589793 / 180)
    
    # Radius bumi dalam kilometer
    R = 6371.0
    
    # Mengonversi latitude dan longitude ke radian
    lat1 = to_radian(lat1)
    lon1 = to_radian(lon1)
    lat2 = to_radian(lat2)
    lon2 = to_radian(lon2)

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = (pow((sin(dlat / 2)), 2) +
         cos(lat1) * cos(lat2) * pow((sin(dlon / 2)), 2))
    
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    # Menghitung jarak
    jarak = R * c
    return jarak

def filtered(locations, center_lat, center_lon, radius):
    # Lokasi yang berada dalam radius
    filtered_locations = []
    
    for name, (lat, lon) in locations.items():
        # Hitung jarak ke pusat
        jarak = saring_radius(center_lat, center_lon, lat, lon)
        
        # Jika jarak dalam radius, tambahkan ke daftar yang terfilter
        if jarak <= radius:
            filtered_locations.append(name)
    
    return filtered_locations

# Fungsi sinus, cosinus, akar kuadrat, dan arctan2 tanpa impor
def sin(x):
    return x - (x**3 / 6) + (x**5 / 120) - (x**7 / 5040)

def cos(x):
    return 1 - (x**2 / 2) + (x**4 / 24) - (x**6 / 720)

def sqrt(x):
    r = x
    precision = 0.000001
    while abs(x - r * r) > precision:
        r = (r + x / r) / 2
    return r

def atan2(y, x):
    pi_value = 3.141592653589793
    if x > 0:
        return atan(y / x)
    elif x < 0 and y >= 0:
        return atan(y / x) + pi_value
    elif x < 0 and y < 0:
        return atan(y / x) - pi_value
    elif x == 0 and y > 0:
        return pi_value / 2
    elif x == 0 and y < 0:
        return -pi_value / 2
    else:
        return 0

def atan(x):
    return x - (x**3 / 3) + (x**5 / 5) - (x**7 / 7)