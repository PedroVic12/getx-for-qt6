# Recebe argumentos do terminal enviados pelo Python
if length(ARGS) > 0
    valor = parse(Float64, ARGS[1])
    resultado = valor ^ 2.5 # Cálculo científico hipotético
    println("Julia processou o valor: ", round(resultado, digits=2))
else
    println("Nenhum dado recebido pelo Julia.")
end


