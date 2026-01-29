import numpy as np
import matplotlib.pyplot as plt

# Parâmetros da linha de transmissão
R = 0.1  # Resistência por unidade de comprimento (ohm/km)
L = 1e-3  # Indutância por unidade de comprimento (H/km)
C = 10e-9  # Capacitância por unidade de comprimento (F/km)
G = 1e-6  # Condutância por unidade de comprimento (S/km)
length = 100  # Comprimento da linha (km)
f = 60  # Frequência (Hz)
omega = 2 * np.pi * f  # Frequência angular (rad/s)

# Impedância e admitância por unidade de comprimento
Z = R + 1j * omega * L  # Impedância série (ohm/km)
Y = G + 1j * omega * C  # Admitância shunt (S/km)

# Parâmetros do modelo π
Z_total = Z * length  # Impedância série total
Y_total = Y * length  # Admitância shunt total
Y_shunt = Y_total / 2  # Admitância shunt em cada extremidade do modelo π

# Impedância característica e constante de propagação
Z0 = np.sqrt(Z / Y)  # Impedância característica
gamma = np.sqrt(Z * Y)  # Constante de propagação

# Matriz ABCD do modelo π
A = 1 + Z_total * Y_shunt
B = Z_total
C = Y_total + Z_total * Y_shunt * Y_shunt
D = A

# Condições da linha
Vs = 100e3  # Tensão na fonte (V, rms)
Z_load = 500  # Impedância da carga (ohm)

# Cálculo de tensão e corrente na carga usando a matriz ABCD
I_load = Vs / (A * Z_load + B)
V_load = Z_load * I_load

# Perfil de tensão ao longo da linha (aproximação para visualização)
n_points = 100
x = np.linspace(0, length, n_points)
V_x = np.zeros(n_points, dtype=complex)
for i in range(n_points):
    l = x[i]
    # Matriz ABCD para uma seção parcial da linha
    Z_partial = Z * l
    Y_partial = Y * l
    Y_shunt_partial = Y_partial / 2
    A_partial = 1 + Z_partial * Y_shunt_partial
    B_partial = Z_partial
    V_x[i] = (A_partial * V_load + B_partial * I_load)

# Plot do perfil de tensão (magnitude)
plt.figure(figsize=(10, 6))
plt.plot(x, np.abs(V_x) / 1e3, label='Magnitude da Tensão (kV)')
plt.xlabel('Distância (km)')
plt.ylabel('Tensão (kV)')
plt.title('Perfil de Tensão ao Longo da Linha (Modelo π)')
plt.grid(True)
plt.legend()
plt.show()

# Exibir parâmetros calculados
print(f"Impedância característica: {np.abs(Z0):.2f} ∠ {np.angle(Z0, deg=True):.2f}° ohm")
print(f"Constante de propagação: {gamma:.2e}")
print(f"Tensão na carga: {np.abs(V_load)/1e3:.2f} kV")
print(f"Corrente na carga: {np.abs(I_load):.2f} A")