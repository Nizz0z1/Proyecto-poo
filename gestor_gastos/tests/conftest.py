"""Configuración de pytest para que encuentre el paquete app."""
import sys
import os

# Agrega la raíz del proyecto al path para que los imports funcionen
sys.path.insert(0, os.path.dirname(__file__) + "/..")
