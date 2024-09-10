# Module to analize de variation of effiency in the fuel cell 
# while varying the inlet of ammonia.


import csv
import parameters as p
import pandas as pd
import matplotlib.pyplot as plt
import os


class Model:
    def __init__(self, data_i, data):
        self.data_i = p.path(data_i)
        self.data = p.path(data)
        self.cp = None
        self.pci = p.pci
        self.current = None
        self.area = p.Area
        self.m_in = p.m_in
        self.df_list = list()
        self.df_i_list = list()
        self.df = None
        self.df_i = None
        self.V = None
        self.T = None
        self.T_inf = p.T_inf
        self.m_out = None
        self.e_suply = None
        self.ee = None      # Efective energy 
        self.amb_loses = None       # Energy lost in the  anode off gases
        # List for plotting
        self.efficiency_list = list()
        self.m_in_list = None
        self.V_list = list()
        # Lists by fuel inlet
        self.v_30 = list()
        self.v_80 = list()
        self.v_130 = list()
        # List of eff by fuel inlet
        self.e_30 = list()
        self.e_80 = list()
        self.e_130 = list()
        # Incializo el modelo
        self.read_csv()
        self.anode_off_gas_cp()
        self.efficiency()


    
    def read_csv(self):
        with open(self.data, "r") as file:
            csvfile = csv.reader(file)
            for lines in csvfile:
                try:
                    float_list = [float(i) for i in lines] 
                    self.df_list.append(float_list) # Converting strings into floats
                except:
                    pass
        self.df = pd.DataFrame(self.df_list, columns=["J_fuel (kg/s)", "Cell Voltage", "Volume outflow (ml/min)", "Mass outflow (ug/s)"])
        self.df["Mass outflow (ug/s)"] = self.df["Mass outflow (ug/s)"] * 1e-9 # Converting from ug/s to kg/s
        self.m_in_list = self.df["J_fuel (kg/s)"].to_numpy().tolist()
        self.df["J_fuel (kg/s)"] = self.df["J_fuel (kg/s)"].apply(p.convertion)
        # Read current density
        with open(self.data_i, "r") as file_i:
            csvfile_i= csv.reader(file_i)
            for lines in csvfile_i:
                try:
                    f_list = [float(i) for i in lines]
                    self.df_i_list.append(f_list)
                except:
                    pass

        self.df_i = pd.DataFrame(self.df_i_list, columns=["T", "Cell Voltage", "Current density (A/cm2)", "Volume flow (ml/min)", "Mass outflow (ug/s)"])
        self.T = self.df_i["T"].mean()
        self.current = self.df_i["Current density (A/cm2)"].mean()

    # This method is not used in this module
    def anode_off_gas_cp(self):
        cp_n2 = p.cp(self.T + 273.15, "nitrogen")
        cp_steam = p.cp(self.T + 273.15, "steam")
        self.cp = (1*cp_n2 + 2*cp_steam)/(28*1 + 18*2)
    

    
    def efficiency(self):
        for n in range(len(self.df)):
            m_in = self.df.iloc[n]["J_fuel (kg/s)"]
            V = self.df.iloc[n]["Cell Voltage"]
            e_suply = m_in*self.pci*1000
            electric_e = V *self.current
            eff = round((electric_e/e_suply)*100,1)
            if m_in == 1.0162271619807454e-07:
                self.v_30.append(V)
                self.e_30.append(eff)
            elif m_in == 2.7099390986153215e-07:
                self.v_80.append(V)
                self.e_80.append(eff)
            elif m_in == 4.403651035249897e-07:
                self.v_130.append(V)
                self.e_130.append(eff)
    
    def graphic(self):
        fig, ax1 = plt.subplots()
        ax1.plot(self.v_30, self.e_30, label = "30 ml/min")
        ax1.plot(self.v_80, self.e_80, label = "80 ml/min")
        ax1.plot(self.v_130, self.e_130, label = "130 ml/min")
        plt.xlabel("Cell Voltage (V)")
        plt.ylabel("Cell efficiency (%)")
        plt.title("SOFC efficiency when varying ammonia suply")

        # ax2 = ax1.twinx()
        # ax2.plot(self.m_in_list, self.V_list)
        plt.legend()
        plt.show()


if __name__ == "__main__":
    model = Model("Outflow_3.csv", "Outflow_multiple.csv")
    model.graphic()