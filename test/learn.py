import pandas as pd
from sklearn.metrics import mean_squared_error

# Load the datasets
train_X = pd.read_csv('train_X.csv')
train_y = pd.read_csv('train_y.csv')

# Sort entries by 'hotel_id' and 'distance' (ascending order)
train_X = train_X.sort_values(by=['hotel_id', 'distance'])

# Assign a sequential number to each entry per hotel_id
train_X['entry_num'] = train_X.groupby('hotel_id').cumcount() + 1


pivot_columns = ['distance', 'rating', 'number_of_ratings']
train_X_pivot = train_X.pivot(index='hotel_id', columns='entry_num', values=pivot_columns)
train_X_pivot.columns = [f'{col}_{num}' for col, num in train_X_pivot.columns]
train_X_pivot.fillna(0, inplace=True)

data = train_y.merge(train_X_pivot, on='hotel_id', how='left')
print(data)
X = data.drop(['hotel_id','price'], axis=1)
y = data['price']
print(y)

from sklearn.discriminant_analysis import StandardScaler
from sklearn.model_selection import train_test_split

# Split the data (e.g., 80% training and 20% validation)
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42
)
scaler = StandardScaler()

# Fit the scaler on the training data
X_train = scaler.fit_transform(X_train)

# Apply the transformation to the validation data
X_val = scaler.transform(X_val)

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import GridSearchCV


# # Define parameter grid
# param_grid = {
#     'n_estimators': [100, 200, 300],
#     'learning_rate': [0.01, 0.05, 0.1],
#     'max_depth': [3, 5, 7],
#     'min_samples_split': [2, 5],
#     'min_samples_leaf': [1, 2],
#     'subsample': [0.6, 0.8, 1.0],
# }
# # Initialize Grid Search
# grid_search_gbr = GridSearchCV(
#     estimator=GradientBoostingRegressor(random_state=42),
#     param_grid=param_grid,
#     cv=5,
#     scoring='neg_mean_squared_error',
#     n_jobs=-1,
#     verbose=1
# )

# # Fit the Grid Search to the data
# grid_search_gbr.fit(X_train, y_train)

# # Best parameters
# print("Best parameters found:", grid_search_gbr.best_params_)

# # Use the best estimator
# best_gbr_model = grid_search_gbr.best_estimator_

# # Predict on validation set
# y_pred_best_gbr = best_gbr_model.predict(X_val)

# # Calculate RMSE
# rmse_best_gbr = mean_squared_error(y_val, y_pred_best_gbr, squared=False)
# print(f'Optimized Gradient Boosting RMSE: {rmse_best_gbr:.2f}')


#----------------------- Random Forest Regressor -----------------------
# Initialize the model
model = RandomForestRegressor(n_estimators=50, random_state=42)

# Train the model
model.fit(X_train, y_train)

from sklearn.metrics import root_mean_squared_error

# Make predictions on the validation set
y_pred = model.predict(X_val)

# Calculate the Root Mean Squared Error (RMSE)
rmse = root_mean_squared_error(y_val, y_pred)
print(f'Root Mean Squared Error: {rmse:.2f}')

import joblib
joblib.dump(model, 'hotel_price_predictor_RFR.pkl')

importances = model.feature_importances_
feature_names = X.columns
feature_importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

print(feature_importance_df.head(10))  # Show top 10 features
# Statistical summary
print(data['price'].describe())

# Visualize the distribution
import matplotlib.pyplot as plt
import seaborn as sns

sns.histplot(data['price'], kde=True)
plt.title('Distribution of Hotel Prices')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()