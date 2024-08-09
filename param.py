# Parámetros del modelo

pci = 18610 # kJ/kg
m_in = 5.475*10**(-7)  # en kg/s (45 ml/min)
I = 10 #A
T_inf = 20 # °C


def cp(T, esp): #Función que determina el poder calorífico de un gas en funcióon de la temperatura (en K), en kJ/kmol*K
    if esp == "ammonia":
        cp = 27.568 + 2.5630*pow(10, -2)*T + 0.99072*pow(10, -5)*T**2 + -6.6909*pow(10, -9)*T**3
    elif esp == "steam":
        cp = 32.24 + 0.1923*pow(10, -2)*T + 1.055*pow(10, -5)*T**2 + -3.595*pow(10, -9)*T**3
    elif esp == "nitrogen":
        cp = 28.90 + -0.1571*pow(10, -2)*T + 0.8081*pow(10, -5)*T**2 + -2.873*pow(10, -9)*T**3
    return cp


