# -*- coding: utf-8 -*-
"""perprocessing_bioactivity_data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/156z9UiQBDNX4jF0SNRQUsmgmhze98pr0

# **Computational Drug Discovery**


---

## **ChEMBL Database**

The [*ChEMBL Database*](https://www.ebi.ac.uk/chembl/) is a database that contains curated bioactivity data of more than 2 million compounds. It is compiled from more than 76,000 documents, 1.2 million assays and the data spans 13,000 targets and 1,800 cells and 33,000 indications.
[Data as of May 8th, 2023; ChEMBL version 32].

### **Installing libraries**

Install the ChEMBL web service package so that we can retrieve bioactivity data from the ChEMBL Database.
"""

! pip install chembl_webresource_client

"""### **Importing libraries**"""

# Import necessary libraries
import pandas as pd
from chembl_webresource_client.new_client import new_client

"""## **Search for Target protein**

### **Target search for coronavirus**
"""

# Target search for coronavirus
target = new_client.target
target_query = target.search('coronavirus')
targets = pd.DataFrame.from_dict(target_query)


"""### **Select and retrieve bioactivity data for *SARS coronavirus 2 Replicase polyprotein 1ab* (8th entry)**

We will assign the fifth entry (which corresponds to the target protein, *coronavirus 3C-like proteinase*) to the ***selected_target*** variable
"""

selected_target = targets.target_chembl_id[7]

"""Here, we will retrieve only bioactivity data for *coronavirus 3C-like proteinase* (CHEMBL3927) that are reported as IC$_{50}$ values in nM (nanomolar) unit.???"""

activity = new_client.activity
res = activity.filter(target_chembl_id=selected_target).filter(standard_type="IC50")

df = pd.DataFrame.from_dict(res)


df.standard_type.unique()

"""Finally we will save the resulting bioactivity data to a CSV file **bioactivity_data.csv**."""

df.to_csv('bioactivity_data.csv', index=False)

"""## **Copying files to Google Drive**

Firstly, we need to mount the Google Drive into Colab so that we can have access to our Google adrive from within Colab.
"""

from google.colab import drive
drive.mount('/content/gdrive/', force_remount=True)

"""Next, we create a **data** folder in our **Colab Notebooks** folder on Google Drive."""

! mkdir "/content/gdrive/My Drive/Colab Notebooks/data"

! cp bioactivity_data.csv "/content/gdrive/My Drive/Colab Notebooks/data"



"""## **Handling missing data**
If any compounds has missing value for the **standard_value** column then drop it
"""

df2 = df[df.standard_value.notna()].reset_index(drop=True)

"""




"""## **Data pre-processing of the bioactivity data**

### **Labeling compounds as either being active, inactive or intermediate**
The bioactivity data is in the IC50 unit. Compounds having values of less than 1000 nM will be considered to be **active** while those greater than 10,000 nM will be considered to be **inactive**. As for those values in between 1,000 and 10,000 nM will be referred to as **intermediate**.
"""

bioactivity_class = []
for i in df2.standard_value:
  if float(i) >= 10000:
    bioactivity_class.append("inactive")
  elif float(i) <= 1000:
    bioactivity_class.append("active")
  else:
    bioactivity_class.append("intermediate")

selection = ['molecule_chembl_id', 'canonical_smiles', 'standard_value']
df3 = df2[selection]


pd.concat([df3,pd.Series(bioactivity_class)], axis=1)



"""Saves dataframe to CSV file"""

df3.to_csv('bioactivity_preprocessed_data.csv', index=False)



"""copy to the Google Drive"""

! cp bioactivity_preprocessed_data.csv "/content/gdrive/My Drive/Colab Notebooks/data"



"""---"""