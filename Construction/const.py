from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Load your Excel file here
file_path = r"C:\Users\SUPER\Downloads\CONSTRUCTION MATERIAL LIST (1).xlsx"
sheet1_data_cleaned = None

# Load the Excel file with error handling
try:
    sheet1_data_cleaned = pd.read_excel(file_path)
    sheet1_data_cleaned['Required Material'] = sheet1_data_cleaned['Required Material'].ffill()
except FileNotFoundError:
    print("File not found. Please check the file path.")
except pd.errors.EmptyDataError:
    print("File is empty.")
except Exception as e:
    print(f"An error occurred: {e}")

# Route to display the search form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the search functionality
@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term'].lower()  # Get search term from the form

    # Filter materials that match the search term (case-insensitive)
    required_materials = sheet1_data_cleaned['Required Material'].dropna().unique()
    matching_materials = [(index + 1, material) for index, material in enumerate(required_materials) if
                          search_term in material.lower()]

    if not matching_materials:
        return "No materials found matching your search. Please try again."

    return render_template('search_results.html', materials=matching_materials, search_term=search_term)

# Route to handle item selection and display unit
@app.route('/select', methods=['POST'])
def select():
    selected_material = request.form.get('selected_material')

    # Filter the DataFrame based on the selected material
    filtered_df = sheet1_data_cleaned[sheet1_data_cleaned['Required Material'] == selected_material]

    filtered_df = filtered_df.reset_index(drop=True)  # Reset the index of the filtered DataFrame
    items = []
    for index, row in filtered_df.iterrows():
        items.append((index + 1, row['Item'], row['Unit']))

    return render_template('items.html', items=items, material=selected_material)

# Route to generate the final report
@app.route('/report', methods=['POST'])
def report():
    selected_items = request.form.getlist('selected_items')  # Get selected items

    report = []
    for item in selected_items:
        row = sheet1_data_cleaned[sheet1_data_cleaned['Item'] == item]
        if not row.empty:
            unit = row['Unit'].values[0]  # Get the unit for the selected item
            report.append({'item': item, 'unit': unit})

    return render_template('report.html', report=report)

if __name__ == "__main__":
    app.run(debug=True)
