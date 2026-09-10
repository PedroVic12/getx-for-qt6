import sys
import os
import subprocess
from pathlib import Path

# Script de Voz Kokoro TTS via run_kokoro_tts.sh (C3PO Assistente Virtual BR)
RUN_KOKORO_SH = "/home/pedrov12/Documentos/GitHub/C3PO-Assistente-Virtual-BR/tools/run_kokoro_tts.sh"
TEXTO_ENTRADA_TXT = "/home/pedrov12/Documentos/GitHub/C3PO-Assistente-Virtual-BR/tools/voz-TTS-pt-br/texto_entrada.txt"

def falar_kokoro(texto: str):
    """Escreve o texto em texto_entrada.txt e dispara run_kokoro_tts.sh."""
    if not texto:
        return

    print(f"🎙️ [Kokoro TTS via run_kokoro_tts.sh] Falando: {texto}")

    # 1. Escreve no arquivo de texto de entrada do Kokoro
    txt_file = Path(TEXTO_ENTRADA_TXT)
    txt_file.parent.mkdir(parents=True, exist_ok=True)
    txt_file.write_text(texto, encoding="utf-8")
    print(f"📝 Texto gravado em: {TEXTO_ENTRADA_TXT}")

    # 2. Executa o script run_kokoro_tts.sh
    if os.path.exists(RUN_KOKORO_SH):
        try:
            subprocess.run(["bash", RUN_KOKORO_SH, str(txt_file)], check=True)
            return
        except Exception as e:
            print(f"⚠️ Erro ao executar run_kokoro_tts.sh: {e}")
    else:
        print(f"⚠️ Script de inicialização não encontrado em {RUN_KOKORO_SH}")

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Boa noite Pedro! Descanse bem. Amanhã vamos estudar Regra de Cramer, Análise de Malhas e Thévenin!"
    falar_kokoro(msg)
