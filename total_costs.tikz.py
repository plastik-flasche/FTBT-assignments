import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tikzplotlib

# Read the provided image data into a DataFrame
data = {
    'Fehlerart': [
        'Bauelement fehlt', 'Bauelement elektrisch defekt', 'Bauelement nicht gelötet',
        'Bauelement versetzt zum Lötpad', 'Lötbrücke', 'Handlingfehler',
        'Leiterplatte gebrochen', 'sonstige Fehler'
    ],
    'Auftreten absolut': [210, 90, 110, 122, 158, 53, 51, 169],
    'Kosten pro Fehler (Cent)': [15, 70, 50, 15, 5, 10, 5, 3]
}

df = pd.DataFrame(data)

# Calculate additional columns for relative frequency and total costs
df['Relative Häufigkeit'] = df['Auftreten absolut'] / df['Auftreten absolut'].sum()
df['Gesamtkosten'] = df['Auftreten absolut'] * df['Kosten pro Fehler (Cent)']

# Sort the DataFrame based on the requirements for the histograms
df_sorted_by_frequency = df.sort_values(by='Relative Häufigkeit', ascending=False)
df_sorted_by_costs = df.sort_values(by='Gesamtkosten', ascending=False)

# Plot the second diagram: Total Costs (vertical) vs. Fehlerart (horizontal)
plt.figure(figsize=(10, 6))
colors = ['lightgreen'] * len(df_sorted_by_frequency['Fehlerart'])
top_3_color = 'red'
colors[:3] = [top_3_color] * 3
plt.bar(df_sorted_by_costs['Fehlerart'], df_sorted_by_costs['Gesamtkosten'], color=colors)
plt.title('Gesamtkosten der Fehlerarten')
plt.ylabel('Gesamtkosten (Cent)')
plt.xlabel('Fehlerart')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
tikz_code = tikzplotlib.get_tikz_code()
print(tikz_code)