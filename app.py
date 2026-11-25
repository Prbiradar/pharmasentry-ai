
import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="PharmaSentry AI",
    page_icon="💊",
    layout="wide"
)

st.title("💊 PharmaSentry AI")
st.caption(
    "Evidence-Grounded Pharmacovigilance "
    "and Medication Safety Platform"
)

# Load drug database
@st.cache_data
def load_drugs():
    file_path = "Drug_Master.csv"

    if os.path.exists(file_path):
        return pd.read_csv(file_path).fillna("")

    return pd.DataFrame()

drugs_df = load_drugs()

# Sidebar navigation
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select module",
    [
        "Home",
        "Drug Safety Assistant",
        "ADR Completeness Checker",
        "Learning Centre",
        "Research Dashboard",
        "About"
    ]
)

st.sidebar.info("Research Prototype | Version 2.0")


# HOME
if page == "Home":

    st.header("Welcome to PharmaSentry AI")

    st.write(
        "A digital platform supporting pharmacovigilance "
        "education, drug safety research and medication safety."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💊 Drug Safety Assistant")
        st.write("Explore the connected drug safety database.")

    with col2:
        st.subheader("📋 ADR Completeness Checker")
        st.write("Identify missing information in ADR reports.")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📚 Learning Centre")
        st.write("Explore pharmacovigilance learning topics.")

    with col4:
        st.subheader("🔬 Research Dashboard")
        st.write("View the database and prototype statistics.")

    st.divider()

    if not drugs_df.empty:
        st.success(
            f"Drug database connected: {len(drugs_df)} records loaded."
        )
    else:
        st.error("Drug database not found. Check CSV filename.")


# DRUG SAFETY ASSISTANT
elif page == "Drug Safety Assistant":

    st.header("💊 Drug Safety Assistant")

    if drugs_df.empty:
        st.error("Unable to load Drug_Master.csv.")
    else:

        if "Drug_Name" not in drugs_df.columns:
            st.error("Drug_Name column is missing.")
        else:

            drug_names = sorted(
                drugs_df["Drug_Name"]
                .astype(str)
                .loc[lambda x: x.str.strip() != ""]
                .unique()
                .tolist()
            )

            if drug_names:

                selected_drug = st.selectbox(
                    "Search or select a medicine",
                    drug_names
                )

                result = drugs_df[
                    drugs_df["Drug_Name"].astype(str)
                    == selected_drug
                ].iloc[0]

                st.subheader(selected_drug)

                fields = [
                    "Drug_Class",
                    "Indication",
                    "Common_ADR",
                    "Serious_ADR",
                    "Warnings",
                    "Contraindications",
                    "Monitoring",
                    "Source",
                    "Source_Date",
                    "Verification_Status"
                ]

                for field in fields:
                    if field in drugs_df.columns:
                        value = str(result[field]).strip()

                        if value:
                            label = field.replace("_", " ")
                            st.markdown(f"**{label}:** {value}")
                        else:
                            st.info(
                                f"{field.replace('_', ' ')}: "
                                "Information not yet entered."
                            )

                st.warning(
                    "Educational research prototype only. "
                    "Unverified information must not be used "
                    "for clinical decisions."
                )

            else:
                st.warning("No medicine names found in the database.")


# ADR COMPLETENESS CHECKER
elif page == "ADR Completeness Checker":

    st.header("📋 ADR Case Completeness Checker")

    st.write("Use fictional cases only during prototype testing.")

    age = st.text_input("Patient age")
    sex = st.selectbox(
        "Patient sex",
        ["Not specified", "Male", "Female", "Other"]
    )
    drug = st.text_input("Suspected medicine")
    reaction = st.text_input("Reaction description")
    onset = st.text_input("Date of reaction onset")
    concomitant = st.text_input("Concomitant medicines")
    history = st.text_area("Relevant medical history")
    reporter = st.text_input("Reporter information")

    if st.button("Check Case Completeness"):

        fields = {
            "Patient age": age,
            "Patient sex": "" if sex == "Not specified" else sex,
            "Suspected medicine": drug,
            "Reaction description": reaction,
            "Date of onset": onset,
            "Concomitant medicines": concomitant,
            "Medical history": history,
            "Reporter information": reporter
        }

        missing = [
            name for name, value in fields.items()
            if not value.strip()
        ]

        st.subheader("Completeness Assessment")

        if missing:
            st.warning(
                f"{len(missing)} fields require attention."
            )

            for item in missing:
                st.write("❌", item)

        else:
            st.success("All prototype fields are completed.")

        st.caption(
            "This is a basic field-completeness check, "
            "not a validated ICSR or causality assessment."
        )


# LEARNING CENTRE
elif page == "Learning Centre":

    st.header("📚 Pharmacovigilance Learning Centre")

    topics = {
        "Introduction to Pharmacovigilance":
            "Pharmacovigilance involves the detection, "
            "assessment, understanding and prevention of "
            "adverse effects and other medicine-related problems.",

        "Adverse Drug Reactions":
            "An adverse drug reaction is a harmful and "
            "unintended response associated with a medicine.",

        "ICSR Reporting":
            "An Individual Case Safety Report documents "
            "information about a suspected adverse reaction.",

        "Serious Adverse Events":
            "Seriousness assessment considers outcomes such "
            "as death, life-threatening events and hospitalisation.",

        "Causality Assessment":
            "Causality assessment evaluates the relationship "
            "between a suspected medicine and an adverse reaction.",

        "Pharmacovigilance in India":
            "The Pharmacovigilance Programme of India "
            "supports monitoring of medicine safety."
    }

    topic = st.selectbox("Select a topic", list(topics.keys()))

    st.subheader(topic)
    st.write(topics[topic])


# RESEARCH DASHBOARD
elif page == "Research Dashboard":

    st.header("🔬 Research Dashboard")

    if not drugs_df.empty:

        st.metric("Drug records", len(drugs_df))

        if "Drug_Class" in drugs_df.columns:
            st.metric(
                "Drug classes",
                drugs_df["Drug_Class"].nunique()
            )

        st.subheader("Drug Database Preview")
        st.dataframe(drugs_df, use_container_width=True)

        st.download_button(
            "Download drug database CSV",
            data=drugs_df.to_csv(index=False),
            file_name="Drug_Master.csv",
            mime="text/csv"
        )

    else:
        st.error("Drug database is not available.")


# ABOUT
elif page == "About":

    st.header("About PharmaSentry AI")

    st.write(
        "PharmaSentry AI is an independent academic "
        "research prototype focused on pharmacovigilance, "
        "medication safety and pharmacy education."
    )

    st.markdown(
        """
        **Development objectives**

        - Evidence-grounded drug safety information
        - ADR case completeness assessment
        - Pharmacovigilance education
        - English and Kannada learning support
        - Research and expert validation
        """
    )

    st.warning(
        "This prototype is not a substitute for "
        "professional clinical judgement."
    )

st.divider()

st.caption(
    "PharmaSentry AI | Academic Research Prototype | Version 2.0"
)
