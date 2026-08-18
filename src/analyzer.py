import pandas as pd


def calculate_kpis(df):
    """Calculate main business KPIs."""

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_quantity = df["Quantity"].sum()
    total_orders = df["Order_ID"].nunique()

    profit_margin = (
        (total_profit / total_sales) * 100
        if total_sales != 0
        else 0
    )

    average_order_value = (
        total_sales / total_orders
        if total_orders != 0
        else 0
    )

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "total_quantity": total_quantity,
        "total_orders": total_orders,
        "profit_margin": profit_margin,
        "average_order_value": average_order_value,
    }


def sales_by_region(df):
    """Calculate sales and profit by region."""

    return (
        df.groupby("Region")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
        )
        .sort_values("Sales", ascending=False)
    )


def sales_by_product(df):
    """Calculate sales and profit by product."""

    return (
        df.groupby("Product")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum"),
        )
        .sort_values("Sales", ascending=False)
    )


def top_products(df, n=5):
    """Return top products by sales."""

    return (
        df.groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )