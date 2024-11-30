# utils.py

# 1 : Plotting

def plot_variable(df, variable, plot_type='hist', **kwargs):
    """
    Plot a variable from a DataFrame with customizable plot type.

    Parameters:
    - df (pd.DataFrame): The dataset.
    - variable (str): The column name of the variable to plot.
    - plot_type (str): The type of plot ('hist', 'line', 'scatter', 'box', etc.).
    - **kwargs: Additional keyword arguments for customization.

    Returns:
    - None: Displays the plot.
    """
    plt.figure(figsize=kwargs.get('figsize', (10, 6)))
    title = kwargs.get('title', f"Plot of {variable}")

    if plot_type == 'hist':
        sns.histplot(df[variable], kde=kwargs.get('kde', True), bins=kwargs.get('bins', 30), color=kwargs.get('color', 'blue'))
    elif plot_type == 'line':
        plt.plot(df[variable], color=kwargs.get('color', 'blue'), label=kwargs.get('label', variable))
        plt.legend()
    elif plot_type == 'scatter':
        x = kwargs.get('x')
        if x is None:
            raise ValueError("For scatter plot, 'x' must be specified as a column name.")
        sns.scatterplot(x=df[x], y=df[variable], color=kwargs.get('color', 'blue'))
    elif plot_type == 'box':
        sns.boxplot(x=df[variable], color=kwargs.get('color', 'blue'))
    else:
        raise ValueError(f"Unsupported plot type: {plot_type}")

    plt.title(title, fontsize=kwargs.get('title_fontsize', 16))
    plt.xlabel(kwargs.get('xlabel', variable), fontsize=kwargs.get('label_fontsize', 14))
    plt.ylabel(kwargs.get('ylabel', 'Frequency' if plot_type == 'hist' else ''), fontsize=kwargs.get('label_fontsize', 14))
    plt.grid(kwargs.get('grid', True))
    plt.show()

def plot_kde_for_column(dataframe, column_name):
    """
    Plots a KDE distribution for a specified column in a DataFrame.
    
    Parameters:
    - dataframe: pandas.DataFrame, the data source
    - column_name: str, the name of the column to plot
    """
    # Set up the figure
    plt.figure(figsize=(10, 5))

    # KDE plot for the specified column
    sns.kdeplot(data=dataframe, x=column_name, fill=True)
    plt.title(f'Distribution of {column_name}')
    plt.xlabel(column_name)
    plt.ylabel('Density')

    # Show the plot
    plt.tight_layout()
    plt.show()

# 2 : Processing

def column_filler(df, col, type=None):
    """
    Fills missing values in a specified column of a DataFrame based on its data type and a chosen method.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the column to fill.
    - col (str): The name of the column to process.
    - type (str, optional): The filling method. Options:
        - 'mean' (default): Fill missing values with the column's mean (for numerical columns).
        - 'median': Fill missing values with the column's median (for numerical columns).
        - For object-type columns, the mode is used by default.

    Behavior:
    - If the column is numeric (int64 or float64):
        - Default ('mean'): Fills missing values with the mean of the column.
        - If 'median' is specified, fills missing values with the median.
        - If an unsupported method is provided, raises a ValueError.
    - If the column is of type 'object' (e.g., strings):
        - Fills missing values with the most frequent value (mode).
    - If the column's data type is unsupported, raises a ValueError.
    """
    if df[col].dtype in ['int64', 'float64']:
        if type is None or type == 'mean':
            df[col].fillna(df[col].mean(), inplace=True)  # Replace NaN with the mean

        elif type == 'median':
            df[col].fillna(df[col].median(), inplace=True)  # Replace NaN with the median

        else:
            raise ValueError(f"Unsupported method: {type}")

    elif df[col].dtype == 'object':
        df[col].fillna(df[col].mode()[0], inplace=True)  # Replace NaN with the most frequent value (mode)

    else:
        raise ValueError(f"Unsupported data type: {df[col].dtype}")


def separate_col(df, list):
    categorical_variables = []
    continuous_variables = []
    for col in list:
        if df[col].dtype in ['int64', 'float64']:
            continuous_variables.append(col)

        elif df[col].dtype == 'object':
            categorical_variables.append(col)

        else:
            raise ValueError(f"Unsupported data type: {df[col].dtype}")

    return categorical_variables, continuous_variables


# 3. Variable Analysis

def compare(df, var1, var2):
    # Check if each value in var1 is associated with a unique value in var2
    unique_var1_to_var2 = df.groupby(var1)[var2].nunique()
    if (unique_var1_to_var2 == 1).all():
        print(f"Each value in {var1} is associated with a unique identifier in {var2}.")
    else:
        print(f"Some values in {var1} are associated with multiple identifiers in {var2}:")
        # Print the values in var1 that have more than one unique corresponding value in var2
        print(unique_var1_to_var2[unique_var1_to_var2 > 1])

    # Check if each value in var2 is associated with a unique value in var1
    unique_var2_to_var1 = df.groupby(var2)[var1].nunique()
    if (unique_var2_to_var1 == 1).all():
        print(f"Each identifier in {var2} is associated with a single value in {var1}.")
    else:
        print(f"Some identifiers in {var2} are associated with multiple values in {var1}:")
        # Print the values in var2 that have more than one unique corresponding value in var1
        print(unique_var2_to_var1[unique_var2_to_var1 > 1])
