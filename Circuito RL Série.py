"""
Este script simula a energização de um circuito RL e um evento 
de curto-circuito parcial, utilizando o método de Equações de Estado
e a integração trapezoidal para a resolução numérica
"""

# Importação de Bibliotecas
# NumPy - cálculos numéricos e manipulação de vetores.
# Matplotlib - gráficos
import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do Sistema e do Evento
# Define as características físicas do circuito elétrico
L = 0.1 # Indutância da linha (Henry). Representa a oposição à mudança de corrente
V_fonte = 220.0 # Tensão da fonte de alimentação (Volts)

# Esta função simula um evento dinâmico no circuito.
# Neste caso, um curto-circuito parcial que ocorre em t=0.05s.
def pegar_resistência(time):
    """Retorna a resistência do circuito baseada no tempo para simular um evento."""
    if time < 0.05:
        # Antes de 50ms, o circuito opera com sua resistência normal.
        return 10.0
    else:
        # Após 50ms, a resistência cai drasticamente, simulando uma falha (curto-circuito).
        return 1.0

# Parâmetros da Simulação
# Define a "qualidade" e a duração da simulação.
t_max = 0.1   # Tempo total que a simulação irá durar (segundos).
dt = 1e-5     # Passo de tempo (segundos). Intervalo entre cada cálculo.
              # Um 'dt' pequeno aumenta a precisão, mas exige mais cálculos!!!
n_steps = int(t_max / dt) # Calcula o número total de passos ou iterações na simulação.
t = np.linspace(0, t_max, n_steps) # Cria um vetor de tempo, com todos os instantes de tempo da simulação.
                                   # Sequência de números que são igualmente espaçados entre si relóio da simulação

# Inicialização das Variáveis 
# Prepara os vetores que armazenarão os resultados em cada passo de tempo
# Começam com zeros e serão preenchidos durante o loop

# A única variável de estado do o sistema é a corrente no indutor (i_L)
# O estado descreve a "memória" ou a condição interna do sistema
i_L = np.zeros(n_steps) # np.zeros cria uma matriz cheia de zeros a serem "completado"

# As saídas são as grandezas a serem medidas
v_R = np.zeros(n_steps) # Tensão no resistor
v_L = np.zeros(n_steps) # Tensão no indutor

# Condição inicial do sistema
# No tempo t=0, o circuito está desligado, então a corrente é zero
x = 0.0  # O estado 'x' é a corrente i_L. x(0) = 0

# A entrada do sistema (sinal de controle)
# Neste caso, é a tensão constante da fonte
u = V_fonte

# Loop Principal da Simulação
for n in range(n_steps - 1): # O loop vai do passo 0 até o penúltimo passo
    
    # Pega o valor da resistência para o instante de tempo atual (t[n])
    R_n = pegar_resistência(t[n])

    # Monta as "matrizes" (que aqui são números únicos) do modelo de estado
    # Essas matrizes vêm da equação: di/dt = (-R/L)*i + (1/L)* V_fonte
    A = -R_n / L   # Matriz A: Como o estado atual (corrente) influencia a sua própria mudança.
    B = 1 / L      # Matriz B: Como a entrada (tensão da fonte) influencia a mudança do estado.

    # Aplica o método da Integração Trapezoidal para encontrar o próximo valor da corrente
    # Este método é numericamente estável e mais preciso que métodos mais simples (como Euler)
    # A fórmula é: (1 - dt/2 * A) * x_próximo = (1 + dt/2 * A) * x_agora + dt * B * u
    
    # Calcula o termo que multiplica o estado futuro (x_próximo)
    lado_esquerdo = 1 - (dt / 2) * A
    
    # Calcula todo o lado direito da equação, que depende apenas de valores conhecidos (do passo atual)
    lado_direito = (1 + (dt / 2) * A) * x + dt * B * u

    # Resolve a equação para encontrar o próximo estado (x_próximo)
    # Como é uma equação simples, basta uma divisão
    x_próximo = lado_direito / lado_esquerdo
    
    # ---- Atualização para o próximo passo ----
    
    # Guarda o valor da corrente calculado no vetor de resultados
    i_L[n + 1] = x_próximo
    
    # Atualiza a variável 'x' para ser usada na próxima iteração do loop
    x = x_próximo
    
    # Calcula as tensões (saídas) com base no novo estado (nova corrente)
    R_proxíma = pegar_resistência(t[n+1])
    v_R[n + 1] = R_proxíma * i_L[n + 1] # Lei de Ohm: v_R = R * i
    v_L[n + 1] = V_fonte - v_R[n + 1] # Lei de Kirchhoff: v_L = V_fonte - v_R

# Visualização dos Resultados
# Cria os gráficos para analisar o que aconteceu na simulação
# 'subplots' cria uma figura com vários gráficos
fig, axes = plt.subplots(2, 1, figsize=(12, 9), sharex=True)
fig.suptitle('Simulação de Curto-Circuito em Circuito RL Série', fontsize=16)

# Gráfico da Corrente (eixo superior)
axes[0].plot(t * 1000, i_L, label='Corrente no Indutor ($i_L$)', color='red')
axes[0].set_ylabel('Corrente (A)')
axes[0].grid(True)
axes[0].legend()
axes[0].set_title('Corrente do Circuito')
# Adiciona uma linha vertical para marcar o momento exato do evento.

# Gráfico das Tensões (eixo inferior)
axes[1].plot(t * 1000, v_R, label='Tensão no Resistor ($v_R$)', color='blue')
axes[1].plot(t * 1000, v_L, label='Tensão no Indutor ($v_L$)', color='green')
axes[1].set_xlabel('Tempo (ms)') # O eixo x é compartilhado, então só precisa de um rótulo.
axes[1].set_ylabel('Tensão (V)')
axes[1].grid(True)
axes[1].legend()
axes[1].set_title('Tensões nos Componentes')


# Ajusta o layout para evitar sobreposição de títulos e rótulos.
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Mostra o gráfico na tela.
plt.show()