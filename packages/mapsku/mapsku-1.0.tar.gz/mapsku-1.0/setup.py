from setuptools import setup, find_packages

setup(
    name="mapsku",
    version="1.0",
    author="Kelompok 1 Algoritma & Pemrograman B",
    description="Package untuk perhitungan jarak dan fungsi sistem koordinat geografis",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Ryannfirmansyah/Perhitungan_jarak_dan_sistem_koordinat.git",  # Ganti dengan URL yang sesuai
    packages=find_packages(),
    install_requires=[
        "geopy",  # library eksternal yang mungkin diperlukan
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
