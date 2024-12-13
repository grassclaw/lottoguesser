def compare_and_save_results(db_path="lottery_analysis.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table for comparison results
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comparison_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            matched_numbers INTEGER,
            matched_bonus INTEGER,
            matched_multiplier INTEGER
        )
    """)
    
    # Fetch predictions and actual results
    predictions = cursor.execute("SELECT combination, bonus, multiplier FROM predictions").fetchall()
    actual_results = cursor.execute("SELECT combination, bonus, multiplier FROM actual_results").fetchone()
    
    if not actual_results:
        print("No actual results available for comparison.")
        conn.close()
        return
    
    actual_combination = set(eval(actual_results[0]))
    actual_bonus = actual_results[1]
    actual_multiplier = actual_results[2]
    
    # Compare each prediction with the actual results
    for prediction in predictions:
        predicted_combination = set(eval(prediction[0]))
        predicted_bonus = prediction[1]
        predicted_multiplier = prediction[2]
        
        matched_numbers = len(predicted_combination.intersection(actual_combination))
        matched_bonus = int(predicted_bonus == actual_bonus)
        matched_multiplier = int(predicted_multiplier == actual_multiplier)
        
        # Save comparison result
        cursor.execute("""
            INSERT INTO comparison_results (date, matched_numbers, matched_bonus, matched_multiplier)
            VALUES (?, ?, ?, ?)
        """, (pd.Timestamp.now(), matched_numbers, matched_bonus, matched_multiplier))
    
    conn.commit()
    conn.close()
    print("Comparison results saved to database.")
