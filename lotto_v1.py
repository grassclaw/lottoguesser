import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


print("hello")
# 1. Load Historical Lottery Data
def load_lottery_data(csv_path):
    df = pd.read_csv(csv_path)
    return df

lottery_data = load_lottery_data("./historical_data/csv/Past180Days_Mega_Millions.csv")

# 2. Feature Engineering
def prepare_features(df):
    # Flatten numbers and calculate frequency
    all_numbers = df.iloc[:, 1:-2].values.flatten()  # Extract only the number columns
    number_freq = pd.Series(all_numbers).value_counts()

    # Create features: Frequency of each number
    features = []
    labels = []
    for idx, row in df.iterrows():
        row_features = [number_freq[num] for num in row[1:-2]]  # Use only numbers, not Bonus/Multiplier
        features.append(row_features)
        labels.append(idx % 2)  # Alternate labels for variety (0, 1, 0, 1, ...)
    return np.array(features), np.array(labels), number_freq


X, y, number_freq = prepare_features(lottery_data)

# 3. Split Data for Training and Testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Generate Predictions for Combinations
def predict_top_combinations(model, number_freq, num_combinations=5, num_numbers=5, range_numbers=69, bonus_range=26, multiplier_range=5):
    # Generate random combinations
    possible_numbers = list(range(1, range_numbers + 1))
    possible_bonus = list(range(1, bonus_range + 1))
    possible_multiplier = list(range(1, multiplier_range + 1))

    combinations = []
    for _ in range(1000):  # Generate 1000 combinations
        main_numbers = sorted(np.random.choice(possible_numbers, num_numbers, replace=False))
        bonus = np.random.choice(possible_bonus)
        multiplier = np.random.choice(possible_multiplier)
        combinations.append(main_numbers + [bonus, multiplier])  # Include bonus and multiplier

    # Compute features for each combination
    features = [[number_freq.get(num, 0) for num in combo[:-2]] for combo in combinations]  # Ignore bonus and multiplier for now
    
    # Predict probabilities for each combination
    probabilities = model.predict_proba(features)
    if probabilities.shape[1] == 1:  # Handle single-class case
        probabilities = probabilities[:, 0]  # Use the only column
    else:
        probabilities = probabilities[:, 1]  # Use class 1 probabilities
    
    # Combine predictions into a DataFrame
    predictions = pd.DataFrame({
        'Combination': [combo[:-2] for combo in combinations],  # Main numbers
        'Bonus': [combo[-2] for combo in combinations],         # Bonus numbers
        'Multiplier': [combo[-1] for combo in combinations],    # Multiplier
        'Probability': probabilities
    })
    
    # Get top N combinations with the highest probabilities
    top_combinations = predictions.sort_values(by='Probability', ascending=False).head(num_combinations)
    return top_combinations

top_5_combinations = predict_top_combinations(model, number_freq, num_combinations=5, num_numbers=5, range_numbers=69)

# 6. Output Results
print("Top 5 Number Combinations Likely to Appear in the Next Draw:")
print(top_5_combinations)

# 16 44 49 55 65 13
# 13 14 18 28 38 9
# 20 21 4 43 47 7
# 12 21 62 67 69 24
# 29 31 35 5 54 2
