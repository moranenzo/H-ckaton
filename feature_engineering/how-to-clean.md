### Étapes principales pour nettoyer un DataFrame

#### 1. **Comprendre le dataset**
   - Examine les premières lignes du dataset : `df.head()`.
   - Obtiens des informations générales : `df.info()`.
   - Vérifie les statistiques de base : `df.describe(include='all')`.

---

#### 2. **Traiter les valeurs manquantes**
   - Identifie les colonnes contenant des valeurs manquantes : `df.isnull().sum()`.
   - Décide comment gérer ces valeurs :
     - **Pour les variables numériques (`int` ou `float`)** :
       - Remplace par la moyenne : `df['col'] = df['col'].fillna(df['col'].mean())`.
       - Remplace par la médiane : `df['col'] = df['col'].fillna(df['col'].median())`.
       - Remplace par une valeur fixe (par exemple 0) : `df['col'] = df['col'].fillna(0)`.
     - **Pour les variables catégoriques (`object`)** :
       - Remplace par la modalité (valeur la plus fréquente) : 
         ```python
         df['col'] = df['col'].fillna(df['col'].mode()[0])
         ```
       - Remplace par une catégorie spéciale : `df['col'] = df['col'].fillna('Unknown')`.
   - Supprime les lignes ou colonnes inutiles si les valeurs manquantes sont trop nombreuses :
     ```python
     df.dropna(axis=0, inplace=True)  # Supprimer les lignes
     df.dropna(axis=1, inplace=True)  # Supprimer les colonnes
     ```

---

#### 3. **Convertir les types de données**
   - Corrige les types de données incorrects :
     ```python
     df['col'] = df['col'].astype(float)  # Exemple : convertir en float
     ```
   - Traite les colonnes qui doivent être des catégories :
     ```python
     df['col'] = df['col'].astype('category')
     ```

---

#### 4. **Supprimer les doublons**
   - Identifie et supprime les lignes dupliquées :
     ```python
     df.drop_duplicates(inplace=True)
     ```

---

#### 5. **Gérer les valeurs aberrantes**
   - **Détection des valeurs aberrantes :**
     - Avec des statistiques : identifie les valeurs qui s'écartent de 3 fois l'écart-type :
       ```python
       df = df[(df['col'] > lower_limit) & (df['col'] < upper_limit)]
       ```
     - Utilise des boîtes à moustaches (`boxplots`) pour les visualiser.
   - **Gérer les valeurs aberrantes :**
     - Supprime ou remplace les valeurs aberrantes :
       ```python
       df['col'] = df['col'].clip(lower=df['col'].quantile(0.05), upper=df['col'].quantile(0.95))
       ```

---

#### 6. **Nettoyer les colonnes `object`**
   - Uniformise la casse (tout en minuscule ou majuscule) :
     ```python
     df['col'] = df['col'].str.lower()
     ```
   - Supprime les espaces inutiles :
     ```python
     df['col'] = df['col'].str.strip()
     ```
   - Traite les valeurs incohérentes (par ex. orthographes différentes pour la même catégorie).

---

#### 7. **Renommer les colonnes**
   - Utilise des noms clairs et standardisés :
     ```python
     df.rename(columns=lambda x: x.strip().lower().replace(' ', '_'), inplace=True)
     ```

---

#### 8. **Vérifications finales**
   - Vérifie les changements appliqués :
     ```python
     print(df.info())
     print(df.isnull().sum())
     ```

---

### Exemple complet de fonction Python

```python
def clean_dataframe(df):
    # 1. Traiter les valeurs manquantes
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            df[col].fillna(df[col].mean(), inplace=True)  # Remplace les NaN par la moyenne
        elif df[col].dtype == 'object':
            df[col].fillna('Unknown', inplace=True)  # Remplace les NaN par 'Unknown'

    # 2. Supprimer les doublons
    df.drop_duplicates(inplace=True)

    # 3. Uniformiser les colonnes object
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.lower().str.strip()

    # 4. Renommer les colonnes
    df.rename(columns=lambda x: x.strip().lower().replace(' ', '_'), inplace=True)

    return df
```

---

### Utilisation

```python
import pandas as pd

# Exemple de dataset
data = {
    'Name': ['Alice', 'Bob', 'Alice', None],
    'Age': [25, None, 25, 30],
    'Salary': [50000.0, 54000.0, None, 70000.0]
}

df = pd.DataFrame(data)

# Nettoyer le DataFrame
df_cleaned = clean_dataframe(df)
print(df_cleaned)
```