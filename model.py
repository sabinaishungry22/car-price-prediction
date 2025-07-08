import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
from datetime import datetime

# Load cleaned data
df = pd.read_csv("processed_data/cleaned_cars.csv")

# 1. Ensure 20-year data range
current_year = datetime.now().year
df = df[df['year'] >= (current_year - 20)]

# 2. Enhanced feature engineering
df['age'] = current_year - df['year']
df['brand'] = df['title'].str.split().str[1]  # Extract brand from title

# 3. Handle missing data
df = df.dropna(subset=['price_clean', 'age'])

# 4. Create features - now with brand and age
features = pd.get_dummies(df[['age', 'brand']], columns=['brand'])
X = features
y = df['price_clean']

# 5. Train-test split for evaluation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Train improved model
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    min_samples_leaf=5,
    random_state=42
)
model.fit(X_train, y_train)

# 7. Evaluate
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)
print(f"Training R²: {train_score:.2f}")
print(f"Test R²: {test_score:.2f}")

# 8. Save model and metadata
joblib.dump({
    'model': model,
    'features': list(X.columns),
    'train_year': current_year,
    'data_size': len(df)
}, 'car_model_enhanced.pkl')

print(f"Enhanced model trained with {len(df)} records (2000-{current_year})")