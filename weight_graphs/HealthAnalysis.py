import pandas as pd
import numpy as np
import yaml
import statistics

#Config-bestand laden als dictionary zodat buiten de functie alle opties
#als key+waarde behandeld kunnen worden
def get_config():
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
    return config

config = get_config()

df = config["weight_file"]
df = pd.read_csv("updated_Data_Results(Jean).csv", sep=';', decimal=',')

# Index verwijderen
blankIndex = [''] * len(df)
df.index = blankIndex

if __name__ = main:
	
