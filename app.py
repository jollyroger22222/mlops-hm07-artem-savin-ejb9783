import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

# Получаем путь к модели из переменной окружения или по умолчанию
MODEL_PATH = os.getenv("MODEL_PATH", "pipeline.joblib")

# Загружаем модель
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Не удалось загрузить модель из {MODEL_PATH}: {e}")

# Инициализируем FastAPI-приложение
app = FastAPI(title="Password Strength Predictor")

# Входная схема
class PasswordRequest(BaseModel):
    passwords: List[str]

# Выходная схема
class PredictionResponse(BaseModel):
    prediction: List[float]

# Эндпоинт для предсказаний
@app.post("/predict", response_model=PredictionResponse)
def predict(request: PasswordRequest):
    predictions = model.predict(request.passwords)
    return {"prediction": predictions.tolist()}


