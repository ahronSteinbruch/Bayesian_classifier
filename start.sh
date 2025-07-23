#!/bin/bash

# This script launches all the microservices required for the application
# inside a single container.

# Start the Data Cleaner service in the background
echo "Starting Data Cleaner service on port 8001..."
uvicorn services.data_cleaner.cleaner_controller:app --host 0.0.0.0 --port 8001 &

# Start the Model Trainer service in the background
echo "Starting Model Trainer service on port 8002..."
uvicorn services.model_trainer.trainer_controller:app --host 0.0.0.0 --port 8002 &

# Start the Prediction Server service in the background
echo "Starting Prediction Server service on port 8003..."
uvicorn services.prediction_server.predictor_controller:app --host 0.0.0.0 --port 8003 &

# Start the Model Evaluator service in the background
echo "Starting Model Evaluator service on port 8004..."
uvicorn services.model_evaluator.evaluator_controller:app --host 0.0.0.0 --port 8004 &

# Start the Result Cache service in the background
echo "Starting Result Cache service on port 8005..."
uvicorn services.result_cache.cache_controller:app --host 0.0.0.0 --port 8005 &

# Wait for a few seconds to ensure the background services have time to initialize
echo "Waiting for services to start..."
sleep 5

# Start the Orchestrator service in the foreground.
# This will be the main public-facing entry point and will keep the container running.
echo "Starting Orchestrator service on port 80..."
uvicorn services.orchestrator.orchestrator_controller:app --host 0.0.0.0 --port 80