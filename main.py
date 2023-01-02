import sqlite3
import properties, managers, sales, business_analytics

def main_menu():
    """Allows user to select where they would like to navigate."""
    print("\nChoose an option:")
    print(" a) Properties")
    print(" b) Managers")
    print(" c) Sales")
    print(" d) Business Analytics")
    print(" e) Log off")

    # Loop until user inputs valid choice
    choice = "sentinel"
    while (choice != "a" and choice != "b" and choice != "c" and choice != "d" and choice != "e"):
        choice = input("=> ")
    return choice

def main():
    """Runs the individual parts as a whole application."""
    conn = sqlite3.connect('data\\property_management.db')
    cur = conn.cursor()
    print("\nWelcome to Little Red Home's property management program!")
    print("You are the CEO of Little Red Home, a property management company. Using this application, you can manage your company!")
    choice = main_menu()
    # Loop until user inputs valid choice
    while (choice != "e"): # e = log off
        if (choice == "a"):# a = properties 
            properties.properties(conn, cur)
            choice = main_menu()
        elif (choice == "b"): # b = managers
            managers.managers(conn, cur)
            choice = main_menu()
        elif (choice == "c"): # c = sales
            sales.sales(conn, cur)
            choice = main_menu()
        elif (choice == "d"): # d = business analytics
            business_analytics.business_analytics(conn, cur)
            choice = main_menu()
        else:
            print("You successfully logged off!")
            conn.close()
            return 0

main()