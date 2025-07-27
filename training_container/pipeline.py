import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException

from cleaner import DataCleaner
from trainer import ModelTrainer
from evaluator import ModelEvaluator
from dataLoader import DataLoader
app = FastAPI()

@app.get("/reload_model")
def run_training_pipeline(file_path='Intelligence_Selection.csv'):
    print(f"\n--- Starting Pipeline for: {file_path} ---", flush=True)
    data_loader = DataLoader()
    cleaner = DataCleaner()
    trainer = ModelTrainer()
    evaluator = ModelEvaluator()
    try:

        full_df = data_loader.load_data(file_path)
        cleaned_df = cleaner.clean(full_df)
        train_df = cleaned_df.sample(frac=0.7, random_state=42)
        test_df = cleaned_df.drop(train_df.index)
        model = trainer.train(train_df)
        evaluation = evaluator.evaluate(model, test_df)
        print("\n--- Pipeline Complete ---", flush=True)
        print(f"Evaluation: {evaluation}", flush=True)
        return {"model": model, "evaluation": evaluation}
    except FileNotFoundError as e:
        print(f"PIPELINE FAILED: {e}", flush=True)
        raise HTTPException(status_code=404, detail=f"Data file not found: {file_path}")
    except Exception as e:
        print(f"PIPELINE FAILED: {e}", flush=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred in the training pipeline: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)