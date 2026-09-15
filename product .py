from database import *
from datetime import date


# Display the details of a single product in a readable format
def display_product(product):
    print(
        product["product_id"],
        "|", product["product_name"],
        "|", product["category"],
        "|", product["supplier"],
        "| Rs.", product["price"],
        "| Qty:", product["quantity"],
        "| Min Stock:", product["min_stock"]
    )


# Display all products stored in the inventory
def view_products():
    products = get_products()

    print("\n===== PRODUCT LIST =====")

    # Handle the case when no products are available
    if not products:
        print("No products found.")
        return

    # Display each product
    for product in products:
        display_product(product)


# Take input from the user to add a new product
def add_new_product():
    print("\n===== ADD PRODUCT =====")

    # Read the unique Product ID
    product_id = input("Enter Product ID: ").strip()

    if not product_id:
        print("Product ID cannot be empty.")
        return

    # Prevent duplicate Product IDs
    if get_product(product_id):
        print("Product ID already exists.")
        return

    # Read the basic product details
    product_name = input("Enter Product Name: ").strip()
    category = input("Enter Category: ").strip()
    supplier = input("Enter Supplier: ").strip()

    # Validate required text fields
    if not product_name or not category or not supplier:
        print("Product Name, Category and Supplier cannot be empty.")
        return

    # Read numeric product details
    try:
        price = float(input("Enter Price: "))
        quantity = int(input("Enter Quantity: "))
        min_stock = int(input("Enter Minimum Stock: "))
    # Handle invalid numeric input
    except ValueError:
        print("Invalid input. Price must be a number and quantity/minimum stock must be integers.")
        return

    # Price cannot be negative
    if price < 0:
        print("Price cannot be negative.")
        return

    # Quantity cannot be negative
    if quantity < 0:
        print("Quantity cannot be negative.")
        return

    # Minimum stock cannot be negative
    if min_stock < 0:
        print("Minimum Stock cannot be negative.")
        return

    # Create the product record
    product = {
        "product_id": product_id,
        "product_name": product_name,
        "category": category,
        "supplier": supplier,
        "price": price,
        "quantity": quantity,
        "min_stock": min_stock,
        # Store today's date as the product creation date
        "created_at": date.today().isoformat()
    }

    try:
        # Add the product to the database
        add_product(product)

        # Create an initial stock-in transaction when quantity is greater than zero
        if quantity>0:
            transaction_id=get_next_transaction_id()

            # Create the stock-in transaction record
            transaction= {
                "transaction_id": transaction_id,
                "product_id" :product_id,
                "type" : "IN",
                "quantity" : quantity,
                "transaction_date" : date.today().isoformat()
            }

            # Save the initial stock transaction
            add_transaction(transaction)

        print("Product added successfully.")

    except Exception as error:
        # Catch any unexpected error while saving the product/transaction
        print(f"Something went wrong while adding the product: {error}")


# Update details of an existing product
def update_existing_product():
    print("\n===== UPDATE PRODUCT =====")

    # Read the Product ID of the product to update
    product_id = input("Enter Product ID to update: ").strip()
    # Find the product in the database
    product = get_product(product_id)

    # Stop if the product does not exist
    if not product:
        print("Product not found.")
        return

    # Show the current details before updating
    print("\nCurrent Product Details:")
    display_product(product)

    # Read new product details; blank input keeps the current value
    product_name = input(
        "Enter new Product Name (leave blank to keep current): "
    ).strip()

    category = input(
        "Enter new Category (leave blank to keep current): "
    ).strip()

    supplier = input(
        "Enter new Supplier (leave blank to keep current): "
    ).strip()

    # Read the new price
    price_input = input(
        "Enter new Price (leave blank to keep current): "
    ).strip()

    # Read the new minimum stock level
    min_stock_input = input(
        "Enter new Minimum Stock (leave blank to keep current): "
    ).strip()

    # Convert numeric inputs and keep old values when input is blank
    try:
        price = float(price_input) if price_input else product["price"]
        min_stock = (
            int(min_stock_input)
            if min_stock_input
            else product["min_stock"]
        )
    # Handle invalid numeric input
    except ValueError:
        print("Invalid input. Price must be a number and quantity/minimum stock must be integers.")
        return

    # Validate updated numeric values
    if price < 0  or min_stock < 0:
        print("Price and minimum stock cannot be negative.")
        return

    # Create the updated product record while keeping unchanged fields
    updated_product = {
        "product_id": product["product_id"],
        "product_name": product_name if product_name else product["product_name"],
        "category": category if category else product["category"],
        "supplier": supplier if supplier else product["supplier"],
        "price": price,
        "quantity":product["quantity"],
        "min_stock": min_stock,
        "created_at": product.get("created_at", date.today().isoformat())
    }

    try:
        # Save the updated product
        update_product(product_id, updated_product)
        print("Product updated successfully.")

    except Exception as error:
        # Catch any unexpected error while saving the updated product
        print(f"Something went wrong while updating the product: {error}")


# Delete an existing product
def delete_existing_product():
    print("\n===== DELETE PRODUCT =====")

    # Read the Product ID of the product to delete
    product_id = input("Enter Product ID to delete: ").strip()
    product = get_product(product_id)

    # Stop if the product does not exist
    if not product:
        print("Product not found.")
        return

    # Show the product before deletion
    print("\nProduct Details:")
    display_product(product)

    # Ask the user to confirm deletion
    confirm = input(
        f"Are you sure you want to delete product "
        f"'{product['product_name']}'? (y/n): "
    ).strip().lower()

    # Delete the product only after confirmation
    if confirm == "y":
        try:
            delete_product(product_id)

            # Renumber remaining products sequentially and update
            # the matching product_id in all transactions
            renumber_products()

            print("Product deleted successfully. Product IDs have been renumbered.")

        except Exception as error:
            # Catch any unexpected error while deleting the product
            print(f"Something went wrong while deleting the product: {error}")
    else:
        print("Deletion cancelled.")


# Search for a product using its Product ID
def search_product():
    print("\n===== SEARCH PRODUCT =====")

    # Read the Product ID to search
    product_id = input("Enter Product ID to search: ").strip()
    product = get_product(product_id)

    # Display the product when it is found
    if product:
        print("\n===== PRODUCT DETAILS =====")
        display_product(product)
    else:
        print("Product not found.")


# Display the Product Management menu
def product_menu():
    # Keep showing the menu until the user returns to the main menu
    while True:
        # Display product management options
        print("\n===== PRODUCT MANAGEMENT =====")
        print("1. View Products")
        print("2. Add Product")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Search Product")
        print("6. Back to Main Menu")

        # Read and clean the user's menu choice
        product_choice = input("Enter your choice: ").strip()

        # View all products
        if product_choice == "1":
            view_products()

        # Add a new product
        elif product_choice == "2":
            add_new_product()

        # Update an existing product
        elif product_choice == "3":
            update_existing_product()

        # Delete an existing product
        elif product_choice == "4":
            delete_existing_product()

        # Search for a product
        elif product_choice == "5":
            search_product()

        # Return to the main menu
        elif product_choice == "6":
            print("Returning to Main Menu.")
            break

        else:
            # Handle an invalid menu choice
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    product_menu()