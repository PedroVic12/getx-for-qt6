# Julia: Resolução de Circuitos por Regra de Cramer 3x3 e 4x4 + Análise de Malhas e Thévenin
using LinearAlgebra
using Printf

# Função para resolver sistema por Regra de Cramer com passo a passo
function resolver_cramer_3x3(A::Matrix{Float64}, b::Vector{Float64})
    println("=========================================================")
    println(" 📐 Julia [Engenharia UFF] : REGRA DE CRAMER (SISTEMA 3x3)")
    println("=========================================================")

    det_A = det(A)
    @printf("1. Determinante Principal (Δ): %.4f\n", det_A)

    if abs(det_A) < 1e-12
        println("⚠️ Sistema sem solução única (Determinante nulo Δ = 0).")
        return nothing
    end

    n = size(A, 1)
    x = zeros(n)

    for i in 1:n
        A_i = copy(A)
        A_i[:, i] = b
        det_Ai = det(A_i)
        x[i] = det_Ai / det_A
        @printf("   - Δ_%d = det(Matriz substituindo Coluna %d) = %.4f  ==>  x_%d = Δ_%d / Δ = %.4f\n", i, i, det_Ai, i, i, x[i])
    end

    return x
end

# Análise de Malhas de um Circuito Elétrico de 3 Malhas
function analise_malhas_e_thevenin()
    println("\n=========================================================")
    println(" ⚡ ANÁLISE DE MALHAS & EQUIVALENTE DE THÉVENIN (3 MALHAS)")
    println("=========================================================")
    println("Circuito Exemplo UFF:")
    println(" - Malha 1: 12*I₁ - 4*I₂ - 2*I₃ = 24  (Fonte 24V)")
    println(" - Malha 2: -4*I₁ + 10*I₂ - 4*I₃ = 0")
    println(" - Malha 3: -2*I₁ - 4*I₂ + 8*I₃ = -12 (Fonte 12V oposta)")

    # Matriz de Resistências das Malhas R_malha
    R_malha = [ 12.0 -4.0 -2.0;
                -4.0 10.0 -4.0;
                -2.0 -4.0  8.0 ]

    # Vetor de Fontes de Tensão V_fontes
    V_fontes = [24.0; 0.0; -12.0]

    println("\n📌 Solução das Correntes de Malha por Cramer:")
    I_malhas = resolver_cramer_3x3(R_malha, V_fontes)

    if I_malhas !== nothing
        @printf("\n💡 Correntes Calculadas:\n")
        @printf("   - Corrente de Malha I₁: %.4f A\n", I_malhas[1])
        @printf("   - Corrente de Malha I₂: %.4f A\n", I_malhas[2])
        @printf("   - Corrente de Malha I₃: %.4f A\n", I_malhas[3])

        # Equivalente de Thévenin nos terminais da Carga na Malha 2
        println("\n🏛️ EQUIVALENTE DE THÉVENIN NOS TERMINAIS DE CARGA (Malha 2):")
        # Tensão de circuito aberto V_th
        V_th = 10.0 * I_malhas[2] # V_oc
        # Resistência equivalente de Thévenin R_th desativando fontes
        R_th = R_malha[2,2] - (R_malha[2,1]^2 / R_malha[1,1] + R_malha[2,3]^2 / R_malha[3,3])

        @printf("   - Tensão de Thévenin (V_th)    : %.4f V\n", V_th)
        @printf("   - Resistência de Thévenin (R_th): %.4f Ω\n", R_th)
    end
    println("=========================================================")
end

analise_malhas_e_thevenin()
