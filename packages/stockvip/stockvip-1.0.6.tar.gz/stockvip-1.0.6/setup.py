# setup.py
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

extensions = [
    Extension(
        "stockvip.config.config",  # Tên module cho file config.c
        ["stockvip/config/config.py"]  # Đường dẫn đến file config.c
    ),
    Extension(
        "stockvip.config.ensure_logged_in",  # Tên module cho file ensure_logged_in.c
        ["stockvip/config/ensure_logged_in.py"]  # Đường dẫn đến file ensure_logged_in.c
    ),
    Extension(
        "stockvip.process_client.login",  # Tên module cho file login.c
        ["stockvip/process_client/login.py"]  # Đường dẫn đến file login.c
    ),
    Extension(
        "stockvip.process_stock.ohlcv",  # Tên module cho file trong thư mục stock/price
        ["stockvip/process_stock/ohlcv.py"]  # Đường dẫn đến file price.c
    )
]

setup(
    name="stockvip",  # Tên gói sử dụng dấu gạch dưới
    version="1.0.6",
    author="stockvip.vn",
    author_email="support@stockvip.vn",
    description="Dữ liệu thị trường chứng khoán Việt Nam",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://stockvip.vn",

    packages=find_packages(), 
    ext_modules=cythonize(
        extensions, 
        compiler_directives={
            'language_level': "3",
            "embedsignature":True}),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "pandas==2.1.2",
        "requests",
    ],
)
