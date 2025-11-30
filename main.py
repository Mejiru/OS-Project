import cpu_schedule  # Hatem
import BankersAlgorithm  # Mohammad and Ahmad
import part3  # Irfan


def show_menu():
    while True:
        print("          OS Simulator         ")
        print("=" * 30)
        print("[1] CPU Scheduling")
        print("[2] Banker's Algorithm")
        print("[3] Page Replacement Algorithms")
        print("[0] Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("\n--- CPU Scheduling ---")
            cpu_schedule.run()
            input("\nPress Enter to return to the menu...")

        elif choice == "2":
            print("\n--- Banker's Algorithm ---")
            algo = BankersAlgorithm.BankersAlgorithm()
            algo.run()
            input("\nPress Enter to return to the menu...")

        elif choice == "3":
            print("\n--- Page Replacement Algorithms ---")
            part3.run()
            input("\nPress Enter to return to the menu...")

        elif choice == "0":
            print("\nExiting program...")
            break

        else:
            print("\nInvalid input, try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    show_menu()
