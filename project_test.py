#Good start, but still broken. Breaks when selecting materials. I also want to be able to see materials \\\
#as a dataframe with pricing and link so that selection is more intuitive. \\FIXED
#FUNCTIONING AS OF 1/30/2015


import pandas as pd
import streamlit as st

# Loading data 
@st.cache_data
def load_data():
    return pd.read_excel('Final_Search_Results.xlsx').sort_values(by='Price', ascending=True)

material_data = load_data()

# Maniuplating data for individual projects
concrete_data = material_data[material_data['Project Source'] == 'concrete project']
plumbing_data = material_data[material_data['Project Source'] == 'plumbing project']
tenant_improvement_data = material_data[material_data['Project Source'] == 'tenant improvement project']
# Title
st.title('Project List')

# List of projects
projects = ['Concrete', 'Plumbing', 'Tenant Improvement']
selected_project = st.selectbox('Select Project', projects)

# Column configuration for the data editor
column_configuration = {
    "Title": st.column_config.TextColumn(
        "Product", help="The name of the product",
        disabled=True, width= "medium",
    ),
    "Price": st.column_config.NumberColumn(
        label=None, help="The price per unit of the product",
        disabled=True, format="$ %.2f",
    ),    
    "Store": st.column_config.TextColumn(
        label=None, help="The store where the product is available",
        disabled=True,
    ),
    "Link": st.column_config.TextColumn(
        label=None, help="A link to the product via Google Shopping",
        disabled=True,
    ),
    "Include": st.column_config.CheckboxColumn(
        label=None, help="Check to include this material in the project",
        disabled=False, pinned=True,
    ),
    "Quantity": st.column_config.NumberColumn(
        label=None, help="The quantity of the product needed for the project",
        disabled=False, format="%d", pinned=True,
    ),

}

column_configuration_labor = {
    "Labor Type": st.column_config.TextColumn(
        "Labor", help="Type of Labor",
        disabled=False, width= "medium",
    ),
    "Square Footage": st.column_config.NumberColumn(
        label=None, help="The square footage for the labor",
        disabled=False, format="%.2f",
    ),    
    "Contact Information": st.column_config.TextColumn(
        label=None, help="Contact information",
        disabled=False,
    ),
    "Labor Rate": st.column_config.NumberColumn(
        label=None, help="Pay rate for labor",
        disabled=False, format="$ %.2f",
    ),
    #"Total Labor Cost": st.column_config.NumberColumn(
    #    label=None, help="Calculated total labor cost",
    #    disabled=False, format="%d",
    #),
}

def select_materials(data):
    product_types = data['Product Type'].unique()
    selected_materials = []

    for product_type in product_types:
        st.write(f"Select materials for {product_type}")
        materials = data[data['Product Type'] == product_type][["Title", "Price", "Store", "Link"]]
        materials["Quantity"] = 0
        materials["Include"] = False
        edited_materials = st.data_editor(materials, use_container_width=True, height=200, column_config=column_configuration, hide_index=True)
        selected_materials.append(edited_materials)
    
    selected_data = pd.concat(selected_materials)
    selected_data = selected_data[selected_data['Include'] == True]
    selected_data['Total Price'] = selected_data['Price'] * selected_data['Quantity']
    
    
    return selected_data

def calculate_and_display_costs(selected_data):
    total_material_cost = selected_data['Total Price'].sum()
    st.write('Selected Materials:')
    st.dataframe(selected_data[['Title', 'Price', 'Quantity', 'Total Price', 'Store', 'Link']])
    st.write(f'Total Material Cost: ${total_material_cost:,.2f}')
    return total_material_cost

if selected_project == 'Concrete':
    st.subheader('Materials List for Concrete Project')
    selected_data = select_materials(concrete_data)
    total_material_cost = calculate_and_display_costs(selected_data)
elif selected_project == 'Plumbing':
    st.subheader('Materials List for Plumbing Project')
    selected_data = select_materials(plumbing_data)
    total_material_cost = calculate_and_display_costs(selected_data)
elif selected_project == 'Tenant Improvement':
    st.subheader('Materials List for Tenant Improvement Project')
    selected_data = select_materials(tenant_improvement_data)
    total_material_cost = calculate_and_display_costs(selected_data)

# Labor Calculations
#square_footage = st.number_input('Enter the square footage of the project', min_value=0.0, value=0.0, step=1.0)
#labor_cost_rate = st.number_input('Enter the per unit labor cost', min_value=0.0, value=0.0, step=1.0)
#labor_cost = square_footage * labor_cost_rate
labor_data = pd.DataFrame({
    "Labor Type": [""],
    "Square Footage": [0.0],
    "Labor Rate": [0.0],
    #Total labor cost column was not calculating dynamically within the dataframe
    #"Total Labor Cost": [0.0],
    "Contact Information": [""]

})
edited_labor_data = st.data_editor(labor_data, use_container_width=True, height=200, column_config=column_configuration_labor, hide_index=True, num_rows='dynamic')

edited_labor_data['Total Labor Cost'] = edited_labor_data['Square Footage'] * edited_labor_data['Labor Rate']
labor_cost = edited_labor_data['Total Labor Cost'].sum()


st.write(f'Total Labor Cost: ${labor_cost:,.2f}')
total_project_cost = (total_material_cost + labor_cost) * 1.25
st.write(f'Total Project Cost: ${total_project_cost:,.2f}')
