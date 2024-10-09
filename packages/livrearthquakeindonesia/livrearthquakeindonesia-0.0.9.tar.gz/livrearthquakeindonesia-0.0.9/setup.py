import setuptools
from setuptools import setup, find_packages

# Metadata proyek
setup(
    name='livrearthquakeindonesia',  # Nama package Anda
    version='0.0.9',  # Versi package
    description='This package will get the latest earthquake form BMKG (Agency from Indonesia)',  # Deskripsi singkat
    long_description=open('README.md').read(),  # File README yang berisi deskripsi lebih lengkap
    long_description_content_type='text/markdown',  # Tipe konten long_description, biasanya markdown
    author='Gugun Muhammad Fauzi',  # Nama Anda sebagai pembuat
    author_email='gugunmfauzi16@gmail.com',  # Email Anda
    url='https://github.com/gugunmfauzi/earthquake-detection-indonesia',  # URL repositori proyek (opsional)
    packages=find_packages(),  # Menggunakan fungsi find_packages untuk menemukan seluruh subpackage
    install_requires=[
        # Daftar dependencies atau package yang dibutuhkan oleh proyek Anda
        'numpy',
        'pandas',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  # Atau lisensi yang sesuai dengan project Anda
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta'
    ],
    python_requires='>=3.6',  # Versi minimal Python yang didukung
    package=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'nama_command=package_name.module:function',  # Jika Anda ingin membuat command line script
        ],
    },
)
