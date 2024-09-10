import csv
import parameters as p
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
    
    import plotly.graph_objects as go

    def graphic(self):
        #7f7f7f
    #AF7AC5
        node_colors = ["#6DCC4E", "#F4D03F", "#FF5733", "#7f7f7f"]
        
        fig = go.Figure(data=[go.Sankey(
            valueformat=".2f",
            valuesuffix=" W",
            node=dict(
                pad=20,
                thickness=30,
                line=dict(color="black", width=1),
                label=["Ammonia Energy Input", "Fuel Cell", "Effective Energy Outlet", "Energy lost in Exhaust Gases"],
                x=[0.1, 0.5, 0.9, 0.78], 
                y=[0.5, 0.5, 0.2, 0.8],
                color=node_colors
            ),
            link=dict(
                source=[0, 1, 1],  
                target=[1, 2, 3], 
                value=[self.e_suply, self.ee, self.amb_loses],  
                color=["rgba(109,204,78,0.6)", "rgba(244,208,63,0.6)", "#7f7f7f"]  
            )
        )])

        fig.update_layout(
            title=dict(
                text="<b> Energy Flow Sankey Diagram </B>",
                x=0.5, 
                xanchor="center",
                font=dict(size=26.5, family="Courier New, monospace", color="black"),
                subtitle=dict(
                text="Sankey diagram to visualise the energy flow in a SOFC operating with ammonia ",
                font=dict(color="gray", size=14 )),
            ),
            font=dict(size=16, family="Arial"),  
            plot_bgcolor='rgba(255,255,255,0)',  
            paper_bgcolor='rgba(245,245,245,1)',
            font_family = "Arial",
            font_size = 20
        )

        fig.add_annotation(
            x=1, y=1,
            text=f" <b> Efficiency: {self.eficiency:.1f}% </b>",
            showarrow=False,
            font=dict(size=22, color="black", family="Courier New, monospace"),
            xanchor="right",
            yanchor="top",
            bordercolor="black",
            borderwidth=2,
            bgcolor="lightblue",
            opacity=0.9
        )
        
        fig.show()



if __name__ == "__main__":
    model = Model("Outflow_3.csv")
    model.graphic()
