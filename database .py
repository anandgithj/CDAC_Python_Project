import json

# Name of the JSON file used for storing inventory data

FILE_NAME = "inventory.json"


# Load all data from JSON file
def load_data():
    # Open the JSON file and read the stored data
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        # Return an empty inventory structure if the file does not exist
        return {
            "products": [],
            "transactions": []
        }

    except json.JSONDecodeError:
        # Handle a corrupted or invalid JSON file instead of crashing
        print(f"Warning: '{FILE_NAME}' is corrupted or invalid. Starting with empty inventory.")
        return {
            "products": [],
            "transactions": []
        }


# Save data to JSON file
def save_data(data):
    # Write the updated inventory data back to the JSON file
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(data, file, indent=4)

    except OSError as error:
        # Handle file-write failures (e.g. permission denied, disk full)
        print(f"Error: Could not save data to '{FILE_NAME}'. ({error})")


# Get all products
def get_products():
    # Return the list of all products
    data = load_data()
    return data["products"]


# Get all transactions
def get_transactions():
    # Return the list of all stock transactions
    data = load_data()
    return data["transactions"]


# Find a product using Product ID
def get_product(product_id):
    # Search for a product by its unique Product ID
    products = get_products()

    for product in products:
        # Return the matching product when the Product ID is found
        if product["product_id"] == product_id:
            return product

    return None


# Add a new product
def add_product(product):
    # Add the new product to the products list
    data = load_data()

    data["products"].append(product)

    # Save the updated product list
    save_data(data)


# Update an existing product
def update_product(product_id, updated_product):
    data = load_data()

# Check each product to find the one that needs to be updated

    for i, product in enumerate(data["products"]):

        if product["product_id"] == product_id:
            # Replace the matching product with the updated product details
            data["products"][i] = updated_product

            save_data(data)
            return True

    return False


# Delete a product
def delete_product(product_id):
    # Check each product before deleting it
    data = load_data()

    for product in data["products"]:

        if product["product_id"] == product_id:
            # Remove the matching product from the products list
            data["products"].remove(product)

            # Mark this product's past transactions as belonging to a
            # deleted product, so this Product ID is never confused with
            # a live product after the remaining products get renumbered
            for transaction in data["transactions"]:
                if transaction.get("product_id") == product_id:
                    transaction["product_id"] = f"{product_id}-DELETED"

            save_data(data)
            return True

    return False


# Renumber all products sequentially (P001, P002, ...) and update
# the product_id in every transaction to match, keeping data consistent
def renumber_products():
    data = load_data()

    products = data["products"]
    transactions = data["transactions"]

    # Build a mapping of old Product ID -> new Product ID, in current order
    id_mapping = {}

    for index, product in enumerate(products, start=1):
        old_id = product["product_id"]
        new_id = f"P{index:03d}"

        id_mapping[old_id] = new_id
        product["product_id"] = new_id

    # Update every transaction's product_id using the same mapping
    for transaction in transactions:

        old_product_id = transaction.get("product_id")

        if old_product_id in id_mapping:
            transaction["product_id"] = id_mapping[old_product_id]

    # Save the renumbered products and updated transactions together
    save_data(data)


# Add a stock transaction
# Add the new stock transaction to the transactions list
def add_transaction(transaction):
    data = load_data()

    data["transactions"].append(transaction)

    save_data(data)


# Get the next transaction ID
# Generate the next transaction ID
def get_next_transaction_id():
    transactions = get_transactions()

    # Start with ID 1 when there are no previous transactions
    if len(transactions) == 0:
        return 1

    # Find the highest existing transaction ID and increment it
    return max(
        transaction["transaction_id"]
        for transaction in transactions
    ) + 1