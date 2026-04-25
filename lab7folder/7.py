#1
import pandas as pd
df=pd.read_excel('catalog_products.xlsx')
print(df.head())
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())
#2
numeric_cols=df.select_dtypes(include='number').columns
df[numeric_cols]=df[numeric_cols].astype(float)
df[numeric_cols]=df[numeric_cols].fillna(df[numeric_cols].mean())
text_cols=df.select_dtypes(include='object').columns
df=df.dropna(subset=text_cols)
#3
import numpy as np
df['total_value']=df['col_2']*df['col_3']
df['log_price']=np.log(df['col_2'])
df['double_stock']=df['col_3']*2
#4
import matplotlib.pyplot as plt
df["col_2"].hist(bins=50)
plt.title("Бағаның таралуы")
plt.show()
plt.scatter(df["col_3"], df["col_2"])
plt.xlabel("Саны")
plt.ylabel("Бағасы")
plt.show()
df.boxplot(column="col_2", by="col_7")
plt.show()
#5
mean=df['col_2'].mean()
std=df['col_2'].std()
upper_limit=mean+3*std
lower_limit=mean-3*std
is_anomaly=np.logical_or(df['col_2']>upper_limit, df['col_2']<lower_limit)
anomalies=df[is_anomaly]
df=df[np.logical_not(is_anomaly)]
#6
df=pd.get_dummies(df, columns=['col_7'])
#7
from sklearn.model_selection import train_test_split
y=df['col_2']
X=df.drop(columns=['col_2'])
X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.2, random_state=42)
#8
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
model=LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print("MAE:", mae)
print("MSE:", mse)

