# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 09:15:46 2023
Applicants - Invventors network
"""
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import re

# Read Excel file
file_location = Path(r"C:\Users\Werner\Documents\app-inv.xlsx")
df = pd.read_excel(file_location)

# Initialize dictionary to store inventors for each applicant
applicants = {}
# Some applicant names appear in different forms. If one word suffices to recognize the applicant substitute in each case the whole name by that word
Tochange = ['JANSSEN', 'GILEAD', 'GLAXOSMITHKLINE', 'TOPELIA', 'BOEHRINGER', 'ABBOTT', \
            'TIBOTEC', 'CILA', 'MERCK']

# Function to standardize applicant names by checking for short name presence in long names
def standardize_applicant_name(name, short_name):
    # Remove integers and non-alphanumeric characters
    name = re.sub(r'[^A-Za-z\s]', '', name)
    # Convert to lowercase and split into words
    name_words = name.lower().split()
    # Check if any word in the name contains the short name as a prefix
    if any(word.startswith(short_name.lower()) for word in name_words):
        return short_name
    return name

# Iterate over rows and populate dictionary
for index, row in df.iterrows():
    # Check if applicant and inventor columns are not empty
    if not pd.isna(row['Applicants']) and not pd.isna(row['Inventors']):
        # Split applicant and inventor strings by new line
        applicant_list = row['Applicants'].split('\n')
        inventor_list = row['Inventors'].split('\n')
        # Iterate over applicants and assign inventors
        for applicant in applicant_list:
            # Remove leading/trailing spaces and quotes
            applicant = applicant.strip().strip('"')
            
            # Standardize the applicant's name by checking for short name presence            
            for x in Tochange:
                applicant = standardize_applicant_name(applicant, x)
            # The line bellow should be edited to include any meaningless words appearing in the resulting network, this case is  
            # a weird result that appeared in the Orbit Intelligence results list. 
            applicant = re.sub('GILEZ', '', applicant)
            
            # Check if applicant is not empty
            if applicant != '':
                # Limit the name of the applicant to achieve at least 20 characters
                applicant_words = applicant.split()
                shortened_applicant = ''
                for word in applicant_words:
                    if len(shortened_applicant) + len(word) >= 35:
                        break
                    shortened_applicant += word + ' '
                # Remove trailing space
                shortened_applicant = shortened_applicant.strip()
                    
                  
                # Add applicant to dictionary if not already present
                if shortened_applicant not in applicants:
                    applicants[shortened_applicant] = set()
                # Add inventors to applicant's set
                for inventor in inventor_list:
                    # Remove leading/trailing spaces and quotes
                    inventor = inventor.strip().strip('"')
                    
                    # Check if inventor is not empty
                    if inventor != '':
                        applicants[shortened_applicant].add(inventor)


# Create graph and add edges between applicants connected by inventors
G = nx.Graph()
for applicant1, inventors1 in applicants.items():
    for applicant2, inventors2 in applicants.items():
        # Check if both applicants have at least one inventor in common
        if applicant1 != applicant2 and len(inventors1 & inventors2) > 0:
            # Add edge with weight equal to number of shared inventors
            G.add_edge(applicant1, applicant2, weight=len(inventors1 & inventors2))

# Get five most connected applicants
top_applicants = sorted(G.degree, key=lambda x: x[1], reverse=True)[:17]

# Create subgraph with only top applicants and their edges
H = G.subgraph([applicant for applicant, degree in top_applicants])

# Set the layout seed
seed_value = 42  # You can adjust this seed value
layout_seed = nx.random_layout(H, seed=seed_value)

# Draw graph with force-directed layout
options = {'node_color': 'lightblue', 'font_size': 8, 'edge_color': 'red', 'node_size': 600, 'width': 3}

pos = nx.spring_layout(H)

# Draw graph
plt.rcParams['figure.figsize'] = [9, 8]
options = {'node_color': 'lightblue', 'font_size':8, 'edge_color':'red', 'node_size': 600, 'width': 3,}
nx.draw_circular(H, **options, with_labels = True)
plt.axis('off')
plt.show()
