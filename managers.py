def managers(conn, cur):
    """Allows user to view managers, edit managers, or go back to the main menu."""
    print("\nChoose an option:")
    print(" a) View Managers")
    print(" b) Edit Managers")
    print(" c) Go Back")

    # Loop until user inputs valid choice
    choice = "sentinel"
    while (choice != "a" and choice != "b" and choice != "c"):
        choice = input("=> ")

    # Select and print all managers
    if (choice == "a"):
        # Select manager ID, and first and last names
        data = cur.execute("SELECT * FROM managers")
        for tup in data:
            manager_id = str(tup[0])
            manager_name = tup[1] + " " + tup[2]
            print(f"{manager_id} - {manager_name}")
        managers(conn, cur)
        return
        
    elif (choice == "b"):
        edit_managers(conn, cur)
        return
    else:
        return

def edit_managers(conn, cur):
    """Allows the user to add and remove managers."""
    print("\nChoose an option:")
    print(" a) Add a Manager")
    print(" b) Remove a Manager")
    print(" c) Edit a Manager")
    print(" d) Go Back")

    # Loop until user inputs valid choice
    choice = "sentinel"
    while (choice != "a" and choice != "b" and choice != "c" and choice != "d"):
        choice = input("=> ")

    if (choice == "a"): # a = add manager
        # Enter the manager's first and last name
        new_manager_first = input("Enter the manager's first name: ")
        new_manager_last = input("Enter the manager's last name: ")
        # Insert new manager into managers
        cur.execute(f"INSERT INTO managers (First_Name, Last_Name) VALUES ('{new_manager_first}', '{new_manager_last}');")
        conn.commit()
        edit_managers(conn, cur)
        return

    if (choice == "b"): # b = remove manager
        # Select manager ID, and first and last names
        data = cur.execute("SELECT * FROM managers")
        manager_ids = []
        for tup in data:
            manager_id = str(tup[0])
            manager_name = tup[1] + " " + tup[2]
            manager_ids.append(manager_id)
            print(f"{manager_id} - {manager_name}")
        # Choose which manager to remove
        manager_to_del = str(input("Enter the manager ID of the manager to remove: "))
        while (manager_to_del not in manager_ids):
            manager_to_del = str(input("Invalid input. Please enter a valid manager ID: "))
        # Select property number and address of the properties that the manager-to-be-removed manages
        data = cur.execute(f"""SELECT Property_Number, Property_Address FROM properties JOIN managers on properties.Manager_ID = managers.Manager_ID 
                                                WHERE managers.Manager_ID = '{manager_to_del}';""")
        properties_to_reassign = []
        for tup in data:
            properties_to_reassign.append(str(tup[0]))
        # If manager has no properties, go back
        if (len(properties_to_reassign) == 0):
            # Remove manager-to-be-removed from managers
            cur.execute(f"DELETE FROM managers WHERE Manager_ID = '{manager_to_del}';")
            conn.commit()
            edit_managers(conn, cur)
            return
        else:
            # Select all managers except the manager-to-be-removed
            data = cur.execute(f"SELECT * FROM managers WHERE NOT Manager_ID = '{manager_to_del}';")
            manager_ids = []
            for tup in data:
                manager_id = str(tup[0])
                manager_name = tup[1] + " " + tup[2]
                manager_ids.append(manager_id)
                print(f"{manager_id} - {manager_name}")
            # Assign other managers to the properties that the manager-to-be-removed's manages
            for property in properties_to_reassign:
                new_manager = str(input(f"Enter the manager ID of the manager to manage property number {property}: "))
                while (new_manager not in manager_ids and new_manager != manager_to_del):
                    new_manager = str(input("Invalid input. Please enter a valid manager ID: "))
                cur.execute(f"UPDATE properties SET Manager_ID = '{new_manager}' WHERE Property_Number = '{property}';")
            # Remove manager-to-be-removed from managers
            cur.execute(f"DELETE FROM managers WHERE Manager_ID = '{manager_to_del}';")
            conn.commit()
            edit_managers(conn, cur)
            return

    if (choice == "c"): # c = edit manager
        # Select manager ID, and first and last names
        data = cur.execute("SELECT * FROM managers")
        manager_ids = []
        for tup in data:
            manager_id = str(tup[0])
            manager_name = tup[1] + " " + tup[2]
            manager_ids.append(manager_id)
            print(f"{manager_id} - {manager_name}")
        # Choose which manager to edit
        manager_to_edit = str(input("Enter the manager ID of the manager to edit: "))
        while (manager_to_edit not in manager_ids):
            manager_to_edit = str(input("Invalid input. Please enter a valid manager ID: "))
        # Enter the manager's new first and last name
        new_manager_first = input("Enter the manager's new first name: ")
        new_manager_last = input("Enter the manager's new last name: ")
        # Update manager with new first and last names
        cur.execute(f"UPDATE managers SET First_Name = '{new_manager_first}', Last_Name = '{new_manager_last}' WHERE Manager_ID = '{manager_to_edit}';")
        conn.commit()
        edit_managers(conn, cur)
        return

    # Return to managers
    else:
        managers(conn, cur)
    return