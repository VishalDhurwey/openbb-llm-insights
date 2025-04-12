from db import get_latest_metrics, save_llm_output, metrics_exist_for_today
from llm_analysis import analyze_with_llm
import fetch_data  # Importing fetch_data script to fetch and insert the data

def run():
    # Step 1: Check if today's metrics exist in the database
    if metrics_exist_for_today():
        print("✅ Metrics for today already exist. Skipping data fetch.")
    else:
        print("📥 Fetching data from OpenBB...")
        # Trigger the fetch_data.py functionality to fetch and insert today's data
        fetch_data  # This runs the entire fetch process from fetch_data.py

    # Step 2: Query today's metrics from the database
    print("📊 Querying today’s metrics...")
    metrics = get_latest_metrics()
    if not metrics:
        print("⚠️ No metrics found for today.")
        return

    # Step 3: Send the metrics to LLM for analysis
    print("🧠 Sending data to LLM for analysis...")
    insights = analyze_with_llm(metrics)

    # Step 4: Parse LLM output into summary and recommendations
    summary, *recs = insights.split("\n\n", 1)
    recommendations = recs[0] if recs else "No recommendations."

    # Step 5: Store the LLM output into the database
    print("💾 Storing LLM recommendations in DB...")
    save_llm_output(summary.strip(), recommendations.strip())

    print("✅ Full pipeline executed successfully!")

if __name__ == "__main__":
    run()
