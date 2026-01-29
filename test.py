import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do sistema (circuito π simplificado)
R = 0.1  # Resistência da linha (ohms) - Não utilizado no modelo de estado simplificado, mas mantido para referência
L = 0.01  # Indutância da linha (henry)
C = 1e-6  # Capacitância da linha (farad)
R_load_initial = 50  # Resistência de carga inicial (ohms)
V_source = 100  # Tensão da fonte (volts, constante para simplificação)

# Parâmetros da simulação
t_max = 0.01  # Tempo total de simulação (segundos)
dt = 1e-6  # Passo de tempo (segundos)
n_steps = int(t_max / dt)  # Número de passos
t = np.linspace(0, t_max, n_steps)  # Vetor de tempo

# Inicialização das variáveis de estado
i_L = np.zeros(n_steps)  # Corrente no indutor
v_C = np.zeros(n_steps)  # Tensão no capacitor
i_load = np.zeros(n_steps)  # Corrente na carga

# Função para calcular a resistência da carga (muda no tempo para simular evento dinâmico)
def load_resistance(time_step):
    """Retorna a resistência da carga baseada no tempo."""
    if time_step < 0.005:  # Antes de 5ms, carga normal
        return R_load_initial
    else:  # Após 5ms, carga reduzida (simula aumento do consumo)
        return R_load_initial / 2

# Estado inicial
x = np.array([0.0, 0.0])  # Estado inicial [i_L, v_C]

# Vetor de entrada (constante)
u_vec = np.array([V_source / L, 0])

# Simulação passo a passo
for n in range(n_steps - 1):
    # Resistência da carga no instante atual
    R_load_n = load_resistance(t[n])
    
    # Matriz de estado A ajustada com a carga atual
    # A equação para dv_C/dt é (i_L - i_load) / C = (i_L - v_C/R_load) / C = i_L/C - v_C/(R_load*C)
    A_load = np.array([[0, -1/L],
                       [1/C, -1/(R_load_n * C)]])
    
    # Matriz Identidade
    I = np.eye(2)
    
    # Equação da integração trapezoidal: (I - dt/2 * A) * x_next = (I + dt/2 * A) * x_now + dt * u
    # O vetor de entrada u só afeta a primeira equação (di_L/dt)
    
    # Lado esquerdo da equação
    left_side = I - (dt / 2) * A_load
    
    # Lado direito da equação
    right_side_matrix = I + (dt / 2) * A_load
    right_side_vector = right_side_matrix @ x + dt * u_vec
    
    # Resolve o sistema linear para encontrar o próximo estado
    x_next = np.linalg.solve(left_side, right_side_vector)
    
    # Atualiza estados para o próximo passo
    x = x_next
    i_L[n + 1] = x[0]
    v_C[n + 1] = x[1]
    i_load[n + 1] = v_C[n + 1] / load_resistance(t[n+1])

# Plot dos resultados
plt.figure(figsize=(12, 8))

# Gráfico da Tensão no Capacitor
ax1 = plt.subplot(2, 1, 1)
ax1.plot(t * 1000, v_C, label="Tensão no Capacitor ($v_C$)", color='blue')
ax1.set_title('Simulação de Transitório Elétrico com Mudança de Carga', fontsize=16)
ax1.set_ylabel("Tensão (V)")
ax1.grid(True)
ax1.axvline(x=5, color='r', linestyle='--', label='Mundança de Carga (5 ms)')
ax1.legend()

# Gráfico das Correntes
ax2 = plt.subplot(2, 1, 2)
ax2.plot(t * 1000, i_L, label="Corrente no Indutor ($i_L$)", color="orange")
ax2.plot(t * 1000, i_load, label="Corrente na Carga ($i_{load}$)", color="green", linestyle='-.')
ax2.set_xlabel("Tempo (ms)")
ax2.set_ylabel("Corrente (A)")
ax2.grid(True)
ax2.axvline(x=5, color='r', linestyle='--', label='Mundança de Carga (5 ms)')
ax2.legend()

plt.tight_layout()
plt.show()


'''Explicação Prévia
Modelo do Sistema:
A linha de transmissão é representada por um circuito π simplificado, com resistência (R), indutância (L) e capacitância (C).
A carga é modelada como uma resistência (R_load) que varia no tempo para simular um evento dinâmico (entrada/saída de carga).
A fonte é uma tensão constante (V_source), mas você pode adaptá-la para uma fonte renovável (ex.: senoide ou intermitente).
Equações de Estado:
As variáveis de estado são a corrente no indutor (i_L) e a tensão no capacitor (v_C).
A matriz de estado (A) é ajustada para incluir a resistência da carga, que afeta a equação do capacitor.
Integração Trapezoidal:
O método de integração trapezoidal é usado para resolver as equações diferenciais de forma numérica.
A cada passo, a resistência da carga é atualizada, e o sistema é resolvido para calcular os novos estados.
Saídas:
O código gera gráficos da tensão no capacitor (v_C), corrente no indutor (i_L) e corrente na carga (i_load), mostrando o comportamento transitório após a mudança de carga.

Sugestões para o Desenvolvimento
Estruturação do Projeto:
Definição do Modelo: Refine os parâmetros do circuito π (valores realistas para R, L, C) com base em dados de linhas de transmissão reais. Considere adicionar mais elementos (ex.: múltiplas linhas ou fontes renováveis).
Implementação: Divida o código em funções para modularidade (ex.: uma função para o modelo, outra para a integração, outra para plotar resultados). Teste diferentes cenários (ex.: curto-circuito, variação de fonte).
Análise de Resultados: Compare os resultados com casos teóricos ou simuladores comerciais (ex.: MATLAB/Simulink) para validar o modelo. Analise o impacto de fontes renováveis (ex.: intermitência de uma fonte eólica).
Aprimoramentos no Código:
Adicione uma fonte renovável realista (ex.: tensão variável para simular geração eólica ou solar).
Inclua mais eventos dinâmicos (ex.: chaveamento, falhas).
Use bibliotecas como SciPy para solvers mais robustos ou PandaPower para modelagem de redes maiores.
Documentação:
No TCC, explique o modelo matemático (equações de estado), o método numérico (integração trapezoidal) e os cenários simulados.
Inclua gráficos comentados e tabelas com resultados para diferentes condições de carga.
'''