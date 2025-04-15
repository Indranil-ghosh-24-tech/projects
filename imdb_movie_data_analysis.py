import pandas as pd
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Load the dataset from the correct path
df = pd.read_csv("C:/Users/91743/Downloads/IMDB.csv")

# Drop unwanted columns
df_cleaned = df.drop(columns=[col for col in df.columns if "Unnamed" in col or col == "Rank"])

sns.set(style="whitegrid")
df_plot = df_cleaned.copy()

top_rated = df_plot.sort_values(by="Rating", ascending=False).head(10)
plt.figure(figsize=(12, 6))
sns.barplot(data=top_rated, x="Rating", y="Title", palette="viridis")
plt.title("Top 10 Movies by IMDb Rating")
plt.tight_layout()
plt.show()


# Fill missing values (optional)

df_cleaned['Revenue (Millions)'] = df_cleaned['Revenue (Millions)'].replace({np.nan: None})
df_cleaned['Metascore'] = df_cleaned['Metascore'].replace({np.nan: None})

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="7439450596@",
    database="imdb_movies"
)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS imdb_movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    genre VARCHAR(100),
    description TEXT,
    director VARCHAR(255),
    actors TEXT,
    year INT,
    runtime INT,
    rating FLOAT,
    votes INT,
    revenue FLOAT,
    metascore FLOAT
)
""")

# Insert data
insert_query = """
INSERT INTO imdb_movies (
    title, genre, description, director, actors, year,
    runtime, rating, votes, revenue, metascore
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for row in df_cleaned.values.tolist():
    cursor.execute(insert_query, tuple(row))

conn.commit()

# CRUD Operations Examples

# Read
cursor.execute("SELECT * FROM imdb_movies LIMIT 5")
for row in cursor.fetchall():
    print(row)

# Update
cursor.execute("""
    UPDATE imdb_movies SET rating = 9.5 WHERE title = 'Inception'
""")
conn.commit()

# Delete
cursor.execute("""
    DELETE FROM imdb_movies WHERE year < 2000
""")
conn.commit()

# Close connection
cursor.close()
conn.close()