println("==================================")
println(" JULIA : SIMULAÇÃO DE SISTEMA")
println("==================================")

if length(ARGS) > 0
    valor = parse(Float64, ARGS[1])
    resultado = valor ^ 2.5
    println("Parâmetro de entrada: ", valor)
    println("-> Resultado da simulação: ", round(resultado, digits=2))
else
    println("Nenhum dado recebido.")
end
