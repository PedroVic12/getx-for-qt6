#include <iostream>
#include <cmath>
#include <iomanip>
#include <cstdlib>

// Algoritmo Prático de Engenharia Elétrica (UFF / ONS):
// Cálculo de Potência Complexa (P, Q, S), Fator de Potência e Correção Capacitiva.
int main(int argc, char* argv[]) {
    std::cout << "=========================================================\n";
    std::cout << " ⚡ C++ [UFF Engenharia Elétrica] : ANÁLISE DE POTÊNCIA AC\n";
    std::cout << "=========================================================\n";

    double V_rms = 220.0; // Tensão padrão em Volts
    double I_rms = 15.0;  // Corrente em Amperes
    double phi_deg = 30.0; // Defasagem angular em graus (carga indutiva)

    if (argc > 1) V_rms = std::atof(argv[1]);
    if (argc > 2) I_rms = std::atof(argv[2]);
    if (argc > 3) phi_deg = std::atof(argv[3]);

    double phi_rad = phi_deg * M_PI / 180.0;
    double P = V_rms * I_rms * std::cos(phi_rad); // Potência Ativa (W)
    double Q = V_rms * I_rms * std::sin(phi_rad); // Potência Reativa (VAr)
    double S = V_rms * I_rms;                     // Potência Aparente (VA)
    double FP = std::cos(phi_rad);                // Fator de Potência

    // Correção do Fator de Potência para FP_alvo = 0.95
    double FP_alvo = 0.95;
    double phi_alvo_rad = std::acos(FP_alvo);
    double Q_desejado = P * std::tan(phi_alvo_rad);
    double Qc_necessario = Q - Q_desejado; // Reativo capacitivo necessário (VAr)

    double freq = 60.0; // 60 Hz
    double omega = 2.0 * M_PI * freq;
    double C_microFarads = (Qc_necessario > 0) ? (Qc_necessario / (omega * V_rms * V_rms)) * 1e6 : 0.0;

    std::cout << std::fixed << std::setprecision(2);
    std::cout << "📌 Parâmetros da Carga:\n";
    std::cout << "   - Tensão RMS (V)    : " << V_rms << " V\n";
    std::cout << "   - Corrente RMS (I)  : " << I_rms << " A\n";
    std::cout << "   -Ângulo de Carga (θ): " << phi_deg << "°\n\n";

    std::cout << "📊 Resultados do Triângulo de Potências:\n";
    std::cout << "   - Potência Ativa (P)   : " << P << " W\n";
    std::cout << "   - Potência Reativa (Q) : " << Q << " VAr\n";
    std::cout << "   - Potência Aparente (S): " << S << " VA\n";
    std::cout << "   - Fator de Potência(FP): " << FP << " (" << (phi_deg >= 0 ? "Indutivo" : "Capacitivo") << ")\n\n";

    std::cout << "💡 Correção do Fator de Potência (Meta: 0.95 Indutivo):\n";
    std::cout << "   - Injeção Reativa (Qc) : " << (Qc_necessario > 0 ? Qc_necessario : 0.0) << " VAr\n";
    std::cout << "   - Capacitância Requerida: " << C_microFarads << " µF (em 60 Hz)\n";
    std::cout << "=========================================================\n";

    return 0;
}
