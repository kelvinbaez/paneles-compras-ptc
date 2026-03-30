"""
Sincroniza todos los paneles HTML al repo de GitHub Pages.
Copia desde sus ubicaciones originales, hace commit y push.

Uso: python sync_paneles.py
"""

import shutil, subprocess, os
from pathlib import Path
from datetime import datetime

# Repo local de GitHub Pages
REPO = Path(__file__).parent

# Mapeo: nombre en repo -> archivo fuente
PANELES = {
    "ids.html": Path(r"c:\Users\kbaez\DesarrolloConIA\proyectos\captura-ids\reportes\dashboard-ids.html"),
    "ids-publico.html": Path(r"c:\Users\kbaez\DesarrolloConIA\proyectos\captura-ids\reportes\dashboard-ids-publico.html"),
    "compradores.html": Path(r"c:\Users\kbaez\proyecto Asisitente de analisis\salida\paneles\evaluacion_compradores.html"),
    "entregas.html": Path(r"c:\Users\kbaez\proyecto Asisitente de analisis\salida\paneles\Panel_Entregas.html"),
    "pendientes.html": Path(r"c:\Users\kbaez\proyecto Asisitente de analisis\salida\paneles\oc_pendientes_proceso.html"),
    "radar.html": Path(r"c:\Users\kbaez\proyecto Asisitente de analisis\salida\paneles\radar_tecnologico.html"),
    "index.html": Path(r"c:\Users\kbaez\proyecto Asisitente de analisis\salida\paneles\hub_paneles.html"),
    "ayb.html": Path(r"c:\Users\kbaez\Analista de AYB\reportes\dashboards\dashboard-ayb.html"),
}


def sync(solo=None):
    """Sincroniza paneles. Si solo=nombre, sincroniza solo ese."""
    actualizados = []

    for nombre, fuente in PANELES.items():
        if solo and nombre != solo:
            continue
        if not fuente.exists():
            print(f"  AVISO: No existe {fuente}")
            continue

        destino = REPO / nombre
        # Copiar solo si cambio
        if destino.exists():
            if fuente.read_bytes() == destino.read_bytes():
                print(f"  Sin cambios: {nombre}")
                continue

        shutil.copy2(fuente, destino)
        actualizados.append(nombre)
        print(f"  Actualizado: {nombre}")

    if not actualizados:
        print("\n  Todos los paneles estan al dia.")
        return []

    # Git commit + push
    os.chdir(REPO)
    subprocess.run(["git", "add", "-A"], check=True)
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    msg = f"fix: actualizar {', '.join(actualizados)} — {fecha}"
    subprocess.run(["git", "commit", "-m", msg], check=True)
    subprocess.run(["git", "push"], check=True)
    print(f"\n  Push completado: {len(actualizados)} panel(es) actualizado(s)")
    return actualizados


if __name__ == "__main__":
    import sys
    print(f"\n{'='*50}")
    print(f"  SYNC PANELES -> GitHub Pages")
    print(f"  {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"{'='*50}\n")

    solo = sys.argv[1] if len(sys.argv) > 1 else None
    sync(solo)
