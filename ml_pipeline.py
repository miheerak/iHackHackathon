from transformers import pipeline

toxic_model = pipeline("text-classification", model="unitary/toxic-bert")

def analyze_content(content):
    result = toxic_model(content)[0]
    is_flagged = result["label"] == "TOXIC"
    return {"is_flagged": is_flagged, "score": result["score"]}
