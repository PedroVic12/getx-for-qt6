#include <iostream>
#include <cstdlib>

int main(int argc, char* argv[]) {
    std::cout << "==================================\n";
    std::cout << " C++ : CÁLCULO DE POTÊNCIA\n";
    std::cout << "==================================\n";

    if (argc > 1) {
        int tensao = std::atoi(argv[1]);
        int corrente = 15; // Fixo para exemplo
        int potencia = tensao * corrente;
        std::cout << "Tensão recebida: " << tensao << "V\n";
        std::cout << "Corrente: " << corrente << "A\n";
        std::cout << "-> Potência Máxima: " << potencia << " W\n";
    } else {
        std::cout << "Nenhum parâmetro de tensão recebido.\n";
    }
    return 0;
}
