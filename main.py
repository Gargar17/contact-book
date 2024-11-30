import tkinter as tk
from tkinter import messagebox
import csv
import json
import os

class ContactBookApp:
    def __init__(self, root, filename="contacts.json", file_format="json"):
        self.root = root
        self.root.title("Contact Book")
        self.filename = filename
        self.file_format = file_format
        self.contacts = self.load_contacts()

        # Set the color theme: Gold and Black
        self.bg_color = "#000000"  # Black background
        self.fg_color = "#FFD700"  # Gold color for text
        self.button_bg_color = "#FFD700"  # Gold button background
        self.button_fg_color = "#000000"  # Black text on buttons
        self.entry_bg_color = "#333333"  # Dark grey for entry fields
        self.entry_fg_color = "#FFD700"  # Gold text in entry fields

        # Configure the root window
        self.root.config(bg=self.bg_color)

        # GUI Widgets with gold and black theme
        self.name_label = tk.Label(root, text="Name:", bg=self.bg_color, fg=self.fg_color, font=("Arial", 12))
        self.name_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.name_entry = tk.Entry(root, bg=self.entry_bg_color, fg=self.entry_fg_color, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.phone_label = tk.Label(root, text="Phone:", bg=self.bg_color, fg=self.fg_color, font=("Arial", 12))
        self.phone_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.phone_entry = tk.Entry(root, bg=self.entry_bg_color, fg=self.entry_fg_color, font=("Arial", 12))
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10)

        self.email_label = tk.Label(root, text="Email:", bg=self.bg_color, fg=self.fg_color, font=("Arial", 12))
        self.email_label.grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.email_entry = tk.Entry(root, bg=self.entry_bg_color, fg=self.entry_fg_color, font=("Arial", 12))
        self.email_entry.grid(row=2, column=1, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add Contact", command=self.add_contact, bg=self.button_bg_color, fg=self.button_fg_color, font=("Arial", 12))
        self.add_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.search_label = tk.Label(root, text="Search:", bg=self.bg_color, fg=self.fg_color, font=("Arial", 12))
        self.search_label.grid(row=4, column=0, sticky="e", padx=10, pady=10)
        self.search_entry = tk.Entry(root, bg=self.entry_bg_color, fg=self.entry_fg_color, font=("Arial", 12))
        self.search_entry.grid(row=4, column=1, padx=10, pady=10)

        self.search_button = tk.Button(root, text="Search", command=self.search_contact, bg=self.button_bg_color, fg=self.button_fg_color, font=("Arial", 12))
        self.search_button.grid(row=5, column=0, columnspan=2, pady=20)

        self.contacts_listbox = tk.Listbox(root, width=50, height=10, font=("Arial", 12))
        self.contacts_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

        self.edit_button = tk.Button(root, text="Edit Contact", command=self.edit_contact, bg=self.button_bg_color, fg=self.button_fg_color, font=("Arial", 12))
        self.edit_button.grid(row=7, column=0, pady=10)

        self.delete_button = tk.Button(root, text="Delete Contact", command=self.delete_contact, bg=self.button_bg_color, fg=self.button_fg_color, font=("Arial", 12))
        self.delete_button.grid(row=7, column=1, pady=10)

    def load_contacts(self):
        """Load contacts from a CSV or JSON file."""
        if not os.path.exists(self.filename):
            return []

        if self.file_format == "csv":
            return self.load_from_csv()
        elif self.file_format == "json":
            return self.load_from_json()

    def load_from_csv(self):
        contacts = []
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                contacts.append(row)
        return contacts

    def load_from_json(self):
        with open(self.filename, 'r') as file:
            return json.load(file)

    def save_contacts(self):
        """Save contacts to a file (CSV or JSON)."""
        if self.file_format == "csv":
            self.save_to_csv()
        elif self.file_format == "json":
            self.save_to_json()

    def save_to_csv(self):
        """Save contacts to a CSV file."""
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["name", "phone", "email"])
            writer.writeheader()
            for contact in self.contacts:
                writer.writerow(contact)

    def save_to_json(self):
        """Save contacts to a JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.contacts, file, indent=4)

    def add_contact(self):
        """Add a new contact."""
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if name and phone and email:
            self.contacts.append({"name": name, "phone": phone, "email": email})
            self.save_contacts()
            self.refresh_listbox()
        else:
            messagebox.showwarning("Input Error", "All fields must be filled!")

    def search_contact(self):
        """Search for a contact by name or phone."""
        search_term = self.search_entry.get().lower()
        result = []
        for contact in self.contacts:
            if search_term in contact['name'].lower() or search_term in contact['phone']:
                result.append(contact)

        self.contacts_listbox.delete(0, tk.END)
        for contact in result:
            self.contacts_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']} - {contact['email']}")

    def edit_contact(self):
        """Edit the selected contact."""
        selected_contact = self.contacts_listbox.curselection()
        if selected_contact:
            index = selected_contact[0]
            contact = self.contacts[index]
            new_name = self.name_entry.get()
            new_phone = self.phone_entry.get()
            new_email = self.email_entry.get()

            if new_name and new_phone and new_email:
                contact['name'] = new_name
                contact['phone'] = new_phone
                contact['email'] = new_email
                self.save_contacts()
                self.refresh_listbox()
            else:
                messagebox.showwarning("Input Error", "All fields must be filled!")
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to edit.")

    def delete_contact(self):
        """Delete the selected contact."""
        selected_contact = self.contacts_listbox.curselection()
        if selected_contact:
            index = selected_contact[0]
            del self.contacts[index]
            self.save_contacts()
            self.refresh_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")

    def refresh_listbox(self):
        """Refresh the listbox to display all contacts."""
        self.contacts_listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.contacts_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']} - {contact['email']}")

# Main function to start the app
def main():
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
