import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# ⭐ Base Models
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.ensemble import StackingRegressor

# ==============================
# ✅ 1. LOAD DATASET
# ==============================
data = pd.read_csv("student_data.csv")

# 🔥 IMPORTANT CLEANING (your dataset has >100 marks)
data = data[data['predicted_marks'] <= 100]

# ==============================
# ✅ 2. FEATURES + TARGET
# ==============================
X = data[['attendance', 'previous_marks', 'assignments', 'absences']]
y = data['predicted_marks']

# ==============================
# ✅ 3. TRAIN TEST SPLIT
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==============================
# ⭐ 4. BASE MODELS
# ==============================

linear_model = LinearRegression()

boost_model = HistGradientBoostingRegressor(
    max_iter=1200,
    learning_rate=0.03,
    max_depth=None,
    min_samples_leaf=5,
    l2_regularization=0.1,
    random_state=42
)

# ==============================
# 🚀 5. STACKING MODEL (LATEST TECHNIQUE)
# ==============================

model = StackingRegressor(
    estimators=[
        ('linear', linear_model),
        ('boost', boost_model)
    ],
    final_estimator=LinearRegression()   # meta learner
)

# ==============================
# ✅ 6. TRAIN
# ==============================
model.fit(X_train, y_train)

# ==============================
# ✅ 7. PREDICT
# ==============================
y_pred = model.predict(X_test)

# ==============================
# ✅ 8. METRICS
# ==============================
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print("\n📊 Stackin Regressor Performance")
print(f"Accuracy (R² Score): {r2*100:.2f}%")
print(f"MAE : {mae:.4f}")
print(f"MSE : {mse:.4f}")
print(f"RMSE: {rmse:.4f}")

# ==============================
# ✅ 9. SAVE MODEL FOR DJANGO
# ==============================
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print(" Stacking model trained successfully and saved as model.pkl")
