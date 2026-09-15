from database import *
from datetime import date

# Handle stock received into the inventory
def stock_in():
    # Read the Product ID
    product_id=input("Enter Product ID: ").strip()
    # Find the product in the database
    product=get_product(product_id)

    if product:
        # Read the quantity received
        try:
            quantity=int(input("Enter quantity received: "))
        # Handle invalid (non-numeric) input
        except ValueError:
            print("Invalid input. Quantity must be a whole number.")
            return

        # Accept only positive quantities
        if quantity>0:
            try:
                # Increase the current stock quantity
                new_quantity=product["quantity"]+quantity
                # Copy the product before updating its quantity
                updated_product=product.copy()
                updated_product["quantity"]=new_quantity

                # Save the updated stock quantity
                update_product(product_id, updated_product)

                # Generate a unique transaction ID
                transaction_id = get_next_transaction_id()

                # Create the stock-in transaction record
                transaction = {
                    "transaction_id": transaction_id,
                    "product_id": product_id,
                    "type": "IN",
                    "quantity": quantity,
                    "transaction_date":date.today().isoformat()
                }

                # Save the stock-in transaction
                add_transaction(transaction)

                # Confirm successful stock addition
                print("Stock added successfully!")

            except Exception as error:
                # Catch any unexpected error while updating stock/saving the transaction
                print(f"Something went wrong while adding stock: {error}")

        else:
            # Reject zero or negative quantities
            print("Quantity must be greater than 0!")

    else:
        # Handle an invalid Product ID
        print("Product not found!")

# stock_in()

# Handle stock issued from the inventory
def stock_out():
    # Read the Product ID
    product_id=input("Enter Product ID: ").strip()
    # Find the product in the database
    product=get_product(product_id)

    if product:
        # Read the quantity issued
        try:
            quantity=int(input("Enter quantity sold: "))
        # Handle invalid (non-numeric) input
        except ValueError:
            print("Invalid input. Quantity must be a whole number.")
            return

        # Check that the quantity is positive and available
        if quantity>0 and quantity <= product["quantity"]:
            try:
                # Decrease the current stock quantity
                new_quantity = product["quantity"] - quantity
                # Copy the product before updating its quantity
                updated_product = product.copy()
                updated_product["quantity"] = new_quantity
                # Save the updated stock quantity
                update_product(product_id, updated_product)

                # Generate a unique transaction ID
                transaction_id = get_next_transaction_id()

                # Create the stock-out transaction record
                transaction = {
                    "transaction_id": transaction_id,
                    "product_id": product_id,
                    "type": "OUT",
                    "quantity": quantity,
                    "transaction_date":date.today().isoformat()
                }
                # Save the stock-out transaction
                add_transaction(transaction)

                # Confirm successful stock removal
                print("Stock removed successfully!")

            except Exception as error:
                # Catch any unexpected error while updating stock/saving the transaction
                print(f"Something went wrong while removing stock: {error}")

        else:
            # Handle invalid or insufficient stock quantity
            if quantity <= 0:
                print("Quantity must be greater than 0!")
            else:
                print("Insufficient stock!")

    else:
        # Handle an invalid Product ID
        print("Product not found!")

# stock_out()

# Display the Inventory Management menu
def stock_menu():

    # Keep showing the menu until the user returns
    while True:

        # Display inventory management options
        print("\n==========================================")
        print("          INVENTORY MANAGEMENT")
        print("==========================================")
        print("1. Stock In")
        print("2. Stock Out")
        print("3. Back to Main Menu")
        print("==========================================")

        # Read and clean the user's menu choice
        choice = input("Enter your choice: ").strip()

        # Open Stock In
        if choice == "1":
            stock_in()

        # Open Stock Out
        elif choice == "2":
            stock_out()

        # Return to the main menu
        elif choice == "3":
            break

        else:
            # Handle an invalid menu choice
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    stock_menu()