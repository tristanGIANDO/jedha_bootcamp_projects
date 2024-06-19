# Projet Speed Dating

<img src="/resources/Tinder-Symbole.png" alt="tinder_symbole" style="width: 500px;">

## _Quelles sont les motivations qui incitent les individus à envisager un second rendez-vous ensemble ?_

Tout d'abord, importons les ressources nécessaires.

```py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv(r"Speed+Dating+Data.csv", encoding="latin1")
```

### 1. Statistiques de départ

Sur les **551** participants :

* **274** sont des femmes
* **277** sont des hommes

```py
df = df.groupby("iid")["gender"].mean().reset_index()
female = df[df["gender"] == 0]
male = df[df["gender"] == 1]

df = pd.DataFrame([{"gender": "female", "count": len(female)},
                   {"gender": "male", "count": len(male)}])
fig = px.pie(df,
             names="gender",
             values="count",
             color_discrete_sequence=["#fd5564"])

fig.update_layout(
    title={
        "text": "<b>Gender distribution during speed datings<b>",
        "x": 0.5
        }
)
fig.show()
```

<img src="/output_images/gender_distribution.png" alt="gender_distribution" style="width: 500px;">

En nettoyant les données, nous avons constaté l'utilisation de plusieurs systèmes de notation. Certains participants donnaient des notes sur 10, tandis que d'autres utilisaient des pourcentages. Pour obtenir une réponse rapide, claire et fiable, et étant donné que les notes sur 10 étaient minoritaires, nous avons décidé de les exclure de l'échantillon. Cela représente 4 vagues sur les 21 initiales.

```py
df = df[~((df["wave"] > 5) & (df["wave"] < 10))]
```

---

### 2. Estimations vs Réalité

Les participants semblent avoir tendance à **surestimer leur propre valeur perçue** par rapport à la valeur qui leur est assignée par les autres. Cela peut refléter un biais de surconfiance.

```py
# keep only useful columns
filtered_columns = ["iid", "pid", "attr_o", "attr5_2", "attr5_3"]
filtered_columns = [col for col in filtered_columns if col in df.columns]
df = df[filtered_columns]

# average of the scores participants think they have
df["estimated"] = (df["attr5_2"] + df["attr5_3"]) / 2
estim_df = df.groupby("iid")["estimated"].mean().reset_index()

# average rating for each partner
note_df = df.groupby("pid")["attr_o"].mean().reset_index()
estim_df["note"] = note_df["attr_o"]

# plot
fig = go.Figure()

fig.add_trace(go.Box(
    y=estim_df["estimated"].dropna(),
    name="Perceived value",
    marker_color=envs.TINDER_ORANGE))

fig.add_trace(go.Box(
    y=estim_df["note"],
    name="Assigned value",
    marker_color=envs.TINDER_GREY))
```

![perceived_value](/output_images/attractiveness_prediction.png)

* La **valeur perçue** est établie à partir des évaluations collectées avant et après les rencontres. Il y a une plus grande variabilité dans la perception que les individus ont de leur propre valeur.
* La **valeur assignée** correspond aux notes données par les partenaires. Elles sont plus concentrées, montrant une évaluation plus cohérente par les autres.

---
**Quelle est l'importance de l'attractivité ?**
Le graphique ci-dessous compare l'importance estimée de l'attractivité par les participants par rapport à son importance réelle lors des speed datings.

```py
def conform_data(attributes: list, status: str) -> None:
    """Convert data to mean and fill missing values."""
    d = []
    for attr in attributes:
        df[attr] = df[attr].fillna(df[attr].mean())
        mean = df[attr].mean()
        d.append({"status": status, "name": attr, "mean": mean})
    return d

data += conform_data(potential_attributes, "Estimated")
data += conform_data(real_attributes, "Reality")

# init a new dataframe with filtered data only
fig_df = pd.DataFrame(data)
fig_df = fig_df.groupby("status")["mean"].mean().reset_index()
```

![attractiveness](/output_images/attractiveness_estimated_vs_real_filtered_waves.png)

Les participants sous-estiment l'importance de l'attirance physique dans leur décision. Ils estimaient que l'attirance représentait environ **un quart** de leur décision finale. En réalité, elle semble plutôt contribuer à environ **un tiers** de leur décision finale.

---

### 3. Un second rendez-vous ?

Au fil de chaque série de rencontres, les participants semblent de moins en moins enclins à accepter un second rendez-vous à mesure que la soirée progresse.

Remarquons que le point culminant des réponses positives survient généralement lors du **sixième tour** de la soirée.

Les derniers rounds montrent une **diminution marquée** des décisions positives, atteignant leur point le plus bas autour des 19ème et 20ème rounds. Au fur et à mesure que l'événement avance, les participants pourraient être plus critiques ou moins enclins à donner un "oui", soit en raison de la **fatigue**, soit parce qu'ils **comparent** les nouveaux partenaires potentiels aux premiers.

Donc, si une personne souhaite maximiser ses chances d'obtenir un "oui", il pourrait être stratégique pour elle de participer aux premiers rounds, lorsque les participants sont encore frais et moins sélectifs.

```py
# id = subject number within wave
mean_decision = df.groupby("id")["dec_o"].sum().reset_index()

fig = px.histogram(mean_decision,
                   x="id",
                   y="dec_o",
                   nbins=22,  # 21 waves + 1
                   color_discrete_sequence=[envs.TINDER_ORANGE],
                   labels={"id": "Rounds",
                           "dec_o": "Number of 'yes' decisions about meeting again"})
```

![decision_times](/output_images/decision_times_02.png)

**La biologie est-elle déterminante dans la décision finale, ou les centres d'intérêts des individus sont-ils plus importants ?**
Eh bien, comme le montre le graphique ci-dessous, ces critères ne semblent pas du tout jouer un rôle significatif.

Au contraire, avoir des **centres d'intérêts différents** a été **deux fois plus** déterminant dans la décision finale que d'avoir des intérêts partagés.

```py
# yes decisions according to origins
origins_df = df.groupby("samerace")["dec_o"].sum().reset_index()
origins_df["dec_o_iid"] = origins_df["dec_o"].apply(lambda x: x//10)  # each participant is mentioned 10 times
# cleaning rows names, dtypes
origins_df["samerace"] = origins_df["samerace"].astype(str)
origins_df.at[0, "samerace"] = "different origins"
origins_df.at[1, "samerace"] = "shared origins"

# yes decisions according to shared interests median
df["shar_mean"] = (df["shar7_2"] + df["shar7_3"]) / 2
shar_score_df = df.groupby("shar_mean")["dec_o"].sum().reset_index()

# split data and rebuild new dataframe
median = shar_score_df["shar_mean"].median()
lower_df = shar_score_df[shar_score_df["shar_mean"] < median]
higher_df = shar_score_df[shar_score_df["shar_mean"] > median]

data = [
    {"shar": "different interests", "dec_o": lower_df["dec_o"].sum()},
    {"shar": "shared interests", "dec_o": higher_df["dec_o"].sum()}
    ]
shar_df = pd.DataFrame(data)
```

![shared_interests](/output_images/shared_interests.png)

**Mais alors, quels attributs ont eu le plus de succès ?**
Pour répondre à cette question, nous pouvons calculer la moyenne des notes attribuées le jour même, le jour suivant, et quelques semaines plus tard pour chaque attribut, puis les comparer au nombre de "oui" pour un second rendez-vous. Cela nous permet d'estimer quels attributs ont le plus d'importance lors de la prise de décision.

```py
def sort_attributes(d, gender: int):
    d = d[d["gender"] == gender]  # mask by gender

    # keep interesting columns only
    attrs = ["attr", "sinc", "intel", "fun", "amb", "shar"]
    for attr in attrs:
        columns = [col for col in d.columns if col.startswith(attr)]
        d[f"{attr}_mean"] = d[columns].mean(axis=1)

    d["attr_higher"] = d[[attr for attr in attrs]].idxmax(axis=1)

    yes_responses = d[d["dec_o"] == 1]
    yes_count = yes_responses.groupby("attr_higher")["dec_o"].count()

    # ratio of "yes"
    total_count = d.groupby("attr_higher")["dec_o"].count()
    no_ratio = yes_count / total_count

    # rename columns
    d = no_ratio.reset_index()
    for i, nice_name in enumerate(["Ambitious", "Attractive",
                                   "Fun", "Intelligence",
                                   "Shared Interests", "Sincere"]):
        d.at[i, "attr_higher"] = nice_name

    d = d.sort_values(by="dec_o", ascending=False)

    return d

df_women = sort_attributes(df, 0)
df_men = sort_attributes(df, 1)
```

!["best_attributes](/output_images/best_attributes.png)

Nous avons différencié les résultats entre hommes et femmes pour voir si les attributs influençaient différemment leurs décisions. Si **être séduisant et marrant semblent être les attributs les plus importants pour les deux sexes**, les attributs qui ont entraîné le plus grand nombre de "non" sont différents.

Chez les femmes, c'est le fait d'être **ambitieux** qui pourrait réduire les chances de succès.
Chez les hommes, c'est plutôt **l'intelligence et la sincérité** qui peuvent avoir cet effet.

---

Nous avons parlé des traits de personnalité, mais qu'en est-il de l'objectif final des participants ? Pourquoi sont-ils venus ?
Pour répondre à cette question, chaque participant a communiqué ses intentions, de la simple bonne soirée à la relation sérieuse.

```py
df = df.groupby("iid")["goal"].value_counts().reset_index()
df = df.groupby("goal")["iid"].count().reset_index()
```

La plupart des participants étaient là pour le loisir ou pour le plaisir de rencontrer de nouvelles personnes.
Nous noterons que seulement 4% des participants cherchaient une relation sérieuse.

<img src="/output_images/goals_proportion.png" alt="goals_proportion" style="width: 500px;">

Et quand on compare avec le nombre de réponses "oui"/"non" quant à se revoir lors d'un prochain date, même s'ils sont en dernière position, un tiers de ceux qui recherchent une relation sérieuse en obtenu une réponse favorable.

```py
# count responses
negative_decisions = df[df["dec_o"] == 0]
goal_no_counts = negative_decisions["goal"].value_counts().reset_index()
goal_no_counts.rename(columns={"count": "n"}, inplace=True)

df = goal_yes_counts.merge(goal_no_counts)

# percentages
df["total"] = df["y"] + df["n"]
df["Yes"] = (df["y"] / df["total"] * 100).round(1)
df["No"] = (df["n"] / df["total"] * 100).round(1)

df_melted = df.melt(id_vars="goal",
                    value_vars=["Yes", "No"],
                    var_name="Response",
                    value_name="Percentage")
```

!["goals](/output_images/goals.png)

---

### 4. Solutions proposées

Pour conclure, nous pouvons proposer quelques solutions :

* Trouver des moyens de communication permettant de **réduire l'écart entre perception individuelle et perception des autres.** (Sujets de conversation, projets ?)

* **Diminuer le nombre de partenaires possibles.** Plus il y a de partenaires à rencontrer, plus l'intérêt diminue. Attention, les centres d'intérêts trop communs ne sont pas recommandés. Ils pourraient éventuellement frustrer l'envie de découvrir des choses nouvelles avec un partenaire.

* Les participants ne sont pas pleinement conscients de l'influence de l'apparence physique sur leurs choix. Proposer des **partenaires potentiels basés sur des critères physiques** ?
