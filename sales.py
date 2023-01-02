def sales(conn, cur):
    """Allows user to view sales, edit sales, or go back to the main menu."""
    print("\nChoose an option:")
    print(" a) View Sales")
    print(" b) Edit Sales")
    print(" c) Go Back")

    # Loop until user inputs valid choice
    choice = "sentinel"
    while (choice != "a" and choice != "b" and choice != "c"):
        choice = input("=> ")

    # Select and print all managers
    if (choice == "a"):
        # Select property number and how much the property was sold for from sales
        data = cur.execute("SELECT Property_Number, Sold_For FROM sales")
        for tup in data:
            property_number = str(tup[0])
            sold_for = str(tup[1])
            print(f"Property #{property_number} - ${sold_for}")
        sales(conn, cur)
        return
        
    elif (choice == "b"):
        edit_sales(conn, cur)
        return
    else:
        return

def edit_sales(conn, cur):
    """Allows the user to add, remove, and edit sales"""
    print("\nChoose an option:")
    print(" a) Add a Sale")
    print(" b) Remove a Sale")
    print(" c) Edit a Sale")
    print(" d) Go Back")

    # Loop until user inputs valid choice
    choice = "sentinel"
    while (choice != "a" and choice != "b" and choice != "c" and choice != "d"):
        choice = input("=> ")

    if (choice == "a"): # a = add sale
        # Select property number of unsold properties
        data = cur.execute("SELECT Property_Number, Property_Address FROM properties WHERE Property_Number NOT IN (SELECT Property_Number FROM sales);")
        unsold_property_ids = []
        for tup in data:
            property_id = str(tup[0])
            property_address = tup[1]
            unsold_property_ids.append(property_id)
            print(f"{property_id} - {property_address}")
        # Get property number of sale
        property_number_to_add = str(input("Enter the property number of the sold property: "))
        while (property_number_to_add not in unsold_property_ids):
            property_number_to_add = str(input("Invalid input. Please enter a valid property number: "))
        # Get how much the property was sold for
        sold_for = str(input("Enter how much the property sold for: "))
        while (sold_for.isdigit() == False):
            sold_for = str(input("Invalid input. Please enter a positive integer: "))
        # Insert the property number of the property and how much it sold for into sales
        cur.execute(f"INSERT INTO sales (Property_Number, Sold_For) VALUES ('{property_number_to_add}', '{sold_for}');")
        conn.commit()
        edit_sales(conn, cur)
        return
    
    elif (choice == "b"): # b = remove sale
        # Select sale number and property address
        data = cur.execute("SELECT Sale_Number, Property_Address FROM sales JOIN properties ON sales.Property_Number = properties.Property_Number;")
        sale_numbers = []
        for tup in data:
            sale_number = str(tup[0])
            property_address = tup[1]
            sale_numbers.append(sale_number)
            print(f"{sale_number} - {property_address}")
        # Choose which sale to remove
        sale_to_del = str(input("Enter the sale number of the sale to remove: "))
        while (sale_to_del not in sale_numbers):
            sale_to_del = str(input("Invalid input. Please enter a valid sale number: "))
        cur.execute(f"DELETE FROM sales WHERE Sale_Number = '{sale_to_del}';")
        conn.commit()
        edit_sales(conn, cur)
        return
    
    elif (choice == "c"): # c = edit sale
        # Select sale number, property number, and property address
        data = cur.execute("SELECT Sale_Number, Property_Number, Property_Address FROM sales JOIN properties ON sales.Property_Number = properties.Property_Number;")
        sale_numbers = []
        for tup in data:
            sale_number = str(tup[0])
            property_number = tup[1]
            property_address = tup[2]
            sale_numbers.append(sale_number)
            print(f"Sale #{sale_number} - Property #{property_number} - {property_address}")
        # Choose which sale to edit
        sale_to_edit = str(input("Enter the sale number of the sale to edit: "))
        while (sale_to_edit not in sale_numbers):
            sale_to_edit = str(input("Invalid input. Please enter a valid sale number: "))
        # Get how much the property was sold for
        sold_for = str(input("Enter how much the property sold for: "))
        while (sold_for.isdigit() == False):
            sold_for = str(input("Invalid input. Please enter a positive integer: "))
        # Update the sale with new sell cost
        cur.execute(f"UPDATE sales SET Sold_For = '{sold_for}' WHERE Sale_Number = '{sale_to_edit}';")
        conn.commit()
        edit_sales(conn, cur)
        return
    
    # Return to sales
    else:
        sales(conn, cur)
    return