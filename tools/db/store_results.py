def save_actual_results_to_db(results, db_path="lottery_analysis.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actual_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            combination TEXT,
            bonus INTEGER,
            multiplier INTEGER
        )
    """)
    
    # Insert actual results
    cursor.execute("""
        INSERT INTO actual_results (date, combination, bonus, multiplier)
        VALUES (?, ?, ?, ?)
    """, (pd.Timestamp.now(), str(results['Combination']), results['Bonus'], results['Multiplier']))
    
    conn.commit()
    conn.close()
    print("Actual results saved to database.")
