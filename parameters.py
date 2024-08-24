# Parámetros del modelo
import os
from thermo.chemical import Chemical


nh3 = Chemical("Ammonia", T=(273.15 + 748), P = 101325)
rho_nh3 = nh3.rho

pci = 18610 # kJ/kg ammonia lower heating value (PCI spanish initials)
m_in = 1.5225*10**(-7)  # kg/s (45 ml/min), rho = P/RT (ammonia at 748 °C aprox) 
Area = 1 # cm2
T_inf = 20 # °C


# NO MODIFICAR


def cp(T, esp): #Función que determina el poder calorífico de un gas en funcióon de la temperatura (en K), en kJ/kmol*K
    if esp == "ammonia":
        cp = 27.568 + 2.5630*pow(10, -2)*T + 0.99072*pow(10, -5)*T**2 + -6.6909*pow(10, -9)*T**3
    elif esp == "steam":
        cp = 32.24 + 0.1923*pow(10, -2)*T + 1.055*pow(10, -5)*T**2 + -3.595*pow(10, -9)*T**3
    elif esp == "nitrogen":
        cp = 28.90 + -0.1571*pow(10, -2)*T + 0.8081*pow(10, -5)*T**2 + -2.873*pow(10, -9)*T**3
    return cp

def path(data_sheet):
    p = os.path.join("Data sheets", data_sheet)
    return p

def convertion(m_in):
    m_in = m_in*(1/60000000)*rho_nh3
    return m_in

