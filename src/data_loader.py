from pathlib import Path

import pandas as pd


DATA_FILE = Path(__file__).parent.parent / "data" / "sales_data.csv"


def load_sales_data():
    """Load sales data from CSV file."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Data file not found: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    if df.empty:
        raise ValueError("Sales data is empty.")

    return df


def validate_sales_data(df):
    """Validate required columns and basic data quality."""

    required_columns = [
        "Order_ID",
        "Order_Date",
        "Customer",
        "Region",
        "Product",
        "Category",
        "Quantity",
        "Unit_Price",
        "Sales",
        "Cost",
        "Profit",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    if df["Order_ID"].duplicated().any():
        print("Warning: Duplicate Order_ID values found.")

    if (df["Quantity"] <= 0).any():
        print("Warning: Invalid Quantity values found.")

    if (df["Sales"] < 0).any():
        print("Warning: Negative Sales values found.")

    if (df["Profit"] < 0).any():
        print("Warning: Negative Profit values found.")

    print("Data validation completed successfully.")


if __name__ == "__main__":
    sales_df = load_sales_data()

    print("=" * 60)
    print("Sales Data Information")
    print("=" * 60)

    print(f"Rows: {len(sales_df)}")
    print(f"Columns: {len(sales_df.columns)}")

    validate_sales_data(sales_df)

    print("\nFirst 5 rows:")
    print(sales_df.head())