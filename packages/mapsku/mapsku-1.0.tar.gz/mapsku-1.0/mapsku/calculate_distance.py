#Fungsi untuk menghitung jarak tengah antar koordinat.
#FERA

def midpoint(lat1, lon1, lat2, lon2):
    def to_radian(degree):
        return degree * (3.141592653589793 / 180)
    
    def to_degree(radian):
        return radian * (180 / 3.141592653589793)

    # Mengonversi derajat ke radian
    lat1 = to_radian(lat1)
    lon1 = to_radian(lon1)
    lat2 = to_radian(lat2)
    lon2 = to_radian(lon2)

    # Menghitung titik tengah
    dlon = lon2 - lon1

    Bx = cos(lat2) * cos(dlon)
    By = cos(lat2) * sin(dlon)
    lat_mid = atan2(sin(lat1) + sin(lat2),
                    sqrt((cos(lat1) + Bx) ** 2 + By ** 2))
    lon_mid = lon1 + atan2(By, cos(lat1) + Bx)

    # Mengonversi kembali ke derajat
    lat_mid = to_degree(lat_mid)
    lon_mid = to_degree(lon_mid)

    return lat_mid, lon_mid

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
