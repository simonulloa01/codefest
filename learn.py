import pandas as pd

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

from sklearn.ensemble import RandomForestRegressor

# Initialize the model
model = RandomForestRegressor(n_estimators=50, random_state=42)

# Train the model
model.fit(X_train, y_train)

from sklearn.metrics import mean_squared_error

# Make predictions on the validation set
y_pred = model.predict(X_val)

# Calculate the Root Mean Squared Error (RMSE)
rmse = mean_squared_error(y_val, y_pred, squared=False)
print(f'Root Mean Squared Error: {rmse:.2f}')