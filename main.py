import BankersAlgorithm
import part3

def show_menu():
    while True:
        print("          OS Simulator         ")
        print("[1] Banker's Algorithm")
        print("[2] Page Replacement Algorithms (Part 3)")
        print("[3] Another Algorithm (placeholder)")
        print("[0] Exit")
        print("="*30)
        choice = input("Enter your choice: ").strip()
        if choice == "1":
          print("\n--- Option 3 selected (placeholder) ---")
          input("\nPress Enter to return to the menu...")
        elif choice == "2":
            print("\n--- Banker's Algorithm ---")
            BankersAlgorithm.run()
            input("\nPress Enter to return to the menu...")
        elif choice == "3":
            print("\n--- Page Replacement Algorithms (Part 3) ---")
            part3.run()
            input("\nPress Enter to return to the menu...")

        elif choice == "0":
            print("\nExiting program...")
            break
        else:
            print("\nInvalid input, try again.")
            input("Press Enter...")
if __name__ == "__main__":
    show_menu()
