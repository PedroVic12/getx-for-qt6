import subprocess
import os
import shutil
from PySide6.QtCore import QObject, Slot

class ProcessManager(QObject):
    def _detectar_terminal(self):
        """Busca os terminais mais comuns instalados no sistema Linux."""
        terminais = ['konsole', 'alacritty', 'kitty', 'gnome-terminal', 'xfce4-terminal', 'xterm']
        for t in terminais:
            if shutil.which(t):
                return t
        return None

    @Slot(str, str, str)
    def executar_no_terminal(self, linguagem, arquivo, parametro):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(base_dir, "scripts", arquivo)

        # Monta o comando de acordo com a linguagem
        if linguagem == "cpp":
            cmd = f"{script_path} {parametro}"
        elif linguagem == "julia":
            cmd = f"julia {script_path} {parametro}"
        elif linguagem == "lua":
            cmd = f"lua {script_path} {parametro}"
        else:
            return

        # Comando final que segura o terminal aberto
        hold_terminal = f'{cmd}; echo ""; read -p "Pressione ENTER para fechar..."'

        terminal = self._detectar_terminal()

        if not terminal:
            print("❌ Erro: Nenhum emulador de terminal compatível foi encontrado no sistema.")
            return

        try:
            # Cada terminal tem uma sintaxe levemente diferente para executar comandos inline
            if terminal == 'konsole':
                subprocess.Popen(['konsole', '-e', 'bash', '-c', hold_terminal])
            elif terminal == 'gnome-terminal':
                subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', hold_terminal])
            elif terminal == 'xfce4-terminal':
                subprocess.Popen(['xfce4-terminal', '-e', f"bash -c '{hold_terminal}'"])
            elif terminal in ['alacritty', 'kitty']:
                subprocess.Popen([terminal, '-e', 'bash', '-c', hold_terminal])
            else: # Fallback genérico para xterm
                subprocess.Popen(['xterm', '-e', f"bash -c '{hold_terminal}'"])

            print(f"✅ Executando no terminal: {terminal}")

        except Exception as e:
            print(f"❌ Erro ao abrir o terminal {terminal}: {e}")
