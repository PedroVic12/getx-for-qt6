import os
import shutil
import subprocess
from PySide6.QtCore import QObject, Slot, Signal

class PolyglotController(QObject):
    """Controller responsável pela execução de scripts poliglotas (C++, Julia, Lua, C, Python)."""

    outputEmitted = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.scripts_dir = os.path.join(self.base_dir, "scripts")

    def _detectar_terminal(self):
        terminais = ['konsole', 'alacritty', 'kitty', 'gnome-terminal', 'xfce4-terminal', 'xterm']
        for t in terminais:
            if shutil.which(t):
                return t
        return None

    @Slot(str, str, str)
    def executar_no_terminal(self, linguagem: str, arquivo: str, parametros: str):
        """Abre o script no terminal Linux escolhido pelo sistema."""
        script_path = os.path.join(self.scripts_dir, arquivo)

        # Monta o comando de acordo com a linguagem
        if linguagem == "cpp":
            cmd = f"{script_path} {parametros}"
        elif linguagem == "c":
            cmd = f"{script_path} {parametros}"
        elif linguagem == "julia":
            cmd = f"julia {script_path} {parametros}"
        elif linguagem == "lua":
            cmd = f"lua {script_path} {parametros}"
        elif linguagem == "python":
            cmd = f"python3 {script_path} {parametros}"
        else:
            self.outputEmitted.emit(f"❌ Linguagem '{linguagem}' não suportada.")
            return

        hold_terminal = f'{cmd}; echo ""; read -p "Pressione ENTER para fechar..."'
        terminal = self._detectar_terminal()

        if not terminal:
            self.outputEmitted.emit("❌ Erro: Nenhum terminal instalado encontrado.")
            return

        try:
            if terminal == 'konsole':
                subprocess.Popen(['konsole', '-e', 'bash', '-c', hold_terminal])
            elif terminal == 'gnome-terminal':
                subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', hold_terminal])
            elif terminal == 'xfce4-terminal':
                subprocess.Popen(['xfce4-terminal', '-e', f"bash -c '{hold_terminal}'"])
            elif terminal in ['alacritty', 'kitty']:
                subprocess.Popen([terminal, '-e', 'bash', '-c', hold_terminal])
            else:
                subprocess.Popen(['xterm', '-e', f"bash -c '{hold_terminal}'"])

            msg = f"🚀 Executando '{arquivo}' ({linguagem.upper()}) no terminal {terminal}."
            self.outputEmitted.emit(msg)
            print(msg)
        except Exception as e:
            msg = f"❌ Erro ao disparar terminal: {e}"
            self.outputEmitted.emit(msg)
            print(msg)

    @Slot(str, str, str, result=str)
    def executar_inline(self, linguagem: str, arquivo: str, parametros: str) -> str:
        """Executa o script e retorna a saída capturada diretamente para a interface QML."""
        script_path = os.path.join(self.scripts_dir, arquivo)
        args_list = parametros.split() if parametros else []

        if linguagem == "cpp" or linguagem == "c":
            cmd_args = [script_path] + args_list
        elif linguagem == "julia":
            cmd_args = ["julia", script_path] + args_list
        elif linguagem == "lua":
            cmd_args = ["lua", script_path] + args_list
        elif linguagem == "python":
            cmd_args = ["python3", script_path] + args_list
        else:
            return f"❌ Linguagem '{linguagem}' desconhecida."

        try:
            res = subprocess.run(cmd_args, capture_output=True, text=True, timeout=10)
            output = res.stdout if res.returncode == 0 else f"STDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"
            self.outputEmitted.emit(output)
            return output
        except Exception as err:
            err_msg = f"❌ Erro de Execução: {str(err)}"
            self.outputEmitted.emit(err_msg)
            return err_msg
