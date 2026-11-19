import pandas as pd
import json

def explore_data():
    # Load the ingested data
    with open('data/records.json', 'r') as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    print("--- InternGuide Records: 3 Fast Facts ---")

    # Fact 1: Total records count
    print(f"1. Total internship rules/activities recorded: {len(df)}")

    # Fact 2: Most common evaluator
    top_evaluator = df['evaluated_by'].value_counts().index[0]
    print(f"2. The most common evaluator for these activities is: {top_evaluator}")

    # Fact 3: Distribution of credits
    credit_types = df['suggested_credits'].nunique()
    print(f"3. There are {credit_types} different credit structures (including N/A for rules) in the dataset.")

if __name__ == "__main__":
    explore_data()
