import csv
import param as p
import pandas as pd
import plotly.graph_objects as go
import os


class Model:
    def __init__(self, data):
        self.data = p.path(data)
        self.cp = None
        self.pci = p.pci
        self.current = None
        self.area = p.Area
        self.m_in = p.m_in
        self.df_list = list()
        self.df = None
        self.V = None
        self.T = None
        self.T_inf = p.T_inf
        self.m_out = None
        self.e_suply = None
        self.ee = None      # Efective energy 
        self.amb_loses = None       # Energy lost in the  anode off gases
        self.eficiency = None
        # Incializo el modelo
        self.read_csv()
        self.anode_off_gas_cp()
        self.energy()

    
    def read_csv(self):
        with open(self.data, "r") as file:
            csvfile = csv.reader(file)
            for lines in csvfile:
                try:
                    float_list = [float(i) for i in lines] 
                    self.df_list.append(float_list) # Converting strings into floats
                except:
                    pass
        self.df = pd.DataFrame(self.df_list, columns=["T", "Cell Voltage", "Current density (A/cm2)", "Volume flow (ml/min)", "Mass outflow (ug/s)"])
        self.df["Mass outflow (ug/s)"] = self.df["Mass outflow (ug/s)"] * 1e-9 # Converting from ug/s to kg/s
        print(self.df)
        self.T = self.df["T"].mean()
        self.V = self.df["Cell Voltage"].mean()
        self.m_out = self.df["Mass outflow (ug/s)"].mean()
        self.current = self.df["Current density (A/cm2)"].mean()
    
    def anode_off_gas_cp(self):
        cp_n2 = p.cp(self.T + 273.15, "nitrogen")
        cp_steam = p.cp(self.T + 273.15, "steam")
        self.cp = (1*cp_n2 + 2*cp_steam)/(28*1 + 18*2)
    

    
    def energy(self):
        self.e_suply = self.m_in * self.pci * 1000
        self.ee = self.V * self.current
        self.amb_loses = self.m_out*self.cp*(self.T - self.T_inf)*1000
        self.eficiency = (self.ee/self.e_suply) * 100
    
    def graphic(self):
        fig = go.Figure(data=[go.Sankey(
        valueformat = ".2f",
        valuesuffix= " W",
        node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = ["Energy Inlet", "Fuel cell", "Efective energy outlet", "Energy anode off gases"],
        color = "blue"
        ),
        link = dict(
        arrowlen = 40,
        source = [0, 1, 1],
        target = [1, 2, 3],
        value = [self.e_suply, self.ee, self.amb_loses]
        ))])
        fig.update_layout(title_text="Sankey model", font_size=15)
        color_for_nodes = ["green", "yellow", "red", "violet" ]
        fig.update_traces(node_color=color_for_nodes)
        # Añadir eficiencia en una esquina
        fig.add_annotation(
        x = 1, y = 1,
        text=f"Efficiency: {self.eficiency:.1f}%",
        showarrow=False,
        font = dict(size=23, color = "black"),
        xanchor = "right",
        yanchor = "top",
        bordercolor = "black",
        borderwidth=2,
        bgcolor = "lightgreen",
        opacity=0.8
        )
        fig.show()



if __name__ == "__main__":
    model = Model("Outflow_3.csv")
    print(f"Cp del gas de escape: {model.cp}")
    print(f"Eficiencia: {model.eficiency}")
    model.graphic()
