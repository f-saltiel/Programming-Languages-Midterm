from pyscript import when
from js import document

from scoring_data import calculate_pfa_score


def get_input_value(element_id):
    return document.getElementById(element_id).value


def set_text(element_id, text):
    document.getElementById(element_id).innerText = str(text)


def show_element(element_id):
    document.getElementById(element_id).classList.remove("d-none")


def hide_element(element_id):
    document.getElementById(element_id).classList.add("d-none")


def set_category_alert(category, passed):
    category_alert = document.getElementById("category-alert")
    score_category = document.getElementById("score-category")

    score_category.innerText = category

    if category == "Excellent":
        category_alert.className = "alert alert-success mb-3"
    elif passed:
        category_alert.className = "alert alert-primary mb-3"
    else:
        category_alert.className = "alert alert-danger mb-3"


def display_warnings(warnings):
    warnings_area = document.getElementById("warnings-area")
    warnings_area.innerHTML = ""

    if len(warnings) == 0:
        warnings_area.innerHTML = """
        <div class="alert alert-success mb-0">
          No component warnings.
        </div>
        """
        return

    warning_items = ""

    for warning in warnings:
        warning_items += f"<li>{warning}</li>"

    warnings_area.innerHTML = f"""
    <div class="alert alert-warning mb-0">
      <strong>Component Warnings:</strong>
      <ul class="mb-0 mt-2">
        {warning_items}
      </ul>
    </div>
    """


def display_error(error_message):
    hide_element("results")

    placeholder = document.getElementById("result-placeholder")
    placeholder.className = "alert alert-danger"
    placeholder.innerText = f"Error: {error_message}"


def display_results(result):
    hide_element("result-placeholder")
    show_element("results")

    set_text("pushup-score", f'{result["pushup_score"]:.1f} pts')
    set_text("situp-score", f'{result["situp_score"]:.1f} pts')
    set_text("run-score", f'{result["run_score"]:.1f} pts')
    set_text("wht-score", f'{result["wht_score"]:.1f} pts')

    set_text("total-score", f'{result["total_score"]:.1f}')
    set_text("result-gender", result["gender"])
    set_text("result-age-group", result["age_group"])
    set_text("result-wht-ratio", result["wht_ratio"])
    set_text("result-wht-risk", result["wht_risk_category"])

    set_category_alert(result["category"], result["passed"])
    display_warnings(result["warnings"])


def validate_run_time(run_time):
    if ":" not in run_time:
        raise ValueError("Run time must be entered in MM:SS format.")

    parts = run_time.split(":")

    if len(parts) != 2:
        raise ValueError("Run time must contain only one colon.")

    minutes, seconds = parts

    if not minutes.isdigit() or not seconds.isdigit():
        raise ValueError("Run time must only contain numbers and one colon.")

    if int(seconds) >= 60:
        raise ValueError("Seconds must be less than 60.")


@when("click", "#calculate-button")
def handle_calculate(event):
    form = document.getElementById("pfa-form")

    # Trigger browser validation for required fields and pattern checks
    if not form.reportValidity():
        return
    
    try:
        gender = get_input_value("gender")
        age_group = get_input_value("age-group")

        pushups = int(get_input_value("pushups"))
        situps = int(get_input_value("situps"))
        run_time = get_input_value("run-time").strip()

        waist = float(get_input_value("waist"))
        height = float(get_input_value("height"))

        if pushups < 0:
            raise ValueError("Push-ups cannot be negative.")

        if situps < 0:
            raise ValueError("Sit-ups cannot be negative.")

        if waist <= 0:
            raise ValueError("Waist measurement must be greater than zero.")

        if height <= 0:
            raise ValueError("Height must be greater than zero.")

        validate_run_time(run_time)

        result = calculate_pfa_score(
            gender,
            age_group,
            pushups,
            situps,
            run_time,
            waist,
            height
        )

        display_results(result)

    except Exception as error:
        display_error(str(error))


print("PFA calculator loaded.")