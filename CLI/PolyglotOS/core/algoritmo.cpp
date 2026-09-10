#include <iostream>

// extern "C" impede o name mangling do C++ para o Python conseguir ler
extern "C" {
    int calcular_potencia_maxima(int tensao, int corrente) {
        // Simulação de um cálculo pesado em C++
        return tensao * corrente;
    }
}
