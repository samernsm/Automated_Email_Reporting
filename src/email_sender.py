import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv
from logger import get_logger

logger = get_logger(__name__)

load_dotenv()


SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")


def create_html_email(kpis, region_summary, product_summary):
    """Create the HTML email body."""

    region_rows = ""

    for region, row in region_summary.iterrows():
        region_rows += f"""
        <tr>
            <td>{region}</td>
            <td>${row['Sales']:,.2f}</td>
            <td>${row['Profit']:,.2f}</td>
            <td>{row['Orders']}</td>
        </tr>
        """

    product_rows = ""

    for product, row in product_summary.iterrows():
        product_rows += f"""
        <tr>
            <td>{product}</td>
            <td>${row['Sales']:,.2f}</td>
            <td>${row['Profit']:,.2f}</td>
            <td>{row['Quantity']}</td>
        </tr>
        """

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">

        <h1>Automated Sales Report</h1>

        <h2>Key Performance Indicators</h2>

        <table border="1"
               cellpadding="10"
               cellspacing="0">

            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>

            <tr>
                <td>Total Sales</td>
                <td>${kpis['total_sales']:,.2f}</td>
            </tr>

            <tr>
                <td>Total Profit</td>
                <td>${kpis['total_profit']:,.2f}</td>
            </tr>

            <tr>
                <td>Total Quantity</td>
                <td>{kpis['total_quantity']:,}</td>
            </tr>

            <tr>
                <td>Total Orders</td>
                <td>{kpis['total_orders']:,}</td>
            </tr>

            <tr>
                <td>Profit Margin</td>
                <td>{kpis['profit_margin']:.2f}%</td>
            </tr>

            <tr>
                <td>Average Order Value</td>
                <td>${kpis['average_order_value']:,.2f}</td>
            </tr>

        </table>


        <h2>Sales by Region</h2>

        <table border="1"
               cellpadding="10"
               cellspacing="0">

            <tr>
                <th>Region</th>
                <th>Sales</th>
                <th>Profit</th>
                <th>Orders</th>
            </tr>

            {region_rows}

        </table>


        <h2>Sales by Product</h2>

        <table border="1"
               cellpadding="10"
               cellspacing="0">

            <tr>
                <th>Product</th>
                <th>Sales</th>
                <th>Profit</th>
                <th>Quantity</th>
            </tr>

            {product_rows}

        </table>


        <p>
            The complete Excel report is attached to this email.
        </p>

        <p>
            Regards,<br>
            Automated Reporting System
        </p>

    </body>
    </html>
    """

    return html


def send_email(
    report_path: Path,
    kpis,
    region_summary,
    product_summary,
):
    """Send HTML email with Excel attachment."""

    if not SMTP_SERVER:
        raise ValueError("SMTP_SERVER is not configured.")

    if not SMTP_USERNAME:
        raise ValueError("SMTP_USERNAME is not configured.")

    if not SMTP_PASSWORD:
        raise ValueError("SMTP_PASSWORD is not configured.")

    if not EMAIL_SENDER:
        raise ValueError("EMAIL_SENDER is not configured.")

    if not EMAIL_RECEIVER:
        raise ValueError("EMAIL_RECEIVER is not configured.")

    if not report_path.exists():
        raise FileNotFoundError(
            f"Report not found: {report_path}"
        )

    # Create email
    message = EmailMessage()

    message["Subject"] = "Automated Sales Report"
    message["From"] = EMAIL_SENDER
    message["To"] = EMAIL_RECEIVER

    # Create HTML body
    html_body = create_html_email(
        kpis,
        region_summary,
        product_summary,
    )

    # Plain text fallback
    message.set_content(
        """
Automated Sales Report

Please open this email in an HTML-compatible email client.

The complete Excel report is attached.
"""
    )

    # HTML version
    message.add_alternative(
        html_body,
        subtype="html",
    )

    # Attach Excel report
    with open(report_path, "rb") as file:
        report_data = file.read()

    message.add_attachment(
        report_data,
        maintype="application",
        subtype=(
            "vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        filename=report_path.name,
    )

    # Connect to SMTP
    with smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT,
    ) as server:

        server.starttls()

        server.login(
            SMTP_USERNAME,
            SMTP_PASSWORD,
        )

        server.send_message(message)
         
    logger.info("HTML email sent successfully to %s", EMAIL_RECEIVER,)