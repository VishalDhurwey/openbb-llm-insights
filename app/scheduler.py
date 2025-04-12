from db import get_latest_metrics, save_llm_output
from llm_analysis import analyze_with_llm

def run():
    print("📊 Fetching today's metrics...")
    metrics = get_latest_metrics()
    if not metrics:
        print("⚠️ No metrics found for today.")
        return

    print("🧠 Sending data to LLM...")
    insights = analyze_with_llm(metrics)

    summary, *recs = insights.split("\n\n", 1)
    recommendations = recs[0] if recs else ""

    print("💾 Storing insights in DB...")
    save_llm_output(summary.strip(), recommendations.strip())
    print("✅ Done!")

if __name__ == "__main__":
    run()
