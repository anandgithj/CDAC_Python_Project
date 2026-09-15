from database import *
from datetime import datetime
import matplotlib.pyplot as plt


# Base class for common report functionality
class Report:

    # Print a formatted heading for a report
    def print_heading(self, heading):
        print("\n" + "=" * 80)
        print(f"{heading:^80}")
        print("=" * 80)


# Report class for inventory-related reports
class InventoryReport(Report):

    # 1. Current Stock Report
    def current_stock(self):

        # Display the report heading
        self.print_heading("CURRENT STOCK REPORT")

        try:
            # Get all products from the database
            products = get_products()

            # Handle the case when no products are available
            if not products:
                print("No products available.")
                return

            # Display column headings
            print(
                f"{'ID':<8}"
                f"{'Product Name':<25}"
                f"{'Category':<20}"
                f"{'Qty':<8}"
                f"{'Min':<8}"
                f"{'Value':<12}"
            )

            print("-" * 81)

            # Store the total value of all inventory
            total_value = 0

            # Calculate the value of each product and add it to the total
            for product in products:

                quantity = product.get("quantity", 0)
                price = product.get("price", 0)
                min_stock = product.get("min_stock", 0)

                # Calculate inventory value for the current product
                value = quantity * price
                total_value += value

                print(
                    f"{product.get('product_id', 'N/A'):<8}"
                    f"{product.get('product_name', 'N/A')[:23]:<25}"
                    f"{product.get('category', 'N/A')[:18]:<20}"
                    f"{quantity:<8}"
                    f"{min_stock:<8}"
                    f"Rs.{value:<9.2f}"
                )

            # Display the total inventory value
            print("-" * 81)
            print(f"Total Inventory Value: Rs. {total_value:.2f}")

        except (KeyError, TypeError, AttributeError) as error:
            # Handle malformed or unexpected product data instead of crashing
            print(f"Could not generate report due to invalid data: {error}")


    # 2. Low Stock Report
    def low_stock(self):

        # Display the report heading
        self.print_heading("LOW STOCK REPORT")

        try:
            # Get all products from the database
            products = get_products()

            # Handle the case when no products are available
            if not products:
                print("No products available.")
                return

            # Store products whose quantity is at or below minimum stock
            low_stock_products = []

            # Check every product for low-stock status
            for product in products:

                quantity = product.get("quantity", 0)
                min_stock = product.get("min_stock", 0)

                # Add products that have reached or fallen below minimum stock
                if quantity <= min_stock:
                    low_stock_products.append(product)

            # Handle the case when there are no low-stock products
            if not low_stock_products:
                print("No low-stock products.")
                return

            # Display low-stock report headings
            print(
                f"{'ID':<8}"
                f"{'Product Name':<25}"
                f"{'Current Qty':<15}"
                f"{'Minimum Qty':<15}"
                f"{'Status'}"
            )

            print("-" * 78)

            # Display each low-stock product
            for product in low_stock_products:

                print(
                    f"{product.get('product_id', 'N/A'):<8}"
                    f"{product.get('product_name', 'N/A')[:23]:<25}"
                    f"{product.get('quantity', 0):<15}"
                    f"{product.get('min_stock', 0):<15}"
                    f"LOW STOCK"
                )

        except (KeyError, TypeError, AttributeError) as error:
            # Handle malformed or unexpected product data instead of crashing
            print(f"Could not generate report due to invalid data: {error}")


    # 3. Transaction History
    def transaction_history(self):

        # Display the report heading
        self.print_heading("TRANSACTION HISTORY")

        try:
            # Get all transactions from the database
            transactions = get_transactions()

            # Handle the case when there are no transactions
            if not transactions:
                print("No transactions available.")
                return

            # Display transaction history headings
            print(
                f"{'ID':<8}"
                f"{'Product ID':<12}"
                f"{'Type':<10}"
                f"{'Quantity':<12}"
                f"{'Date':<15}"
                f"{'Product Name'}"
            )

            print("-" * 85)

            # Process each transaction
            for transaction in transactions:

                # Read the transaction ID
                transaction_id = transaction.get(
                    "transaction_id",
                    "N/A"
                )

                # Read the Product ID from the transaction
                product_id = transaction.get(
                    "product_id",
                    "N/A"
                )

                # Support both transaction_type and type field names
                transaction_type = transaction.get(
                    "transaction_type",
                    transaction.get("type", "N/A")
                )

                # Read the transaction quantity
                quantity = transaction.get(
                    "quantity",
                    0
                )

                # Read the transaction date
                transaction_date = transaction.get(
                    "transaction_date",
                    "N/A"
                )

                # Find the product linked to the transaction
                product = get_product(product_id)

                # Use the product name when the product still exists
                if product:
                    product_name = product.get(
                        "product_name",
                        "N/A"
                    )
                else:
                    # Show a clear message when the product has been deleted
                    product_name = "Product Deleted"

                # Display the transaction details
                print(
                    f"{transaction_id:<8}"
                    f"{product_id:<12}"
                    f"{transaction_type:<10}"
                    f"{quantity:<12}"
                    f"{transaction_date:<15}"
                    f"{product_name}"
                )

        except (KeyError, TypeError, AttributeError) as error:
            # Handle malformed or unexpected transaction data instead of crashing
            print(f"Could not generate report due to invalid data: {error}")


    # 4. Stock In / Out Summary
    def stock_summary(self):

        # Display the report heading
        self.print_heading("STOCK IN / OUT SUMMARY")

        try:
            # Get all transactions from the database
            transactions = get_transactions()

            # Handle the case when there are no transactions
            if not transactions:
                print("No transactions available.")
                return

            # Store total stock received and issued
            total_in = 0
            total_out = 0

            # Process each transaction
            for transaction in transactions:

                # Read the transaction type, supporting both field names
                transaction_type = transaction.get(
                    "transaction_type",
                    transaction.get("type")
                )

                # Read the transaction quantity
                quantity = transaction.get(
                    "quantity",
                    0
                )

                # Add quantities for stock-in transactions
                if transaction_type == "IN":
                    total_in += quantity

                # Add quantities for stock-out transactions
                elif transaction_type == "OUT":
                    total_out += quantity

            # Calculate the net stock movement
            net_movement = total_in - total_out

            print(f"Total Stock In  : {total_in}")
            print(f"Total Stock Out : {total_out}")
            print(f"Net Movement    : {net_movement}")

        except (KeyError, TypeError, AttributeError) as error:
            # Handle malformed or unexpected transaction data instead of crashing
            print(f"Could not generate report due to invalid data: {error}")


    # 5. Date-wise Stock In / Out Summary (single date or date range)
    def date_wise_summary(self):

        # Display the report heading
        self.print_heading("DATE-WISE STOCK SUMMARY")

        # Read the start date from the user
        start_date_input = input("Enter start date (DD-MM-YYYY): ").strip()

        # Read the end date; leave blank for a single-day report
        end_date_input = input(
            "Enter end date (DD-MM-YYYY, leave blank for single day report): "
        ).strip()

        # If end date is left blank, use the start date for both
        if not end_date_input:
            end_date_input = start_date_input

        # Convert the user-entered dates (DD-MM-YYYY) to the stored format (YYYY-MM-DD)
        try:
            start_date = datetime.strptime(
                start_date_input, "%d-%m-%Y"
            ).strftime("%Y-%m-%d")

            end_date = datetime.strptime(
                end_date_input, "%d-%m-%Y"
            ).strftime("%Y-%m-%d")

        # Handle invalid date format
        except ValueError:
            print("Invalid date format. Please enter dates as DD-MM-YYYY.")
            return

        # Make sure the start date is not after the end date
        if start_date > end_date:
            print("Start date cannot be after end date.")
            return

        try:
            # Get all transactions from the database
            transactions = get_transactions()

            # Handle the case when there are no transactions
            if not transactions:
                print("No transactions available.")
                return

            # Store total stock received and issued within the date range
            total_in = 0
            total_out = 0

            # Store matching transactions to display them
            matching_transactions = []

            # Process each transaction
            for transaction in transactions:

                # Read the transaction date
                transaction_date = transaction.get("transaction_date", "")

                # Skip transactions outside the requested date range
                if not (start_date <= transaction_date <= end_date):
                    continue

                # Read the transaction type, supporting both field names
                transaction_type = transaction.get(
                    "transaction_type",
                    transaction.get("type")
                )

                # Read the transaction quantity
                quantity = transaction.get("quantity", 0)

                # Add quantities for stock-in transactions
                if transaction_type == "IN":
                    total_in += quantity

                # Add quantities for stock-out transactions
                elif transaction_type == "OUT":
                    total_out += quantity

                matching_transactions.append(transaction)

            # Handle the case when no transactions fall in the given range
            if not matching_transactions:
                print("No transactions found in the given date range.")
                return

            # Display the date range covered
            if start_date_input == end_date_input:
                print(f"Date: {start_date_input}")
            else:
                print(f"Date Range: {start_date_input} to {end_date_input}")

            # Display column headings for the matching transactions
            print(
                f"{'ID':<8}"
                f"{'Product ID':<12}"
                f"{'Type':<10}"
                f"{'Quantity':<12}"
                f"{'Date':<15}"
                f"{'Product Name'}"
            )

            print("-" * 85)

            # Display each matching transaction with the product name
            for transaction in matching_transactions:

                transaction_id = transaction.get("transaction_id", "N/A")
                product_id = transaction.get("product_id", "N/A")

                transaction_type = transaction.get(
                    "transaction_type",
                    transaction.get("type", "N/A")
                )

                quantity = transaction.get("quantity", 0)
                transaction_date = transaction.get("transaction_date", "N/A")

                # Find the product linked to the transaction
                product = get_product(product_id)

                # Use the product name when the product still exists
                if product:
                    product_name = product.get("product_name", "N/A")
                else:
                    # Show a clear message when the product has been deleted
                    product_name = "Product Deleted"

                print(
                    f"{transaction_id:<8}"
                    f"{product_id:<12}"
                    f"{transaction_type:<10}"
                    f"{quantity:<12}"
                    f"{transaction_date:<15}"
                    f"{product_name}"
                )

            print("-" * 85)

            # Calculate the net stock movement
            net_movement = total_in - total_out

            print(f"Total Stock In  : {total_in}")
            print(f"Total Stock Out : {total_out}")
            print(f"Net Movement    : {net_movement}")

        except (KeyError, TypeError, AttributeError) as error:
            # Handle malformed or unexpected transaction data instead of crashing
            print(f"Could not generate report due to invalid data: {error}")


    # 6. Low Stock Chart (bar chart)
    def low_stock_chart(self):

        try:
            # Get all products from the database
            products = get_products()

            # Handle the case when no products are available
            if not products:
                print("No products available.")
                return

            # Collect products whose quantity is at or below minimum stock
            names = []
            quantities = []
            min_stocks = []

            for product in products:

                quantity = product.get("quantity", 0)
                min_stock = product.get("min_stock", 0)

                if quantity <= min_stock:
                    names.append(product.get("product_name", "N/A"))
                    quantities.append(quantity)
                    min_stocks.append(min_stock)

            # Handle the case when there are no low-stock products
            if not names:
                print("No low-stock products to chart.")
                return

            # Build the bar chart: current quantity vs minimum stock
            x = range(len(names))

            plt.figure(figsize=(10, 6))
            plt.bar(x, quantities, width=0.4, label="Current Qty", align="center")
            plt.bar(
                [i + 0.4 for i in x],
                min_stocks,
                width=0.4,
                label="Min Stock",
                align="center"
            )
            plt.xticks([i + 0.2 for i in x], names, rotation=30, ha="right")
            plt.ylabel("Quantity")
            plt.title("Low Stock Products")
            plt.legend()
            plt.tight_layout()

            # Save the chart as a PNG file
            plt.savefig("low_stock_chart.png")
            print("Chart saved as low_stock_chart.png")

            # Also display the chart
            plt.show()

        except (KeyError, TypeError, AttributeError) as error:
            # Handle malformed or unexpected product data instead of crashing
            print(f"Could not generate chart due to invalid data: {error}")


    # 7. Category-wise Inventory Value Chart (pie chart)
    def category_value_chart(self):

        try:
            # Get all products from the database
            products = get_products()

            # Handle the case when no products are available
            if not products:
                print("No products available.")
                return

            # Sum up inventory value per category
            category_values = {}

            for product in products:

                category = product.get("category", "N/A")
                quantity = product.get("quantity", 0)
                price = product.get("price", 0)

                value = quantity * price

                category_values[category] = category_values.get(category, 0) + value

            # Handle the case when there is no value to chart
            if not category_values:
                print("No category data to chart.")
                return

            categories = list(category_values.keys())
            values = list(category_values.values())

            # Build the pie chart
            plt.figure(figsize=(8, 8))
            plt.pie(values, labels=categories, autopct="%1.1f%%", startangle=90)
            plt.title("Inventory Value by Category")
            plt.tight_layout()

            # Save the chart as a PNG file
            plt.savefig("category_value_chart.png")
            print("Chart saved as category_value_chart.png")

            # Also display the chart
            plt.show()

        except (KeyError, TypeError, AttributeError) as error:
            # Handle malformed or unexpected product data instead of crashing
            print(f"Could not generate chart due to invalid data: {error}")


    # 8. Stock IN/OUT Trend Chart (line chart)
    def stock_trend_chart(self):

        try:
            # Get all transactions from the database
            transactions = get_transactions()

            # Handle the case when there are no transactions
            if not transactions:
                print("No transactions available.")
                return

            # Sum up IN and OUT quantities per date
            in_by_date = {}
            out_by_date = {}

            for transaction in transactions:

                transaction_date = transaction.get("transaction_date", "N/A")

                transaction_type = transaction.get(
                    "transaction_type",
                    transaction.get("type")
                )

                quantity = transaction.get("quantity", 0)

                if transaction_type == "IN":
                    in_by_date[transaction_date] = in_by_date.get(transaction_date, 0) + quantity

                elif transaction_type == "OUT":
                    out_by_date[transaction_date] = out_by_date.get(transaction_date, 0) + quantity

            # Handle the case when there is no dated data to chart
            if not in_by_date and not out_by_date:
                print("No dated transactions to chart.")
                return

            # Build a sorted list of all dates involved
            all_dates = sorted(set(in_by_date.keys()) | set(out_by_date.keys()))

            in_values = [in_by_date.get(d, 0) for d in all_dates]
            out_values = [out_by_date.get(d, 0) for d in all_dates]

            # Build the line chart
            plt.figure(figsize=(10, 6))
            plt.plot(all_dates, in_values, marker="o", label="Stock In")
            plt.plot(all_dates, out_values, marker="o", label="Stock Out")
            plt.xticks(rotation=45, ha="right")
            plt.xlabel("Date")
            plt.ylabel("Quantity")
            plt.title("Stock In/Out Trend")
            plt.legend()
            plt.tight_layout()

            # Save the chart as a PNG file
            plt.savefig("stock_trend_chart.png")
            print("Chart saved as stock_trend_chart.png")

            # Also display the chart
            plt.show()

        except (KeyError, TypeError, AttributeError) as error:
            # Handle malformed or unexpected transaction data instead of crashing
            print(f"Could not generate chart due to invalid data: {error}")


def report_menu():

    # Create the inventory report object
    report = InventoryReport()

    # Keep displaying the report menu until the user exits
    while True:

        # Display report options
        print("\n==========================================")
        print("                 REPORTS")
        print("==========================================")
        print("1. Current Stock Report")
        print("2. Low Stock Report")
        print("3. Transaction History")
        print("4. Stock In/Out Summary")
        print("5. Date-wise Stock Summary")
        print("6. Low Stock Chart")
        print("7. Category-wise Value Chart")
        print("8. Stock In/Out Trend Chart")
        print("9. Back to Main Menu")
        print("==========================================")

        # Read and clean the user's menu choice
        choice = input("Enter your choice: ").strip()

        # Show the current stock report
        if choice == "1":
            report.current_stock()

        # Show the low-stock report
        elif choice == "2":
            report.low_stock()

        # Show the transaction history
        elif choice == "3":
            report.transaction_history()

        # Show the stock in/out summary
        elif choice == "4":
            report.stock_summary()

        # Show the date-wise stock summary
        elif choice == "5":
            report.date_wise_summary()

        # Show the low stock chart
        elif choice == "6":
            report.low_stock_chart()

        # Show the category-wise value chart
        elif choice == "7":
            report.category_value_chart()

        # Show the stock in/out trend chart
        elif choice == "8":
            report.stock_trend_chart()

        # Return to the main menu
        elif choice == "9":
            break

        else:
            # Handle an invalid menu choice
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    report_menu()