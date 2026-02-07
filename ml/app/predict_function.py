import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
import os
from config.config import settings as s


def predict(client_id: int)->float:

    df = pd.read_csv(s.csv_data_path, sep = ';')
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

    with open(s.columns_list_path, 'r', encoding='utf-8') as f:
        columns_array = [line.strip() for line in f]

    df = df[columns_array]
    cat_columns = [i for i in df.columns if df[i].dtype == object]
    le = LabelEncoder()
    for col in cat_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))

    with open(s.model_path, 'rb') as f:
        loaded_model = pickle.load(f)
    predictions = loaded_model.predict(df)

    if client_id < 0 or client_id >= len(predictions):
        raise ValueError("Invalid client_id")

    return float(predictions[client_id])
