#(points, speed): Fungsi untuk estimasi waktu mengunjungi beberapa titik.
#VELIN
def e2t(jarak, kecepatan):
    """Hitung waktu tempuh berdasarkan jarak dan kecepatan.

    Args:
        jarak (float): Jarak dalam kilometer.
        kecepatan (float): Kecepatan dalam kilometer per jam.

    Returns:
        float: Waktu tempuh dalam jam.
    """

    waktu = jarak / kecepatan
    jam = int(waktu)
    menit = int((waktu - jam) * 60)
    detik = int(((waktu - jam) * 60 - menit) * 60)
    formatted_time = f"{jam:02}.{menit:02}.{detik:02}"
    return formatted_time