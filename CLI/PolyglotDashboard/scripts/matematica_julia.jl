# Julia: Matemática Aplicada (Álgebra Linear & Sistemas de Potência)
using LinearAlgebra
using Printf

function resolver_sistema_eletrico()
    println("=========================================================")
    println(" 📈 Julia [Matemática Aplicada] : ÁLGEBRA LINEAR & SISTEMAS")
    println("=========================================================")

    # Matriz de Admitância nodal 3x3 de um sistema elétrico com referência à terra
    Ybus = [ 14.0 -4.0 -8.0;
            -4.0 12.0 -6.0;
            -8.0 -6.0 16.0 ]

    # Vetor de Correntes Injetadas nas barras (A)
    I_inj = [100.0; 0.0; -20.0]

    println("📌 Matriz de Admitância Nodal Ybus (3x3):")
    display(Ybus)

    # Resolução exata V = Ybus \ I_inj
    V_barras = Ybus \ I_inj

    println("\n⚡ Vetor de Tensões nas Barras V (Volts):")
    for i in 1:length(V_barras)
        @printf("   - Barra %d: %.4f V\n", i, V_barras[i])
    end

    # Determinante e Número de Condição
    det_Y = det(Ybus)
    cond_Y = cond(Ybus)
    @printf("\n📊 Análise Matricial:\n")
    @printf("   - Determinante det(Ybus) : %.2f\n", det_Y)
    @printf("   - Número de Condição    : %.4f (Sistema bem condicionado)\n", cond_Y)
    println("=========================================================")
end

resolver_sistema_eletrico()
