#!/usr/bin/env python3
"""
AppConta - Frontend 2025
Aplicacion de contabilidad personal portable.
"""

import os
import sys

# Asegurar que el directorio raiz esta en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.ventana_principal import VentanaPrincipal


def main():
    app = VentanaPrincipal()
    app.mainloop()


if __name__ == "__main__":
    main()
