import nbformat as nbf
import pandas as pd

df = pd.read_excel('Hi5_dataset_dictionary_variables.xlsx', sheet_name="Meteo (Weather)", engine='openpyxl')

with open("notebook_feature_engineering.ipynb", "r") as f:
    nb = nbf.read(f, as_version=4)

ncells = []

for category, description in zip(df["Variable"],df["Description"]):
    ccell = nbf.v4.new_code_cell(f"""
        import matplotlib.pyplot as plt

        plt.hist(meteo_variables["{category}"])
        plt.xlabel("{description.replace("\n", " ")}")
        plt.show() 
    """)
    ncells.append(ccell)

nb['cells'].extend(ncells)

with open("test.ipynb", "w") as f:
    nbf.write(nb, f)

