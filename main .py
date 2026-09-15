# Import the product management menu
from product import product_menu
# Import the inventory management menu
from stock import stock_menu
# Import the reports menu
from reports import report_menu



def main():

    # Keep displaying the main menu until the user chooses to exit
    while True:

        # Display the main menu options
        print("\n==========================================")
        print("       HARDWARE INVENTORY SYSTEM")
        print("==========================================")
        print("1. Product Management")
        print("2. Inventory Management")
        print("3. Reports")
       
        print("5. Exit")
        print("==========================================")

        # Read and clean the user's menu choice
        choice = input("Enter your choice: ").strip()

        # Open Product Management
        if choice == "1":
            product_menu()

        # Open Inventory Management
        elif choice == "2":
            stock_menu()

        # Open Reports
        elif choice == "3":
            report_menu()


        # Exit the application
        elif choice == "5":
            print("\nThank you for using Hardware Inventory System.")
            break

        else:
            # Handle an invalid menu choice
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()