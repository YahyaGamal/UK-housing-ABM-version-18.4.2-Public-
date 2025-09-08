# UK Housing Agent Based Model

This repository includes the source code for the housing ABM used in the following JASSS publication: Gamal, Yahya. Elsenbroich, Corinna. Gilbert, Nigel. Heppenstall, Alison and Zia, Kashif (2024) 'A Behavioural Agent-Based Model for Housing Markets: Impact of Financial Shocks in the UK' Journal of Artificial Societies and Social Simulation 27 (4) 5 <http://jasss.soc.surrey.ac.uk/27/4/5.html>. doi: 10.18564/jasss.5518

The model simulates the private rental and mortgage housing markets while considering financial restrictions (interest rates and loan-to-value ratios). The full description of the ABM is available in the aforementioned publication.

The files included in this repository are:

1. `\NetLogo\Housing_Market_Model_18.4.2.nlogo`: the ABM with a complete UI
2. `\NetLogo\Housing_Market_Model_A18.4.1.nlogo`: the ABM with a simplified UI (less input parameters that the user can control)
3. `\Python\Housing_Model_ABPandas.py`: the ABM definition in Python. This requires installing the Python library `ABPandas` version 0.0.34. For documentation and instructions to install, visit [https://github.com/YahyaGamal/ABPandas_Documentation](https://github.com/YahyaGamal/ABPandas_Documentation)
4. `\Python\run_ABPandas.py`: the python file which runs the Python version of the ABM.

A version of the simplified UI ABM designed for teaching (in NetLogo) is available in the this repository: <https://github.com/YahyaGamal/Housing_ABM_Simple_UI>


