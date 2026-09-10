#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// C Language: Simulação de Fila de Despacho de Eventos (ONS / Automação)
int main(int argc, char* argv[]) {
    printf("=========================================================\n");
    printf(" ⚙️ C [Sistemas / ONS] : SIMULAÇÃO DE FILA DE EVENTOS\n");
    printf("=========================================================\n");

    int num_eventos = (argc > 1) ? atoi(argv[1]) : 100;
    int buffer_max = 50;
    int eventos_processados = 0;
    int eventos_descartados = 0;
    int fila_atual = 0;

    srand(12345); // Semente fixa para reprodutibilidade

    for (int i = 1; i <= num_eventos; i++) {
        // Chegada aleatória de solicitações de manobra / pacotes
        int chegaram = rand() % 4; // 0 a 3 novos eventos
        if (fila_atual + chegaram <= buffer_max) {
            fila_atual += chegaram;
        } else {
            int aceitos = buffer_max - fila_atual;
            eventos_descartados += (chegaram - aceitos);
            fila_atual = buffer_max;
        }

        // Processamento de 1 a 2 eventos por ciclo
        int processados = rand() % 3; // 0 a 2
        if (processados > fila_atual) processados = fila_atual;
        fila_atual -= processados;
        eventos_processados += processados;
    }

    printf("📊 Estatísticas da Simulação:\n");
    printf("   - Total de Eventos Solicitados: %d\n", num_eventos);
    printf("   - Eventos Processados com Éxito: %d\n", eventos_processados);
    printf("   - Eventos Descartados (Buffer Overflow): %d\n", eventos_descartados);
    printf("   - Eventos Remanescentes na Fila: %d\n", fila_atual);
    printf("   - Taxa de Sucesso: %.2f%%\n", (double)eventos_processados / num_eventos * 100.0);
    printf("=========================================================\n");

    return 0;
}
