
# -------- STEP 1: Import Libraries --------
import pandas as pd
import numpy as np
import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt

# -------- STEP 2: Load and Preview CSV --------
try:
    df = pd.read_csv('cleaned_best_sellers.csv')
    print("CSV loaded successfully!")
except FileNotFoundError:
    print(" CSV file not found. Please check the path.")
    exit()

# Print actual column names to debug
print(" Original Columns:", df.columns.tolist())

# -------- STEP 3: Clean & Normalize Columns --------
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

df.rename(columns={
    'product_price': 'price',
    'product_star_rating': 'rating',
    'product_num_ratings': 'reviews',
    'product_title': 'name',
    'rank': 'rank',
    'country': 'country'
}, inplace=True)

print(" Normalized Columns:", df.columns.tolist())

# -------- STEP 4: Clean Data --------
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# Clean price column
if 'price' in df.columns:
    df['price'] = df['price'].astype(str)
    df['price'] = df['price'].replace(r'[^\d.]', '', regex=True).replace('', '0').astype(float)
else:
    print(" 'price' column not found.")
    exit()

# Clean rating column
if 'rating' in df.columns:
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
else:
    print(" 'rating' column not found.")
    exit()

# Clean reviews column
if 'reviews' in df.columns:
    df['reviews'] = df['reviews'].replace('[,]', '', regex=True).astype(int)
else:
    print(" 'reviews' column not found.")
    exit()

# -------- STEP 5: Analytical Computation --------

# Add Free/Paid price type
df['price_type'] = df['price'].apply(lambda x: 'Free' if x == 0 else 'Paid')

# -------- STEP 6: Console Output --------
print("\n Top 10 Best-Selling Software by Rating:")
print(df.sort_values(by='rating', ascending=False)[['name', 'rating', 'reviews', 'price']].head(10))

print("\n Average Price of Software per Country:")
print(df.groupby('country')['price'].mean().sort_values(ascending=False))

print("\n Pricing Trend Summary:")
print(f"Min Price: ₹{df['price'].min():.2f}")
print(f"Max Price: ₹{df['price'].max():.2f}")
print(f"Average Price: ₹{df['price'].mean():.2f}")
print(f"Median Price: ₹{df['price'].median():.2f}")

print("\n Most Reviewed Software Categories:")
print(df.groupby('country')['reviews'].sum().sort_values(ascending=False))

print("\n Average Rating and Reviews per Category:")
print(df.groupby('country')[['rating', 'reviews']].mean().sort_values(by='rating', ascending=False))

print("\n Free vs Paid Software Performance (Avg Rating & Reviews):")
print(df.groupby('price_type')[['rating', 'reviews']].mean())

# -------- STEP 7: Visualizations --------
# Rating vs Review Count
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='reviews', y='rating', hue='price_type', alpha=0.7)
plt.title('Rating vs Review Count')
plt.xlabel('Number of Reviews')
plt.ylabel('Star Rating')
plt.grid(True)
plt.tight_layout()
plt.show()


# -------- STEP 8: Save Cleaned Data (Optional) --------
df.to_csv('cleaned_best_sellers.csv', index=False)
print(" Cleaned data saved as 'cleaned_best_sellers.csv'")
