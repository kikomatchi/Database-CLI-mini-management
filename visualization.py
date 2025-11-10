from read_table import read_table_
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_histogram(df, col):
    if col not in df.columns:
        print(f"\nColumn '{col}' not found.")
        return
    plt.figure(figsize=(10, 6))
    if pd.api.types.is_numeric_dtype(df[col]):
        sns.histplot(df[col].dropna(), bins=20, kde=True)
        plt.title(f"Histogram of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
    else:
        counts = df[col].value_counts()
        colors = sns.color_palette("viridis", len(counts))
        sns.barplot(x=counts.index, y=counts.values, palette=colors)
        plt.xticks(rotation=45)
        plt.title(f"Category Frequency in '{col}'")
        plt.xlabel(col)
        plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

def plot_boxplot(df, col):
    if col not in df.columns:
        print(f"\nColumn '{col}' not found.")
        return
    plt.figure(figsize=(10, 6))
    sns.set(style="whitegrid")
    if pd.api.types.is_numeric_dtype(df[col]):
        sns.boxplot(y=df[col].dropna(), color="#4c72b0", width=0.4, fliersize=4)
        plt.title(f"Boxplot of '{col}'", fontsize=14, fontweight="bold")
        plt.ylabel(col, fontsize=12)
        plt.xlabel("")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    else:
        counts = df[col].value_counts().head(20)
        colors = sns.color_palette("viridis", len(counts))
        sns.barplot(x=counts.index, y=counts.values, palette=colors)
        plt.title(f"Category Frequency in '{col}'", fontsize=14, fontweight="bold")
        plt.ylabel("Count", fontsize=12)
        plt.xlabel(col, fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_group_statistics(df, group_col, target_col, agg_func='mean'):
    if group_col not in df.columns or target_col not in df.columns:
        print("One or both columns not found.")
        return
    if not pd.api.types.is_numeric_dtype(df[target_col]):
        print(f"'{target_col}' must be numeric.")
        return
    grouped = df.groupby(group_col)[target_col].agg(agg_func).sort_values(ascending=False).head(15)
    plt.figure(figsize=(10, 6))
    colors = sns.color_palette("viridis", len(grouped))
    sns.barplot(x=grouped.index, y=grouped.values, palette=colors)
    plt.title(f"{agg_func.capitalize()} of {target_col} by {group_col}", fontsize=14, fontweight='bold')
    plt.ylabel(f"{agg_func.capitalize()} of {target_col}")
    plt.xlabel(group_col)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

def plot_category_distribution(df, col):
    if col not in df.columns:
        print(f"Column '{col}' not found.")
        return
    if not (pd.api.types.is_categorical_dtype(df[col]) or pd.api.types.is_string_dtype(df[col])):
        print(f"'{col}' is not a categorical column.")
        return
    counts = df[col].value_counts().head(15)
    colors = sns.color_palette("viridis", len(counts))
    plt.figure(figsize=(10, 6))
    sns.barplot(x=counts.index, y=counts.values, palette=colors)
    plt.title(f"Top Categories in '{col}'", fontsize=14, fontweight='bold')
    plt.xlabel(col)
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
