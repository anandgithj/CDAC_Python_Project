# Hardware Inventory System

A simple command-line inventory management system built in Python. It manages products, tracks stock in/out transactions, and generates reports (including charts) — all stored locally in a JSON file, no database setup needed.

## Features

- **Product Management** — Add, view, update, delete, and search products
- **Inventory Management** — Record Stock In (purchases/restocking) and Stock Out (sales/issued) transactions
- **Reports**
  - Current Stock Report (with total inventory value)
  - Low Stock Report (products at or below minimum stock)
  - Transaction History
  - Stock In/Out Summary
  - Date-wise Stock Summary
  - Low Stock Chart (bar chart)
  - Category-wise Inventory Value Chart (pie chart)
  - Stock In/Out Trend Chart (line chart)

## Project Structure

```
├── main.py          # Entry point — main menu
├── product.py       # Product management (CRUD + search)
├── stock.py         # Stock in / stock out operations
├── reports.py        # Reports and chart generation
├── database.py       # JSON read/write helper functions
├── seed_data.py       # Creates inventory.json with sample data
└── inventory.json      # Data storage file (auto-created)
```

## Requirements

- Python 3.x
- `matplotlib` (for chart-based reports)

Install the dependency:
```bash
pip install matplotlib
```

## How to Run

1. (Optional) Seed the system with sample data:
   ```bash
   python seed_data.py
   ```
2. Start the application:
   ```bash
   python main.py
   ```
3. Use the on-screen menu to navigate between Product Management, Inventory Management, and Reports.

## Data Model

**Product**
| Field | Type | Description |
|---|---|---|
| product_id | string | Unique ID (e.g. P001) |
| product_name | string | Name of the product |
| category | string | Product category |
| supplier | string | Supplier name |
| price | float | Unit price |
| quantity | int | Current stock quantity |
| min_stock | int | Minimum stock threshold |
| created_at | string | Date added (YYYY-MM-DD) |

**Transaction**
| Field | Type | Description |
|---|---|---|
| transaction_id | int | Unique transaction ID |
| product_id | string | Linked product ID |
| transaction_type | string | `IN` or `OUT` |
| quantity | int | Quantity moved |
| transaction_date | string | Date of transaction (YYYY-MM-DD) |

## Notes

- All data is stored in `inventory.json`, which is created automatically on first run if it doesn't exist.
- Deleting a product renumbers all remaining product IDs sequentially (P001, P002, ...) and updates related transactions to stay consistent.
- Charts generated from the Reports menu are saved as PNG files in the project folder.
