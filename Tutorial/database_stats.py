import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "sample.db")


def create_sample_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, product TEXT, units INTEGER, revenue REAL)")
    c.execute("DELETE FROM sales")
    c.executemany(
        "INSERT INTO sales (date, product, units, revenue) VALUES (?, ?, ?, ?)",
        [
            ("2026-03-01", "Widget A", 11, 220.0),
            ("2026-03-01", "Widget B", 7, 140.0),
            ("2026-03-02", "Widget A", 12, 240.0),
            ("2026-03-02", "Widget C", 4, 120.0),
            ("2026-03-03", "Widget B", 9, 180.0),
        ],
    )
    conn.commit()
    conn.close()


def read_data_and_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Read table rows
    rows = c.execute("SELECT date, product, units, revenue FROM sales ORDER BY date").fetchall()
    print("\nRows from sales table:")
    for row in rows:
        print(row)

    # Basic stats from the table
    stats = c.execute(
        "SELECT COUNT(*) AS total_rows, SUM(units) AS total_units, SUM(revenue) AS total_revenue, AVG(revenue) AS avg_revenue FROM sales"
    ).fetchone()
    print("\nBasic statistics:")
    print(f"Total rows: {stats[0]}")
    print(f"Total units sold: {stats[1]}")
    print(f"Total revenue: {stats[2]:.2f}")
    print(f"Average revenue per row: {stats[3]:.2f}")

    # Group-by statistics
    print("\nRevenue by product:")
    for product, total_units, total_revenue in c.execute(
        "SELECT product, SUM(units), SUM(revenue) FROM sales GROUP BY product ORDER BY SUM(revenue) DESC"
    ):
        print(f"{product}: units={total_units}, revenue={total_revenue:.2f}")

    conn.close()


if __name__ == "__main__":
    create_sample_data()
    read_data_and_stats()
