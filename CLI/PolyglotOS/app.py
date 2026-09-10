import subprocess
import ctypes
import os
from PySide6.QtCore import QObject, Slot

class PolyglotBackend(QObject):
    def __init__(self):
        super().__init__()
        # Carrega a biblioteca C++ compilada
        base_dir = os.path.dirname(os.path.abspath(__file__))
        lib_path = os.path.join(base_dir, "core", "libalgoritmo.so")
        self.cpp_lib = ctypes.CDLL(lib_path)
    
    @Slot(int, int, result=str)
    def run_cpp(self, tensao, corrente):
        # Executa a função em C++ diretamente na memória
        resultado = self.cpp_lib.calcular_potencia_maxima(tensao, corrente)
        return f"C++ retornou a potência: {resultado} W"

    @Slot(str, result=str)
    def run_julia(self, valor):
        # Executa o script Julia via subprocesso
        base_dir = os.path.dirname(os.path.abspath(__file__))
        script = os.path.join(base_dir, "core", "simulacao.jl")
        result = subprocess.run(["julia", script, valor], capture_output=True, text=True)
        return result.stdout.strip()

    @Slot(str, result=str)
    def run_lua(self, nome):
        # Executa o script Lua via subprocesso
        base_dir = os.path.dirname(os.path.abspath(__file__))
        script = os.path.join(base_dir, "core", "regras.lua")
        result = subprocess.run(["lua", script, nome], capture_output=True, text=True)
        return result.stdout.strip()
