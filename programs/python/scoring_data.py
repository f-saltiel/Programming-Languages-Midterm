"""
scoring_data.py

Data and helper functions for the Air Force PFRA Score Estimator.

This file supports:
- 1-minute push-ups
- 1-minute sit-ups
- 2-mile run
- Waist-to-height ratio (WHtR)
"""

PASSING_SCORE = 75.0
EXCELLENT_SCORE = 90.0


AGE_GROUPS = {
    "under_25": "Under 25",
    "25_29": "25-29",
    "30_34": "30-34",
    "35_39": "35-39"
}


GENDERS = {
    "male": "Male",
    "female": "Female"
}


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def time_to_seconds(time_string):
    """
    Converts a run time string in MM:SS format into total seconds.

    Example:
    "13:45" -> 825
    """
    minutes, seconds = time_string.strip().split(":")
    return int(minutes) * 60 + int(seconds)


def calculate_wht_ratio(waist, height):
    """
    Calculates waist-to-height ratio.

    Waist and height must use the same unit.
    Example:
    waist = 32 inches
    height = 70 inches
    WHtR = 32 / 70 = 0.46
    """
    if height <= 0:
        raise ValueError("Height must be greater than zero.")

    return round(waist / height, 2)


def score_repetition_component(reps, standards):
    """
    Scores push-ups or sit-ups.

    standards format:
    [
        {"min_reps": 60, "points": 15.0},
        {"min_reps": 59, "points": 14.8},
        ...
    ]

    The function returns the highest point value where reps >= min_reps.
    """
    for row in standards:
        if reps >= row["min_reps"]:
            return row["points"]

    return 0.0


def score_run_component(run_time, standards):
    """
    Scores the 2-mile run.

    run_time format:
    "MM:SS"

    standards format:
    [
        {"max_time": "13:25", "points": 50.0},
        {"max_time": "13:55", "points": 49.4},
        ...
    ]

    The function returns the highest point value where run_time <= max_time.
    """
    user_seconds = time_to_seconds(run_time)

    for row in standards:
        standard_seconds = time_to_seconds(row["max_time"])

        if user_seconds <= standard_seconds:
            return row["points"]

    return 0.0


def score_wht_component(waist, height):
    """
    Scores waist-to-height ratio.

    Waist and height must use the same unit.

    The official chart scores WHtR as a 20-point component.
    Lower WHtR is better.
    """
    ratio = calculate_wht_ratio(waist, height)

    for row in WHTR_STANDARDS:
        if ratio <= row["max_ratio"]:
            return {
                "ratio": ratio,
                "points": row["points"],
                "risk_category": row["risk_category"]
            }

    return {
        "ratio": ratio,
        "points": 0.0,
        "risk_category": "High Risk"
    }


def get_score_category(total_score):
    """
    Returns the composite score category.
    """
    if total_score >= EXCELLENT_SCORE:
        return "Excellent"
    elif total_score >= PASSING_SCORE:
        return "Satisfactory"
    else:
        return "Unsatisfactory"


def get_component_warnings(pushup_score, situp_score, run_score, wht_score):
    """
    Returns warnings for components that scored zero points.

    This helps flag possible minimum component failures.
    """
    warnings = []

    if pushup_score <= 0:
        warnings.append("Push-up score is below the minimum scoring value.")

    if situp_score <= 0:
        warnings.append("Sit-up score is below the minimum scoring value.")

    if run_score <= 0:
        warnings.append("Run score is below the minimum scoring value.")

    if wht_score <= 0:
        warnings.append("Waist-to-height ratio scored zero points.")

    return warnings


def calculate_pfra_score(gender, age_group, pushups, situps, run_time, waist, height):
    """
    Calculates the total PFRA score using:
    - gender
    - age group
    - push-up count
    - sit-up count
    - 2-mile run time
    - waist measurement
    - height measurement

    Waist and height must use the same unit.
    """
    table = SCORE_TABLES[gender][age_group]

    pushup_score = score_repetition_component(pushups, table["pushups"])
    situp_score = score_repetition_component(situps, table["situps"])
    run_score = score_run_component(run_time, table["run"])

    wht_result = score_wht_component(waist, height)
    wht_score = wht_result["points"]

    total_score = round(
        pushup_score + situp_score + run_score + wht_score,
        1
    )

    category = get_score_category(total_score)
    warnings = get_component_warnings(
        pushup_score,
        situp_score,
        run_score,
        wht_score
    )

    passed = total_score >= PASSING_SCORE and len(warnings) == 0

    return {
        "gender": GENDERS[gender],
        "age_group": AGE_GROUPS[age_group],
        "pushups": pushups,
        "situps": situps,
        "run_time": run_time,
        "waist": waist,
        "height": height,
        "wht_ratio": wht_result["ratio"],
        "wht_risk_category": wht_result["risk_category"],
        "pushup_score": pushup_score,
        "situp_score": situp_score,
        "run_score": run_score,
        "wht_score": wht_score,
        "total_score": total_score,
        "category": category,
        "passed": passed,
        "warnings": warnings
    }


# ---------------------------------------------------------------------------
# WAIST-TO-HEIGHT RATIO SCORING TABLE
# ---------------------------------------------------------------------------
# The WHtR scoring table appears as a separate 20-point component.
# It is stored globally because the same WHtR scoring values apply to all.

WHTR_STANDARDS = [
    {"max_ratio": 0.49, "risk_category": "Low Risk", "points": 20.0},
    {"max_ratio": 0.50, "risk_category": "Moderate Risk", "points": 19.0},
    {"max_ratio": 0.51, "risk_category": "Moderate Risk", "points": 18.0},
    {"max_ratio": 0.52, "risk_category": "Moderate Risk", "points": 17.0},
    {"max_ratio": 0.53, "risk_category": "Moderate Risk", "points": 16.0},
    {"max_ratio": 0.54, "risk_category": "Moderate Risk", "points": 15.0},
    {"max_ratio": 0.55, "risk_category": "High Risk", "points": 12.5},
    {"max_ratio": 0.56, "risk_category": "High Risk", "points": 10.0},
    {"max_ratio": 0.57, "risk_category": "High Risk", "points": 7.5},
    {"max_ratio": 0.58, "risk_category": "High Risk", "points": 5.0},
    {"max_ratio": 0.59, "risk_category": "High Risk", "points": 2.5},
    {"max_ratio": 999.0, "risk_category": "High Risk", "points": 0.0}
]


# ---------------------------------------------------------------------------
# SCORING TABLES
# ---------------------------------------------------------------------------
# Scoring breakdown:
#
# Cardiorespiratory:
#   2-mile run = up to 50 points
#
# Muscular fitness:
#   1-minute push-ups = up to 15 points
#   1-minute sit-ups = up to 15 points
#
# Body composition:
#   Waist-to-height ratio = up to 20 points
#
# Total possible score:
#   50 + 15 + 15 + 20 = 100 points
# ---------------------------------------------------------------------------

SCORE_TABLES = {
    "male": {
        "under_25": {
            "pushups": [
                {"min_reps": 67, "points": 15.0},
                {"min_reps": 66, "points": 14.9},
                {"min_reps": 65, "points": 14.7},
                {"min_reps": 64, "points": 14.6},
                {"min_reps": 63, "points": 14.4},
                {"min_reps": 62, "points": 14.3},
                {"min_reps": 61, "points": 14.1},
                {"min_reps": 60, "points": 14.0},
                {"min_reps": 59, "points": 13.8},
                {"min_reps": 58, "points": 13.7},
                {"min_reps": 57, "points": 13.5},
                {"min_reps": 56, "points": 13.4},
                {"min_reps": 55, "points": 13.2},
                {"min_reps": 54, "points": 13.1},
                {"min_reps": 53, "points": 12.9},
                {"min_reps": 52, "points": 12.8},
                {"min_reps": 51, "points": 12.6},
                {"min_reps": 50, "points": 12.5},
                {"min_reps": 49, "points": 12.3},
                {"min_reps": 48, "points": 12.2},
                {"min_reps": 47, "points": 12.0},
                {"min_reps": 46, "points": 11.7},
                {"min_reps": 45, "points": 11.6},
                {"min_reps": 44, "points": 11.3},
                {"min_reps": 43, "points": 11.0},
                {"min_reps": 42, "points": 10.8},
                {"min_reps": 41, "points": 10.5},
                {"min_reps": 40, "points": 10.2},
                {"min_reps": 39, "points": 9.8},
                {"min_reps": 38, "points": 9.5},
                {"min_reps": 37, "points": 9.0},
                {"min_reps": 36, "points": 8.7},
                {"min_reps": 35, "points": 8.3},
                {"min_reps": 34, "points": 8.0},
                {"min_reps": 33, "points": 7.5},
                {"min_reps": 32, "points": 5.3},
                {"min_reps": 31, "points": 3.0},
                {"min_reps": 30, "points": 0.8}
            ],

            "situps": [
                {"min_reps": 58, "points": 15.0},
                {"min_reps": 57, "points": 14.8},
                {"min_reps": 56, "points": 14.6},
                {"min_reps": 55, "points": 14.3},
                {"min_reps": 54, "points": 14.1},
                {"min_reps": 53, "points": 13.8},
                {"min_reps": 52, "points": 13.5},
                {"min_reps": 51, "points": 13.2},
                {"min_reps": 50, "points": 13.1},
                {"min_reps": 49, "points": 12.8},
                {"min_reps": 48, "points": 12.5},
                {"min_reps": 47, "points": 12.0},
                {"min_reps": 46, "points": 11.3},
                {"min_reps": 45, "points": 10.5},
                {"min_reps": 44, "points": 9.8},
                {"min_reps": 43, "points": 9.5},
                {"min_reps": 42, "points": 9.0},
                {"min_reps": 41, "points": 6.8},
                {"min_reps": 40, "points": 4.5},
                {"min_reps": 39, "points": 2.3}
            ],

            "run": [
                {"max_time": "13:25", "points": 50.0},
                {"max_time": "13:55", "points": 49.4},
                {"max_time": "14:12", "points": 48.8},
                {"max_time": "14:27", "points": 48.1},
                {"max_time": "14:41", "points": 47.5},
                {"max_time": "15:05", "points": 46.9},
                {"max_time": "15:17", "points": 46.3},
                {"max_time": "15:28", "points": 45.6},
                {"max_time": "15:38", "points": 45.0},
                {"max_time": "16:09", "points": 43.9},
                {"max_time": "16:29", "points": 42.9},
                {"max_time": "16:49", "points": 41.8},
                {"max_time": "17:08", "points": 40.7},
                {"max_time": "17:18", "points": 39.6},
                {"max_time": "17:37", "points": 38.6},
                {"max_time": "17:55", "points": 37.5},
                {"max_time": "18:23", "points": 35.5},
                {"max_time": "18:39", "points": 34.0},
                {"max_time": "19:07", "points": 32.5},
                {"max_time": "19:36", "points": 31.0},
                {"max_time": "19:45", "points": 29.5}
            ]
        },

        "25_29": {
            "pushups": [
                {"min_reps": 62, "points": 15.0},
                {"min_reps": 61, "points": 14.8},
                {"min_reps": 60, "points": 14.6},
                {"min_reps": 59, "points": 14.3},
                {"min_reps": 58, "points": 14.1},
                {"min_reps": 57, "points": 14.0},
                {"min_reps": 56, "points": 13.8},
                {"min_reps": 55, "points": 13.7},
                {"min_reps": 54, "points": 13.5},
                {"min_reps": 53, "points": 13.4},
                {"min_reps": 52, "points": 13.2},
                {"min_reps": 51, "points": 13.1},
                {"min_reps": 50, "points": 13.0},
                {"min_reps": 49, "points": 12.9},
                {"min_reps": 48, "points": 12.8},
                {"min_reps": 47, "points": 12.6},
                {"min_reps": 46, "points": 12.5},
                {"min_reps": 45, "points": 12.2},
                {"min_reps": 44, "points": 12.0},
                {"min_reps": 43, "points": 11.7},
                {"min_reps": 42, "points": 11.6},
                {"min_reps": 41, "points": 11.3},
                {"min_reps": 40, "points": 11.0},
                {"min_reps": 39, "points": 10.8},
                {"min_reps": 38, "points": 10.5},
                {"min_reps": 37, "points": 10.2},
                {"min_reps": 36, "points": 9.8},
                {"min_reps": 35, "points": 9.5},
                {"min_reps": 34, "points": 9.0},
                {"min_reps": 33, "points": 8.7},
                {"min_reps": 32, "points": 8.3},
                {"min_reps": 31, "points": 8.0},
                {"min_reps": 30, "points": 7.5},
                {"min_reps": 29, "points": 5.3},
                {"min_reps": 28, "points": 3.0},
                {"min_reps": 27, "points": 0.8}
            ],

            "situps": [
                {"min_reps": 56, "points": 15.0},
                {"min_reps": 55, "points": 14.6},
                {"min_reps": 54, "points": 14.3},
                {"min_reps": 53, "points": 14.1},
                {"min_reps": 52, "points": 13.8},
                {"min_reps": 51, "points": 13.5},
                {"min_reps": 50, "points": 13.2},
                {"min_reps": 49, "points": 13.1},
                {"min_reps": 48, "points": 12.8},
                {"min_reps": 47, "points": 12.5},
                {"min_reps": 45, "points": 11.3},
                {"min_reps": 44, "points": 10.5},
                {"min_reps": 43, "points": 9.8},
                {"min_reps": 42, "points": 9.5},
                {"min_reps": 40, "points": 6.8},
                {"min_reps": 39, "points": 4.5},
                {"min_reps": 38, "points": 2.3}
            ],

            "run": [
                {"max_time": "13:25", "points": 50.0},
                {"max_time": "13:55", "points": 49.4},
                {"max_time": "14:12", "points": 48.8},
                {"max_time": "14:27", "points": 48.1},
                {"max_time": "14:41", "points": 47.5},
                {"max_time": "15:05", "points": 46.9},
                {"max_time": "15:17", "points": 46.3},
                {"max_time": "15:28", "points": 45.6},
                {"max_time": "15:38", "points": 45.0},
                {"max_time": "16:14", "points": 43.9},
                {"max_time": "16:33", "points": 42.9},
                {"max_time": "16:52", "points": 41.8},
                {"max_time": "17:12", "points": 40.7},
                {"max_time": "17:30", "points": 39.6},
                {"max_time": "17:47", "points": 38.6},
                {"max_time": "18:04", "points": 37.5},
                {"max_time": "18:23", "points": 35.5},
                {"max_time": "18:39", "points": 34.0},
                {"max_time": "19:15", "points": 32.5},
                {"max_time": "19:30", "points": 31.0},
                {"max_time": "19:45", "points": 29.5}
            ]
        },

        "30_34": {
            "pushups": [
                {"min_reps": 57, "points": 15.0},
                {"min_reps": 56, "points": 14.9},
                {"min_reps": 55, "points": 14.7},
                {"min_reps": 54, "points": 14.6},
                {"min_reps": 53, "points": 14.4},
                {"min_reps": 52, "points": 14.3},
                {"min_reps": 51, "points": 14.1},
                {"min_reps": 50, "points": 14.0},
                {"min_reps": 49, "points": 13.9},
                {"min_reps": 48, "points": 13.8},
                {"min_reps": 47, "points": 13.7},
                {"min_reps": 46, "points": 13.5},
                {"min_reps": 45, "points": 13.4},
                {"min_reps": 44, "points": 13.2},
                {"min_reps": 43, "points": 13.1},
                {"min_reps": 42, "points": 12.9},
                {"min_reps": 41, "points": 12.8},
                {"min_reps": 40, "points": 12.5},
                {"min_reps": 39, "points": 12.0},
                {"min_reps": 38, "points": 11.7},
                {"min_reps": 37, "points": 11.6},
                {"min_reps": 36, "points": 11.3},
                {"min_reps": 35, "points": 11.0},
                {"min_reps": 34, "points": 10.5},
                {"min_reps": 33, "points": 10.2},
                {"min_reps": 32, "points": 10.1},
                {"min_reps": 31, "points": 9.8},
                {"min_reps": 30, "points": 9.0},
                {"min_reps": 29, "points": 8.3},
                {"min_reps": 28, "points": 8.0},
                {"min_reps": 27, "points": 7.5},
                {"min_reps": 26, "points": 5.3},
                {"min_reps": 25, "points": 3.0},
                {"min_reps": 24, "points": 0.8}
            ],

            "situps": [
                {"min_reps": 54, "points": 15.0},
                {"min_reps": 53, "points": 14.8},
                {"min_reps": 52, "points": 14.6},
                {"min_reps": 51, "points": 14.3},
                {"min_reps": 50, "points": 14.1},
                {"min_reps": 49, "points": 13.8},
                {"min_reps": 48, "points": 13.5},
                {"min_reps": 47, "points": 13.2},
                {"min_reps": 46, "points": 13.1},
                {"min_reps": 45, "points": 12.8},
                {"min_reps": 44, "points": 12.5},
                {"min_reps": 43, "points": 12.0},
                {"min_reps": 42, "points": 11.3},
                {"min_reps": 41, "points": 10.5},
                {"min_reps": 40, "points": 9.8},
                {"min_reps": 39, "points": 9.0},
                {"min_reps": 38, "points": 6.8},
                {"min_reps": 37, "points": 4.5},
                {"min_reps": 36, "points": 2.3}
            ],

            "run": [
                {"max_time": "13:42", "points": 50.0},
                {"max_time": "14:23", "points": 49.4},
                {"max_time": "14:37", "points": 48.8},
                {"max_time": "14:49", "points": 48.1},
                {"max_time": "15:01", "points": 47.5},
                {"max_time": "15:23", "points": 46.9},
                {"max_time": "15:33", "points": 46.3},
                {"max_time": "15:43", "points": 45.6},
                {"max_time": "15:50", "points": 45.0},
                {"max_time": "16:12", "points": 43.9},
                {"max_time": "16:30", "points": 42.9},
                {"max_time": "16:49", "points": 41.8},
                {"max_time": "17:07", "points": 40.7},
                {"max_time": "17:26", "points": 39.6},
                {"max_time": "17:42", "points": 38.6},
                {"max_time": "17:58", "points": 37.5},
                {"max_time": "18:30", "points": 35.5},
                {"max_time": "19:06", "points": 34.0},
                {"max_time": "19:34", "points": 32.5},
                {"max_time": "20:06", "points": 31.0},
                {"max_time": "20:44", "points": 29.5}
            ]
        },

        "35_39": {
            "pushups": [
                {"min_reps": 51, "points": 15.0},
                {"min_reps": 50, "points": 14.6},
                {"min_reps": 49, "points": 14.3},
                {"min_reps": 48, "points": 14.1},
                {"min_reps": 47, "points": 14.0},
                {"min_reps": 46, "points": 13.9},
                {"min_reps": 45, "points": 13.8},
                {"min_reps": 44, "points": 13.7},
                {"min_reps": 43, "points": 13.5},
                {"min_reps": 42, "points": 13.4},
                {"min_reps": 41, "points": 13.2},
                {"min_reps": 40, "points": 13.1},
                {"min_reps": 39, "points": 12.9},
                {"min_reps": 38, "points": 12.8},
                {"min_reps": 37, "points": 12.5},
                {"min_reps": 36, "points": 12.0},
                {"min_reps": 35, "points": 11.7},
                {"min_reps": 34, "points": 11.6},
                {"min_reps": 33, "points": 11.3},
                {"min_reps": 32, "points": 11.0},
                {"min_reps": 31, "points": 10.5},
                {"min_reps": 30, "points": 10.2},
                {"min_reps": 29, "points": 10.1},
                {"min_reps": 28, "points": 9.8},
                {"min_reps": 27, "points": 9.0},
                {"min_reps": 26, "points": 8.3},
                {"min_reps": 25, "points": 8.0},
                {"min_reps": 24, "points": 7.5},
                {"min_reps": 23, "points": 5.3},
                {"min_reps": 22, "points": 3.0},
                {"min_reps": 21, "points": 0.8}
            ],

            "situps": [
                {"min_reps": 52, "points": 15.0},
                {"min_reps": 51, "points": 14.8},
                {"min_reps": 50, "points": 14.6},
                {"min_reps": 49, "points": 14.3},
                {"min_reps": 48, "points": 14.1},
                {"min_reps": 47, "points": 13.8},
                {"min_reps": 46, "points": 13.5},
                {"min_reps": 45, "points": 13.2},
                {"min_reps": 44, "points": 13.1},
                {"min_reps": 43, "points": 12.8},
                {"min_reps": 42, "points": 12.5},
                {"min_reps": 41, "points": 12.0},
                {"min_reps": 40, "points": 11.3},
                {"min_reps": 39, "points": 10.5},
                {"min_reps": 38, "points": 9.8},
                {"min_reps": 37, "points": 9.0},
                {"min_reps": 36, "points": 6.8},
                {"min_reps": 35, "points": 4.5},
                {"min_reps": 34, "points": 2.3}
            ],

            "run": [
                {"max_time": "13:42", "points": 50.0},
                {"max_time": "14:32", "points": 49.4},
                {"max_time": "14:46", "points": 48.8},
                {"max_time": "14:59", "points": 48.1},
                {"max_time": "15:10", "points": 47.5},
                {"max_time": "15:32", "points": 46.9},
                {"max_time": "15:42", "points": 46.3},
                {"max_time": "15:52", "points": 45.6},
                {"max_time": "16:01", "points": 45.0},
                {"max_time": "16:29", "points": 43.9},
                {"max_time": "16:48", "points": 42.9},
                {"max_time": "17:06", "points": 41.8},
                {"max_time": "17:24", "points": 40.7},
                {"max_time": "17:41", "points": 39.6},
                {"max_time": "17:58", "points": 38.6},
                {"max_time": "18:14", "points": 37.5},
                {"max_time": "18:35", "points": 35.5},
                {"max_time": "19:04", "points": 34.0},
                {"max_time": "19:31", "points": 32.5},
                {"max_time": "20:12", "points": 31.0},
                {"max_time": "20:44", "points": 29.5}
            ]
        }
    },

    "female": {
        "under_25": {
            "pushups": [
                {"min_reps": 47, "points": 15.0},
                {"min_reps": 46, "points": 14.9},
                {"min_reps": 45, "points": 14.7},
                {"min_reps": 44, "points": 14.6},
                {"min_reps": 43, "points": 14.4},
                {"min_reps": 42, "points": 14.3},
                {"min_reps": 41, "points": 14.1},
                {"min_reps": 40, "points": 14.0},
                {"min_reps": 39, "points": 13.8},
                {"min_reps": 38, "points": 13.7},
                {"min_reps": 37, "points": 13.5},
                {"min_reps": 36, "points": 13.4},
                {"min_reps": 35, "points": 13.2},
                {"min_reps": 34, "points": 12.9},
                {"min_reps": 33, "points": 12.8},
                {"min_reps": 32, "points": 12.6},
                {"min_reps": 31, "points": 12.5},
                {"min_reps": 30, "points": 12.3},
                {"min_reps": 29, "points": 12.2},
                {"min_reps": 28, "points": 12.0},
                {"min_reps": 27, "points": 11.3},
                {"min_reps": 26, "points": 11.0},
                {"min_reps": 25, "points": 10.8},
                {"min_reps": 24, "points": 10.5},
                {"min_reps": 23, "points": 9.8},
                {"min_reps": 22, "points": 9.5},
                {"min_reps": 21, "points": 9.0},
                {"min_reps": 20, "points": 8.7},
                {"min_reps": 19, "points": 8.3},
                {"min_reps": 18, "points": 7.5},
                {"min_reps": 17, "points": 5.3},
                {"min_reps": 16, "points": 3.0},
                {"min_reps": 15, "points": 0.8}
            ],

            "situps": [
                {"min_reps": 54, "points": 15.0},
                {"min_reps": 53, "points": 14.8},
                {"min_reps": 52, "points": 14.6},
                {"min_reps": 51, "points": 14.3},
                {"min_reps": 50, "points": 14.1},
                {"min_reps": 49, "points": 13.5},
                {"min_reps": 48, "points": 13.4},
                {"min_reps": 47, "points": 13.2},
                {"min_reps": 46, "points": 12.9},
                {"min_reps": 45, "points": 12.8},
                {"min_reps": 44, "points": 12.0},
                {"min_reps": 43, "points": 11.7},
                {"min_reps": 42, "points": 11.3},
                {"min_reps": 41, "points": 10.5},
                {"min_reps": 40, "points": 10.2},
                {"min_reps": 39, "points": 9.8},
                {"min_reps": 38, "points": 9.0},
                {"min_reps": 37, "points": 6.8},
                {"min_reps": 36, "points": 4.5},
                {"min_reps": 35, "points": 2.3}
            ],

            "run": [
                {"max_time": "15:30", "points": 50.0},
                {"max_time": "15:55", "points": 49.4},
                {"max_time": "16:00", "points": 48.8},
                {"max_time": "16:04", "points": 48.1},
                {"max_time": "16:27", "points": 47.5},
                {"max_time": "17:03", "points": 46.9},
                {"max_time": "17:17", "points": 46.3},
                {"max_time": "17:31", "points": 45.6},
                {"max_time": "17:44", "points": 45.0},
                {"max_time": "18:18", "points": 43.9},
                {"max_time": "18:38", "points": 42.9},
                {"max_time": "18:58", "points": 41.8},
                {"max_time": "19:16", "points": 40.7},
                {"max_time": "19:34", "points": 39.6},
                {"max_time": "19:52", "points": 38.6},
                {"max_time": "20:12", "points": 37.5},
                {"max_time": "20:57", "points": 35.5},
                {"max_time": "21:40", "points": 34.0},
                {"max_time": "22:07", "points": 32.5},
                {"max_time": "22:37", "points": 31.0},
                {"max_time": "22:45", "points": 29.5}
            ]
        },

        "25_29": {
            "pushups": [
                {"min_reps": 47, "points": 15.0},
                {"min_reps": 46, "points": 14.9},
                {"min_reps": 45, "points": 14.7},
                {"min_reps": 44, "points": 14.6},
                {"min_reps": 43, "points": 14.4},
                {"min_reps": 42, "points": 14.3},
                {"min_reps": 41, "points": 14.1},
                {"min_reps": 40, "points": 14.0},
                {"min_reps": 39, "points": 13.8},
                {"min_reps": 38, "points": 13.7},
                {"min_reps": 37, "points": 13.5},
                {"min_reps": 36, "points": 13.4},
                {"min_reps": 35, "points": 13.2},
                {"min_reps": 34, "points": 12.9},
                {"min_reps": 33, "points": 12.8},
                {"min_reps": 32, "points": 12.6},
                {"min_reps": 31, "points": 12.5},
                {"min_reps": 30, "points": 12.3},
                {"min_reps": 29, "points": 12.2},
                {"min_reps": 28, "points": 12.0},
                {"min_reps": 27, "points": 11.3},
                {"min_reps": 26, "points": 11.0},
                {"min_reps": 25, "points": 10.8},
                {"min_reps": 24, "points": 10.5},
                {"min_reps": 23, "points": 9.8},
                {"min_reps": 22, "points": 9.5},
                {"min_reps": 21, "points": 9.0},
                {"min_reps": 20, "points": 8.7},
                {"min_reps": 19, "points": 8.3},
                {"min_reps": 18, "points": 8.0},
                {"min_reps": 17, "points": 7.5},
                {"min_reps": 16, "points": 5.3},
                {"min_reps": 15, "points": 3.0},
                {"min_reps": 14, "points": 0.8}
            ],

            "situps": [
                {"min_reps": 50, "points": 15.0},
                {"min_reps": 49, "points": 14.6},
                {"min_reps": 48, "points": 14.3},
                {"min_reps": 47, "points": 14.1},
                {"min_reps": 46, "points": 13.5},
                {"min_reps": 45, "points": 13.4},
                {"min_reps": 44, "points": 12.9},
                {"min_reps": 43, "points": 12.8},
                {"min_reps": 42, "points": 12.0},
                {"min_reps": 41, "points": 11.7},
                {"min_reps": 40, "points": 11.3},
                {"min_reps": 39, "points": 11.0},
                {"min_reps": 38, "points": 10.5},
                {"min_reps": 37, "points": 10.2},
                {"min_reps": 36, "points": 9.8},
                {"min_reps": 35, "points": 9.5},
                {"min_reps": 34, "points": 9.0},
                {"min_reps": 33, "points": 6.8},
                {"min_reps": 32, "points": 4.5},
                {"min_reps": 31, "points": 2.3}
            ],

            "run": [
                {"max_time": "15:30", "points": 50.0},
                {"max_time": "15:55", "points": 49.4},
                {"max_time": "16:00", "points": 48.8},
                {"max_time": "16:04", "points": 48.1},
                {"max_time": "16:27", "points": 47.5},
                {"max_time": "17:03", "points": 46.9},
                {"max_time": "17:17", "points": 46.3},
                {"max_time": "17:31", "points": 45.6},
                {"max_time": "17:44", "points": 45.0},
                {"max_time": "18:40", "points": 43.9},
                {"max_time": "18:59", "points": 42.9},
                {"max_time": "19:18", "points": 41.8},
                {"max_time": "19:36", "points": 40.7},
                {"max_time": "19:53", "points": 39.6},
                {"max_time": "20:10", "points": 38.6},
                {"max_time": "20:26", "points": 37.5},
                {"max_time": "20:58", "points": 35.5},
                {"max_time": "21:23", "points": 34.0},
                {"max_time": "21:49", "points": 32.5},
                {"max_time": "22:19", "points": 31.0},
                {"max_time": "22:45", "points": 29.5}
            ]
        },

        "30_34": {
            "pushups": [
                {"min_reps": 46, "points": 15.0},
                {"min_reps": 45, "points": 14.9},
                {"min_reps": 44, "points": 14.8},
                {"min_reps": 43, "points": 14.7},
                {"min_reps": 42, "points": 14.6},
                {"min_reps": 41, "points": 14.4},
                {"min_reps": 40, "points": 14.3},
                {"min_reps": 39, "points": 14.1},
                {"min_reps": 38, "points": 14.0},
                {"min_reps": 37, "points": 13.9},
                {"min_reps": 36, "points": 13.8},
                {"min_reps": 35, "points": 13.7},
                {"min_reps": 34, "points": 13.6},
                {"min_reps": 33, "points": 13.5},
                {"min_reps": 32, "points": 13.4},
                {"min_reps": 31, "points": 13.3},
                {"min_reps": 30, "points": 13.2},
                {"min_reps": 29, "points": 13.1},
                {"min_reps": 28, "points": 13.0},
                {"min_reps": 27, "points": 12.9},
                {"min_reps": 26, "points": 12.8},
                {"min_reps": 25, "points": 12.5},
                {"min_reps": 24, "points": 12.3},
                {"min_reps": 23, "points": 12.0},
                {"min_reps": 22, "points": 11.9},
                {"min_reps": 21, "points": 11.7},
                {"min_reps": 20, "points": 11.4},
                {"min_reps": 19, "points": 11.3},
                {"min_reps": 18, "points": 10.5},
                {"min_reps": 17, "points": 10.2},
                {"min_reps": 16, "points": 9.8},
                {"min_reps": 15, "points": 9.0},
                {"min_reps": 14, "points": 7.5},
                {"min_reps": 13, "points": 5.3},
                {"min_reps": 12, "points": 3.0},
                {"min_reps": 11, "points": 0.8}
            ],

            "situps": [
                {"min_reps": 45, "points": 15.0},
                {"min_reps": 44, "points": 14.8},
                {"min_reps": 43, "points": 14.6},
                {"min_reps": 42, "points": 14.3},
                {"min_reps": 41, "points": 14.1},
                {"min_reps": 40, "points": 13.5},
                {"min_reps": 39, "points": 13.2},
                {"min_reps": 38, "points": 12.8},
                {"min_reps": 37, "points": 12.5},
                {"min_reps": 36, "points": 12.3},
                {"min_reps": 35, "points": 12.0},
                {"min_reps": 34, "points": 11.7},
                {"min_reps": 33, "points": 11.3},
                {"min_reps": 32, "points": 10.5},
                {"min_reps": 31, "points": 10.2},
                {"min_reps": 30, "points": 9.8},
                {"min_reps": 29, "points": 9.0},
                {"min_reps": 28, "points": 6.8},
                {"min_reps": 27, "points": 4.5},
                {"min_reps": 26, "points": 2.3}
            ],

            "run": [
                {"max_time": "15:48", "points": 50.0},
                {"max_time": "16:36", "points": 49.4},
                {"max_time": "16:54", "points": 48.8},
                {"max_time": "17:09", "points": 48.1},
                {"max_time": "17:23", "points": 47.5},
                {"max_time": "17:48", "points": 46.9},
                {"max_time": "17:59", "points": 46.3},
                {"max_time": "18:10", "points": 45.6},
                {"max_time": "18:21", "points": 45.0},
                {"max_time": "18:50", "points": 43.9},
                {"max_time": "19:09", "points": 42.9},
                {"max_time": "19:27", "points": 41.8},
                {"max_time": "19:45", "points": 40.7},
                {"max_time": "20:01", "points": 39.6},
                {"max_time": "20:17", "points": 38.6},
                {"max_time": "20:33", "points": 37.5},
                {"max_time": "21:05", "points": 35.5},
                {"max_time": "21:29", "points": 34.0},
                {"max_time": "21:55", "points": 32.5},
                {"max_time": "22:24", "points": 31.0},
                {"max_time": "22:50", "points": 29.5}
            ]
        },

        "35_39": {
            "pushups": [
                {"min_reps": 42, "points": 15.0},
                {"min_reps": 41, "points": 14.8},
                {"min_reps": 40, "points": 14.6},
                {"min_reps": 39, "points": 14.3},
                {"min_reps": 38, "points": 14.1},
                {"min_reps": 37, "points": 14.0},
                {"min_reps": 36, "points": 13.9},
                {"min_reps": 35, "points": 13.8},
                {"min_reps": 34, "points": 13.7},
                {"min_reps": 33, "points": 13.6},
                {"min_reps": 32, "points": 13.5},
                {"min_reps": 31, "points": 13.4},
                {"min_reps": 30, "points": 13.3},
                {"min_reps": 29, "points": 13.2},
                {"min_reps": 28, "points": 13.1},
                {"min_reps": 27, "points": 13.0},
                {"min_reps": 26, "points": 12.9},
                {"min_reps": 25, "points": 12.8},
                {"min_reps": 24, "points": 12.5},
                {"min_reps": 23, "points": 12.3},
                {"min_reps": 22, "points": 12.0},
                {"min_reps": 21, "points": 11.9},
                {"min_reps": 20, "points": 11.7},
                {"min_reps": 19, "points": 11.4},
                {"min_reps": 18, "points": 11.3},
                {"min_reps": 17, "points": 10.5},
                {"min_reps": 16, "points": 10.2},
                {"min_reps": 15, "points": 9.8},
                {"min_reps": 14, "points": 9.0},
                {"min_reps": 13, "points": 7.5},
                {"min_reps": 12, "points": 5.3},
                {"min_reps": 11, "points": 3.0},
                {"min_reps": 10, "points": 0.8}
            ],

            "situps": [
                {"min_reps": 43, "points": 15.0},
                {"min_reps": 42, "points": 14.8},
                {"min_reps": 41, "points": 14.6},
                {"min_reps": 40, "points": 14.3},
                {"min_reps": 39, "points": 14.1},
                {"min_reps": 38, "points": 13.5},
                {"min_reps": 37, "points": 13.2},
                {"min_reps": 36, "points": 12.8},
                {"min_reps": 35, "points": 12.5},
                {"min_reps": 34, "points": 12.3},
                {"min_reps": 33, "points": 12.0},
                {"min_reps": 32, "points": 11.7},
                {"min_reps": 31, "points": 11.3},
                {"min_reps": 30, "points": 10.5},
                {"min_reps": 29, "points": 10.2},
                {"min_reps": 28, "points": 9.8},
                {"min_reps": 27, "points": 9.0},
                {"min_reps": 26, "points": 6.8},
                {"min_reps": 25, "points": 4.5},
                {"min_reps": 24, "points": 2.3}
            ],

            "run": [
                {"max_time": "15:51", "points": 50.0},
                {"max_time": "16:42", "points": 49.4},
                {"max_time": "16:59", "points": 48.8},
                {"max_time": "17:14", "points": 48.1},
                {"max_time": "17:28", "points": 47.5},
                {"max_time": "17:53", "points": 46.9},
                {"max_time": "18:04", "points": 46.3},
                {"max_time": "18:15", "points": 45.6},
                {"max_time": "18:25", "points": 45.0},
                {"max_time": "18:54", "points": 43.9},
                {"max_time": "19:13", "points": 42.9},
                {"max_time": "19:31", "points": 41.8},
                {"max_time": "19:49", "points": 40.7},
                {"max_time": "20:05", "points": 39.6},
                {"max_time": "20:21", "points": 38.6},
                {"max_time": "20:37", "points": 37.5},
                {"max_time": "21:08", "points": 35.5},
                {"max_time": "21:32", "points": 34.0},
                {"max_time": "21:58", "points": 32.5},
                {"max_time": "22:27", "points": 31.0},
                {"max_time": "22:59", "points": 29.5}
            ]
        }
    }
}
