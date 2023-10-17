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
                     (LicenseFileId INTEGER PRIMARY KEY AUTOINCREMENT, FileName TEXT UNIQUE)''')

    cursor.execute("INSERT OR IGNORE INTO LicenseFiles (FileName) VALUES (?)", (filename,))
    cursor.execute("SELECT LicenseFileId FROM LicenseFiles WHERE FileName=?", (filename,))
    license_file_id = cursor.fetchone()[0]

    cursor.execute('''CREATE TABLE IF NOT EXISTS Features
                     (FeatureId INTEGER PRIMARY KEY AUTOINCREMENT, FeatureName TEXT UNIQUE)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Products
                     (ProductId TEXT PRIMARY KEY, ProductName TEXT(256))''')

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
import tkinter.font as tkFont

def adjust_column_width(tree, columns):
    font = tkFont.Font()
    for column in columns:
        width = tree.column(column, 'width')
        for item in tree.get_children():
            entry = tree.item(item, 'values')
            if entry:
                entry_width = font.measure(entry[columns.index(column)])
                width = max(width, entry_width)
        tree.column(column, width=width)

def retrieve_license_info_by_feature(feature_name):
    conn = sqlite3.connect('license.db')
    cursor = conn.cursor()

    query = """
    SELECT pd.StartDate, pd.EndDate, pd.Quantity, lf.FileName, p.ProductId
    FROM ProductDates pd
    JOIN Products p ON pd.ProductId = p.ProductId
    JOIN ProductFeatureRelation pfr ON p.ProductId = pfr.ProductId
    JOIN Features f ON pfr.FeatureId = f.FeatureId
    JOIN LicenseFiles lf ON pd.LicenseFileId = lf.LicenseFileId
    WHERE f.FeatureName = ?
    """
    
    cursor.execute(query, (feature_name,))
    results = cursor.fetchall()
    conn.close()
    return results

def retrieve_license_info_by_product(product_id):
    conn = sqlite3.connect('license.db')
    cursor = conn.cursor()

    query = """
    SELECT pd.StartDate, pd.EndDate, pd.Quantity, lf.FileName, p.ProductId
    FROM ProductDates pd
    JOIN Products p ON pd.ProductId = p.ProductId
    JOIN LicenseFiles lf ON pd.LicenseFileId = lf.LicenseFileId
    WHERE p.ProductId = ?
    """
    
    cursor.execute(query, (product_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_features():
    conn = sqlite3.connect('license.db')
    cursor = conn.cursor()
    cursor.execute("SELECT FeatureName FROM Features")
    features = [row[0] for row in cursor.fetchall()]
    conn.close()
    return features

def get_all_products():
    conn = sqlite3.connect('license.db')
    cursor = conn.cursor()
    cursor.execute("SELECT ProductId FROM Products")
    products = [row[0] for row in cursor.fetchall()]
    conn.close()
    return products

def on_search_by_feature():
    feature_name = feature_name_combobox.get()
    results = retrieve_license_info_by_feature(feature_name)
    tree_by_feature.delete(*tree_by_feature.get_children())  # Clear previous results
    for index, result in enumerate(results, 1):
        tree_by_feature.insert("", "end", values=(index, *result))
    adjust_column_width(tree_by_feature, tree_by_feature["columns"])

def on_search_by_product():
    product_id = product_id_combobox.get()
    results = retrieve_license_info_by_product(product_id)
    tree_by_product.delete(*tree_by_product.get_children())  # Clear previous results
    for index, result in enumerate(results, 1):
        tree_by_product.insert("", "end", values=(index, *result))
    adjust_column_width(tree_by_product, tree_by_product["columns"])

app = tk.Tk()
app.title("License Info Retrieval")

notebook = ttk.Notebook(app)
notebook.pack(pady=10, padx=10, expand=True, fill='both')

# Tab for Feature Name
tab_feature = ttk.Frame(notebook)
notebook.add(tab_feature, text="By Feature Name")

feature_names = get_all_features()
ttk.Label(tab_feature, text="Feature Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
feature_name_combobox = ttk.Combobox(tab_feature, values=feature_names)
feature_name_combobox.grid(row=0, column=1, pady=5, padx=5)
ttk.Button(tab_feature, text="Search", command=on_search_by_feature).grid(row=0, column=2, pady=5, padx=5)

tree_by_feature = ttk.Treeview(tab_feature, columns=("Index", "StartDate", "EndDate", "Quantity", "FileName", "ProductId"), show="headings")
tree_by_feature.heading("Index", text="#")
tree_by_feature.column("Index", width=30)  # Set width for the index column
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
ttk.Label(tab_product, text="Product Id:").grid(row=0, column=0, sticky=tk.W, pady=5)
product_id_combobox = ttk.Combobox(tab_product, values=product_ids)
product_id_combobox.grid(row=0, column=1, pady=5, padx=5)
ttk.Button(tab_product, text="Search", command=on_search_by_product).grid(row=0, column=2, pady=5, padx=5)

tree_by_product = ttk.Treeview(tab_product, columns=("Index", "StartDate", "EndDate", "Quantity", "FileName", "ProductId"), show="headings")
tree_by_product.heading("Index", text="#")
tree_by_product.column("Index", width=30)  # Set width for the index column
tree_by_product.heading("StartDate", text="Start Date")
tree_by_product.heading("EndDate", text="End Date")
tree_by_product.heading("Quantity", text="Quantity")
tree_by_product.heading("FileName", text="License File")
tree_by_product.heading("ProductId", text="Product Id")
tree_by_product.grid(row=1, column=0, columnspan=3, pady=10, padx=5, sticky=(tk.W, tk.E))

# About Tab
tab_about = ttk.Frame(notebook)
notebook.add(tab_about, text="关于")

ttk.Label(tab_about, text="作者：wanlinwang").pack(pady=10)
ttk.Label(tab_about, text="日期：Oct-16-2023").pack(pady=10)
ttk.Label(tab_about, text="帮助：如有疑问，请联系wanlinwang").pack(pady=10)
# Move the "关于" tab to the rightmost position
notebook.tab(notebook.index("end")-1, state="normal")

app.mainloop()

```

<img width="1068" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/eef82880-16c9-496f-a83d-dc64cd201bbd">

<img width="1067" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/1307cb85-589d-483e-adf8-50af00733c1a">

<img width="1069" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/52258c17-dd58-418a-9908-ddc027a25fe5">



