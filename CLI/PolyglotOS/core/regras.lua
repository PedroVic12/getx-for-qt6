-- Script Lua chamado pelo Python
local args = {...}
if #args > 0 then
    local usuario = args[1]
    print("Lua diz: Bem-vindo ao sistema de XP, " .. usuario .. "!")
else
    print("Lua executou com sucesso, mas sem argumentos.")
end
