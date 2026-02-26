import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import pickle
import numpy as np

# Load dataset
data = pd.read_csv("student_data.csv")

# Features (X)
X = data[['attendance', 'previous_marks', 'assignments', 'absences']]

# Target (y)
y = data['predicted_marks']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation metrics
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print("📊 Linear Regression Performance:")
print(f"Accuracy (R² Score): {r2*100:.2f}%")
print(f"MAE: {mae:.4f}")
print(f"MSE: {mse:.4f}")
print(f"RMSE: {rmse:.4f}")

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Linear Regression Model trained sucessfully and saved as model.pkl")
