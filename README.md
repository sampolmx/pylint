# IgotYou — Detector/Monitor básico de malware (ejemplo)

Detecta hashes conocidos, procesos sospechosos, monitoriza archivos en tiempo real y ofrece un sniffer de red simple.

⚠️ Nota rápida y honesta: esto es un prototipo educativo — no es un antivirus listo para producción.  
Úsalo para aprender, mejorar y probar en entornos controlados.  
Si buscas protección real: compra una solución probada y certificada. 😉

---

## 📚 Índice
- [Descripción](#descripción)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Configuración y personalización](#configuración-y-personalización)
- [Ejecución como administrador / root](#ejecución-como-administrador--root)
- [Problemas conocidos y correcciones sugeridas](#problemas-conocidos-y-correcciones-sugeridas)
- [Buenas prácticas y legalidad](#buenas-prácticas-y-legalidad)
- [Cómo contribuir](#cómo-contribuir)
- [Licencia](#licencia)

---

## 📖 Descripción

Este repositorio contiene un script en Python que:

- Escanea archivos en una carpeta comparando hashes MD5 con una base de datos local de hashes maliciosos.
- Monitorea nuevos archivos creados en una ruta (watchdog).
- Detecta procesos con nombres sospechosos (psutil).
- Permite capturar tráfico de red (scapy) y detectar payloads con palabras clave.
- Incluye import para `virus_total_apis` con intención de integrar consultas a VirusTotal (no implementado por defecto).

👉 Es una **base educativa** para construir herramientas de detección/monitoreo en laboratorios o entornos de pruebas.

---

## ⚙️ Características

- Escaneo recursivo por carpeta (MD5).
- Monitor en tiempo real de creación de archivos.
- Detección simple de procesos por nombre.
- Sniffer de red básico (opcional).
- Plantilla para integrar VirusTotal.

---

## 🖥️ Requisitos

- Python 3.8+ (recomendado 3.10+)
- Dependencias Python (instalar con pip):

```bash
pip install -r requirements.txt
##En sistemas Linux/macOS puede que necesites privilegios de root para sniffing o monitorización de procesos.##

 ##🚀 Instalación##
git clone https://github.com/tuusuario/igotyouscanner.git
cd igotyouscanner

# Crear entorno virtual (opcional)
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.\.venv\Scripts\activate    # Windows

# Instalar dependencias
pip install -r requirements.txt


##▶️ Uso

Archivo principal: igotyouscanner.py.

Ejecutar escaneo y monitor:##

python igotyouscanner.py

##Dentro del script hay 3 caminos principales:
	•	escanear_carpeta("/ruta/a/escaneo") → escaneo manual.
	•	iniciar_monitor("/ruta/a/monitorear") → monitor de archivos + comprobar procesos periódicamente.
	•	iniciar_sniffer() → sniffer de red (descomentar manualmente si lo vas a usar).##
    
    ##⚡ Configuración y personalización
	•	Base de datos de hashes → edita malware_hashes:##
    malware_hashes = {
    "44d88612fea8a8f36de82e1278abb02f",
    "e99a18c428cb38d5f260853678922e03"
}
##Procesos sospechosos → edita la lista procesos_sospechosos.
	•	Palabras clave en payloads → ajusta palabras_clave = [b"password", b"malware", b"spyware"].
	•	VirusTotal → importa tu API key e implementa consultas si lo deseas.##
    
    ## 🔑 Ejecución como administrador / root
	•	Para scapy.sniff() se requieren permisos elevados (root en Linux/macOS; administrador en Windows).
	•	Para monitorizar carpetas protegidas o inspeccionar procesos del sistema también puede requerirse permisos.##
    
    ##⚖️ Buenas prácticas y legalidad
	•	Solo analiza sistemas que posees o para los que tienes autorización explícita.
	•	El sniffing de red sin permiso es ilegal en muchos países.
	•	No uses la lista de procesos como única guía: se pueden falsificar.
	•	Protege tus API keys y evita exponerlas en repos públicos##
    
    ##🤝 Cómo contribuir
	1.	Haz fork del repo.
	2.	Crea una rama (feature/mi-mejora).
	3.	Añade tus cambios con documentación clara.
	4.	Abre un Pull Request.

Ideas de mejora:
	•	Integrar consultas reales a VirusTotal.
	•	Base de datos SQLite de detecciones.
	•	Mejorar el análisis de tráfico (HTTP, credenciales).
	•	Añadir logging y alertas##
    
    ##📜 Licencia

MIT License.##

---

## 📄 requirements.txt

```txt
psutil
watchdog
scapy
virus_total_apis

