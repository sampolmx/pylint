# 2) `Antimalware.py` — versión corregida y mejorada

Corto, funcional y comentado. Pega esto encima del archivo actual o reemplázalo.  

```python
#!/usr/bin/env python3
"""
Antimalware.py - versión corregida básica.
Funciones:
 - escaneo por hash (MD5)
 - monitor de archivos (watchdog)
 - detección básica de procesos (psutil)
 - sniffer básico (scapy) opcional (requiere privilegios)
"""

import os
import hashlib
import time
from typing import Optional
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import scapy.all as scapy
import logging

# --- Configuración básica de logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# --- Base de datos de hashes de malware (ejemplo) ---
# IMPORTANTE: añade hashes reales aquí como strings en el set.
malware_hashes = {
    "44d88612fea8a8f36de82e1278abb02f",  # EJEMPLO
    "e99a18c428cb38d5f260853678922e03",  # Ejemplo (EICAR test file MD5 hipotético)
}

# --- Función para calcular el MD5 de un archivo ---
def calcular_hash(archivo: str) -> Optional[str]:
    hasher = hashlib.md5()
    try:
        with open(archivo, "rb") as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (FileNotFoundError, PermissionError) as e:
        logging.debug(f"No se pudo leer {archivo}: {e}")
        return None
    except Exception as e:
        logging.exception(f"Error calculando hash de {archivo}: {e}")
        return None

# --- Escanear archivos en una carpeta (recursivo) ---
def escanear_carpeta(ruta: str) -> None:
    ruta = os.path.abspath(ruta)
    logging.info(f"Escaneando: {ruta}")
    if not os.path.exists(ruta):
        logging.warning(f"La ruta {ruta} no existe.")
        return
    for root, _, files in os.walk(ruta):
        for file in files:
            archivo_path = os.path.join(root, file)
            file_hash = calcular_hash(archivo_path)
            if file_hash:
                if file_hash in malware_hashes:
                    logging.warning(f"[ALERTA] Malware detectado: {archivo_path} (MD5: {file_hash})")
                else:
                    logging.debug(f"No coincide: {archivo_path} (MD5: {file_hash})")

# --- Detección de procesos sospechosos ---
def detectar_procesos() -> None:
    procesos_sospechosos = {"keylogger.exe", "trojan.exe", "rat.exe"}  # nombres ejemplo
    for proceso in psutil.process_iter(attrs=['pid', 'name']):
        try:
            nombre = (proceso.info.get('name') or "").lower()
            if nombre in procesos_sospechosos:
                logging.warning(f"[ALERTA] Proceso sospechoso detectado: {proceso.info['name']} (PID: {proceso.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        except Exception:
            logging.exception("Error iterando procesos")

# --- Monitor de archivos en tiempo real ---
class MonitorArchivos(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"[MONITOR] Nuevo archivo detectado: {event.src_path}")
            file_hash = calcular_hash(event.src_path)
            if file_hash and file_hash in malware_hashes:
                logging.warning(f"[ALERTA] Malware detectado en: {event.src_path} (MD5: {file_hash})")

    def on_modified(self, event):
        # opcional: reaccionar a modificaciones
        if not event.is_directory:
            logging.info(f"[MONITOR] Archivo modificado: {event.src_path}")

# --- Sniffer de red para detectar actividad sospechosa ---
def analizar_paquetes(paquete):
    try:
        if paquete.haslayer(scapy.TCP) and paquete.haslayer(scapy.Raw):
            payload = bytes(paquete[scapy.Raw].load)
            palabras_clave = [b"password", b"malware", b"spyware"]
            if any(palabra in payload for palabra in palabras_clave):
                src = paquete[scapy.IP].src if paquete.haslayer(scapy.IP) else "unknown"
                dst = paquete[scapy.IP].dst if paquete.haslayer(scapy.IP) else "unknown"
                logging.warning(f"[ALERTA] Tráfico sospechoso ({src} -> {dst}): {payload[:200]!r}")
    except Exception:
        logging.exception("Error analizando paquete")

# --- Inicializar el monitor de archivos y procesos ---
def iniciar_monitor(ruta_a_monitorear: str) -> None:
    ruta_a_monitorear = os.path.abspath(ruta_a_monitorear)
    if not os.path.exists(ruta_a_monitorear):
        logging.error(f"La ruta a monitorear no existe: {ruta_a_monitorear}")
        return

    event_handler = MonitorArchivos()
    observer = Observer()
    observer.schedule(event_handler, ruta_a_monitorear, recursive=True)
    observer.start()
    logging.info(f"[INFO] Monitor de archivos iniciado en: {ruta_a_monitorear}")

    try:
        while True:
            detectar_procesos()
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("Interrupción por teclado. Deteniendo monitor...")
        observer.stop()
    except Exception:
        logging.exception("Error en el bucle principal del monitor")
        observer.stop()
    observer.join()
    logging.info("Monitor detenido.")

# --- Iniciar sniffer de red (requiere permisos) ---
def iniciar_sniffer(interface: Optional[str] = None) -> None:
    logging.info("[INFO] Iniciando sniffer de red... (Presiona Ctrl-C para detener)")
    # Nota: escanear tráfico en interfaces reales requiere privilegios.
    try:
        scapy.sniff(store=False, prn=analizar_paquetes, iface=interface)
    except PermissionError:
        logging.error("Permiso denegado: ejecuta con privilegios de administrador/root para sniffing.")
    except Exception:
        logging.exception("Error iniciando sniffer")

# --- Punto de entrada ---
if __name__ == "__main__":
    # Cambia estas rutas según tu uso:
    RUTA_ESCANEO = "./"          # carpeta para escaneo manual inicial
    RUTA_MONITOREO = "./"       # carpeta que vigilar en tiempo real

    # Escaneo manual al inicio
    escanear_carpeta(RUTA_ESCANEO)

    # Iniciar monitor (esto queda en bucle hasta Ctrl-C)
    # Si quieres solo ejecutar sniffer, comenta la línea de abajo y descomenta iniciar_sniffer()
    iniciar_monitor(RUTA_MONITOREO)

    # Para arrancar sniffing en vez del monitor, usa:
    # iniciar_sniffer()  # descomentar si quieres sniffear (requiere permisos)
