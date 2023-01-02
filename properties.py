def properties(conn, cur):
    """Allows user to view properties, edit properties, or go back to the main menu."""
    print("\nChoose an option:")
    print(" a) View Properties")
    print(" b) Edit Properties")
    print(" c) Go Back")

    # Loop until user inputs valid choice
    choice = "sentinel"
    while (choice != "a" and choice != "b" and choice != "c"):
        choice = input("=> ")

    # Select and print all properties
    if (choice == "a"):
        # Select addresses and property manager name of all properties
        data = cur.execute("""SELECT properties.Property_Address, managers.First_Name, managers.Last_Name FROM properties JOIN managers
                           ON properties.Manager_ID = managers.Manager_ID;""")
        for tup in data:
            property_address = tup[0]
            manager_name = tup[1] + " " + tup[2]
            print(f"{property_address} - managed by {manager_name}")
        properties(conn, cur)
        return
        
    elif (choice == "b"):
        edit_properties(conn, cur)
        return
    else:
        return

def edit_properties(conn, cur):
    """Allows the user to add, remove, and edit properties."""
    print("\nChoose an option:")
    print(" a) Add a Property")
    print(" b) Remove a Property")
    print(" c) Edit a Property")
    print(" d) Go Back")

    # Loop until user inputs valid choice
    choice = "sentinel"
    while (choice != "a" and choice != "b" and choice != "c" and choice != "d"):
        choice = input("=> ")
    
    if (choice == "a"): # a = add property
        # Select property address of all properties
        data = cur.execute("SELECT Property_Address FROM properties")
        property_addresses = []
        for tup in data:
            property_addresses.append(tup[0])
        # Choose the new property's address
        property_address_to_add = input("Enter the property's address: ")
        while (property_address_to_add in property_addresses):
            property_address_to_add = input("That property is already in the system. Enter a different address: ")
        data = cur.execute("SELECT * FROM managers")
        manager_ids = []
        for tup in data:
            manager_id = str(tup[0])
            manager_name = tup[1] + " " + tup[2]
            manager_ids.append(manager_id)
            print(f"{manager_id} - {manager_name}")
        # Choose which manager will manage the property
        manager_to_add = str(input("Enter the ID of the manager that will manage this property: "))
        while (manager_to_add not in manager_ids):
            manager_to_add = str(input("Invalid input. Please enter a valid ID: "))
        # Insert new property into properties
        cur.execute(f"INSERT INTO properties (Manager_ID, Property_Address) VALUES ('{manager_to_add}', '{property_address_to_add}');")
        conn.commit()
        edit_properties(conn, cur)
        return

    elif (choice == "b"): # b = remove property
        # Select unsold properties
        data = cur.execute("SELECT Property_Number, Property_Address FROM properties WHERE Property_Number NOT IN (SELECT Property_Number FROM sales);")
        unsold_property_ids = []
        for tup in data:
            property_id = str(tup[0])
            property_address = tup[1]
            unsold_property_ids.append(property_id)
            print(f"{property_id} - {property_address}")
        print("Note: Only unsold properties can be removed.")
        # Choose which property to remove
        property_to_del = str(input("Enter the property number of the property to remove: "))
        while (property_to_del not in unsold_property_ids):
            property_to_del = str(input("Invalid input. Please enter a valid property number: "))
        # Remove selected property from properties
        cur.execute(f"DELETE FROM properties WHERE Property_Number = '{property_to_del}';")
        conn.commit()
        edit_properties(conn, cur)
        return

    elif (choice == "c"): # c = edit property
        # Select property number and property address of all properties
        data = cur.execute("SELECT Property_Number, Property_Address FROM properties;")
        property_ids = []
        property_addresses = []
        for tup in data:
            property_id = str(tup[0])
            property_address = tup[1]
            property_ids.append(property_id)
            property_addresses.append(property_address)
            print(f"{property_id} - {property_address}")
        # Choose which property to edit
        property_to_edit = str(input("Enter the property number of the property to edit: "))
        while (property_to_edit not in property_ids):
            property_to_edit = str(input("Invalid input. Please enter a valid property number: "))
        # Choose new address
        new_property_address = input("Enter the property's new address: ")
        while (new_property_address in property_addresses):
            new_property_address = input("That property is already in the system. Enter a different address: ")
        # Select all managers
        data = cur.execute("SELECT * FROM managers")
        manager_ids = []
        for tup in data:
            manager_id = str(tup[0])
            manager_name = tup[1] + " " + tup[2]
            manager_ids.append(manager_id)
            print(f"{manager_id} - {manager_name}")
        # Choose which manager will manage the property
        new_manager = str(input("Enter the ID of the manager that will manage this property: "))
        while (new_manager not in manager_ids):
            new_manager = str(input("Invalid input. Please enter a valid ID: "))
        # Update the property with new address and manager ID
        cur.execute(f"UPDATE properties SET Property_Address = '{new_property_address}', Manager_ID = '{new_manager}' WHERE Property_Number = '{property_to_edit}';")
        conn.commit()
        edit_properties(conn, cur)
        return

    # Return to properties 
    else:
        properties(conn, cur)
    return
