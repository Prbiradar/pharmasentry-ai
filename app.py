import streamlit as st
import pandas as pd
import os

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

drugs = load_drugs()

st.title("💊 PharmaSentry AI")
st.caption("Evidence-Grounded Pharmacovigilance and Medication Safety Assistant")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Home",
        "Drug Safety Assistant",
        "Drug-ADR Safety Screening",
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
    st.write("4. Research Dashboard")

    st.info("This is an educational prototype, not a substitute for professional clinical judgement.")

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

    st.header("Drug-ADR Safety Screening")
    st.write("Compare a reported reaction with the drug database.")

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
            placeholder="Example: Liver damage"
        )

        if st.button("Screen Drug-ADR Record"):

            if not reaction.strip():
                st.warning("Please enter an adverse reaction.")

            else:
                selected_record = drugs[
                    drugs["Drug_Name"].astype(str) == selected_drug
                ].iloc[0]

                common_adr = str(
                    selected_record.get("Common_ADR", "")
                ).lower()

                serious_adr = str(
                    selected_record.get("Serious_ADR", "")
                ).lower()

                aliases = {
                    "liver damage": ["liver injury", "hepatotoxicity"],
                    "hepatotoxicity": ["liver injury", "liver damage"],
                    "liver injury": ["liver damage", "hepatotoxicity"],
                    "diarrhea": ["diarrhoea"],
                    "diarrhoea": ["diarrhea"],
                    "skin rash": ["rash"],
                    "rash": ["skin rash"]
                }

                entered_terms = [
                    term.strip().lower()
                    for term in reaction.split(",")
                    if term.strip()
                ]

                expanded_terms = set(entered_terms)

                for term in entered_terms:
                    expanded_terms.update(aliases.get(term, []))

                common_match = any(
                    term in common_adr
                    for term in expanded_terms
                )

                serious_match = any(
                    term in serious_adr
                    for term in expanded_terms
                )

                st.subheader("Screening Result")

                if serious_match:
                    st.error("Potential match with a serious ADR.")

                elif common_match:
                    st.success("Potential match with a common ADR.")

                else:
                    st.warning("No direct database match found.")

                st.write("Medicine:", selected_drug)
                st.write("Reported reaction:", reaction)
                st.write("Common ADRs:", common_adr)
                st.write("Serious ADRs:", serious_adr)

                st.info(
                    "This is preliminary text matching, not a "
                    "validated causality assessment. A match does "
                    "not prove that the medicine caused the reaction."
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

    st.header("📚 Pharmacovigilance Learning Centre")

    topics = {
        "Pharmacovigilance": "Science and activities relating to the detection, assessment, understanding and prevention of adverse effects or other medicine-related problems.",
        "Adverse Drug Reaction": "A harmful and unintended response to a medicinal product.",
        "ICSR": "Individual Case Safety Report containing information about a suspected adverse reaction in an individual patient.",
        "Signal Detection": "Process of identifying information suggesting a new potentially causal association or a new aspect of a known association.",
        "PVPI": "Pharmacovigilance Programme of India, the national pharmacovigilance programme."
    }

    for topic, description in topics.items():
        with st.expander(topic):
            st.write(description)

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

    st.header("About PharmaSentry AI")

    st.write(
        "PharmaSentry AI is an academic prototype designed "
        "to support pharmacovigilance education and medication safety awareness."
    )

    st.write("Developer: Pharmacy Research and Academic Project")

    st.warning(
        "The current prototype uses a local CSV database. "
        "It does not yet contain an integrated AI model or independently "
        "verified clinical decision-support functionality."
    )
