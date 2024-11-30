# utils.py

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime


# 1 : Plotting

def plot_variable(df, variable, plot_type='hist', figsize=(10, 6), title=None, kde=True, bins=30, color='blue', label=None, x=None, xlabel=None, ylabel=None, grid=True, title_fontsize=16, label_fontsize=14):
    """
    Plot a variable from a DataFrame with customizable plot type.

    Parameters:
    - df (pd.DataFrame): The dataset.
    - variable (str): The column name of the variable to plot.
    - plot_type (str): The type of plot ('hist', 'line', 'scatter', 'box', etc.).
    - figsize (tuple): The size of the figure (width, height).
    - title (str): Title of the plot.
    - kde (bool): Show KDE for histogram (applies only to 'hist').
    - bins (int): Number of bins for histogram (applies only to 'hist').
    - color (str): Color of the plot.
    - label (str): Label for the plot (applies to 'line').
    - x (str): Column name for x-axis (required for 'scatter').
    - xlabel (str): Label for the x-axis.
    - ylabel (str): Label for the y-axis.
    - grid (bool): Whether to display grid lines.
    - title_fontsize (int): Font size for the title.
    - label_fontsize (int): Font size for axis labels.

    Returns:
    - None: Displays the plot.
    """
    plt.figure(figsize=figsize)
    if title is None:
        title = f"Plot of {variable}"

    if plot_type == 'hist':
        sns.histplot(df[variable], kde=kde, bins=bins, color=color)
    elif plot_type == 'line':
        plt.plot(df[variable], color=color, label=label or variable)
        if label:
            plt.legend()
    elif plot_type == 'scatter':
        if x is None:
            raise ValueError("For scatter plot, 'x' must be specified as a column name.")
        sns.scatterplot(x=df[x], y=df[variable], color=color)
    elif plot_type == 'box':
        sns.boxplot(x=df[variable], color=color)
    else:
        raise ValueError(f"Unsupported plot type: {plot_type}")

    plt.title(title, fontsize=title_fontsize)
    plt.xlabel(xlabel or variable, fontsize=label_fontsize)
    plt.ylabel(ylabel or ('Frequency' if plot_type == 'hist' else ''), fontsize=label_fontsize)
    plt.grid(grid)
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
            df.loc[:, col] = df[col].fillna(df[col].mean())  # Replace NaN with the mean

        elif type == 'median':
            df.loc[:, col] = df[col].fillna(df[col].median())  # Replace NaN with the median

        else:
            raise ValueError(f"Unsupported method: {type}")

    elif df[col].dtype == 'object':
        df.loc[:, col] = df[col].fillna(df[col].mode()[0])  # Replace NaN with the most frequent value (mode)

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


def days_since_start_of_2020(date_str):
    """
    Function to calculate the number of days elapsed since January 1, 2020
    """
    # Convert the date to a datetime object
    parsed_date = pd.to_datetime(date_str, format='%Y-%m-%d')

    # Set the reference date (January 1, 2020)
    ref_date = datetime(2020, 1, 1)

    # Calculate the delta between the date and January 1, 2020
    delta = parsed_date - ref_date

    # Return the number of days elapsed
    return delta.days


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
