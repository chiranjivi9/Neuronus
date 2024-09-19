# Neuronus ML Component - Key Eviction Strategy

This folder contains scripts and data for implementing an ML-based key eviction strategy in Neuronus. The goal is to use machine learning to predict which keys should be evicted based on access patterns and importance.

## Workflow

1. **Generate Data**: 
   - The `generate_entries.py` script simulates random `SET`, `GET`, `DEL`, and `EXPIRE` operations on the Neuronus key-value store.
   - It collects access patterns like access count, last accessed time, and key size into a file (`generated_analytics.json`) for later use in ML models.

2. **Simulate Operations**:
   - Run the script to simulate key operations and generate the dataset for ML preprocessing:
     ```bash
     python src/ml/generate_entries.py
     ```
   - This script will generate 5000 operations by default and save the analytics data in JSON format (`generated_analytics.json`).

3. **Analyze the Generated Data**:
   - The `generated_analytics.json` file contains key access patterns for thousands of key-value operations.
   - You can preprocess this data to train a machine learning model that can predict which keys are least important and should be evicted based on usage.

## Machine Learning Model
