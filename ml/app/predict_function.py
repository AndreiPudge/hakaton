import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import os

def predict()->list[float]:

    # Поднимаемся из app в ml и спускаемся в data
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    
    # Формируем пути
    columns_path = os.path.join(data_dir, 'columns_list.txt')
    model_path = os.path.join(data_dir, 'model.pkl')

    df = pd.read_csv(csv_path, sep = ';')
    df = df.drop(columns=['dt', 'id'])
    def convert_european_number(x):
        if isinstance(x, str):
            # удаляем пробелы
            x_clean = x.replace(' ', '').replace(',', '.')
            # проверяем, можно ли превратить в число
            try:
                return float(x_clean)
            except ValueError:
                return x  # оставляем строку без изменений
        return x

    for col in df.columns:
        df[col] = df[col].apply(convert_european_number)

    for col in df.columns:
        converted = pd.to_numeric(df[col], errors='coerce')
        if converted.notna().sum() == df[col].notna().sum():
            df[col] = converted

    with open(columns_path, 'r', encoding='utf-8') as f:
        columns_array = [line.strip() for line in f]

    df = df[columns_array]
    cat_columns = [i for i in df.columns if df[i].dtype == object]
    le = LabelEncoder()
    for col in cat_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))

    with open(model_path, 'rb') as f:
        loaded_model = pickle.load(f)
    predictions = loaded_model.predict(df)
    return predictions.tolist()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, 'data')
csv_path = os.path.join(data_dir, 'hackathon_income_test.csv')