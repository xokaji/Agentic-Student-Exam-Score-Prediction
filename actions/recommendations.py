def get_recommendation(decision: str):
    if decision == "INTENSIVE_SUPPORT":
        return "Increase daily study time and attend remedial classes."
    elif decision == "IMPROVEMENT_PLAN":
        return "Focus on weak areas and practice regularly."
    elif decision == "ADVANCED_TRACK":
        return "Attempt advanced problems and mentor peers."
    else:
        return "No recommendation available."
