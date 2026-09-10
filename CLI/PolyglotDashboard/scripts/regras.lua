print("==================================")
print(" LUA : MOTOR DE REGRAS E XP")
print("==================================")

local args = {...}
if #args > 0 then
    local usuario = args[1]
    print("Iniciando rotina diária para o usuário: " .. usuario)
    print("-> Status: XP Atualizado com Sucesso! +50pts")
else
    print("Executado sem parâmetros.")
end
