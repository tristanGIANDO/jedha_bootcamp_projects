import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Données pour le premier graphique en barres
x1 = ['A', 'B', 'C']
y1 = [10, 20, 30]


# Données pour le deuxième graphique en barres
x2 = ['D', 'E', 'F']
y2 = [15, 25, 35]

# Création de la figure avec deux sous-graphiques
fig = make_subplots(rows=1, cols=2, subplot_titles=("Graphique en barres 1", "Graphique en barres 2"))

# Ajout du premier graphique en barres
fig.add_trace(go.Bar(x=x1, y=y1, name='Barres 1'), row=1, col=1)

# Ajout du deuxième graphique en barres
fig.add_trace(go.Bar(x=x2, y=y2, name='Barres 2'), row=1, col=2)

# Mise en forme de la disposition
fig.update_layout(title_text="Exemple de graphiques en barres avec sous-graphiques")

# Affichage de la figure
fig.show()
