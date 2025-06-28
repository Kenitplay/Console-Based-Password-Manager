import requests
from getpass import getpass

SERVER = input("Enter server IP (e.g. 192.168.1.11): ").strip()
BASE_URL = f"http://{SERVER}:5000"

def show_menu():
    while True:
        print("\n=== Password Manager ===")
        print("1. View credentials")
        print("2. Add credential")
        print("3. Update credential")
        print("4. Delete credential")
        print("5. Exit")
        choice = input("Select: ").strip()

        if choice == "1":
            try:
                res = requests.get(f"{BASE_URL}/credentials")
                res.raise_for_status()
                creds = res.json()
                if not creds:
                    print("📭 No credentials saved.")
                    continue
                print("\nSaved Credentials:")
                for i, c in enumerate(creds, 1):
                    print(f"{i}. {c['site']} - {c['username']}")
                sel = input("Reveal which? (number or blank to cancel): ").strip()
                if not sel.isdigit():
                    continue
                index = int(sel) - 1
                if 0 <= index < len(creds):
                    selected = creds[index]
                    print("\nDetails:")
                    print(f"Site:     {selected['site']}")
                    print(f"Username: {selected['username']}")
                    print(f"Password: {selected['password']}")
                    print(f"Hash:     {selected['hash']}")
                else:
                    print("Invalid selection.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            site = input("Site: ")
            username = input("Username: ")
            password = getpass("Password: ")
            try:
                res = requests.post(f"{BASE_URL}/credentials", json={
                    "site": site,
                    "username": username,
                    "password": password
                })
                res.raise_for_status()
                print(res.json().get("message", "Unknown response"))
            except Exception as e:
                print(f"Failed to add. Error: {e}")

        elif choice == "3":
            cred_id = input("ID to update: ").strip()
            site = input("New Site (blank to skip): ")
            username = input("New Username (blank to skip): ")
            password = getpass("New Password (blank to skip): ")
            data = {}
            if site: data['site'] = site
            if username: data['username'] = username
            if password: data['password'] = password
            try:
                res = requests.put(f"{BASE_URL}/credentials/{cred_id}", json=data)
                res.raise_for_status()
                print(res.json().get("message", "Unknown response"))
            except Exception as e:
                print(f"Failed to update. Error: {e}")

        elif choice == "4":
            cred_id = input("ID to delete: ")
            try:
                res = requests.delete(f"{BASE_URL}/credentials/{cred_id}")
                res.raise_for_status()
                print(res.json().get("message", "Unknown response"))
            except Exception as e:
                print(f"Failed to delete. Error: {e}")

        elif choice == "5":
            break
        else:
            print("Invalid choice.")

if _name_ == "_main_":
    show_menu()
