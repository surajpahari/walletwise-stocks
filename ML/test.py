import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
import streamlit as st
import yfinance as yf
from keras.models import load_model

st.title('Stock Trend Prediction')
user_input = st.text_input('Enter Stock Ticker', 'AAPL')
df = yf.download(user_input, start='2015-01-01', end='2022-12-31')

st.subheader('Data From 2015 to 2022')
st.write(df.describe())

# Visualization
st.subheader('Closing price VS Time Chart')
fig1 = plt.figure(figsize=(12, 6))
plt.plot(df.Close)
plt.xlabel('Time')
plt.ylabel('Price')
st.pyplot(fig1)

# Plotting 100 days moving average
st.subheader('Closing price VS Time Chart with 100MA')
ma100 = df.Close.rolling(100).mean()
fig3 = plt.figure(figsize=(12, 6))
plt.plot(df.Close, label='Closing Price')
plt.plot(ma100, 'Red', label='100days moving average')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig3)

# Plotting 200 days moving average
st.subheader('Closing VS Time Chart with 100MA & 200MA')
ma200 = df.Close.rolling(200).mean()
fig4 = plt.figure(figsize=(12, 6))
plt.plot(df.Close, label='Original Closing Price')
plt.plot(ma100, 'Red', label='100days moving average')
plt.plot(ma200, 'Green', label='200days moving average')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig4)

# Splitting data into training and testing data
data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
data_training_array = scaler.fit_transform(data_training)

# Load the model
model = load_model('keras_model.h5')

# Testing part
past_100_days = data_training.tail(100)
final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
input_data = scaler.fit_transform(final_df)
x_test = []
y_test = []
for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)
y_predicted = model.predict(x_test)
scaler = scaler.scale_
scale_factor = 1/scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor

# Final Graph
st.subheader('Prediction vs Original')
fig2 = plt.figure(figsize=(12, 6))
plt.plot(y_test, 'blue', label='Original Price')
plt.plot(y_predicted, 'red', label='Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)

# Predicting the next 30 days
st.subheader('Predicting the next 30 days')
future_input = input_data[-100:]
future_input = np.array(future_input).reshape(1, -1)
temp_input = list(future_input)
temp_input = temp_input[0].tolist()

future_output = []
n_steps = 100
for i in range(30):
    if len(temp_input) > 100:
        future_input = np.array(temp_input[1:])
        future_input = future_input.reshape(1, n_steps, 1)
        pred = model.predict(future_input, verbose=0)
        temp_input.extend(pred[0].tolist())
        temp_input = temp_input[1:]
        future_output.extend(pred.tolist())
    else:
        future_input = future_input.reshape((1, n_steps, 1))
        pred = model.predict(future_input, verbose=0)
        temp_input.extend(pred[0].tolist())
        future_output.extend(pred.tolist())

# Rescaling future predictions
future_output = np.array(future_output)
future_output = future_output * scale_factor

# Create a DataFrame for the future predictions
future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=30)
future_df = pd.DataFrame(future_output, index=future_dates, columns=['Predicted Price'])

# Display the future predictions in a table
st.subheader('Next 30 Days Predicted Prices')
st.write(future_df)

# Visualize the future predictions
st.subheader('Future 30 Days Prediction')
fig5 = plt.figure(figsize=(12, 6))
plt.plot(np.arange(1, len(df.Close)+1), df['Close'], label='Historical Price')
plt.plot(np.arange(len(df.Close)+1, len(df.Close)+31), future_output, label='Future Prediction', color='red')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig5)

