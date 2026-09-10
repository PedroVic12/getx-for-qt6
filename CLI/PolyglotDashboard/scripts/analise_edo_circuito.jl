# Julia - Análise de Equações Diferenciais (EDO) de Circuitos RLC (UFF)
# Simulação Numérica e Análise do Regime de Amortecimento

using Printf

function analisar_circuito_rlc(R::Float64, L::Float64, C::Float64)
    println("=========================================================")
    println(" 📈 Julia [UFF Engenharia] : EDO DE CIRCUITO RLC DE 2ª ORDEM")
    println("=========================================================")
    @printf("Parâmetros do Circuito:\n")
    @printf("   - Resistência (R): %.2f Ω\n", R)
    @printf("   - Indutância (L) : %.4f H\n", L)
    @printf("   - Capacitância(C): %.6f F (%.2f µF)\n\n", C, C*1e6)

    # Coeficiente de Amortecimento (alpha) e Frequência Ressonante (omega_0)
    alpha = R / (2.0 * L)
    omega_0 = 1.0 / sqrt(L * C)

    @printf("Análise Teórica do Sistema:\n")
    @printf("   - Coeficiente de Amortecimento (α): %.4f rad/s\n", alpha)
    @printf("   - Frequência Natural (ω₀)        : %.4f rad/s\n\n", omega_0)

    delta = alpha^2 - omega_0^2

    if delta > 1e-9
        s1 = -alpha + sqrt(delta)
        s2 = -alpha - sqrt(delta)
        println("⚡ Regime: SUPERAMORTECIDO (Overdamped)")
        @printf("   Raízes caracteristicas s₁, s₂: %.4f, %.4f\n", s1, s2)
        @printf("   Forma da Solução: i(t) = A₁*e^(%.2ft) + A₂*e^(%.2ft)\n", s1, s2)
    elseif abs(delta) <= 1e-9
        s = -alpha
        println("🎯 Regime: CRITICAMENTE AMORTECIDO (Critically Damped)")
        @printf("   Raiz dupla s: %.4f\n", s)
        @printf("   Forma da Solução: i(t) = (A₁ + A₂*t)*e^(%.2ft)\n", s)
    else
        omega_d = sqrt(omega_0^2 - alpha^2)
        println("🌊 Regime: SUBAMORTECIDO (Underdamped / Oscilatório)")
        @printf("   Frequência Amortecida (ω_d): %.4f rad/s (%.2f Hz)\n", omega_d, omega_d/(2*pi))
        @printf("   Raízes Complexas: s = %.4f ± j%.4f\n", -alpha, omega_d)
        @printf("   Forma da Solução: i(t) = e^(%.2ft) * [A₁*cos(%.2ft) + A₂*sin(%.2ft)]\n", -alpha, omega_d, omega_d)
    end
    println("=========================================================")
end

# Execução dinâmica via argumentos de linha de comando
R_arg = length(ARGS) >= 1 ? parse(Float64, ARGS[1]) : 10.0
L_arg = length(ARGS) >= 2 ? parse(Float64, ARGS[2]) : 0.1
C_arg = length(ARGS) >= 3 ? parse(Float64, ARGS[3]) : 0.0001

analisar_circuito_rlc(R_arg, L_arg, C_arg)
