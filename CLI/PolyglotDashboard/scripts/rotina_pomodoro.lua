-- Lua Script: Gestão da Rotina Diária & Anti-Kanban (Regras AGENTS.md / Batcaverna)

local user_name = arg[1] or "Pedro Victor"
local pomodoros_concluidos = tonumber(arg[2]) or 4
local tarefas_ativas = tonumber(arg[3]) or 3

print("=========================================================")
print(" 🎮 Lua [Batcaverna 2026] : ROTINA DIÁRIA & REGRAS WIP")
print("=========================================================")
print(string.format("👤 Desenvolvedor: %s", user_name))
print(string.format("⏱️  Pomodoros Concluídos Hoje: %d (%.1f horas)", pomodoros_concluidos, pomodoros_concluidos * 0.416))
print(string.format("📋 Tarefas Ativas no Post-it: %d / 3 (Limite Máximo)", tarefas_ativas))
print("---------------------------------------------------------")

if tarefas_ativas <= 3 then
    print("✅ REGRA WIP VERIFICADA: Dentro do limite saudável do Post-it digital!")
else
    print("⚠️ ALERT DE DISPERSÃO: Excesso de frentes abertas! Feche tarefas antes de abrir novas.")
end

-- Hierarquia de Prioridades (AGENTS.md)
print("\n📌 HIERARQUIA DE PRIORIDADES HOJE:")
print("   1. 🎓 Faculdade (UFF Engenharia Elétrica / Provas)")
print("   2. 🏋️  Saúde & Bem-Estar (Treino / Descanso)")
print("   3. 🚀 Projetos Pessoais (Qt6 / Polyglot QML)")

-- Cálculo de Meta de Expediente
if pomodoros_concluidos >= 6 and tarefas_ativas <= 3 then
    print("\n🎉 META DO DIA ATINGIDA! Expediente de código concluído com sucesso.")
else
    local faltam = 6 - pomodoros_concluidos
    if faltam > 0 then
        print(string.format("\n💪 Faltam %d pomodoro(s) para completar a meta diária de foco.", faltam))
    else
        print("\n🔥 Excelente foco mantido ao longo do dia!")
    end
end
print("=========================================================")
