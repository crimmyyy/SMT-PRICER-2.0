import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os

# Function to find or create the path to items.json in the user's Desktop directory
def get_json_file_path():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "SMT Pricer GUI")
    os.makedirs(desktop_path, exist_ok=True)
    return os.path.join(desktop_path, "items.json")

# Load items from the JSON file
def load_items():
    json_file_path = get_json_file_path()
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            return json.load(f)
    return []

# Save an item to the JSON file
def save_item(name, market_price, final_price):
    json_file_path = get_json_file_path()
    items = load_items()
    items.append({"Name": name, "Market Value": market_price, "Final Price": final_price})
    with open(json_file_path, 'w') as f:
        json.dump(items, f, indent=4)

# Display items list in a new window with a red border
def show_list():
    items = load_items()
    
    # Create a new Toplevel window with a red border frame
    list_window = tk.Toplevel(root)
    list_window.title("Items List")
    list_window.configure(bg="red")  # Set window border color
    
    # Add a content frame with padding inside the red border
    content_frame = tk.Frame(list_window, bg="white", padx=5, pady=5)
    content_frame.pack(padx=5, pady=5)
    
    list_frame = tk.Frame(content_frame, bg="white")
    list_frame.pack()

    columns = ('Item Name', 'Market Price', 'New Price')
    tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=len(items))
    tree.heading('Item Name', text='Item Name')
    tree.heading('Market Price', text='Market Price')
    tree.heading('New Price', text='New Price')
    tree.column('Item Name', anchor='center', width=200)
    tree.column('Market Price', anchor='center', width=150)
    tree.column('New Price', anchor='center', width=150)

    # Insert items into the table with dollar symbols
    for item in items:
        market_value = f"${item['Market Value']:.2f}"
        final_price = f"${item['Final Price']:.2f}"
        tree.insert('', tk.END, values=(item['Name'], market_value, final_price))

    tree.pack(fill='both', expand=True)

    # Set font size for headers to 16 pt
    style = ttk.Style()
    style.configure('Treeview', font=('Arial', 20), foreground='black', background='white', rowheight=30, fieldbackground='white')
    style.configure('Treeview.Heading', font=('Arial', 16, 'bold'), foreground='black')  # Reduced to 16 pt
    style.map('Treeview.Heading', background=[('active', '#f7e3d4')], foreground=[('active', 'black')])

# Calculate new price and add the item to the JSON file
def calculate_price():
    item_name = item_name_entry.get()
    try:
        market_price = float(market_price_entry.get())
        final_price = market_price * 2
        save_item(item_name, market_price, final_price)
        messagebox.showinfo("Success", f"Item '{item_name}' added with New Price: ${final_price:.2f}")
        item_name_entry.delete(0, tk.END)
        market_price_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number for the market price.")

# Find and load the image
def load_image():
    for root_dir, _, files in os.walk(os.path.expanduser("~")):
        if 'Images' in root_dir and 'SMTLogo.jpg' in files:
            return os.path.join(root_dir, 'SMTLogo.jpg')
    return None

def display_image():
    image_path = load_image()
    if image_path:
        img = Image.open(image_path)
        img = img.resize((200, 150), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk
    else:
        messagebox.showerror("File Not Found", "SMTLogo.jpg not found in Images folder.")

# Initialize main window with a red border frame
root = tk.Tk()
root.title("Item Price Calculator")
root.configure(bg="red")  # Set window border color

# Add a content frame with padding inside the red border
content_frame = tk.Frame(root, bg="grey", padx=5, pady=5)
content_frame.pack(padx=5, pady=5)

# Image Display Area
image_label = tk.Label(content_frame, bg="grey")
image_label.pack(pady=10)

# Load the image immediately when the program starts
display_image()

# Item Name Entry
tk.Label(content_frame, text="Item Name:", bg="grey").pack()
item_name_entry = tk.Entry(content_frame)
item_name_entry.pack()

# Market Price Entry
tk.Label(content_frame, text="Market Price:", bg="grey").pack()
market_price_entry = tk.Entry(content_frame)
market_price_entry.pack()

new_price_label = tk.Label(content_frame, text="New Price: ", bg="grey")
new_price_label.pack()

calculate_button = tk.Button(content_frame, text="Calculate New Price", command=calculate_price)
calculate_button.pack(pady=10)

show_list_button = tk.Button(content_frame, text="Show List", command=show_list)
show_list_button.pack(pady=10)

root.mainloop()
