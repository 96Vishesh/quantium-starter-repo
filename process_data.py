import pandas as pd
import glob

# Path where CSV files are stored
file_path = "data/*.csv"

# Get list of all CSV files
files = glob.glob(file_path)

# List to store dataframes
df_list = []

for file in files:
    df = pd.read_csv(file)

    # Filter only Pink Morsel
    df = df[df['product'].str.lower() == 'pink morsel']

    # Create sales column
    df['sales'] = df['quantity'] * df['price']

    # Keep only required columns
    df = df[['sales', 'date', 'region']]

    df_list.append(df)

# Combine all files
final_df = pd.concat(df_list)

# Save output
final_df.to_csv("formatted_sales.csv", index=False)

print("Processing complete! File saved as formatted_sales.csv")
