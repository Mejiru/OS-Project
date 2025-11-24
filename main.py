import BankersAlgorithm
import part3

def show_menu():
    while True:
        print("          OS Simulator         ")
        print("=" * 30)
        print("[1] Hatem's Part")
        print("[2] Banker's Algorithm")
        print("[3] Page Replacement Algorithms")
        print("[0] Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
          print("\nHatem's part")
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
