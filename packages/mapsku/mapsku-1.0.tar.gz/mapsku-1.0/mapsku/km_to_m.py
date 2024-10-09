# Fungsi untuk konversi kilometer ke meter.
#JABBAR
def konv_m(ukuran, jenis="meter"):
    if jenis == "km":
         hasil = ukuran / 1000
    elif jenis == "dm":
         hasil = ukuran * 10
    elif jenis == "cm":
         hasil = ukuran * 100
    elif jenis == "mm":
         hasil = ukuran * 1000
    elif jenis == "miles":
         hasil =  ukuran / 1609.34
    elif jenis == "kaki":
         hasil = ukuran / 0.3048
    elif jenis == "yard":
         hasil = ukuran / 0.9144
    return round(hasil, 3)
