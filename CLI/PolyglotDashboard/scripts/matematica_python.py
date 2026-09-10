import sys
import math

# Python: Matemática Aplicada (Método de Newton-Raphson & Cálculo de Matrizes)
def f(x):
    # Exemplo: f(x) = x^3 - 2x - 5 (Busca de raiz real)
    return x**3 - 2*x - 5

def df(x):
    # Derivada f'(x) = 3x^2 - 2
    return 3*x**2 - 2

def newton_raphson(x0, tol=1e-6, max_iter=50):
    print("=========================================================")
    print(" 🐍 Python [Matemática Aplicada] : MÉTODO DE NEWTON-RAPHSON")
    print("=========================================================")
    print(f"📌 Buscando raiz de f(x) = x³ - 2x - 5 a partir de x₀ = {x0}")

    x = x0
    for i in range(1, max_iter + 1):
        y = f(x)
        dy = df(x)
        if abs(dy) < 1e-12:
            print("⚠️ Derivada nula. Interrompendo.")
            break
        x_next = x - y / dy
        erro = abs(x_next - x)
        print(f"   Iteração {i:02d}: x = {x_next:.6f} | f(x) = {y:.6e} | Erro = {erro:.6e}")
        if erro < tol:
            print(f"\n🎯 Raiz encontrada com sucesso: x* = {x_next:.8f}")
            print("=========================================================")
            return x_next
        x = x_next

    print("=========================================================")
    return x

if __name__ == "__main__":
    chute_inicial = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
    newton_raphson(chute_inicial)
