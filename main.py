import pandas as pd
from sklearn.model_selection import train_test_split

from services.data_cleaner.cleaner_service import Cleaner
from services.model_evaluator.evaluator_service import Evaluator
from services.model_trainer.trainer_model import Trainer_model
from services.prediction_server.predictor_service import Predictor

df = pd.read_csv('Intelligence_Selection.csv')
df = df.dropna()

clean_df = Cleaner(df,"accepted").getData()

# 1. חלוקת הנתונים
train_df, test_df = train_test_split(clean_df, test_size=0.3, random_state=42)

# 2. אימון המודל על 70%
weights, targets_size = Trainer_model(train_df).getWeights()
predictor = Predictor(weights, targets_size)

# 3. בדיקה על 30% מהנתונים
evaluator = Evaluator(test_df, predictor)
metrics = evaluator.evaluate()
print(metrics)
# # 4. הדפסת התוצאות
# print("Evaluation Results:")
# for metric, value in metrics.items():
#     print(f"{metric.capitalize()}: {value}")