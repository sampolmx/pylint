from setuptools import setup, find_packages

setup(
    name="igotyouscanner",
    version="0.1.0",
    description="Detector/Monitor básico de malware (ejemplo educativo)",
    author="Tu Nombre",
    author_email="tunombre@example.com",
    url="https://github.com/tuusuario/igotyouscanner",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "watchdog",
        "scapy",
        "virus_total_apis"
    ],
    entry_points={
        "console_scripts": [
            "igotyouscanner=igotyouscanner.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)