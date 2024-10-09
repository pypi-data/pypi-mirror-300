# (points): Fungsi untuk menghitung jarak total untuk beberapa titik
# SITI
# my_package/calculate_total_distance.py

def jarak_total(titik):
    total_jarak = 0.0

    for i in range(len(titik) - 1):
        x1, y1 = titik[i]
        x2, y2 = titik[i + 1]
        
        # Rumus jarak Euclidean yang benar
        jarak = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        total_jarak += jarak

    return total_jarak 

    