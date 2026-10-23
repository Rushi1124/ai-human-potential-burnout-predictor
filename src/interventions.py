def recommend_actions(answers):
    """Return general, optional suggestions based on self-reported answers."""
    actions = []

    if answers["sleep_hours"] < 7:
        actions.append(
            "Rest: consider protecting a consistent sleep window and leaving enough time to wind down."
        )
    if answers["workload_hours"] >= 9:
        actions.append(
            "Workload: identify one task to postpone, delegate, or break into smaller steps."
        )
    if answers["stress"] >= 7:
        actions.append(
            "Stress: take a brief pause, try slow breathing, or talk with someone you trust."
        )
    if answers["motivation"] <= 4:
        actions.append(
            "Motivation: choose one small, realistic task to begin with instead of planning everything at once."
        )
    if answers["focus"] <= 4:
        actions.append(
            "Focus: try one short distraction-reduced work session, followed by a break."
        )
    if answers["work_life_balance"] <= 4:
        actions.append(
            "Boundaries: schedule time away from work or study and review whether your commitments are manageable."
        )
    if answers["exercise_days"] == 0:
        actions.append(
            "Movement: if suitable for you, consider adding a short walk or gentle movement break."
        )
    if not actions:
        actions.append(
            "Maintenance: keep reviewing what helps you rest, focus, and recover; small adjustments are optional."
        )

    actions.append(
        "Support: if stress or exhaustion persists or affects daily life, consider speaking with a trusted person or qualified professional."
    )
    return actions
