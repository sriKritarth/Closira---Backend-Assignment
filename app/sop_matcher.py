SOPS = [
    (
        "pricing_enquiry",
        ["price", "pricing", "cost", "how much", "quote", "rates"],
        "Thanks for your interest! Our plans start at ₹999/month..."
    ),
    (
        "booking_enquiry",
        ["book", "appointment", "schedule", "slot", "demo", "meeting"],
        "We'd love to set up a time! Let me check available slots..."
    ),
    (
        "complaint",
        ["complaint", "unhappy", "angry", "issue", "problem", "refund", "disappointed"],
        "We sincerely apologise. A senior agent will reach out shortly..."
    ),
    (
        "after_hours",
        ["tonight", "weekend", "sunday", "saturday", "after hours", "closed"],
        "Our team is offline but will respond first thing tomorrow..."
    ),
    (
        "general_support",
        ["help", "support", "question", "info", "how"],
        "Thanks for reaching out! An agent will respond within 2 hours..."
    ),
]


def match_sop(in_msg : str):
    in_msg = in_msg.strip().lower()

    for keys in SOPS:
        sop_name = keys[0]
        keyword_list = keys[1]
        suggested_response = keys[2]

        for matched_key in keyword_list:
            if matched_key in in_msg:
                return {
                    "matched_sop": sop_name,
                    "suggested_response": suggested_response,
                    "matched_keyword": matched_key
                }

    return None 
   