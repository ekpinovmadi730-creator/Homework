import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
df=pd.read_excel('catalog_products.xlsx')
#1
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())
print(df.head())
#2
numeric_cols=[]
for col in df.columns:
    if df[col].dtype=='int64' or df[col].dtype=='float64':
        numeric_cols=[]
for col in df.columns:
    df[col]=df[col].astype(float)
    mean_val=df[col].mean()
    df[col]=df[col].fillna(mean_val)
print(df[numeric_cols].isnull().sum().sum())
print(df[['col_2', 'col_3']].head(3))
#3
df['total_value']=df['col_2']*df['col_3']
df['double_stock']=df['col_3']*2
df['log_price']=np.log(df['col_2'])
print(df[['col_2', 'col_3', 'total_value', 'log_price']].head(3))
#4
mask=(df['col_2']>500)&(df['col_7']=='Electronics')
electronis_expensive=df[mask]
print(electronis_expensive[['col_1','col_2','col_7']])
#5
groups=df.groupby('col_7')
result=groups['col_2'].mean().reset_index()
result.columns=['category', 'mean_price']
result['max_price']=groups['col_2'].max().values
result['total_quantity']=groups['col_3'].sum().values
print(result)
#6
cols=['col_2', 'col_3', 'col_5', 'col_6', 'col_8', 'col_9', 'col_11']
for col in cols:
    print(col, 'mean:', round(df[col].mean(), 2),
               'median:', round(df[col].median(), 2),
               'std:', round(df[col].std(), 2))
#7
mean_price=df['col_2'].mean()
std_price=df['col_2'].std()
anomalies=df[df['col_2']>mean_price+3*std_price]
print(anomalies[['col_1','col_2','col_7']].head())
#8
num10=['col_2','col_3', 'col_5', 'col_6', 'col_8', 'col_9', 'col_11']
corr_matrix=df[num10].corr()
print(corr_matrix.round(3))
#9
plt.figure(figsize=(10,5))
plt.hist(df['col_2'], bins=50, color='blue', edgecolor='red')
plt.title('Price distribution')
plt.xlabel('Price')
plt.ylabal('Amount')
plt.grid(axis='y')
plt.show()
#10
sample=df.sample(1000, random_state=42)
plt.figure(figsize=(9,5))
sns.regplot(data=sample, x='col_2', y='col_3', scatter_kws={'alpha':0.3}, line_kws={'color':'red'})
plt.title('Price vs Amount')
plt.xlabel('Price')
plt.ylabel('Amount')
plt.show()
#11
plt.figure(figsize=(9, 5))
sns.boxplot(data=df, x='col_7', y='col_2', hue='col_7', legend=False)
plt.title('Price by category')
plt.xlabel('Category')
plt.ylabel('Price')
plt.show()
#12
pair_df = df[['col_2', 'col_3', 'col_5', 'col_6', 'col_7']].sample(500, random_state=42)
sns.pairplot(pair_df, hue='col_7')
plt.show()
#14
save_cols=list(df.columns[:50])+['total_value', 'log_price']
df[save_cols].to_excel('catalog_analysis.xlsx', index=False)
print("File saved")
#13
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Correlation heatmap')
plt.show()
#15
category_summary=df.groupby('col_7').agg(
    count=('col_2','count'),
    mean_price=('col_2', 'count'),
    total_quantity=('col_3', 'sum'),
    mean_log_price=('log_price','mean'),
).reset_index()
category_summary.columns=['category','count', 'mean_price', 'total_quantity','mean_log_price']
print(category_summary.head())
#16
most_expensive=df.loc[df.groupby('col_7')['col_2'].idmax()]
print(most_expensive[['col_1', 'col_2', 'col_7']].reset_index(drop=True))
#17
top10 = df.sort_values('total_value', ascending=False).head(10)
print(top10[['col_1', 'col_2', 'col_3', 'total_value']].reset_index(drop=True))

# 18 — Распределение по диапазонам цен
bins = [0, 50, 200, 500, 1000, float('inf')]
labels = ['0-50', '50-200', '200-500', '500-1000', '>1000']
df['price_range'] = pd.cut(df['col_2'], bins=bins, labels=labels)

range_counts = df['price_range'].value_counts().sort_index().reset_index()
range_counts.columns = ['price_range', 'count']
print(range_counts)

plt.figure(figsize=(8, 5))
sns.barplot(data=range_counts, x='price_range', y='count',
            hue='price_range', legend=False)
plt.title('Price range distribution')
plt.xlabel('Price range')
plt.ylabel('Count')
plt.show()

# 19 — Категория с наибольшей суммарной стоимостью
cat_stock = df.groupby('col_7')['total_value'].sum().reset_index()
cat_stock.columns = ['category', 'total_stock_value']
cat_stock = cat_stock.sort_values('total_stock_value', ascending=False)
print(cat_stock)

plt.figure(figsize=(8, 5))
sns.barplot(data=cat_stock, x='category', y='total_stock_value',
            hue='category', legend=False)
plt.title('Total stock value by category')
plt.xlabel('Category')
plt.ylabel('Total value')
plt.show()

# 20 — Средняя цена и средний запас
cat_means = df.groupby('col_7').agg(
    mean_price=('col_2', 'mean'),
    mean_quantity=('col_3', 'mean')
).reset_index()

plt.figure(figsize=(7, 5))
for i, row in cat_means.iterrows():
    plt.scatter(row['mean_price'], row['mean_quantity'], s=120, label=row['col_7'])
    plt.annotate(row['col_7'], (row['mean_price'], row['mean_quantity']),
                 textcoords='offset points', xytext=(6, 4))
plt.title('Mean price vs Mean quantity')
plt.xlabel('Mean price')
plt.ylabel('Mean quantity')
plt.legend()
plt.show()

# 21 — Категории с наибольшим разбросом цены
std_by_cat = df.groupby('col_7')['col_2'].std().reset_index()
std_by_cat.columns = ['category', 'std_price']

plt.figure(figsize=(8, 5))
sns.barplot(data=std_by_cat, y='category', x='std_price',
            hue='category', legend=False)
plt.title('Price std by category')
plt.xlabel('Std price')
plt.ylabel('Category')
plt.show()

# 22 — Товары с нулевым запасом
zero_stock = df[df['col_3'] == 0]
print(zero_stock[['col_1', 'col_7', 'col_2']].head(10))

# 23 — Топ-5 категорий по количеству товаров
cat_count = df.groupby('col_7')['col_1'].count().reset_index()
cat_count.columns = ['category', 'count']
cat_count = cat_count.sort_values('count', ascending=False).head(5)
print(cat_count)

plt.figure(figsize=(8, 5))
sns.barplot(data=cat_count, x='category', y='count',
            hue='category', legend=False)
plt.title('Top 5 categories')
plt.xlabel('Category')
plt.ylabel('Count')
plt.show()

# 24 — Самые популярные товары по запасу
top10_stock = df.sort_values('col_3', ascending=False).head(10)

plt.figure(figsize=(8, 5))
sns.barplot(data=top10_stock, y='col_1', x='col_3',
            hue='col_1', legend=False)
plt.title('Top 10 by stock')
plt.xlabel('Stock')
plt.ylabel('Product')
plt.show()

# 25 — Тепловая карта категорий и диапазонов цены
pivot = df.pivot_table(index='col_7', columns='price_range',
                       values='col_1', aggfunc='count', fill_value=0)

plt.figure(figsize=(10, 6))
sns.heatmap(pivot, annot=True, fmt='d', cmap='Blues')
plt.title('Products by category and price range')
plt.xlabel('Price range')
plt.ylabel('Category')
plt.show()

# 36 — Сравнение категорий по средней цене и запасу
cat_means2 = df.groupby('col_7').agg(
    mean_price=('col_2', 'mean'),
    mean_quantity=('col_3', 'mean')
).reset_index()

plt.figure(figsize=(7, 5))
for i, row in cat_means2.iterrows():
    plt.scatter(row['mean_price'], row['mean_quantity'], s=120, label=row['col_7'])
    plt.annotate(row['col_7'], (row['mean_price'], row['mean_quantity']),
                 textcoords='offset points', xytext=(6, 4))
plt.title('Mean price vs Mean quantity')
plt.xlabel('Mean price')
plt.ylabel('Mean quantity')
plt.legend()
plt.show()

# 37 — Категории с наибольшим разбросом цены
std_by_cat2 = df.groupby('col_7')['col_2'].std().reset_index()
std_by_cat2.columns = ['category', 'std_price']

plt.figure(figsize=(8, 5))
sns.barplot(data=std_by_cat2, y='category', x='std_price',
            hue='category', legend=False)
plt.title('Price std by category')
plt.xlabel('Std price')
plt.ylabel('Category')
plt.show()

# 38 — Фильтрация товаров без запаса
zero_stock2 = df[df['col_3'] == 0]
print(zero_stock2[['col_1', 'col_7', 'col_2']].head(10))

# 39 — Топ-5 категорий по количеству товаров
cat_count2 = df.groupby('col_7')['col_1'].count().reset_index()
cat_count2.columns = ['category', 'count']
cat_count2 = cat_count2.sort_values('count', ascending=False).head(5)

plt.figure(figsize=(8, 5))
sns.barplot(data=cat_count2, x='category', y='count',
            hue='category', legend=False)
plt.title('Top 5 categories')
plt.xlabel('Category')
plt.ylabel('Count')
plt.show()

# 40 — Самые популярные товары по запасу
top10_stock2 = df.sort_values('col_3', ascending=False).head(10)

plt.figure(figsize=(8, 5))
sns.barplot(data=top10_stock2, y='col_1', x='col_3',
            hue='col_1', legend=False)
plt.title('Top 10 by stock')
plt.xlabel('Stock')
plt.ylabel('Product')
plt.show()

# 41 — Тепловая карта категорий и ценовых диапазонов
pivot2 = df.pivot_table(index='col_7', columns='price_range',
                        values='col_1', aggfunc='count', fill_value=0)

plt.figure(figsize=(10, 6))
sns.heatmap(pivot2, annot=True, fmt='d', cmap='Blues')
plt.title('Products by category and price range')
plt.xlabel('Price range')
plt.ylabel('Category')
plt.show()

# 42 — Взаимосвязь цены и рейтинга
sample2 = df.sample(1000, random_state=42)
plt.figure(figsize=(8, 5))
sns.regplot(data=sample2, x='col_2', y='col_5',
            scatter_kws={'alpha': 0.3}, line_kws={'color': 'red'})
plt.title('Price vs Rating')
plt.xlabel('Price')
plt.ylabel('Rating')
plt.show()

# 43 — Парные диаграммы числовых характеристик
pair_df2 = df[['col_2', 'col_3', 'col_5', 'col_6', 'col_7']].sample(500, random_state=42)
sns.pairplot(pair_df2, hue='col_7')
plt.show()

# 44 — Анализ аномальных товаров
mean_col2 = df['col_2'].mean()
std_col2 = df['col_2'].std()
mean_col3 = df['col_3'].mean()
std_col3 = df['col_3'].std()

mask_extreme = (df['col_2'] > mean_col2 + 3 * std_col2) | (df['col_3'] > mean_col3 + 3 * std_col3)
extreme_items = df[mask_extreme]
print(extreme_items[['col_1', 'col_2', 'col_3', 'col_7']].head())

# 45 — Финальный Excel-отчет
save_cols2 = list(df.columns[:50]) + ['total_value', 'double_stock', 'log_price']
df[save_cols2].to_excel('catalog_final_report.xlsx', index=False)
print('Финальный отчет сақталды')