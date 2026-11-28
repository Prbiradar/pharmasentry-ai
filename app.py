import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import os
from supabase import create_client

# SUPABASE AUTHENTICATION CONNECTION

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

if "supabase_client" not in st.session_state:
    st.session_state.supabase_client = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

supabase = st.session_state.supabase_client
st.set_page_config(
    page_title="PharmaSentry AI",
    page_icon="💊",
    layout="wide"
)

@st.cache_data
def load_drugs():
    file_path = "Drug_Master.csv"

    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding="utf-8-sig").fillna("")
        df.columns = df.columns.str.strip()
        return df

    return pd.DataFrame()

@st.cache_data
def load_interactions():
    file_path = "Interaction_Master.csv"

    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding="utf-8-sig").fillna("")
        df.columns = df.columns.str.strip()
        return df

    return pd.DataFrame()

drugs = load_drugs()
interactions = load_interactions()
st.title("💊 PharmaSentry AI")
st.caption("Evidence-Grounded Pharmacovigilance and Medication Safety Assistant")

# ==========================================
# PHARMASENTRY AI - USER AUTHENTICATION
# ==========================================

if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None

# LOGIN PAGE DESIGN

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg, #071A35, #123E68, #087E8B);
}

/* Main headings */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp p,
.stApp label,
.stApp .stMarkdown {
    color: #FFFFFF !important;
}

/* Login title */
.login-title {
    text-align: center;
    color: #FFFFFF !important;
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 5px;
}

/* Subtitle */
.login-subtitle {
    text-align: center;
    color: #FFFFFF !important;
    font-size: 15px;
    margin-bottom: 25px;
}

/* Input fields */
.stTextInput input {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    border: 2px solid #38BDF8 !important;
    border-radius: 8px !important;
}

/* Input labels */
.stTextInput label {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* Radio buttons */
.stRadio label {
    color: #FFFFFF !important;
}

/* Buttons */
.stButton button {
    background-color: #00A6A6 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    min-height: 45px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #071A35;
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# PASSWORD RECOVERY LINK HANDLING
# ==========================================

if "recovery_mode" not in st.session_state:
    st.session_state.recovery_mode = False

if "recovery_error" not in st.session_state:
    st.session_state.recovery_error = None

recovery_code = st.query_params.get("code")

if recovery_code and not st.session_state.recovery_mode:

    try:
        recovery_response = supabase.auth.exchange_code_for_session(
            {"auth_code": recovery_code}
        )

        st.session_state.authenticated_user = recovery_response.user
        st.session_state.recovery_mode = True

        st.query_params.clear()
        st.rerun()

    except Exception as e:
        st.session_state.recovery_error = str(e)
        st.query_params.clear()

# ==========================================
# SET NEW PASSWORD SCREEN
# ==========================================

if st.session_state.recovery_mode:

    st.title("🔐 Reset Your Password")

    st.write("Create a new password for your PharmaSentry AI account.")

    new_password = st.text_input(
        "New Password",
        type="password",
        key="new_password"
    )

    confirm_new_password = st.text_input(
        "Confirm New Password",
        type="password",
        key="confirm_new_password"
    )

    if st.button("Update Password", use_container_width=True):

        if len(new_password) < 8:
            st.warning("Password must contain at least 8 characters.")

        elif new_password != confirm_new_password:
            st.error("Passwords do not match.")

        else:
            try:
                supabase.auth.update_user({
                    "password": new_password
                })

                st.success("Your password has been updated successfully.")

                st.session_state.recovery_mode = False
                st.session_state.authenticated_user = None

                supabase.auth.sign_out()

                st.rerun()

            except Exception as e:
                st.error("Password update failed.")
                st.code(str(e))

    st.stop()

# ==========================================
# LOGIN SCREEN
# ==========================================

if st.session_state.authenticated_user is None:

    st.markdown(
        '<div class="login-title">🛡️ PharmaSentry AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-subtitle">'
        'Intelligent Pharmacovigilance & Drug Safety Platform'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    auth_option = st.radio(
        "Choose an option",
        ["Sign In", "Create Account", "Forgot Password"],
        horizontal=True,
        key="authentication_option"
    )

    # ======================================
    # SIGN IN
    # ======================================

    if auth_option == "Sign In":

        st.subheader("Welcome Back")

        email = st.text_input(
            "Email Address",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Sign In",
            use_container_width=True,
            key="login_button"
        ):

            if not email.strip() or not password:
                st.warning("Please enter your email and password.")

            else:
                try:
                    response = supabase.auth.sign_in_with_password({
                        "email": email.strip(),
                        "password": password
                    })

                    if response.user is not None:
                        st.session_state.authenticated_user = response.user
                        st.success("Login successful!")
                        st.rerun()

                    else:
                        st.error("Unable to sign in. Please try again.")

                except Exception as e:
                    st.error("Sign in failed.")
                    st.code(str(e))

    # ======================================
    # CREATE ACCOUNT
    # ======================================

    elif auth_option == "Create Account":

        st.subheader("Create Your Account")

        name = st.text_input(
            "Full Name",
            key="register_name"
        )

        email = st.text_input(
            "Email Address",
            key="register_email"
        )

        password = st.text_input(
            "Create Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )

        if st.button(
            "Create Account",
            use_container_width=True,
            key="register_button"
        ):

            if not name.strip():
                st.warning("Please enter your full name.")

            elif not email.strip():
                st.warning("Please enter your email address.")

            elif len(password) < 8:
                st.warning(
                    "Password must contain at least 8 characters."
                )

            elif password != confirm_password:
                st.error("Passwords do not match.")

            else:
                try:
                    response = supabase.auth.sign_up({
                        "email": email.strip(),
                        "password": password,
                        "options": {
                            "data": {
                                "full_name": name.strip()
                            }
                        }
                    })

                    st.success(
                        "Registration request submitted successfully."
                    )

                    st.info(
                        "Please check your email and verify your "
                        "account before signing in."
                    )

                except Exception as e:
                    st.error("Registration failed.")
                    st.error("Supabase error details:")
                    st.code(str(e))

    # ======================================
    # FORGOT PASSWORD
    # ======================================

    elif auth_option == "Forgot Password":

        st.subheader("Reset Your Password")

        st.write(
            "Open the secure PharmaSentry AI recovery page "
            "to request a password reset email and create a new password."
        )

        st.link_button(
            "Open Secure Password Recovery",
            "https://prbiradar.github.io/pharmasentry-ai/reset-password.html",
            use_container_width=True
        )

        st.info(
            "Enter your registered email address on the recovery page. "
            "Check your inbox for the password reset link."
        )

    st.markdown("---")

    st.markdown(
        "<center>Developed by <b>Dr. Praveen R Biradar</b>"
        "<br>PharmaSentry AI | Educational Pharmacovigilance Platform"
        "</center>",
        unsafe_allow_html=True
    )

    st.stop()



# ==========================================
# LOGGED-IN USER SECTION
# ==========================================

else:

    st.sidebar.markdown(
    f"""
    <div style="
        color: white;
        background-color: #17324d;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #48c6cf;
        font-weight: 600;
        overflow-wrap: anywhere;">
        Signed in:<br>
        {st.session_state.authenticated_user.email}
    </div>
    """,
    unsafe_allow_html=True
    )

    if st.sidebar.button("Logout", use_container_width=True):

        try:
            supabase.auth.sign_out()
        except Exception:
            pass

        st.session_state.authenticated_user = None
        st.rerun()


# ==========================================
# EXISTING APP NAVIGATION STARTS BELOW
# ==========================================

          
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Home",
        "Drug Safety Assistant",
        "Drug-ADR Safety Screening",
        "Drug Interaction Checker",
        "ADR Completeness Checker",
        "Pharmacovigilance Learning Centre",
        "Research Dashboard",
        "About"
    ]
)

if page == "Home":
    st.header("Welcome to PharmaSentry AI")
    st.write(
        "An academic prototype for drug safety information, "
        "adverse drug reaction awareness and pharmacovigilance education."
    )

    st.subheader("Available Modules")
    st.write("1. Drug Safety Assistant")
    st.write("2. ADR Case Completeness Checker")
    st.write("3. Pharmacovigilance Learning Centre")
    st.write("4.💊 Drug–ADR Safety Screening")
    st.write("5. Research Dashboard")

    st.markdown(
    """
    <div style="
        color: white;
        background-color: #17324d;
        padding: 12px 16px;
        border-radius: 10px;
        border: 1px solid #48c6cf;
        font-weight: 500;
        text-align: center;">
        This is an educational prototype, not a substitute for professional clinical judgement.
    </div>
    """,
    unsafe_allow_html=True
    )

elif page == "Drug Safety Assistant":

    st.header("💊 Drug Safety Assistant")

    if drugs.empty:
        st.error("Drug database not found. Please check Drug_Master.csv.")
    elif "Drug_Name" not in drugs.columns:
        st.error("Drug_Name column is missing from the database.")
    else:
        drug_names = sorted(
            drugs["Drug_Name"].astype(str).unique().tolist()
        )

        selected_drug = st.selectbox(
            "Search and select a medicine",
            drug_names
        )

        result = drugs[
            drugs["Drug_Name"].astype(str) == selected_drug
        ].iloc[0]

        st.subheader(str(result.get("Drug_Name", "")))
        st.write("**Drug Class:**", result.get("Drug_Class", "Not available"))

        st.divider()

        fields = {
            "Indication": "Indications",
            "Common_ADR": "Common Adverse Drug Reactions",
            "Serious_ADR": "Serious Adverse Drug Reactions",
            "Warnings": "Warnings",
            "Contraindications": "Contraindications",
            "Monitoring": "Monitoring Recommendations",
            "Source": "Information Source",
            "Source_Date": "Source Date",
            "Verification_Status": "Verification Status"
        }

        for column, heading in fields.items():
            value = str(result.get(column, "")).strip()

            st.markdown("### " + heading)

            if value and value.lower() != "nan":
                st.write(value)
            else:
                st.warning("Information not yet entered or verified.")

        st.divider()
        st.caption(
            "Drug information is preliminary and requires verification "
            "against authoritative product labels and expert review."
        )


elif page == "Drug-ADR Safety Screening":

    st.header("💊 Drug-ADR Safety Screening")
    st.write("Compare reported reactions with the available drug database.")

    if drugs.empty:
        st.error("Drug database is not available.")

    else:
        selected_drug = st.selectbox(
            "Select suspected medicine",
            sorted(drugs["Drug_Name"].astype(str).unique()),
            key="screening_drug"
        )

        reaction = st.text_input(
            "Enter reported adverse reaction",
            placeholder="Example: Liver damage",
            key="reported_adr"
        )

        if st.button("Screen Drug-ADR Record", key="screen_adr"):

            if not reaction.strip():
                st.warning("Please enter an adverse reaction.")

            else:
                selected_record = drugs[
                    drugs["Drug_Name"].astype(str) == selected_drug
                ].iloc[0]

                import re

                def normalize_adr(value):
                    value = str(value).lower()
                    value = value.replace("/", " ")
                    value = value.replace("-", " ")
                    value = re.sub(r"[^a-z0-9 ]", " ", value)
                    return " ".join(value.split())

                aliases = {
                    "liver damage": ["hepatotoxicity", "liver injury"],
                    "hepatotoxicity": ["liver damage", "liver injury"],
                    "vomiting": ["emesis"],
                    "diarrhea": ["loose stools"],
                    "loose stools": ["diarrhea"],
                    "stomach pain": ["abdominal pain"],
                    "abdominal pain": ["stomach pain"],
                    "skin rash": ["rash"],
                    "rash": ["skin rash"],
                    "kidney injury": ["renal injury"],
                    "renal injury": ["kidney injury"],
                    "muscle pain": ["myalgia"],
                    "myalgia": ["muscle pain"]
                }

                def split_terms(value):
                    return [
                        normalize_adr(term)
                        for term in re.split(r"[,;]", str(value))
                        if normalize_adr(term)
                    ]

                reported_terms = split_terms(reaction)

                common_terms = split_terms(
                    selected_record.get("Common_ADR", "")
                )

                serious_terms = split_terms(
                    selected_record.get("Serious_ADR", "")
                )

                def find_matches(reported, database_terms):
                    matches = []

                    for term in reported:
                        possible_terms = [term] + aliases.get(term, [])

                        for db_term in database_terms:
                            if any(
                                possible == db_term
                                or possible in db_term
                                or db_term in possible
                                for possible in possible_terms
                            ):
                                matches.append((term, db_term))
                                break

                    return matches

                serious_matches = find_matches(
                    reported_terms, serious_terms
                )

                common_matches = find_matches(
                    reported_terms, common_terms
                )

                st.divider()
                st.subheader("Screening Result")

                st.write("Suspected Medicine:", selected_drug)
                st.write("Reported Reaction:", reaction)

                if serious_matches:
                    st.error("Potential Serious ADR Match")

                    for reported, matched in serious_matches:
                        st.write(f"{reported} → {matched}")

                if common_matches:
                    st.success("Potential Common ADR Match")

                    for reported, matched in common_matches:
                        st.write(f"{reported} → {matched}")

                if not serious_matches and not common_matches:
                    st.info(
                        "No direct ADR match found in the available database."
                    )

                st.caption(
                    "Educational keyword matching only. These database "
                    "categories do not determine individual patient severity "
                    "or establish ADR causality. Professional review is required."
                )


elif page == "Drug Interaction Checker":

    st.header("💊 Drug Interaction Checker")

    st.write(
        "Screen medicines for documented Drug-Drug "
        "and Drug-Food interactions."
    )

    if interactions.empty:

        st.error(
            "Interaction database is not available. "
            "Please check Interaction_Master.csv."
        )

    else:

        interaction_type = st.radio(
            "Select Interaction Type",
            ["Drug-Drug", "Drug-Food"],
            horizontal=True
        )

if interaction_type == "Drug-Drug":

    st.subheader("Drug-Drug Interaction Checker")

    dd_data = interactions[
        interactions["Interaction_Type"].astype(str).str.strip()
        == "Drug-Drug"
    ]

    if dd_data.empty:

        st.warning("No Drug-Drug records available.")

    else:

        drug_options = sorted(
            set(dd_data["Item_A"].astype(str).str.strip())
            | set(dd_data["Item_B"].astype(str).str.strip())
        )

        drug1 = st.selectbox(
            "Search First Medicine",
            drug_options,
            index=None,
            placeholder="Type or select first medicine",
            key="interaction_drug1"
        )

        drug2 = st.selectbox(
            "Search Second Medicine",
            drug_options,
            index=None,
            placeholder="Type or select second medicine",
            key="interaction_drug2"
        )

        if st.button(
            "Check Drug-Drug Interaction",
            key="check_dd"
        ):

            if not drug1 or not drug2:
                st.warning("Please select both medicines.")

            elif drug1 == drug2:
                st.warning("Please select two different medicines.")

            else:

                matches = dd_data[
                    (
                        (dd_data["Item_A"].astype(str).str.strip() == drug1)
                        & (dd_data["Item_B"].astype(str).str.strip() == drug2)
                    )
                    |
                    (
                        (dd_data["Item_A"].astype(str).str.strip() == drug2)
                        & (dd_data["Item_B"].astype(str).str.strip() == drug1)
                    )
                ]

                if not matches.empty:

                    for _, record in matches.iterrows():

                        st.warning(
                            "Documented Drug-Drug Interaction Found"
                        )

                        severity = str(
                            record["Interaction_Level"]
                        ).strip().lower()

                        if severity == "major":
                            st.error(
                                "HIGH-RISK SAFETY ALERT: This interaction may cause serious harm. Seek review by a qualified prescriber."
                            )

                        elif severity == "moderate":
                            st.warning(
                                "CLINICAL CAUTION: Clinical assessment, monitoring or dose adjustment may be needed."
                            )

                        elif severity == "minor":
                            st.info(
                                "SAFETY INFORMATION: This interaction is generally of lower clinical significance."
                            )

                        else:
                            st.info(
                                "Review this interaction with a qualified prescriber."
                            )

                        st.write(
                            "**Interaction Level:**",
                            record["Interaction_Level"]
                        )

                        st.write(
                            "**Mechanism:**",
                            record["Mechanism"]
                        )

                        st.write(
                            "**Potential Effect:**",
                            record["Potential_Effect"]
                        )

                        st.write(
                            "**Management / Precautions:**",
                            record["Management"]
                        )

                        st.write(
                            "**Reference:**",
                            record["Source"]
                        )

                        if record["Source_URL"]:
                            st.markdown(
                                f"[VIEW SOURCE]({record['Source_URL']})"
                            )

                        st.write(
                            "**Verification Status:**",
                            record["Verification_Status"]
                        )

                else:
                    st.info(
                        "No matching interaction record found in the current database. "
                        "This does not rule out a possible interaction."
                    )

        elif interaction_type == "Drug-Food":

            st.subheader("Drug-Food Interaction Checker")

            df_data = interactions[
                interactions["Interaction_Type"].astype(str).str.strip()
                == "Drug-Food"
            ]

            if df_data.empty:

                st.warning("No Drug-Food records available.")

            else:

                medicine_options = sorted(
                    df_data["Item_A"].astype(str).str.strip().unique()
                )

                food_options = sorted(
                    df_data["Item_B"].astype(str).str.strip().unique()
                )

                medicine = st.selectbox(
                    "Search Medicine",
                    medicine_options,
                    index=None,
                    placeholder="Type or select medicine",
                    key="food_medicine"
                )

                food = st.selectbox(
                    "Search Food / Beverage",
                    food_options,
                    index=None,
                    placeholder="Type or select food or beverage",
                    key="food_item"
                )

                if st.button(
                    "Check Drug-Food Interaction",
                    key="check_df"
                ):

if not medicine or not food:

    st.warning(
        "Please select both medicine and food."
    )

else:

    matches = df_data[
        (df_data["Item_A"].astype(str).str.strip() == medicine)
        & (df_data["Item_B"].astype(str).str.strip() == food)
    ]

    if not matches.empty:

        for _, record in matches.iterrows():

            st.warning(
                "Documented Drug-Food Interaction Found"
            )

            st.write(
                "**Interaction Level:**",
                record["Interaction_Level"]
            )

            st.write(
                "**Mechanism:**",
                record["Mechanism"]
            )

            st.write(
                "**Potential Effect:**",
                record["Potential_Effect"]
            )

    else:

        st.info(
            "No matching Drug-Food interaction record found."
        )    "in the current database. This does not "
                                "rule out a possible interaction."
                            )
    st.divider()

    st.caption(
        "Educational interaction screening prototype based on a "
        "limited database. It does not identify all possible "
        "interactions or replace professional clinical judgement. "
        "Consult a qualified pharmacist or prescriber before "
        "making medication-related decisions."
    )

elif page == "ADR Completeness Checker":

    st.header("ADR Case Completeness Checker")
    st.write("Enter a fictitious ADR case for educational completeness assessment.")

    age = st.text_input("Patient Age")
    sex = st.selectbox("Patient Sex", ["Select", "Male", "Female", "Other"])
    drug = st.text_input("Suspected Drug")
    reaction = st.text_input("Adverse Reaction")
    onset = st.text_input("Reaction Onset Date")
    history = st.text_area("Relevant Medical History")
    concomitant = st.text_area("Concomitant Medicines")
    seriousness = st.selectbox(
        "Seriousness",
        ["Select", "Serious", "Non-serious", "Not assessed"]
    )

    if st.button("Check Completeness"):
        missing = []

        if not age.strip():
            missing.append("Patient Age")
        if sex == "Select":
            missing.append("Patient Sex")
        if not drug.strip():
            missing.append("Suspected Drug")
        if not reaction.strip():
            missing.append("Adverse Reaction")
        if not onset.strip():
            missing.append("Reaction Onset Date")
        if not history.strip():
            missing.append("Medical History")
        if not concomitant.strip():
            missing.append("Concomitant Medicines")
        if seriousness == "Select":
            missing.append("Seriousness")

        if missing:
            st.warning("Missing information:")
            for item in missing:
                st.write("- " + item)
        else:
            st.success("All selected basic fields are completed.")

        st.info("This is a basic educational completeness check, not an official ADR reporting assessment.")

elif page == "Pharmacovigilance Learning Centre":

    st.header("Pharmacovigilance Learning Centre")
    st.write(
        "An educational resource covering the principles, "
        "processes and regulatory framework of pharmacovigilance."
    )

    topics = {

        "1. About Pharmacovigilance": """
### Definition

Pharmacovigilance (PV) is the science and activities relating to the
detection, assessment, understanding and prevention of adverse effects
or any other drug-related problems.

**Main objectives**
- Improve patient safety.
- Detect previously unknown adverse drug reactions.
- Identify changes in the frequency or severity of known reactions.
- Evaluate the benefit-risk balance of medicines.
- Promote rational and safe use of medicines.
- Support regulatory decision-making.

### Scope of Pharmacovigilance

Pharmacovigilance covers:
- Prescription medicines.
- Over-the-counter medicines.
- Vaccines and biological products.
- Herbal and traditional medicines.
- Medical devices (through relevant safety-monitoring programmes).
- Medication errors and medication-related problems.

### Important Activities

1. ADR reporting and collection.
2. Case processing and assessment.
3. Signal detection and evaluation.
4. Risk assessment and risk minimisation.
5. Safety communication.
6. Post-marketing surveillance.

### Pharmacovigilance Cycle

Detection → Reporting → Assessment → Signal Evaluation →
Regulatory Action → Risk Communication.

**Remember:** Pharmacovigilance continues throughout the life cycle
of a medicine, including after marketing approval.

**Reference:** [WHO – Pharmacovigilance](https://www.who.int/teams/regulation-prequalification/regulation-and-safety/pharmacovigilance)
""",

        "2. ADR and Its Types": """
### Definition of ADR

An adverse drug reaction (ADR) is a harmful and unintended response
to a medicinal product.

An adverse event is any unfavourable medical occurrence following
medicine use; it does not necessarily have a causal relationship
with the medicine.

### Classification of ADRs

The Rawlins and Thompson classification describes six types.

**Type A – Augmented**
- Dose-related and predictable.
- Related to the known pharmacological action.
- Usually more common.
- Example: Hypoglycaemia caused by insulin.

**Type B – Bizarre**
- Not dose-related in the usual way.
- Unpredictable and often uncommon.
- Example: Anaphylaxis associated with penicillin.

**Type C – Chronic**
- Related to prolonged medicine use.
- Example: Adrenal suppression following prolonged
  glucocorticoid therapy.

**Type D – Delayed**
- Appears after a time interval.
- Example: Certain cancers developing years after exposure
  to a causative medicine.

**Type E – End-of-use**
- Associated with withdrawal or discontinuation.
- Example: Rebound hypertension after abrupt withdrawal
  of certain antihypertensive medicines.

**Type F – Failure**
- Unexpected failure of therapy.
- Example: Reduced contraceptive effectiveness due to
  a clinically significant drug interaction.

### Other Classifications

**According to seriousness**
- Serious ADR
- Non-serious ADR

**According to severity**
- Mild
- Moderate
- Severe

**Important distinction:**
Seriousness is a regulatory classification based on outcomes,
whereas severity describes the clinical intensity of a reaction.

### Criteria for a Serious Adverse Event

- Death.
- Life-threatening condition.
- Hospitalisation or prolongation of hospitalisation.
- Persistent or significant disability.
- Congenital anomaly or birth defect.
- Other medically important events requiring intervention
  to prevent serious outcomes.

**Remember:** A severe headache is not automatically a
serious adverse event. Severity and seriousness are different concepts.
""",

        "3. Individual Case Safety Report (ICSR)": """
### Definition

An Individual Case Safety Report (ICSR) is a structured report
containing information about one individual who experienced one
or more suspected adverse events associated with one or more
medicinal products.

### Four Minimum Elements of a Valid ICSR

1. An identifiable patient.
2. An identifiable reporter.
3. A suspected medicinal product.
4. A suspected adverse reaction.

All four elements are necessary for a valid individual case report.

### Important Components of an ICSR

**A. Patient Information**
- Patient identification code.
- Age or date of birth.
- Sex.
- Relevant medical history.

**B. Reporter Information**
- Reporter qualification.
- Contact details.
- Country of report.

**C. Suspected Medicine Information**
- Generic and brand name.
- Dose and dosage form.
- Route of administration.
- Therapy start and stop dates.
- Indication for use.
- Batch number, where relevant.

**D. Adverse Reaction Information**
- Description of reaction.
- Date of onset.
- Seriousness criteria.
- Outcome.
- Relevant investigations.

**E. Additional Information**
- Concomitant medicines.
- Dechallenge information.
- Rechallenge information.
- Medical history.
- Laboratory findings.

### ICSR Processing Workflow

1. Receipt of the safety report.
2. Validation of minimum case information.
3. Duplicate case detection.
4. Data entry and medical coding.
5. Seriousness and expectedness assessment.
6. Causality assessment.
7. Follow-up for missing information.
8. Regulatory reporting, where applicable.
9. Case storage and signal evaluation.

### Important Terminology

- Dechallenge: Observation of the reaction after stopping
  or reducing the suspected medicine.
- Rechallenge: Observation after reintroducing the medicine.
- Concomitant medicine: Another medicine used during the
  relevant treatment period.
- Follow-up: Additional information collected after the
  initial case report.

### ICSR Example

A patient develops a skin rash after taking a suspected medicine.

The reporter provides patient details, medicine information,
reaction description and relevant dates.

This information can form the basis of an ICSR if all four
minimum elements are present.

**Remember:** An ICSR documents a suspected association;
it does not automatically prove causality.

Reference: [WHO Programme for International Drug Monitoring](https://www.who.int/teams/regulation-prequalification/regulation-and-safety/pharmacovigilance/networks/pidm)
""",

        "4. Signal Detection": """
### Definition

A safety signal is information from one or more sources that
suggests a new potentially causal association, or a new aspect
of a known association, between an intervention and an adverse event
that warrants further investigation.

### Objectives of Signal Detection

- Identify previously unrecognised ADRs.
- Detect changes in known ADR patterns.
- Identify vulnerable patient populations.
- Detect potential drug interactions.
- Support benefit-risk evaluation.
- Initiate further safety investigations when necessary.

### Sources of Safety Signals

1. Spontaneous ADR reports.
2. Clinical trials.
3. Published medical literature.
4. Observational studies.
5. Electronic health records.
6. Prescription and healthcare databases.
7. Patient and healthcare professional reports.

### Methods of Signal Detection

**1. Qualitative Methods**
- Clinical review of individual reports.
- Medical literature review.
- Expert evaluation.
- Review of case series.

**2. Quantitative Methods**
- Proportional Reporting Ratio (PRR).
- Reporting Odds Ratio (ROR).
- Information Component (IC).
- Empirical Bayes methods.

These statistical methods identify disproportionate reporting
patterns. They do not independently establish causality.

### Signal Management Process

1. Signal detection.
2. Signal validation.
3. Signal prioritisation.
4. Signal assessment.
5. Recommendation and regulatory action.
6. Communication and monitoring.

### Example

Suppose multiple reports describe a previously unrecognised
serious reaction associated with a particular medicine.

The reports are reviewed for duplicates, clinical consistency,
alternative explanations and supporting evidence.

If the association warrants investigation, it may be treated
as a safety signal.

### Important Point

A signal is a hypothesis that requires evaluation.
It is not proof that a medicine causes the reported reaction.

**Remember:** Signal detection is an essential activity in
post-marketing pharmacovigilance.
""",

        "5. Establishment and Development of PvPI": """
### What is PvPI?

The Pharmacovigilance Programme of India (PvPI) is the
Government of India's national programme for monitoring
the safety of medicines.

### Establishment

- July 2010: PvPI was launched by the Ministry of Health
  and Family Welfare, Government of India.
- Initially, AIIMS, New Delhi, served as the National
  Coordination Centre (NCC).
- The programme initially included 22 ADR Monitoring Centres.
- 15 April 2011: The National Coordination Centre was shifted
  from AIIMS to the Indian Pharmacopoeia Commission (IPC),
  Ghaziabad.
- 30 October 2017: IPC-NCC PvPI was launched as a WHO
  Collaborating Centre for Pharmacovigilance in Public Health
  Programmes and Regulatory Services.

### Objectives of PvPI

1. Establish a nationwide medicine-safety reporting system.
2. Collect and evaluate suspected ADR reports.
3. Detect and analyse safety signals.
4. Assess the benefit-risk balance of medicines.
5. Support evidence-based regulatory decisions.
6. Communicate medicine-safety information.
7. Promote awareness among healthcare professionals
   and the public.

### Organisational Structure

**Ministry of Health and Family Welfare**
↓
**Indian Pharmacopoeia Commission (IPC)**
↓
**National Coordination Centre – PvPI**
↓
**ADR Monitoring Centres (AMCs)**
↓
**Healthcare professionals and consumers reporting
suspected adverse reactions**

### Role of ADR Monitoring Centres

- Receive suspected ADR reports.
- Review and process case information.
- Follow up for missing details.
- Forward reports through the programme's reporting system.
- Promote ADR-reporting awareness.

### How to Report an ADR in India

Healthcare professionals and consumers can report suspected
adverse reactions through the official PvPI reporting channels
and ADR Monitoring Centres.

**Remember:** Reporting a suspected ADR does not require
the reporter to establish definite causality.

Official reference:
[Pharmacovigilance Programme of India – IPC](https://www.ipc.gov.in/PvPI/about.html)
""",

        "6. CDSCO – Functions and Role in Pharmacovigilance": """
### What is CDSCO?

The Central Drugs Standard Control Organisation (CDSCO) is
India's central drug regulatory authority under the Ministry
of Health and Family Welfare.

It is headed by the Drugs Controller General (India), commonly
known as DCGI.

### Major Functions of CDSCO

1. Approval of new drugs.
2. Regulation of clinical trials.
3. Regulation of imported drugs.
4. Coordination of drug regulatory activities.
5. Setting and enforcement of applicable regulatory standards.
6. Regulation of specified categories of drugs and medical devices.
7. Regulatory action concerning unsafe or non-compliant products.
8. Pharmacovigilance-related regulatory activities.

### Role of CDSCO in Drug Safety

- Supports the regulatory framework for medicine safety.
- Receives and considers safety recommendations and evidence.
- Takes appropriate regulatory decisions within its authority.
- May require safety-related labelling changes.
- May restrict or suspend the use of medicines when justified.
- Coordinates with relevant national safety-monitoring programmes.

### Relationship Between CDSCO and PvPI

**PvPI**
- Collects suspected ADR reports.
- Evaluates and analyses safety information.
- Identifies potential safety signals.
- Provides safety recommendations.

**CDSCO**
- Acts as the central drug regulatory authority.
- Considers scientific and safety evidence.
- Makes appropriate regulatory decisions.
- Implements regulatory measures within its authority.

### Difference Between PvPI and CDSCO

| Parameter | PvPI | CDSCO |
|---|---|---|
| Full form | Pharmacovigilance Programme of India | Central Drugs Standard Control Organisation |
| Main role | Medicine safety monitoring | Drug regulation |
| Main activity | ADR collection and evaluation | Regulatory oversight |
| National structure | NCC and AMCs | Central regulatory organisation |
| Outcome | Safety recommendations | Regulatory decisions |

**Remember:** PvPI and CDSCO have complementary roles
in protecting public health through medicine safety monitoring
and regulation.

Official reference:
[CDSCO – Government of India](https://cdsco.gov.in/)
"""
    }

    topic = st.selectbox(
        "Select a learning topic",
        list(topics.keys())
    )

    st.divider()

    st.subheader(topic)
    st.markdown(topics[topic])

    st.divider()
    st.header("📝 Interactive Pharmacovigilance Quiz")
    st.write("Test your knowledge of the selected topic.")

    quiz_data = {

        "1. About Pharmacovigilance": [
            ("What is the primary objective of pharmacovigilance?",
             ["Increasing drug sales", "Improving patient safety",
              "Reducing medicine prices", "Manufacturing medicines"],
             1, "Pharmacovigilance aims to improve patient safety through medicine safety monitoring."),
            ("Which organisation launched the WHO Programme for International Drug Monitoring?",
             ["WHO", "UNICEF", "UNESCO", "World Bank"],
             0, "WHO established the international programme to promote global ADR monitoring."),
            ("When was the WHO international monitoring programme established?",
             ["1950", "1968", "1985", "2000"],
             1, "The WHO Programme for International Drug Monitoring was established in 1968."),
            ("Pharmacovigilance mainly deals with:",
             ["Only drug manufacturing", "Detection and prevention of medicine-related problems",
              "Only drug marketing", "Only prescription writing"],
             1, "It covers detection, assessment, understanding and prevention of adverse effects and other drug-related problems."),
            ("Which activity is part of pharmacovigilance?",
             ["Signal detection", "Drug packaging design", "Tablet coating only",
              "Pharmaceutical advertising"],
             0, "Signal detection is an important pharmacovigilance activity."),
            ("Pharmacovigilance is important during:",
             ["Only clinical trials", "Only drug development",
              "The entire medicine life cycle", "Only drug manufacturing"],
             2, "Medicine safety must be monitored throughout its life cycle."),
            ("Who can report a suspected ADR?",
             ["Only doctors", "Only pharmacists", "Only nurses",
              "Healthcare professionals and consumers"],
             3, "Suspected ADRs can be reported by healthcare professionals and consumers."),
            ("Which is a source of pharmacovigilance information?",
             ["Spontaneous ADR reports", "Clinical studies",
              "Medical literature", "All of the above"],
             3, "All these sources contribute to medicine safety monitoring."),
            ("What does benefit-risk assessment evaluate?",
             ["Medicine colour", "Balance between therapeutic benefits and risks",
              "Tablet size", "Packaging cost"],
             1, "Benefit-risk assessment considers the medicine's benefits in relation to its risks."),
            ("Which term describes monitoring medicine safety after marketing?",
             ["Post-marketing surveillance", "Preclinical formulation",
              "Drug packaging", "Inventory management"],
             0, "Post-marketing surveillance monitors medicine safety after approval and marketing.")
        ],

        "2. ADR and Its Types": [
            ("What does ADR stand for?",
             ["Adverse Drug Reaction", "Approved Drug Regulation",
              "Active Drug Research", "Adverse Dose Requirement"],
             0, "ADR means Adverse Drug Reaction."),
            ("Type A ADRs are generally:",
             ["Unpredictable", "Dose-related and predictable",
              "Always delayed", "Withdrawal reactions"],
             1, "Type A reactions are augmented pharmacological effects and are generally dose-related."),
            ("Anaphylaxis due to penicillin is an example of:",
             ["Type A", "Type B", "Type C", "Type E"],
             1, "Type B reactions are bizarre and generally unpredictable."),
            ("Type C ADRs are associated with:",
             ["Chronic use", "Drug withdrawal",
              "Immediate allergy", "Treatment failure"],
             0, "Type C reactions are associated with prolonged or chronic medicine use."),
            ("Type D ADRs are:",
             ["Dose-related", "Delayed", "Withdrawal-related",
              "Treatment failures"],
             1, "Type D reactions appear after a time interval."),
            ("Type E ADRs occur due to:",
             ["Drug withdrawal", "Drug overdose",
              "Chronic exposure", "Drug allergy"],
             0, "Type E refers to reactions associated with the end of treatment or withdrawal."),
            ("Type F ADRs refer to:",
             ["Treatment failure", "Delayed reactions",
              "Chronic reactions", "Bizarre reactions"],
             0, "Type F describes unexpected failure of therapy."),
            ("Which is a criterion for a serious adverse event?",
             ["Mild headache only", "Hospitalisation",
              "Temporary unpleasant taste", "Mild nausea only"],
             1, "Hospitalisation is one of the regulatory seriousness criteria."),
            ("Severity and seriousness are:",
             ["Always identical", "Different concepts",
              "Unrelated to ADRs", "Synonyms"],
             1, "Severity describes intensity; seriousness is based on regulatory outcome criteria."),
            ("An adverse event necessarily proves drug causality:",
             ["True", "False", "Only in adults", "Only in clinical trials"],
             1, "An adverse event does not automatically establish a causal relationship with a medicine.")
        ],

        "3. Individual Case Safety Report (ICSR)": [
            ("What is the full form of ICSR?",
             ["Individual Case Safety Report", "International Clinical Safety Review",
              "Individual Clinical Study Record", "Internal Case Summary Report"],
             0, "ICSR stands for Individual Case Safety Report."),
            ("How many minimum elements are needed for a valid ICSR?",
             ["Two", "Three", "Four", "Six"],
             2, "Four elements are required: identifiable patient, reporter, suspected product and suspected reaction."),
            ("Which is NOT one of the four minimum ICSR elements?",
             ["Identifiable patient", "Identifiable reporter",
              "Suspected medicinal product", "Laboratory investigation"],
             3, "A laboratory investigation may support a case but is not one of the four minimum elements."),
            ("What is dechallenge?",
             ["Stopping or reducing the suspected medicine and observing the reaction",
              "Increasing the dose", "Changing the brand",
              "Starting another medicine"],
             0, "Dechallenge assesses what happens after withdrawal or reduction of the suspected medicine."),
            ("What is rechallenge?",
             ["Stopping treatment permanently", "Reintroducing the suspected medicine and observing the reaction",
              "Changing the dosage form", "Reporting a new patient"],
             1, "Rechallenge involves re-exposure to the suspected medicine."),
            ("Which information belongs to patient details?",
             ["Age and sex", "Medicine price", "Manufacturer profit",
              "Hospital building details"],
             0, "Patient demographics such as age and sex are relevant ICSR information."),
            ("What is duplicate case detection?",
             ["Identifying repeated reports of the same case",
              "Deleting all serious cases", "Changing the patient identity",
              "Ignoring follow-up reports"],
             0, "Duplicate detection prevents the same case from being counted more than once."),
            ("Which is an example of concomitant medication information?",
             ["Other medicines used by the patient",
              "The patient's occupation only", "Medicine packaging",
              "Hospital location"],
             0, "Concomitant medicines are other medicines used during the relevant period."),
            ("Does a valid ICSR automatically prove causality?",
             ["Yes", "No", "Only for serious cases", "Only for new drugs"],
             1, "An ICSR records a suspected association; causality requires further assessment."),
            ("What is the purpose of follow-up in ICSR processing?",
             ["To obtain missing or additional case information",
              "To increase medicine sales", "To change the reporter",
              "To remove the suspected reaction"],
             0, "Follow-up improves the completeness and quality of case information.")
        ],

        "4. Signal Detection": [
            ("What is a safety signal?",
             ["A hypothesis suggesting a potentially new or changed safety association",
              "Proof of drug toxicity", "A prescription order",
              "A manufacturing licence"],
             0, "A signal suggests a potential association that warrants further investigation."),
            ("Which is a source of safety signals?",
             ["Spontaneous reports", "Medical literature",
              "Clinical studies", "All of the above"],
             3, "Safety signals can arise from multiple data sources."),
            ("What is PRR?",
             ["Proportional Reporting Ratio", "Patient Reaction Record",
              "Pharmaceutical Risk Review", "Product Registration Report"],
             0, "PRR is a statistical method used in signal detection."),
            ("What does ROR stand for?",
             ["Reporting Odds Ratio", "Reaction Outcome Record",
              "Risk Observation Review", "Regulatory Order Report"],
             0, "ROR is Reporting Odds Ratio, a disproportionality measure."),
            ("Which stage follows signal detection in signal management?",
             ["Signal validation", "Drug advertising",
              "Product packaging", "Prescription renewal"],
             0, "Potential signals are validated before further assessment."),
            ("Does a statistical signal prove causality?",
             ["Yes, always", "No, it requires further evaluation",
              "Only in children", "Only for vaccines"],
             1, "Disproportionality methods identify reporting patterns, not proof of causation."),
            ("Which method is used for quantitative signal detection?",
             ["ROR", "Tablet hardness test", "Friability test",
              "Dissolution test"],
             0, "ROR is a quantitative pharmacovigilance signal detection method."),
            ("What is signal prioritisation?",
             ["Ranking signals according to their potential importance",
              "Deleting all signals", "Changing medicine names",
              "Stopping all clinical trials"],
             0, "Prioritisation helps focus assessment on important potential safety concerns."),
            ("What may follow confirmation of an important safety concern?",
             ["Further investigation and regulatory action where appropriate",
              "Automatic approval of the drug", "Ignoring the reports",
              "Deleting the database"],
             0, "Evidence may support additional investigation and appropriate safety measures."),
            ("Which is an important source of spontaneous safety information?",
             ["Healthcare professional reports", "Product advertisements",
              "Packaging artwork", "Sales invoices"],
             0, "Healthcare professionals can submit suspected ADR reports.")
        ],

        "5. Establishment and Development of PvPI": [
            ("What is the full form of PvPI?",
             ["Pharmacovigilance Programme of India", "Pharmaceutical Vaccine Programme of India",
              "Patient Verification Programme of India", "Pharmacy Validation Programme of India"],
             0, "PvPI stands for Pharmacovigilance Programme of India."),
            ("In which year was PvPI launched?",
             ["2005", "2010", "2015", "2020"],
             1, "PvPI was launched in July 2010."),
            ("Which ministry launched PvPI?",
             ["Ministry of Health and Family Welfare",
              "Ministry of Education", "Ministry of Finance",
              "Ministry of Commerce"],
             0, "PvPI was launched under the Ministry of Health and Family Welfare."),
            ("Which institution is the current National Coordination Centre of PvPI?",
             ["Indian Pharmacopoeia Commission",
              "AIIMS Mumbai", "ICMR New Delhi", "NIPER Mohali"],
             0, "IPC in Ghaziabad is the National Coordination Centre of PvPI."),
            ("Where was the initial National Coordination Centre located?",
             ["AIIMS New Delhi", "IPC Ghaziabad",
              "CDSCO Mumbai", "NIPER Hyderabad"],
             0, "AIIMS New Delhi initially served as the National Coordination Centre."),
            ("In which year was the NCC shifted to IPC?",
             ["2010", "2011", "2015", "2018"],
             1, "The National Coordination Centre shifted to IPC on 15 April 2011."),
            ("What does AMC stand for in PvPI?",
             ["ADR Monitoring Centre", "Approved Medicine Committee",
              "Adverse Medicine Council", "Annual Monitoring Cell"],
             0, "AMCs are ADR Monitoring Centres participating in the programme."),
            ("What is a major function of PvPI?",
             ["Collection and evaluation of suspected ADR reports",
              "Manufacturing all medicines", "Issuing driving licences",
              "Conducting pharmacy admissions"],
             0, "PvPI collects and evaluates suspected adverse drug reaction reports."),
            ("Who can submit suspected ADR reports to PvPI?",
             ["Only physicians", "Only pharmacists",
              "Healthcare professionals and consumers", "Only manufacturers"],
             2, "Healthcare professionals and consumers can report suspected ADRs."),
            ("What is the main purpose of PvPI?",
             ["Improving medicine safety in India",
              "Increasing drug advertisements", "Controlling pharmacy fees",
              "Manufacturing vaccines"],
             0, "PvPI supports patient safety through medicine safety monitoring.")
        ],

        "6. CDSCO – Functions and Role in Pharmacovigilance": [
            ("What is the full form of CDSCO?",
             ["Central Drugs Standard Control Organisation",
              "Central Drug Safety Coordination Office",
              "Council for Drug Standards and Clinical Operations",
              "Central Department of Scientific Clinical Oversight"],
             0, "CDSCO stands for Central Drugs Standard Control Organisation."),
            ("CDSCO functions under which ministry?",
             ["Ministry of Health and Family Welfare",
              "Ministry of Education", "Ministry of Finance",
              "Ministry of Agriculture"],
             0, "CDSCO functions under the Ministry of Health and Family Welfare."),
            ("Who heads CDSCO?",
             ["Drugs Controller General (India)",
              "Director of WHO", "President of PCI",
              "Director of AICTE"],
             0, "The Drugs Controller General (India), or DCGI, heads CDSCO."),
            ("Which is a major function of CDSCO?",
             ["Regulation of new drugs and clinical trials",
              "Conducting university examinations", "Teaching pharmacology",
              "Manufacturing all generic medicines"],
             0, "CDSCO performs regulatory functions relating to new drugs and clinical trials."),
            ("What is the relationship between PvPI and CDSCO?",
             ["They have complementary roles in medicine safety",
              "They are the same organisation", "They are unrelated to drug safety",
              "Both are pharmaceutical manufacturers"],
             0, "PvPI monitors medicine safety and CDSCO performs regulatory functions."),
            ("Which organisation is the National Coordination Centre of PvPI?",
             ["IPC", "CDSCO headquarters", "AICTE", "UGC"],
             0, "Indian Pharmacopoeia Commission is the National Coordination Centre."),
            ("Which activity falls within CDSCO regulatory functions?",
             ["Regulation of imported drugs",
              "Conducting college sports", "Awarding university degrees",
              "Issuing driving licences"],
             0, "CDSCO has regulatory responsibilities concerning imported drugs."),
            ("What may be an outcome of a regulatory safety review?",
             ["Appropriate labelling changes or other regulatory measures",
              "Automatic withdrawal of every medicine",
              "No action under any circumstances", "Changing the patient's diagnosis"],
             0, "Regulatory decisions depend on evidence and may include appropriate safety measures."),
            ("Which is the correct distinction?",
             ["PvPI monitors and evaluates safety information; CDSCO performs regulatory oversight",
              "CDSCO collects all prescriptions; PvPI manufactures drugs",
              "Both only conduct clinical examinations",
              "Neither has a medicine safety role"],
             0, "PvPI and CDSCO have complementary medicine-safety and regulatory roles."),
            ("What does DCGI stand for?",
             ["Drugs Controller General (India)",
              "Drug Clinical Guidance Institute",
              "Director of Clinical Government Inspection",
              "Drug Coordination Group of India"],
             0, "DCGI stands for Drugs Controller General (India).")
        ]
    }

    if topic in quiz_data:

        questions = quiz_data[topic]

        st.write("**Number of questions:** 10")
        st.write("**Maximum marks:** 10")

        with st.form("pv_quiz_form"):

            answers = []

            for i, q in enumerate(questions):
                st.markdown(f"**Q{i + 1}. {q[0]}**")

                selected = st.radio(
                    "Choose your answer:",
                    q[1],
                    index=None,
                    key=f"pv_{topic}_{i}",
                    label_visibility="collapsed"
                )

                answers.append(selected)
                st.divider()

            submitted = st.form_submit_button(
                "Submit Quiz",
                use_container_width=True
            )

        if submitted:

            if any(answer is None for answer in answers):
                st.warning("Please answer all 10 questions before submitting.")

            else:
                score = 0

                for i, q in enumerate(questions):
                    if answers[i] == q[1][q[2]]:
                        score += 1

                percentage = (score / len(questions)) * 100

                st.subheader("Your Quiz Result")
                st.metric("Score", f"{score}/10")
                st.metric("Percentage", f"{percentage:.0f}%")

                if percentage >= 80:
                    st.success("Excellent! Outstanding knowledge.")
                elif percentage >= 60:
                    st.info("Good performance! Keep learning.")
                else:
                    st.warning("Keep practising and revise this topic.")

                st.subheader("Answer Review")

                for i, q in enumerate(questions):

                    with st.expander(f"Question {i + 1}: {q[0]}"):

                        correct_answer = q[1][q[2]]

                        st.write("Your answer:", answers[i])
                        st.write("Correct answer:", correct_answer)
                        st.write("Explanation:", q[3])

                        if answers[i] == correct_answer:
                            st.success("Correct answer")
                        else:
                            st.error("Incorrect answer")

                if st.button("Retake Quiz"):
                    for i in range(len(questions)):
                        key = f"pv_{topic}_{i}"
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()

    st.info(
        "Educational content for pharmacy students and healthcare "
        "professionals. Refer to current official guidelines and "
        "regulatory documents for professional practice."
    )

elif page == "Research Dashboard":

    st.header("📊 Research Dashboard")

    if not drugs.empty:
        st.metric("Total Medicines in Database", len(drugs))

        if "Drug_Class" in drugs.columns:
            st.metric(
                "Different Drug Classes",
                drugs["Drug_Class"].nunique()
            )

        st.subheader("Drug Master Database")
        st.dataframe(drugs, use_container_width=True)

        st.download_button(
            "Download Drug Database",
            data=drugs.to_csv(index=False).encode("utf-8"),
            file_name="PharmaSentry_Drug_Master.csv",
            mime="text/csv"
        )
    else:
        st.warning("Drug database is not available.")

elif page == "About":

    st.title("🛡️ About PharmaSentry AI")

    st.subheader("Application Overview")

    st.write(
        "PharmaSentry AI is an academic, research-oriented and "
        "educational digital initiative designed to integrate "
        "pharmaceutical sciences with artificial intelligence "
        "concepts and digital technology."
    )

    st.write(
        "The application focuses on pharmacovigilance, adverse "
        "drug reaction (ADR) awareness, medicine safety information, "
        "ADR documentation and rational medicine use."
    )

    st.write(
        "Its primary objective is to provide an educational platform "
        "for pharmacy students, academicians, researchers and "
        "healthcare professionals to explore fundamental concepts "
        "related to medication safety and pharmacovigilance."
    )

    st.divider()

    st.subheader("💊 Application Features and Uses")

    st.markdown("""
    **1. Drug Safety Assistant**

    Provides access to available drug information, including drug
    classification, indications, common adverse reactions, serious
    adverse reactions, warnings, contraindications and monitoring.

    **2. Drug–ADR Safety Screening**

    Compares user-entered adverse reactions with the available
    medicine database using preliminary keyword-matching logic.

    **3. ADR Completeness Checker**

    Supports educational understanding of essential information
    required for documenting an Individual Case Safety Report (ICSR).

    **4. Pharmacovigilance Learning Centre**

    Provides learning material covering:
    - Introduction to Pharmacovigilance
    - Adverse Drug Reactions and their classification
    - Individual Case Safety Reports (ICSR)
    - Signal Detection
    - Pharmacovigilance Programme of India (PvPI)
    - Central Drugs Standard Control Organisation (CDSCO)

    **5. Research Dashboard**

    Provides an overview of the application's research,
    development and evaluation activities.

    **6. Educational and Awareness Platform**

    Encourages awareness of medication safety, adverse drug
    reaction reporting and rational medicine use.
    """)

    st.divider()

    st.subheader("⚙️ How the Application Works")

    st.write(
        "PharmaSentry AI currently uses a structured drug database "
        "and rule-based keyword-matching techniques to demonstrate "
        "basic drug–ADR screening concepts."
    )

    st.write(
        "The screening output depends on the information available "
        "in the database. The present prototype does not use an "
        "integrated AI language model or independently establish "
        "clinical causality."
    )

    st.divider()

    st.subheader("👨‍⚕️ About the Author")

    st.write("Dr. Praveen R Biradar")

    st.write(
        "Pharm.D | Assistant Professor | Pharmacy Educator | "
        "Pharmacovigilance and Medication Safety Researcher"
    )

    st.write("Institutional Affiliation")

    st.write(
        "Shantha College of Pharmacy, Peresandra, "
        "Chikkaballapura, Karnataka – 562104"
    )

    st.write(
        "The application is conceptualised and developed by "
        "Dr. Praveen R Biradar as an academic and research-oriented "
        "initiative to explore the integration of pharmaceutical "
        "knowledge, pharmacovigilance and digital innovation."
    )

    st.write(
        "The project reflects an interest in promoting "
        "pharmacovigilance education, ADR awareness, medication "
        "safety research and technology-supported pharmacy practice."
    )

    st.divider()

    st.subheader("🔬 Vision and Future Scope")

    st.write(
        "The vision of PharmaSentry AI is to encourage the integration "
        "of pharmaceutical sciences, pharmacovigilance and emerging "
        "digital technologies to promote awareness of safer medicine use."
    )

    st.write("Future development objectives include:")

    st.markdown("""
    - Expansion of the verified drug safety database.
    - Incorporation of authoritative Indian medicine safety information.
    - Improvement of ADR terminology recognition and matching.
    - Development of structured ADR documentation and evaluation tools.
    - Integration of evidence-based information retrieval.
    - Expert validation and systematic performance evaluation.
    - Advancement towards more comprehensive digital pharmacovigilance tools.
    """)

    st.divider()

    st.subheader("⚠️ Disclaimer")

    st.warning(
        "PharmaSentry AI is an academic and educational prototype "
        "developed for learning, research and pharmacovigilance awareness."
    )

    st.write(
        "The medicine information displayed in this application is "
        "based on the currently available project database. Source "
        "verification status may vary, and Indian product-label "
        "verification is pending for some entries."
    )

    st.write(
        "The Drug–ADR Safety Screening module uses preliminary "
        "keyword matching. A database match does not establish "
        "a causal relationship between a medicine and an adverse "
        "reaction. Classification into common or serious database "
        "entries does not determine the actual clinical severity "
        "of an individual patient's reaction."
    )

    st.write(
        "A negative screening result does not exclude the possibility "
        "of an adverse drug reaction. The application must not be used "
        "as a substitute for professional medical judgement, clinical "
        "diagnosis, treatment decisions or prescribing decisions."
    )

    st.write(
        "The ADR Completeness Checker is intended for educational "
        "demonstration and does not replace official ICSR submission "
        "requirements or pharmacovigilance expert review."
    )

    st.write(
        "Users should consult current official guidance from WHO, "
        "CDSCO, PvPI, ICH and other relevant regulatory authorities "
        "before using information for professional purposes."
    )

    st.write(
        "Do not enter identifiable patient information or confidential "
        "medical records into this prototype."
    )

    st.divider()

    st.caption(
        "PharmaSentry AI | Conceptualised and Developed by "
        "Dr. Praveen R Biradar | Shantha College of Pharmacy, "
        "Peresandra, Chikkaballapura, Karnataka – 562104"
    )
