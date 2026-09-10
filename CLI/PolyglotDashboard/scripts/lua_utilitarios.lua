-- Lua Script: Utilitários Diários de Produtividade & Estudo (Batcaverna 2026)

local modo = arg[1] or "rotina"
local horas_estudo = tonumber(arg[2]) or 4.0
local horas_treino = tonumber(arg[3]) or 1.5

print("=========================================================")
print(" 🎮 Lua [Batcaverna 2026] : UTILITÁRIO DIÁRIO DE PRODUTIVIDADE")
print("=========================================================")

if modo == "rotina" or modo == "pomodoro" then
    print("📌 Calculadora de Distribuição de Foco Diário:")
    print(string.format("   - Horas Dedicadas à UFF / Estudos: %.1f h", horas_estudo))
    print(string.format("   - Horas Dedicadas a Saúde / Treino: %.1f h", horas_treino))

    local pomodoros_estudo = math.floor(horas_estudo * 60 / 25)
    local pausas_curtas = pomodoros_estudo * 5 -- 5 min por pausa
    local tempo_total_min = (pomodoros_estudo * 25) + pausas_curtas

    print(string.format("\n⏱️  Planejamento de Pomodoros (25min foco + 5min pausa):"))
    print(string.format("   - Total de Pomodoros Recomendados: %d ciclos", pomodoros_estudo))
    print(string.format("   - Tempo Total Previsto: %d min (%.1f h)", tempo_total_min, tempo_total_min / 60))
    print("   - Regra de Ouro: Fazer pausa longa de 15min a cada 4 pomodoros.")

elseif modo == "markdown" then
    print("📝 Modelo de Diário de Bordo Diário (Daily Markdown):")
    print("---------------------------------------------------------")
    print("## 📅 Daily - Pedro Victor")
    print("### 1. O que fiz ontem?")
    print("- Concluí a arquitetura MVC em QML + PySide6 para o Polyglot Dashboard.")
    print("### 2. O que farei hoje?")
    print("- Revisar matérias da UFF e praticar métodos numéricos em Julia/Python.")
    print("### 3. Bloqueios?")
    print("- Nenhum no momento.")
end

print("=========================================================")
