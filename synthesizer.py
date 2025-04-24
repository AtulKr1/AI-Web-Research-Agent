def synthesize_information(summaries):
    pros = []
    cons = []
    contradictions = []

    for summary in summaries:
        text = summary.lower()
        if "connect" in text or "benefit" in text or "positive" in text:
            pros.append(summary)
        if "misinformation" in text or "negative" in text or "harm" in text:
            cons.append(summary)

    # Simple contradiction finder
    if pros and cons:
        contradictions.append("Some sources highlight social media's benefits, while others warn of its dangers.")

    # Final synthesis
    final_report = (
        f"**Pros Identified:**\n"
        + "\n".join(f"- {p}" for p in pros[:3]) + "\n\n"
        f"**Cons Identified:**\n"
        + "\n".join(f"- {c}" for c in cons[:3]) + "\n\n"
        f"**Contradictions:**\n"
        + "\n".join(f"- {c}" for c in contradictions) + "\n\n"
        f"**Conclusion:**\nSocial media has both advantages and disadvantages. It’s essential to use it wisely, staying informed and mindful of its effects on individuals and society."
    )
    return final_report
