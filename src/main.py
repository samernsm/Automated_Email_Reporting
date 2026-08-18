from data_loader import load_sales_data, validate_sales_data
from report_generator import generate_excel_report
from analyzer import (
    calculate_kpis,
    sales_by_region,
    sales_by_product,
    top_products,
)
from email_sender import send_email
from logger import get_logger


logger = get_logger()


def main():
    logger.info("Automation process started.")

    try:
        print("=" * 60)
        print("AUTOMATED EMAIL REPORTING SYSTEM")
        print("=" * 60)

        # 1. Load data
        df = load_sales_data()

        logger.info(
            "Sales data loaded successfully. Rows: %s",
            len(df),
        )

        # 2. Validate data
        validate_sales_data(df)

        # 3. Calculate KPIs
        kpis = calculate_kpis(df)

        print("\nKEY PERFORMANCE INDICATORS")
        print("-" * 40)

        print(f"Total Sales: ${kpis['total_sales']:,.2f}")
        print(f"Total Profit: ${kpis['total_profit']:,.2f}")
        print(f"Total Quantity: {kpis['total_quantity']:,}")
        print(f"Total Orders: {kpis['total_orders']:,}")
        print(f"Profit Margin: {kpis['profit_margin']:.2f}%")
        print(
            f"Average Order Value: "
            f"${kpis['average_order_value']:,.2f}"
        )

        # 4. Sales by region
        region_summary = sales_by_region(df)

        print("\nSALES BY REGION")
        print("-" * 40)
        print(region_summary)

        # 5. Sales by product
        product_summary = sales_by_product(df)

        print("\nSALES BY PRODUCT")
        print("-" * 40)
        print(product_summary)

        # 6. Top products
        print("\nTOP PRODUCTS")
        print("-" * 40)
        print(top_products(df))

        # 7. Generate Excel report
        report_path = generate_excel_report(
            df,
            kpis,
            region_summary,
            product_summary,
        )

        print(f"\nReport saved to: {report_path}")

        logger.info(
            "Excel report generated successfully: %s",
            report_path,
        )

        # 8. Send email
        send_email(
            report_path,
            kpis,
            region_summary,
            product_summary,
        )

        logger.info(
            "Automation process completed successfully."
        )

    except Exception:
        logger.exception(
            "Automation process failed."
        )

        print(
            "\nERROR: Automation process failed."
            "\nCheck output/logs/automation.log"
            " for details."
        )


if __name__ == "__main__":
    main()