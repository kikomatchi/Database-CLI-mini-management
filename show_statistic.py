import pandas as pd
import numpy as np

def show_overview(df):
    print("\nData Overview: ")
    print(df.info())
    print("\nDescribe Statistic: ")
    print(df.describe())

def missing_summary(df):
    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if missing.empty:
        print("\nNo missing values detected.")
    else:
        print("\n=== MISSING VALUE SUMMARY ===")
        print(missing)

def show_correlation(df):
    numeric_df = df.select_dtypes(include=['int64', 'float64'])
    if numeric_df.empty:
        print("\nNo numeric columns avail for correlation.")
        return
    corr = numeric_df.corr()
    print("\nCorrelation Matrix: ")
    print(corr)

def top_categories(df, column, top_n=5):
    if column not in df.columns:
        print(f"\nColumn {column} not found")
        return
    print(f"\nTop {top_n} categories in '{column}:")
    print(df[column].value_counts().head(top_n))

def group_stats(df, group_col, target_col, agg_func='mean'):
    if group_col not in df.columns or target_col not in df.columns:
        print("\nColumn not found.")
        return
    print(f"\n{agg_func.capitalize()} of {target_col} grouped by {group_col}:")
    print(df.groupby(group_col)[target_col].agg(agg_func).sort_values(ascending=False))