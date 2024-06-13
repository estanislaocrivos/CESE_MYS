import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz, firwin

# Use LaTeX font for all text
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"]
})

# ---------------------------------------------------------------------------------------------- #

# This function generates a simple input signal.
def input_signal(f, f_sampling, N):
    A = 1  # Signal amplitude

    # Time vector
    t = np.linspace(0, (N-1)/f_sampling, N)

    # Signal
    x = np.cos(2 * np.pi * f * t) 

    # Add harmonics
    harmonics = [1.5e6, 1.3e6, 1.9e6, 2.9e6, 3.1e6]
    for h in harmonics:
        x += np.cos(2 * np.pi * h * t)

    # Add DC component
    x += 6

    return x

# ---------------------------------------------------------------------------------------------- #

def bandpass_filter_response(f_sampling, f_cutoff_1, f_cutoff_2, M):
    # Normalizar frecuencias de corte
    nyquist = f_sampling / 2
    f_cutoff_1_normalized = f_cutoff_1 / nyquist
    f_cutoff_2_normalized = f_cutoff_2 / nyquist

    # Calcular el filtro pasabanda FIR
    h = firwin(M, [f_cutoff_1_normalized, f_cutoff_2_normalized], pass_zero=False, window='blackman')

    return h

# ---------------------------------------------------------------------------------------------- #

def plot_fir_response(h, f_sampling):
    w, mag_response = freqz(h)

    # Calcula la magnitud en dB
    mag_response_db = 20 * np.log10(np.abs(mag_response))

    # Calcula la fase en grados y la fase desenrollada
    phase_response_deg = np.angle(mag_response, deg=True)
    phase_response_unwrapped_deg = np.unwrap(phase_response_deg)

    # Convierte la frecuencia de radianes a Hertz
    freq_hz = w * f_sampling / (2 * np.pi)

    # Grafica la magnitud de la respuesta en frecuencia
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(freq_hz / 1000, mag_response_db)
    plt.title("FIR Filter's Magnitude Response", fontsize=10)
    plt.ylabel('Magnitude [dB]', fontsize=10)
    plt.xlabel('Frequency [kHz]', fontsize=10)
    plt.grid()

    # Grafica la fase de la respuesta en frecuencia
    plt.subplot(2, 1, 2)
    plt.plot(freq_hz / 1000, phase_response_unwrapped_deg)
    plt.title("FIR Filter's Phase Response", fontsize=10)
    plt.ylabel('Phase [degrees]', fontsize=10)
    plt.xlabel('Frequency [kHz]', fontsize=10)
    plt.grid()

    plt.subplots_adjust(hspace=0.5)
    plt.savefig('Plots/Plot_Bandpass_1MHz_Frequency.png', dpi=300) # Save plot as .png file


# ---------------------------------------------------------------------------------------------- #

def plot_input_output(x, y):
    plt.figure()

    plt.figure(figsize=(8, 6))

    # Plot x and y in two subplots:
    plt.subplot(2, 1, 1)
    plt.plot(np.linspace(0, len(x), len(x)), x, color='#1f77b4')
    plt.title("FIR Filter's Input Signal", fontsize=10)
    plt.xlabel('Samples', fontsize=10)
    plt.ylabel('Amplitude', fontsize=10)
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(np.linspace(0, len(y), len(y)), y, color='#ff7f0e')
    plt.title("FIR Filter's Output Signal", fontsize=10)
    plt.xlabel('Samples', fontsize=10)
    plt.ylabel('Amplitude', fontsize=10)
    plt.grid()

    plt.subplots_adjust(hspace=0.5)
    # plt.show()
    plt.savefig('Plots/Plot_Bandpass_1MHz_Time.png', dpi=300) # Save plot as .png file


# ---------------------------------------------------------------------------------------------- #

# Especificaciones del filtro
N = 2001  # Longitud de la señal
M = 13  # Longitud del filtro
f = 55e3  # Frecuencia de la señal
f_sampling = 10e6  # Frecuencia de muestreo

f_center = 2e6  # Frecuencia central
bw = 0.2e6  # Ancho de banda
f_cutoff_1 = f_center - bw / 2  # Frecuencia de corte baja
f_cutoff_2 = f_center + bw / 2  # Frecuencia de corte alta

# Generar los coeficientes del filtro
h = bandpass_filter_response(f_sampling, f_cutoff_1, f_cutoff_2, M)

print("Filter coefficients:", h)

# Generar la señal de entrada
x = input_signal(f, f_sampling, N)

# Aplicar el filtro a la señal de entrada
y = np.convolve(x, h, mode='same')

# Graficar la señal de entrada y salida
plot_input_output(x, y)

# Graficar la respuesta en frecuencia del filtro FIR
plot_fir_response(h, f_sampling, 'Plots/Plot_Bandpass_1MHz_Frequency.png')