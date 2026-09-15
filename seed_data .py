import json


# Name of the JSON file used to store the initial data
FILE_NAME = "inventory.json"


# Define the initial product records
# Initial product data
products = [
    {
        "product_id": "P001",
        "product_name": "Wireless Mouse",
        "category": "Computer Accessories",
        "supplier": "Logitech",
        "price": 699,
        "quantity": 50,
        "min_stock": 10,
        "created_at": "2026-09-01"
    },
    {
        "product_id": "P002",
        "product_name": "Mechanical Keyboard",
        "category": "Computer Accessories",
        "supplier": "Redragon",
        "price": 2499,
        "quantity": 25,
        "min_stock": 5,
        "created_at": "2026-09-01"
    },
    {
        "product_id": "P003",
        "product_name": "USB-C Cable",
        "category": "Cables",
        "supplier": "Portronics",
        "price": 299,
        "quantity": 80,
        "min_stock": 15,
        "created_at": "2026-09-02"
    },
    {
        "product_id": "P004",
        "product_name": "Bluetooth Speaker",
        "category": "Audio",
        "supplier": "JBL",
        "price": 3499,
        "quantity": 18,
        "min_stock": 5,
        "created_at": "2026-09-02"
    },
    {
        "product_id": "P005",
        "product_name": "Webcam",
        "category": "Computer Accessories",
        "supplier": "HP",
        "price": 1899,
        "quantity": 12,
        "min_stock": 5,
        "created_at": "2026-09-03"
    },
    {
        "product_id": "P006",
        "product_name": "Power Bank",
        "category": "Mobile Accessories",
        "supplier": "MI",
        "price": 1499,
        "quantity": 30,
        "min_stock": 8,
        "created_at": "2026-09-03"
    },
    {
        "product_id": "P007",
        "product_name": "Wireless Earbuds",
        "category": "Audio",
        "supplier": "Boat",
        "price": 1299,
        "quantity": 7,
        "min_stock": 10,
        "created_at": "2026-09-04"
    },
    {
        "product_id": "P008",
        "product_name": "HDMI Cable",
        "category": "Cables",
        "supplier": "Amazon Basics",
        "price": 499,
        "quantity": 4,
        "min_stock": 10,
        "created_at": "2026-09-04"
    }
]


# Define the initial stock transaction records
# Initial transaction data
transactions = [
    {
        "transaction_id": 1,
        "product_id": "P001",
        "transaction_type": "IN",
        "quantity": 60,
        "transaction_date": "2026-09-01"
    },
    {
        "transaction_id": 2,
        "product_id": "P001",
        "transaction_type": "OUT",
        "quantity": 10,
        "transaction_date": "2026-09-03"
    },
    {
        "transaction_id": 3,
        "product_id": "P002",
        "transaction_type": "IN",
        "quantity": 30,
        "transaction_date": "2026-09-01"
    },
    {
        "transaction_id": 4,
        "product_id": "P002",
        "transaction_type": "OUT",
        "quantity": 5,
        "transaction_date": "2026-09-05"
    },
    {
        "transaction_id": 5,
        "product_id": "P003",
        "transaction_type": "IN",
        "quantity": 100,
        "transaction_date": "2026-09-02"
    },
    {
        "transaction_id": 6,
        "product_id": "P003",
        "transaction_type": "OUT",
        "quantity": 20,
        "transaction_date": "2026-09-06"
    },
    {
        "transaction_id": 7,
        "product_id": "P004",
        "transaction_type": "IN",
        "quantity": 20,
        "transaction_date": "2026-09-02"
    },
    {
        "transaction_id": 8,
        "product_id": "P004",
        "transaction_type": "OUT",
        "quantity": 2,
        "transaction_date": "2026-09-06"
    },
    {
        "transaction_id": 9,
        "product_id": "P005",
        "transaction_type": "IN",
        "quantity": 15,
        "transaction_date": "2026-09-03"
    },
    {
        "transaction_id": 10,
        "product_id": "P005",
        "transaction_type": "OUT",
        "quantity": 3,
        "transaction_date": "2026-09-07"
    },
    {
        "transaction_id": 11,
        "product_id": "P006",
        "transaction_type": "IN",
        "quantity": 40,
        "transaction_date": "2026-09-03"
    },
    {
        "transaction_id": 12,
        "product_id": "P006",
        "transaction_type": "OUT",
        "quantity": 10,
        "transaction_date": "2026-09-07"
    },
    {
        "transaction_id": 13,
        "product_id": "P007",
        "transaction_type": "IN",
        "quantity": 10,
        "transaction_date": "2026-09-04"
    },
    {
        "transaction_id": 14,
        "product_id": "P007",
        "transaction_type": "OUT",
        "quantity": 3,
        "transaction_date": "2026-09-08"
    },
    {
        "transaction_id": 15,
        "product_id": "P008",
        "transaction_type": "IN",
        "quantity": 10,
        "transaction_date": "2026-09-04"
    },
    {
        "transaction_id": 16,
        "product_id": "P008",
        "transaction_type": "OUT",
        "quantity": 6,
        "transaction_date": "2026-09-08"
    }
]


# Combine the product and transaction data
# Combine products and transactions
data = {
    "products": products,
    "transactions": transactions
}


# Write the initial inventory data to the JSON file
# Write data into JSON file
with open(FILE_NAME, "w") as file:
    json.dump(data, file, indent=4)


# Confirm that the initial data was created
print("Inventory data created successfully!")
# Display the number of products added
print("8 products added.")
# Display the number of transactions added
print("16 transactions added.")