import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.utils import to_categorical

# Load and preprocess data
training_data = "./training_data/team_stats_noh2h.csv"
prediction_file = "./prediction_test/team_stats_noh2h.csv"
output_file = "./prediction_test/2023-teams-predictions-LSTM.csv"

df = pd.read_csv(training_data)

# Feature selection
# what to use to predict 
X = df.drop(
    columns=[
        "Date", 
        "HomeTeam", 
        "AwayTeam", 
        "FTR", 
        "FTHG", 
        "FTAG", 
        "HR", 
        "AR", 
        "HST", 
        "AST"]
)

# Target selection
# what we're trying to predict 
y = df["FTR"]

# Encode target labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)  # Convert FTR column to numeric values, for example: "H", "A", "D" to 0, 1, 2 
y = to_categorical(y)  # One-hot encode the target

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Reshape data to 3D for LSTM (samples, timesteps, features)
sequence_length = 10  # Define a sequence length (e.g., last 10 games)
X_sequences = []
y_sequences = []

for i in range(len(X_scaled) - sequence_length):
    X_sequences.append(X_scaled[i : i + sequence_length])
    y_sequences.append(y[i + sequence_length - 1])

X_sequences = np.array(X_sequences)
y_sequences = np.array(y_sequences)

# Split data into training and validation sets
train_size = int(0.8 * len(X_sequences))
X_train, X_val = X_sequences[:train_size], X_sequences[train_size:]
y_train, y_val = y_sequences[:train_size], y_sequences[train_size:]

# Build the LSTM model
model = Sequential()
model.add(LSTM(64, input_shape=(sequence_length, X.shape[1]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(32, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation="softmax"))

# Compile the model
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Train the model
history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=20, batch_size=32)

# Evaluate the model
val_loss, val_accuracy = model.evaluate(X_val, y_val)
print(f"Validation Accuracy: {val_accuracy * 100:.2f}%")

# Load and preprocess new data for prediction
new_data = pd.read_csv(prediction_file)

# Prepare the features for prediction (drop non-feature columns)
X_new = new_data.drop(
    columns=["Date", "HomeTeam", "AwayTeam", "FTR", "FTHG", "FTAG", "HR", "AR", "HST", "AST"], 
    errors="ignore"
)
X_new_scaled = scaler.transform(X_new)

# Reshape new data to match the sequence length and 3D format
X_new_sequences = []

for i in range(len(X_new_scaled) - sequence_length):
    X_new_sequences.append(X_new_scaled[i : i + sequence_length])

X_new_sequences = np.array(X_new_sequences)

# Make predictions
y_new_pred = model.predict(X_new_sequences)
y_new_pred_labels = label_encoder.inverse_transform(np.argmax(y_new_pred, axis=1))

# Add predictions to new_data and save results
prediction_dates = new_data["Date"].iloc[sequence_length:]  # Adjust index to match sequence length
prediction_teams = new_data[["HomeTeam", "AwayTeam"]].iloc[sequence_length:]
predictions_df = new_data.iloc[sequence_length:].copy()  # Copy the rows from the original data
predictions_df["FTR_Prediction"] = y_new_pred_labels

# Save the predictions to the output file
predictions_df.to_csv(output_file, index=False)

# Display the predictions dataframe
print(predictions_df.head())
