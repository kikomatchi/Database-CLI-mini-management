import pandas as pd
from add_data import show_available_tables, show_table_columns, insert_row, update_row
from read_table import read_table_, view_table, search_table
from import_data import import_csv_to_table
from show_statistic import show_correlation, show_overview, missing_summary, top_categories, group_stats
from visualization import plot_histogram, plot_category_distribution, plot_boxplot, plot_group_statistics


# =======================
# MENU DEFINITIONS
# =======================
def main_menu():
    print("\n=== SUPRA DB MANAGEMENT APP ===")
    print("1. Table Management")
    print("2. Import Data (CSV)")
    print("3. Statistics & Summary")
    print("4. Visualization")
    print("0. Exit")
def table_menu():
    print("\n=== TABLE MANAGEMENT ===")
    print("1. Show available tables")
    print("2. Show table columns")
    print("3. Read table")
    print("4. View table")
    print("5. Search table")
    print("6. Insert new row")
    print("7. Update row")
    print("0. Back")
def statistics_menu():
    print("\n=== STATISTICS MENU ===")
    print("1. Overview")
    print("2. Missing Summary")
    print("3. Correlation")
    print("4. Top Categories")
    print("5. Group Statistics")
    print("0. Back")
def visualization_menu():
    print("\n=== VISUALIZATION MENU ===")
    print("1. Histogram")
    print("2. Boxplot")
    print("3. Category Distribution")
    print("4. Group Statistics")
    print("0. Back")
# =======================
# MAIN APP LOGIC
# =======================
def main():
    df = None
    while True:
        main_menu()
        choice = input("Select an option: ")

        # ===== TABLE MANAGEMENT =====
        if choice == "1":
            while True:
                table_menu()
                t_choice = input("Select option: ")

                # 1. Show available tables
                if t_choice == "1":
                    show_available_tables()

                # 2. Show table columns
                elif t_choice == "2":
                    table = input("Enter table name: ")
                    show_table_columns(table)

                # 3. Read table
                elif t_choice == "3":
                    table = input("Enter table name: ")
                    df = read_table_(table)

               # 4. View table (with sort/limit)
                elif t_choice == "4":
                    table = input("Enter table name: ").strip()
                    if not table:
                        print("Table name cannot be empty.")
                        continue

                    df = read_table_(table)
                    if df.empty:
                        print(f"No data found in '{table}'.")
                        continue
                    print(df.columns.tolist())
                    sort = input("Enter sorting column (leave blank for none): ").strip()
                    limit_line = input("Enter number of rows to display (leave blank for all): ").strip()

                    # convert limit to int if provided
                    limit = int(limit_line) if limit_line.isdigit() else None

                    view_table(df, sort_by=sort if sort else None, limit=limit)

     # 5. Search table (simplified interactive filters)
                elif t_choice == "5":
                    table = input("Enter table name: ").strip()
                    if not table:
                        print("Table name cannot be empty.")
                        continue

                    df = read_table_(table)
                    if df.empty:
                        print(f"No data found in '{table}'.")
                        continue

                    print("\nAvailable columns:")
                    print(", ".join(df.columns))

                    print("\nLet's build your filters interactively.")
                    print("Press Enter without typing anything to skip filtering for a column.\n")

                    filters = {}

                    for col in df.columns:
                        response = input(f"Do you want to filter by '{col}'? (y/n): ").strip().lower()
                        if response != "y":
                            continue

                        col_dtype = df[col].dtype
                        print(f"\nColumn '{col}' type detected as: {col_dtype}")

                        if pd.api.types.is_numeric_dtype(col_dtype):
                            print("Choose filter type:")
                            print("1. Equal to (=)")
                            print("2. Greater than (>)")
                            print("3. Less than (<)")
                            print("4. Between range (min, max)")
                            choice = input("Enter choice (1-4): ").strip()

                            if choice == "1":
                                val = input("Enter value: ").strip()
                                try:
                                    val = float(val)
                                except ValueError:
                                    pass
                                filters[col] = ("==", val)

                            elif choice == "2":
                                val = input("Enter minimum value: ").strip()
                                try:
                                    val = float(val)
                                except ValueError:
                                    pass
                                filters[col] = (">", val)

                            elif choice == "3":
                                val = input("Enter maximum value: ").strip()
                                try:
                                    val = float(val)
                                except ValueError:
                                    pass
                                filters[col] = ("<", val)

                            elif choice == "4":
                                low = input("Enter minimum: ").strip()
                                high = input("Enter maximum: ").strip()
                                try:
                                    filters[col] = (float(low), float(high))
                                except ValueError:
                                    print("⚠️ Invalid range input — skipping this filter.")
                                    continue

                        else:  # categorical or text columns
                            print("Choose filter type:")
                            print("1. Contains (partial match)")
                            print("2. Equal to (exact match)")
                            print("3. In list (e.g. multiple categories)")
                            choice = input("Enter choice (1-3): ").strip()

                            if choice == "1":
                                val = input("Enter text to search for: ").strip()
                                filters[col] = val

                            elif choice == "2":
                                val = input("Enter exact value: ").strip()
                                filters[col] = ("==", val)

                            elif choice == "3":
                                val = input("Enter comma-separated values: ").strip()
                                filters[col] = [v.strip() for v in val.split(",") if v.strip()]

                    if not filters:
                        print("⚠️ No filters applied.")
                        results = df
                    else:
                        results = search_table(df, **filters)

                    print(f"\n✅ Found {len(results)} matching rows.")
                    n = input("How many rows to display? (default 10): ").strip()
                    n = int(n) if n.isdigit() else 10
                    print(results.head(n))

                # 6. Insert new row
                elif t_choice == "6":
                    table = input("Enter table name: ").strip()
                    columns = show_table_columns(table)
                    if not columns:
                        continue

                    print(f"\nAvailable columns in '{table}': {', '.join(columns)}")
                    print("Enter a value for each column (leave blank to skip):\n")

                    data = {}
                    for col in columns:
                        val = input(f"Enter {col}: ").strip()
                        if not val:
                            continue
                        if val.lower() == "null":
                            data[col] = None
                        elif val.isdigit():
                            data[col] = int(val)
                        else:
                            try:
                                data[col] = float(val)
                            except ValueError:
                                data[col] = val
                    insert_row(table, data)

                # 7. Update existing row
                elif t_choice == "7":
                    table = input("Enter table name: ").strip()
                    id_col = input("Enter ID column name (default 'id'): ").strip() or "id"
                    record_id = input(f"Enter value of {id_col} to update: ").strip()
                    columns = show_table_columns(table)
                    if not columns:
                        continue

                    data = {}
                    print("Enter new values for columns (leave blank to skip):\n")
                    for col in columns:
                        val = input(f"New value for {col}: ").strip()
                        if not val:
                            continue
                        if val.lower() == "null":
                            data[col] = None
                        elif val.isdigit():
                            data[col] = int(val)
                        else:
                            try:
                                data[col] = float(val)
                            except ValueError:
                                data[col] = val

                    update_row(table, record_id, data, id_column=id_col)

                elif t_choice == "0":
                    break
                else:
                    print("Invalid choice.")


        # ===== Import Data =====
        elif choice == "2":
            file_path = input("Enter CSV file path: ")
            table_name = input("Enter target table name: ")
            import_csv_to_table(file_path, table_name)

        # ===== Statistics =====
        elif choice == "3":
            table = input("Enter table name: ")
            df = read_table_(table)
            if df is None:
                print("Please read a table first.")
                continue
            while True:
                statistics_menu()
                s_choice = input("Select option: ")

                if s_choice == "1":
                    show_overview(df)
                elif s_choice == "2":
                    missing_summary(df)
                elif s_choice == "3":
                    show_correlation(df)
                elif s_choice == "4":
                    print(df.columns.tolist())
                    col = input("Enter column: ")
                    top_categories(df, col)
                elif s_choice == "5":
                    print(df.columns.tolist())
                    gcol = input("Group column: ")
                    tcol = input("Target column: ")
                    agg = input("Aggregation (mean/sum/max/min): ")
                    group_stats(df, gcol, tcol, agg)
                elif s_choice == "0":
                    break

        # ===== Visualization =====
        elif choice == "4":
            table = input("Enter table name: ")
            df = read_table_(table)
            if df is None:
                print("Please read a table first.")
                continue
            while True:
                visualization_menu()
                v_choice = input("Select option: ")

                if v_choice == "1":
                    print(df.columns.tolist())
                    col = input("Column: ")
                    plot_histogram(df, col)
                elif v_choice == "2":
                    print(df.columns.tolist())
                    col = input("Column: ")
                    plot_boxplot(df, col)
                elif v_choice == "3":
                    print(df.columns.tolist())
                    col = input("Column: ")
                    plot_category_distribution(df, col)
                elif v_choice == "4":
                    print(df.columns.tolist())
                    gcol = input("Group column: ")
                    tcol = input("Target column: ")
                    agg = input("Aggregation (mean/sum/max/min): ")
                    plot_group_statistics(df, gcol, tcol, agg)
                elif v_choice == "0":
                    break

        elif choice == "0":
            print("\nGoodbye!")
            break

        else:
            print("Invalid option.")

main()