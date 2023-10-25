---
layout: post
title: License管理器应用
date: 2023-10-16 23:00+0800
description: 
tags: license
giscus_comments: true
categories: icenv
---

读取License文件，并存入sqlite3数据库。
```python3
#!/Users/wanlinwang/spack/opt/spack/darwin-ventura-m1/apple-clang-14.0.3/python-3.10.8-b7rgkczw4yfgrkbgttbcbur3ksmwho5d/bin/python3


import sqlite3
import re
import argparse

def parse_license_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
        start_index = content.find("##     PRODUCT TO FEATURE MAPPING")
        products_data = content[start_index:].split("# Product Id  :")

    products = []
    for product_data in products_data[1:]:
        product = {}
        product['id'] = product_data.split(",")[0].strip()
        product['name'] = re.search(r'Product Name: (.+)', product_data).group(1).strip()
        product['version'] = re.search(r'\[Version: (.+?)\]', product_data).group(1).strip()
        product['features'] = re.findall(r'Feature: (.+?)\s*\[', product_data)
        product['dates'] = re.findall(r'Start Date: (.+?) Exp Date: (.+?)\s*Product Qty: (\d+)', product_data)
        products.append(product)
    return products

def store_to_db(products, filename):
    conn = sqlite3.connect('license.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS LicenseFiles
                     (LicenseFileId INTEGER PRIMARY KEY AUTOINCREMENT, FileName TEXT UNIQUE, hostname TEXT, hostid TEXT, lmgrd_port TEXT, vendor_daemon_port TEXT, lmgrd_file_id INTEGER, vendor_daemon_file_id INTEGER, options_file_id INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO LicenseFiles (FileName) VALUES (?)", (filename,))
    cursor.execute("SELECT LicenseFileId FROM LicenseFiles WHERE FileName=?", (filename,))
    license_file_id = cursor.fetchone()[0]

    cursor.execute('''CREATE TABLE IF NOT EXISTS LicenseRelatedFiles
                     (ExecutableFileId INTEGER PRIMARY KEY AUTOINCREMENT, FileName TEXT UNIQUE)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Features
                     (FeatureId INTEGER PRIMARY KEY AUTOINCREMENT, FeatureName TEXT UNIQUE)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Products
                     (ProductId TEXT PRIMARY KEY, ProductName TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ProductFeatureRelation
                     (RelationId INTEGER PRIMARY KEY AUTOINCREMENT, ProductId TEXT, FeatureId INTEGER, 
                     FOREIGN KEY(ProductId) REFERENCES Products(ProductId), 
                     FOREIGN KEY(FeatureId) REFERENCES Features(FeatureId))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ProductDates
                     (DateId INTEGER PRIMARY KEY AUTOINCREMENT, ProductId TEXT, StartDate DATE, EndDate DATE, Version TEXT, Quantity INTEGER, LicenseFileId INTEGER,
                     FOREIGN KEY(ProductId) REFERENCES Products(ProductId),
                     FOREIGN KEY(LicenseFileId) REFERENCES LicenseFiles(LicenseFileId))''')

    for product in products:
        cursor.execute("INSERT OR REPLACE INTO Products (ProductId, ProductName) VALUES (?, ?)", (product['id'], product['name']))

        for feature in product['features']:
            cursor.execute("INSERT OR IGNORE INTO Features (FeatureName) VALUES (?)", (feature,))
            cursor.execute("SELECT FeatureId FROM Features WHERE FeatureName=?", (feature,))
            feature_id = cursor.fetchone()[0]
            
            cursor.execute("SELECT 1 FROM ProductFeatureRelation WHERE ProductId=? AND FeatureId=?", (product['id'], feature_id))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO ProductFeatureRelation (ProductId, FeatureId) VALUES (?, ?)", (product['id'], feature_id))
        
        for start_date, end_date, quantity in product['dates']:
            cursor.execute("SELECT 1 FROM ProductDates WHERE ProductId=? AND StartDate=? AND EndDate=? AND Version=? AND LicenseFileId=?", (product['id'], start_date, end_date, product['version'], license_file_id))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO ProductDates (ProductId, StartDate, EndDate, Version, Quantity, LicenseFileId) VALUES (?, ?, ?, ?, ?, ?)", (product['id'], start_date, end_date, product['version'], quantity, license_file_id))

    conn.commit()
    conn.close()

def main():
    parser = argparse.ArgumentParser(description="Process License Files and Store to Database")
    parser.add_argument('license_files', metavar='N', type=str, nargs='+', help='License file(s) to process')
    
    args = parser.parse_args()

    for filename in args.license_files:
        products = parse_license_file(filename)
        store_to_db(products, filename)

if __name__ == "__main__":
    main()

```

读取sqlite3数据库，并显示在客户端内，
```python3
#!/home/centos/spack/opt/spack/linux-centos7-x86_64_v4/gcc-13.2.0/python-3.10.10-64a4t27o3c2cnk23lenooydikdsiqzgv/bin/python3


import sqlite3
import tkinter as tk
from tkinter import ttk
from contextlib import contextmanager
import tkinter.messagebox
from datetime import datetime, timedelta
from collections import defaultdict

def get_row_color(start_date, end_date):
    current_date = datetime.now().date()
    end_date_obj = datetime.strptime(end_date, "%d-%b-%Y").date()

    if end_date_obj < current_date:
        return "light gray"
    elif current_date <= end_date_obj <= (current_date + timedelta(days=14)):
        return "red"
    else:
        return "black"

@contextmanager
def get_db_connection():
    conn = sqlite3.connect('license.db')
    try:
        yield conn
    finally:
        conn.close()

def execute_query(query, params=()):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def execute_commit(query, params=()):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

def retrieve_license_info_by_feature(feature_name):
    query = """
    SELECT pd.StartDate, pd.EndDate, pd.Quantity, lf.FileName, p.ProductId
    FROM ProductDates pd
    JOIN Products p ON pd.ProductId = p.ProductId
    JOIN ProductFeatureRelation pfr ON p.ProductId = pfr.ProductId
    JOIN Features f ON pfr.FeatureId = f.FeatureId
    JOIN LicenseFiles lf ON pd.LicenseFileId = lf.LicenseFileId
    WHERE f.FeatureName = ?
    """
    return execute_query(query, (feature_name,))

def retrieve_license_info_by_product(product_id):
    query = """
    SELECT pd.StartDate, pd.EndDate, pd.Quantity, lf.FileName, p.ProductId
    FROM ProductDates pd
    JOIN Products p ON pd.ProductId = p.ProductId
    JOIN LicenseFiles lf ON pd.LicenseFileId = lf.LicenseFileId
    WHERE p.ProductId = ?
    """
    return execute_query(query, (product_id,))

def get_all_features():
    return [row[0] for row in execute_query("SELECT FeatureName FROM Features")]

def get_all_products():
    return [row[0] for row in execute_query("SELECT ProductId FROM Products")]

def get_all_license_files():
    return [row[0] for row in execute_query("SELECT FileName FROM LicenseFiles")]

def get_all_license_related_files():
    return [row[0] for row in execute_query("SELECT FileName FROM LicenseRelatedFiles")]

def on_search_by_feature():
    tree_by_feature.delete(*tree_by_feature.get_children())  # Clear the treeview
    feature_name = feature_name_combobox.get()
    results = retrieve_license_info_by_feature(feature_name)
    sorted_results = sorted(results, key=lambda x: datetime.strptime(x[1], "%d-%b-%Y"))
    for result in sorted_results:
        color = get_row_color(result[0], result[1])
        tree_by_feature.insert("", "end", values=result, tags=(color,))
        tree_by_feature.tag_configure(color, foreground=color)


def on_search_by_product():
    tree_by_product.delete(*tree_by_product.get_children())  # Clear the treeview
    product_id = product_id_combobox.get()
    results = retrieve_license_info_by_product(product_id)
    sorted_results = sorted(results, key=lambda x: datetime.strptime(x[1], "%d-%b-%Y"))
    for result in sorted_results:
        color = get_row_color(result[0], result[1])
        tree_by_product.insert("", "end", values=result, tags=(color,))
        tree_by_product.tag_configure(color, foreground=color)

def load_license_info(event):
    data = execute_query("SELECT hostname, hostid, lmgrd_port, vendor_daemon_port, lmgrd_file_id, vendor_daemon_file_id, options_file_id FROM LicenseFiles WHERE FileName=?", (license_file_combobox.get(),))
    if data:
        data = data[0]
        
        hostname_entry.delete(0, tk.END)
        hostid_entry.delete(0, tk.END)
        lmgrd_port_entry.delete(0, tk.END)
        vendor_daemon_port_entry.delete(0, tk.END)

        # Clear all entries and comboboxes first
        hostname_entry.delete(0, tk.END)
        hostid_entry.delete(0, tk.END)
        lmgrd_port_entry.delete(0, tk.END)
        vendor_daemon_port_entry.delete(0, tk.END)
        lmgrd_file_combobox.set('')
        vendor_daemon_file_combobox.set('')
        options_file_combobox.set('')

        if data:
            if data[0]:
                hostname_entry.insert(0, data[0])
            if data[1]:
                hostid_entry.insert(0, data[1])
            if data[2]:
                lmgrd_port_entry.insert(0, data[2])
            if data[3]:
                vendor_daemon_port_entry.insert(0, data[3])
            if data[4]:
                lmgrd_file = execute_query("SELECT FileName FROM LicenseRelatedFiles WHERE ExecutableFileId=?", (data[4],))
                if lmgrd_file:
                    lmgrd_file = lmgrd_file[0]
                    lmgrd_file_combobox.set(lmgrd_file)
            if data[5]:
                vendor_daemon_file = execute_query("SELECT FileName FROM LicenseRelatedFiles WHERE ExecutableFileId=?", (data[5],))
                if vendor_daemon_file:
                    vendor_daemon_file = vendor_daemon_file[0]
                    vendor_daemon_file_combobox.set(vendor_daemon_file)
            if data[6]:
                options_file = execute_query("SELECT FileName FROM LicenseRelatedFiles WHERE ExecutableFileId=?", (data[6],))
                if options_file:
                    options_file = options_file[0]
                    options_file_combobox.set(options_file)

        if (not hostname_entry.get() and not lmgrd_port_entry.get() and not vendor_daemon_port_entry.get() and not lmgrd_file_combobox.get() and not vendor_daemon_file_combobox.get() and not options_file_combobox.get()):
            copy_from_prev_button['state'] = tk.NORMAL
        else:
            copy_from_prev_button['state'] = tk.DISABLED

def check_inputs_filled():
    # Check if all required fields are filled
    if (license_file_combobox.get() and hostname_entry.get() and hostid_entry.get() and lmgrd_port_entry.get() and lmgrd_file_combobox.get() and vendor_daemon_file_combobox.get()):
        save_button['state'] = tk.NORMAL
        modify_button['state'] = tk.NORMAL
    else:
        save_button['state'] = tk.DISABLED
        modify_button['state'] = tk.DISABLED

def copy_from_previous_file():
    license_file_name = license_file_combobox.get()
    if not license_file_name:
        tkinter.messagebox.showerror("Error", "Please select a License File first.")
        return

    # Extract hostid from the license file's filename
    try:
        hostid = license_file_name.split('_')[2]
    except IndexError:
        tkinter.messagebox.showerror("Error", "Invalid License File name format.")
        return

    data = execute_query("SELECT hostname, lmgrd_port, vendor_daemon_port, lmgrd_file_id, vendor_daemon_file_id, options_file_id FROM LicenseFiles WHERE hostid=? ORDER BY LicenseFileId DESC LIMIT 1", (hostid,))
    if data:
        data = data[0]
    else:
        tkinter.messagebox.showinfo("Info", "No previous data found for the given Host ID.")
        return

    hostname, lmgrd_port, vendor_daemon_port, lmgrd_file_id, vendor_daemon_file_id, options_file_id = data

    # Populate the fields
    hostname_entry.delete(0, tk.END)
    hostname_entry.insert(0, hostname)

    hostid_entry.delete(0, tk.END)
    hostid_entry.insert(0, hostid)

    lmgrd_port_entry.delete(0, tk.END)
    lmgrd_port_entry.insert(0, lmgrd_port)

    vendor_daemon_port_entry.delete(0, tk.END)
    vendor_daemon_port_entry.insert(0, vendor_daemon_port)

    # Fetch filenames for the file IDs
    lmgrd_file = execute_query("SELECT FileName FROM LicenseRelatedFiles WHERE ExecutableFileId=?", (lmgrd_file_id,))
    if lmgrd_file:
        lmgrd_file = lmgrd_file[0]
        lmgrd_file_combobox.set(lmgrd_file)
    vendor_daemon_file = execute_query("SELECT FileName FROM LicenseRelatedFiles WHERE ExecutableFileId=?", (vendor_daemon_file_id,))
    if vendor_daemon_file:
        vendor_daemon_file = vendor_daemon_file[0]
        vendor_daemon_file_combobox.set(vendor_daemon_file)

    if options_file_id:
        options_file = execute_query("SELECT FileName FROM LicenseRelatedFiles WHERE ExecutableFileId=?", (options_file_id,))
        if options_file:
            options_file = options_file[0]
            options_file_combobox.set(options_file)

    # Enable the "Copy From Previous File" button only when the other fields are empty
    if not hostname_entry.get() and not lmgrd_port_entry.get() and not vendor_daemon_port_entry.get():
        copy_from_prev_button['state'] = tk.NORMAL
    else:
        copy_from_prev_button['state'] = tk.DISABLED

def save_license_info():
    license_file_id = execute_query("SELECT LicenseFileId FROM LicenseFiles WHERE FileName=?", (license_file_combobox.get(),))
    if license_file_id:
        license_file_id = license_file_id[0]
        
        lmgrd_file = lmgrd_file_combobox.get()
        vendor_daemon_file = vendor_daemon_file_combobox.get()
        options_file = options_file_combobox.get()

        update_sub_str_list = []
        insert_sub_str_list = []
        value_sub_str_list = []
        if lmgrd_file:
            execute_commit("INSERT OR IGNORE INTO LicenseRelatedFiles (FileName) VALUES (?)", (lmgrd_file,))
            lmgrd_file_id = execute_query("SELECT ExecutableFileId FROM LicenseRelatedFiles WHERE FileName=?", (lmgrd_file,))
            if lmgrd_file_id:
                lmgrd_file_id = lmgrd_file_id[0][0]
                update_sub_str_list.append("lmgrd_file_id=?")
                insert_sub_str_list.append("lmgrd_file_id")
                value_sub_str_list.append(lmgrd_file_id)

        if vendor_daemon_file:
            execute_commit("INSERT OR IGNORE INTO LicenseRelatedFiles (FileName) VALUES (?)", (vendor_daemon_file,))
            vendor_daemon_file_id = execute_query("SELECT ExecutableFileId FROM LicenseRelatedFiles WHERE FileName=?", (vendor_daemon_file,))
            if vendor_daemon_file_id:
                vendor_daemon_file_id = vendor_daemon_file_id[0][0]
                update_sub_str_list.append("vendor_daemon_file_id=?")
                insert_sub_str_list.append("vendor_daemon_file_id")
                value_sub_str_list.append(vendor_daemon_file_id)

        if options_file:
            # Check if options_file exists.
            execute_commit("INSERT OR IGNORE INTO LicenseRelatedFiles (FileName) VALUES (?)", (options_file,))
            options_file_id = execute_query("SELECT ExecutableFileId FROM LicenseRelatedFiles WHERE FileName=?", (options_file,))
            if options_file_id:
                options_file_id = options_file_id[0][0]
                update_sub_str_list.append("options_file_id=?")
                insert_sub_str_list.append("options_file_id")
                value_sub_str_list.append(options_file_id)

        if license_file_id:
            # Update the existing record
            #cursor.execute("UPDATE LicenseFiles SET hostname=?, hostid=?, lmgrd_port=?, vendor_daemon_port=?, lmgrd_file_id=?, vendor_daemon_file_id=?, options_file_id=? WHERE LicenseFileId=?", 
            #               (hostname_entry.get(), hostid_entry.get(), lmgrd_port_entry.get(), vendor_daemon_port_entry.get(), lmgrd_file_id, vendor_daemon_file_id, options_file_id, license_file_id[0]))
            if lmgrd_file or vendor_daemon_file or options_file:
                param = (
                    hostname_entry.get(), 
                    hostid_entry.get(), 
                    lmgrd_port_entry.get(), 
                    vendor_daemon_port_entry.get(), 
                    *value_sub_str_list, 
                    license_file_id[0]
                )
                execute_commit(f"UPDATE LicenseFiles SET hostname=?, hostid=?, lmgrd_port=?, vendor_daemon_port=?, {','.join(update_sub_str_list)} WHERE LicenseFileId=?", param)
            else:
                execute_commit("UPDATE LicenseFiles SET hostname=?, hostid=?, lmgrd_port=?, vendor_daemon_port=? WHERE LicenseFileId=?", 
                               (hostname_entry.get(), hostid_entry.get(), lmgrd_port_entry.get(), vendor_daemon_port_entry.get(), license_file_id[0]))
        else:
            # Insert a new record
            #cursor.execute("INSERT INTO LicenseFiles (FileName, hostname, hostid, lmgrd_port, vendor_daemon_port, lmgrd_file_id, vendor_daemon_file_id, options_file_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
            #               (license_file_combobox.get(), hostname_entry.get(), hostid_entry.get(), lmgrd_port_entry.get(), vendor_daemon_port_entry.get(), lmgrd_file_id, vendor_daemon_file_id, options_file_id))
            if lmgrd_file or vendor_daemon_file or options_file:
                param = (
                    license_file_combobox.get(),
                    hostname_entry.get(), 
                    hostid_entry.get(), 
                    lmgrd_port_entry.get(), 
                    vendor_daemon_port_entry.get(), 
                    *value_sub_str_list
                )
                execute_commit(f"INSERT INTO LicenseFiles (FileName, hostname, hostid, lmgrd_port, vendor_daemon_port, {','.join(insert_sub_str_list)}) VALUES (?, ?, ?, ?, ?, {','.join(['?'] * len(insert_sub_str_list))})", param)
            else:
                execute_commit("INSERT INTO LicenseFiles (FileName, hostname, hostid, lmgrd_port, vendor_daemon_port, lmgrd_file_id, vendor_daemon_file_id, options_file_id) VALUES (?, ?, ?, ?, ?)", 
                               (license_file_combobox.get(), hostname_entry.get(), hostid_entry.get(), lmgrd_port_entry.get(), vendor_daemon_port_entry.get()))
        
        #conn.commit()
        # Disable "Save" button after saved.
        save_button['state'] = tk.DISABLED
        tk.messagebox.showinfo("Info", "License file config saved successfully!")

app = tk.Tk()
app.title("License Manager")

notebook = ttk.Notebook(app)
notebook.pack(pady=10, padx=10, expand=True, fill='both')

# Tab for Feature Name
tab_feature = ttk.Frame(notebook)
notebook.add(tab_feature, text="By Feature Name")

feature_names = get_all_features()
ttk.Label(tab_feature, text="Feature Name:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
feature_name_combobox = ttk.Combobox(tab_feature, values=feature_names, width=30)
feature_name_combobox.grid(row=0, column=1, pady=5, padx=5)
ttk.Button(tab_feature, text="Search", command=on_search_by_feature).grid(row=0, column=2, pady=5, padx=5)

tree_by_feature = ttk.Treeview(tab_feature, columns=("StartDate", "EndDate", "Quantity", "FileName", "ProductId"), show="headings")
tree_by_feature.heading("StartDate", text="Start Date")
tree_by_feature.heading("EndDate", text="End Date")
tree_by_feature.heading("Quantity", text="Quantity")
tree_by_feature.heading("FileName", text="License File")
tree_by_feature.heading("ProductId", text="Product Id")
tree_by_feature.grid(row=1, column=0, columnspan=3, pady=10, padx=5, sticky=(tk.W, tk.E))

# Tab for Product Id
tab_product = ttk.Frame(notebook)
notebook.add(tab_product, text="By Product Id")

product_ids = get_all_products()
ttk.Label(tab_product, text="Product Id:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
product_id_combobox = ttk.Combobox(tab_product, values=product_ids, width=30)
product_id_combobox.grid(row=0, column=1, pady=5, padx=5)
ttk.Button(tab_product, text="Search", command=on_search_by_product).grid(row=0, column=2, pady=5, padx=5)

tree_by_product = ttk.Treeview(tab_product, columns=("StartDate", "EndDate", "Quantity", "FileName", "ProductId"), show="headings")
tree_by_product.heading("StartDate", text="Start Date")
tree_by_product.heading("EndDate", text="End Date")
tree_by_product.heading("Quantity", text="Quantity")
tree_by_product.heading("FileName", text="License File")
tree_by_product.heading("ProductId", text="Product Id")
tree_by_product.grid(row=1, column=0, columnspan=3, pady=10, padx=5, sticky=(tk.W, tk.E))

# Tab for License Settings
tab_settings = ttk.Frame(notebook)
notebook.add(tab_settings, text="License Settings")

license_files = get_all_license_files()
ttk.Label(tab_settings, text="License File:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
license_file_combobox = ttk.Combobox(tab_settings, values=license_files, width=64)
license_file_combobox.grid(row=0, column=1, pady=5, padx=5)
license_file_combobox.bind("<<ComboboxSelected>>", load_license_info)

ttk.Label(tab_settings, text="Hostname:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
hostname_entry = ttk.Entry(tab_settings, width=64)
hostname_entry.grid(row=1, column=1, pady=5, padx=5)

ttk.Label(tab_settings, text="Host ID:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
hostid_entry = ttk.Entry(tab_settings, width=64)
hostid_entry.grid(row=2, column=1, pady=5, padx=5)

ttk.Label(tab_settings, text="Lmgrd Port:").grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
lmgrd_port_entry = ttk.Entry(tab_settings, width=64)
lmgrd_port_entry.grid(row=3, column=1, pady=5, padx=5)

ttk.Label(tab_settings, text="Vendor Daemon Port:").grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
vendor_daemon_port_entry = ttk.Entry(tab_settings, width=64)
vendor_daemon_port_entry.grid(row=4, column=1, pady=5, padx=5)

license_related_files = get_all_license_related_files()
ttk.Label(tab_settings, text="LMGRD FILE:").grid(row=5, column=0, sticky=tk.W, pady=5, padx=5)
lmgrd_file_combobox = ttk.Combobox(tab_settings, values=license_related_files, width=64)
lmgrd_file_combobox.grid(row=5, column=1, pady=5, padx=5)

ttk.Label(tab_settings, text="VENDOR DAEMON FILE:").grid(row=6, column=0, sticky=tk.W, pady=5, padx=5)
vendor_daemon_file_combobox = ttk.Combobox(tab_settings, values=license_related_files, width=64)
vendor_daemon_file_combobox.grid(row=6, column=1, pady=5, padx=5)

ttk.Label(tab_settings, text="OPTIONS FILE:").grid(row=7, column=0, sticky=tk.W, pady=5, padx=5)
options_file_combobox = ttk.Combobox(tab_settings, values=license_related_files, width=64)
options_file_combobox.grid(row=7, column=1, pady=5, padx=5)

# Bind the check_inputs_filled function to the inputs
hostname_entry.bind("<KeyRelease>", lambda e: check_inputs_filled())
hostid_entry.bind("<KeyRelease>", lambda e: check_inputs_filled())
lmgrd_port_entry.bind("<KeyRelease>", lambda e: check_inputs_filled())
vendor_daemon_port_entry.bind("<KeyRelease>", lambda e: check_inputs_filled())
lmgrd_file_combobox.bind("<<ComboboxSelected>>", lambda e: check_inputs_filled())
vendor_daemon_file_combobox.bind("<<ComboboxSelected>>", lambda e: check_inputs_filled())
options_file_combobox.bind("<<ComboboxSelected>>", lambda e: check_inputs_filled())

save_button = ttk.Button(tab_settings, text="Save to DB", command=save_license_info, state=tk.DISABLED)
save_button.grid(row=8, column=1, pady=10, padx=5, sticky=tk.E)

copy_from_prev_button = ttk.Button(tab_settings, text="Copy From Previous File", command=copy_from_previous_file, state=tk.DISABLED)
copy_from_prev_button.grid(row=9, column=1, pady=10, padx=5, sticky=tk.W)

def modify_license_file():
    license_file = license_file_combobox.get()
    hostname = hostname_entry.get()
    hostid = hostid_entry.get()
    lmgrd_port = lmgrd_port_entry.get()
    vendor_daemon_port = vendor_daemon_port_entry.get()
    vendor_daemon_file = vendor_daemon_file_combobox.get()
    options_file = options_file_combobox.get()

    with open(license_file, 'r') as f:
        lines = f.readlines()

    modified = False
    for i, line in enumerate(lines):
        if line.startswith("SERVER"):
            if line != f"SERVER {hostname} {hostid} {lmgrd_port}\n":
                lines[i] = f"SERVER {hostname} {hostid} {lmgrd_port}\n"
                modified = True
        elif line.startswith("DAEMON"):
            daemon_line = f"DAEMON cdslmd {vendor_daemon_file}"
            if options_file:
                daemon_line = daemon_line + f" OPTIONS={options_file}"
            if vendor_daemon_port:
                daemon_line = daemon_line + f" PORT={vendor_daemon_port}"
            if options_file and line != f"{daemon_line}\n":
                lines[i] = f"{daemon_line}\n"
                modified = True

    if modified:
        with open(license_file, 'w') as f:
            f.writelines(lines)
        tk.messagebox.showinfo("Info", "License file modified successfully!")
    else:
        tk.messagebox.showinfo("Info", "License file is already up-to-date!")

    # Disable modify_button
    modify_button['state'] = tk.DISABLED

# 在License Settings tab中添加Modify按钮
modify_button = ttk.Button(tab_settings, text="Modify Lic File", command=modify_license_file, state=tk.DISABLED)
modify_button.grid(row=9, column=1, pady=10, padx=5, sticky=tk.E)

# 比较两个License文件差异
def compare_license_files():
    file1 = license_file_combobox1.get()
    file2 = license_file_combobox2.get()

    if not file1 or not file2:
        tk.messagebox.showerror("Error", "Please select both license files.")
        return

    data1 = retrieve_license_info_by_file(file1)
    data2 = retrieve_license_info_by_file(file2)

    # Convert data to a dictionary with product_id as key and list of date ranges as values
    dict1 = defaultdict(list)
    dict2 = defaultdict(list)

    for item in data1:
        dict1[item[4]].append(item)
    for item in data2:
        dict2[item[4]].append(item)

    compare_tree.delete(*compare_tree.get_children())  # Clear the treeview

    for product_id, date_ranges1 in dict1.items():
        if product_id in dict2:
            date_ranges2 = dict2[product_id]
            for range1 in date_ranges1:
                for range2 in date_ranges2:
                    if range1 != range2:
                        compare_tree.insert("", "end", values=(product_id, range1[2], range2[2], range1[0] + " to " + range1[1], range2[0] + " to " + range2[1]))
            del dict2[product_id]
        else:
            for range1 in date_ranges1:
                compare_tree.insert("", "end", values=(product_id, range1[2], "Not in File 2", range1[0] + " to " + range1[1], "Not in File 2"))

    for product_id, date_ranges2 in dict2.items():
        for range2 in date_ranges2:
            compare_tree.insert("", "end", values=(product_id, "Not in File 1", range2[2], "Not in File 1", range2[0] + " to " + range2[1]))

def retrieve_license_info_by_file(file_name):
    query = """
    SELECT pd.StartDate, pd.EndDate, pd.Quantity, lf.FileName, p.ProductId
    FROM ProductDates pd
    JOIN Products p ON pd.ProductId = p.ProductId
    JOIN LicenseFiles lf ON pd.LicenseFileId = lf.LicenseFileId
    WHERE lf.FileName = ?
    """
    return execute_query(query, (file_name,))

# Code for New Tab for Comparing License Files
tab_compare = ttk.Frame(notebook)
notebook.add(tab_compare, text="Compare Lic Files")

license_files = get_all_license_files()
ttk.Label(tab_compare, text="License File 1:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
license_file_combobox1 = ttk.Combobox(tab_compare, values=license_files, width=30)
license_file_combobox1.grid(row=0, column=1, pady=5, padx=5)

ttk.Label(tab_compare, text="License File 2:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
license_file_combobox2 = ttk.Combobox(tab_compare, values=license_files, width=30)
license_file_combobox2.grid(row=1, column=1, pady=5, padx=5)

ttk.Button(tab_compare, text="Compare", command=compare_license_files).grid(row=2, column=0, columnspan=2, pady=5, padx=5)

compare_tree = ttk.Treeview(tab_compare, columns=("ProductId", "Quantity1", "Quantity2", "DateRange1", "DateRange2"), show="headings")
compare_tree.heading("ProductId", text="Product Id")
compare_tree.heading("Quantity1", text="Quantity (File 1)")
compare_tree.heading("Quantity2", text="Quantity (File 2)")
compare_tree.heading("DateRange1", text="Date Range (File 1)")
compare_tree.heading("DateRange2", text="Date Range (File 2)")
compare_tree.grid(row=3, column=0, columnspan=2, pady=10, padx=5, sticky=(tk.W, tk.E))

# About Tab
tab_about = ttk.Frame(notebook)
notebook.add(tab_about, text="关于")

ttk.Label(tab_about, text="作者：wanlinwang").grid(row=0, column=0, pady=10, padx=10)
ttk.Label(tab_about, text="日期：Oct-16-2023").grid(row=1, column=0, pady=10, padx=10)
ttk.Label(tab_about, text="帮助：如有疑问，请联系wanlinwang").grid(row=2, column=0, pady=10, padx=10)

app.mainloop()
```

<img width="1038" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/9a394483-c67f-44c2-8a6b-6c8599a9e6cf">

<img width="1056" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/a40f6d8d-45e2-467c-9767-741377ad4427">

<img width="1069" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/52258c17-dd58-418a-9908-ddc027a25fe5">



