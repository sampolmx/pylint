import argparse
from igotyouscanner import core

def main():
    parser = argparse.ArgumentParser(
        description="IgotYou Scanner — Detector/Monitor básico de malware (ejemplo educativo)"
    )
    parser.add_argument(
        "--scan", metavar="PATH", help="Escanear carpeta específica"
    )
    parser.add_argument(
        "--monitor", metavar="PATH", help="Monitorear carpeta en tiempo real"
    )
    parser.add_argument(
        "--sniffer", action="store_true", help="Iniciar sniffer de red"
    )

    args = parser.parse_args()

    if args.scan:
        core.escanear_carpeta(args.scan)
    elif args.monitor:
        core.iniciar_monitor(args.monitor)
    elif args.sniffer:
        core.iniciar_sniffer()
    else:
        parser.print_help()