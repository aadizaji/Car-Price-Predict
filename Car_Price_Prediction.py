'''
AmirAli Dizaji
'''


#region Libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from joblib import dump

#endregion


# region Data Understanding

df_206 = pd.read_csv('datasets/divar_206.csv',
                     index_col='Unnamed: 0'
                     )

df_207 = pd.read_csv('datasets/divar_207.csv',
                     index_col='Unnamed: 0'
                     )

df_optima = pd.read_csv('datasets/divar_optima.csv',
                        index_col='Unnamed: 0'
                        )

df_sportage = pd.read_csv('datasets/divar_sportage.csv',
                          index_col='Unnamed: 0'
                          )

# sns.heatmap(df_206.corr(numeric_only=True), annot=True)
# plt.show()
# print('-'*100)
# sns.heatmap(df_207.corr(numeric_only=True), annot=True)
# plt.show()
# print('-'*100)
# sns.heatmap(df_optima.corr(numeric_only=True), annot=True)
# plt.show()
# print('-'*100)
# sns.heatmap(df_sportage.corr(numeric_only=True), annot=True)
# plt.show()

# Missing Data
# print(df_206.isna().sum())
# print(df_207.isna().sum())
# print(df_optima.isna().sum())
# print(df_sportage.isna().sum())

# Data Visualize

# sns.histplot(df_206['price'])
# plt.show()

# sns.histplot(df_207['price'])
# plt.show()

# sns.histplot(df_optima['price'])
# plt.show()

# sns.histplot(df_sportage['price'])
# plt.show()


# print(df_206["price"].median()) # 1460000000.0
# print(df_206["price"].skew()) # -0.13150793876998687

# print(df_207["price"].median()) # 2850000000.0
# print(df_207["price"].skew()) # -0.14611266031751402

# print(df_optima["price"].median()) # 9595000000.0
# print(df_optima["price"].skew()) # 0.4257540055690469

# print(df_sportage["price"].median()) # 8000000000.0
# print(df_sportage["price"].skew()) # 0.2893798571551287


# outlier data داده های پَرت

# sns.boxplot(x="price", data=df_206)
# plt.show()
#
# sns.boxplot(x="price", data=df_207)
# plt.show()
#
# sns.boxplot(x="price", data=df_optima)
# plt.show()
#
# sns.boxplot(x="price", data=df_sportage)
# plt.show()

# endregion


#region Data Preparation

df_206['car_group'] = '206'
df_207['car_group'] = '207'
df_optima['car_group'] = 'optima'
df_sportage['car_group'] = 'sportage'


df = pd.concat([df_206, df_207, df_optima, df_sportage], ignore_index=True)

print(f'Merged DataFrame: {df.shape}') #(2260, 8)



text_columns = ["brand", "model", "color", "gearbox"]

for col in text_columns:
    df[col] = (
        df[col]
        .astype('string')
        .str.strip()
        .replace('', pd.NA)
        .fillna('نامشخص')
        .astype(str)
    )


# Numerical
for col in ['year', 'mileage', 'price']:
    df[col] = pd.to_numeric(df[col], errors='coerce')


# Remove Invalid Data
df = df.dropna(subset=['year', 'mileage', 'price'])

df = df[(df['price'] > 0) & (df['mileage'] >= 0) & (df['year'] > 0)].copy()


# Features and Target ( X & Y )
X = df[["brand", "model", "year", "mileage", "color", "gearbox"]]

y = df["price"]


# Train and Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=df['car_group']
)


train = X_train.copy()
train['price'] = y_train

train['car_group'] = df.loc[X_train.index, 'car_group'] # برای ارزیابی دقیق تر قیمت خودرو در هر گروه

clean_parts = []

for car in ['206', '207', 'optima', 'sportage']:

    group = train[train['car_group'] == car]

    # Remove Outlier Data (IQR)
    Q1 = group['price'].quantile(0.25)
    Q3 = group['price'].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    clean_group = group[
        group['price'].between(lower_bound, upper_bound)
    ]

    print(car, f'training outliers removed: {len(group) - len(clean_group)}')
    clean_parts.append(clean_group)


train_clean = pd.concat(clean_parts)

X_train = train_clean[["brand", "model", "year", "mileage", "color", "gearbox"]]
y_train = train_clean['price']


# One-Hot Encoding

encoder = ColumnTransformer(
    transformers=[
        (
            "one_hot",
            OneHotEncoder(handle_unknown="ignore"),
            text_columns
        )
    ],
    remainder="passthrough"
)

# endregion


#region Modeling

model = Pipeline([
    ('preprocessing', encoder),
    ('linear_regression', LinearRegression())
])

model.fit(X_train, y_train)

# endregion


#region Evaluation

y_pred = model.predict(X_test)

MAE = mean_absolute_error(y_test, y_pred)
MSE = mean_squared_error(y_test, y_pred)
RMSE = np.sqrt(MSE)
R2 = r2_score(y_test, y_pred)

print('MAE:', round(MAE))
print('MSE:', round(MSE))
print('RMSE:', round(RMSE))
print('R2:', round(R2, 3))
'''
MAE: 810062435
MSE: 1637566313982953216
RMSE: 1279674300
R2: 0.896
206 MAE: 419994714 R2: -1.105
207 MAE: 645265402 R2: -0.051
optima MAE: 1708259769 R2: 0.653
sportage MAE: 1754102154 R2: 0.584
'''


# Evaluation for Each Car
for car in ['206', '207', 'optima', 'sportage']:

    mask = df.loc[X_test.index, 'car_group'] == car

    actual = y_test[mask]
    prediction = y_pred[mask.to_numpy()]

    print(
        car,
        'MAE:', round(mean_absolute_error(actual, prediction)),
        'R2:', round(r2_score(actual, prediction), 3)
    )

#endregion


#region Deployment

dump(model, 'Car_Price_Prediction.joblib')

print('Model Saved')

#endregion