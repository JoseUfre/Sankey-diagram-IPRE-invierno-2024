# Sankey diagram IPRE invierno 2024
### Creation of a sankey diagram to plot energy flow and determine efficiency of a SOFC fuell cell operating with ammonia.

 
This repository has the code developed to create a Sankey diagram based on the open source [plotly graphing library](https://plotly.com).

Based in OOP, the code its composed by a ***Model*** class, that has 4 methods:

* ***read_csv(self)***: Reads the information given to the instance and converts it into a pandas data frame.
* ***anode_off_gas_cp(self)***: Calculates the heat capacity of the anode exhaust gases according to the cell temperature. It could be useful to use the [thermo](https://thermo.readthedocs.io/thermo.chemical.html) library, but its still under development.
* ***energy(self)***: It calculates the energy delivered to the cell, the heat lost in the exhaust gases, the effective energy used by the cell and finally the efficiency of the SOFC. 
* ***graphic(self)***: Method that initialises the graph and its dependencies. 

When the ***Model*** class is instantiated, the csv file to be read must be given as a parameter.

```python
model = Model("file_to_read")
```

Diferent parameters can be modified at the ```param.py``` file.


# Disclaimer

The code and its results were made for academic purposes only, it is open to errors and does not expect to deliver definitive results or a working framework.


