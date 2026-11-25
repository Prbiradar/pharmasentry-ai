
import streamlit as st

st.set_page_config(
    page_title="PharmaSentry AI",
    page_icon="💊",
    layout="wide"
)

st.title("💊 PharmaSentry AI")
st.caption(
    "AI-Assisted Pharmacovigilance and Medication Safety Platform"
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a module",
    [
        "Home",
        "Drug Safety Assistant",
        "ADR Completeness Checker",
        "Learning Centre",
        "About"
    ]
)

st.sidebar.info("Research Prototype | Version 1.0")


if page == "Home":

    st.header("Welcome to PharmaSentry AI")

    st.write(
        "A digital platform designed to support "
        "pharmacovigilance education, drug safety research "
        "and medication safety awareness."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💊 Drug Safety Assistant")
        st.write(
            "Explore drug safety information and "
            "evidence-based medication resources."
        )

    with col2:
        st.subheader("📋 ADR Completeness Checker")
        st.write(
            "Identify missing information in "
            "adverse drug reaction case reports."
        )

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📚 Learning Centre")
        st.write(
            "Learn pharmacovigilance concepts "
            "through structured educational content."
        )

    with col4:
        st.subheader("🔬 Research Platform")
        st.write(
            "Develop and evaluate tools for "
            "medication safety research."
        )

    st.divider()
    st.success("PharmaSentry AI prototype interface is ready.")


elif page == "Drug Safety Assistant":

    st.header("💊 Drug Safety Assistant")

    st.write(
        "Search the prototype drug list. "
        "Detailed safety evidence will be added after source verification."
    )

    drugs = {
        "Paracetamol": "Analgesic",
        "Amoxicillin": "Penicillin antibiotic",
        "Metformin": "Biguanide",
        "Ibuprofen": "NSAID",
        "Amlodipine": "Calcium channel blocker",
        "Atorvastatin": "HMG-CoA reductase inhibitor",
        "Pantoprazole": "Proton pump inhibitor",
        "Ciprofloxacin": "Fluoroquinolone",
        "Losartan": "Angiotensin receptor blocker",
        "Glimepiride": "Sulfonylurea"
    }

    drug = st.selectbox(
        "Select a medicine",
        list(drugs.keys())
    )

    st.subheader(drug)
    st.write("Drug class:", drugs[drug])

    st.warning(
        "Verified indications, adverse reactions, warnings "
        "and contraindications have not yet been populated. "
        "Do not use this prototype for clinical decisions."
    )

    st.info(
        "Future feature: source-linked drug safety information "
        "with evidence verification."
    )


elif page == "ADR Completeness Checker":

    st.header("📋 ADR Case Completeness Checker")

    st.write(
        "Enter a fictional adverse drug reaction case "
        "to identify missing reporting information."
    )

    age = st.text_input("Patient age")
    sex = st.selectbox(
        "Patient sex",
        ["Not specified", "Male", "Female", "Other"]
    )
    drug = st.text_input("Suspected medicine")
    reaction = st.text_input("Description of reaction")
    onset = st.text_input("Date of reaction onset")
    reporter = st.text_input("Reporter information")

    if st.button("Check Case Completeness"):

        fields = {
            "Patient age": age,
            "Patient sex": sex if sex != "Not specified" else "",
            "Suspected medicine": drug,
            "Reaction description": reaction,
            "Date of onset": onset,
            "Reporter information": reporter
        }

        missing = [
            name for name, value in fields.items()
            if not value.strip()
        ]

        st.subheader("Completeness Assessment")

        if missing:
            st.warning("Some information is missing.")

            for item in missing:
                st.write("❌", item)

        else:
            st.success(
                "All six prototype fields have been completed."
            )

        st.caption(
            "This is a basic field-completeness check, "
            "not a validated ICSR assessment or causality assessment."
        )


elif page == "Learning Centre":

    st.header("📚 Pharmacovigilance Learning Centre")

    topic = st.selectbox(
        "Choose a learning topic",
        [
            "Introduction to Pharmacovigilance",
            "Adverse Drug Reactions",
            "ICSR Reporting",
            "Serious Adverse Events",
            "Causality Assessment",
            "Pharmacovigilance in India"
        ]
    )

    descriptions = {
        "Introduction to Pharmacovigilance":
            "Pharmacovigilance involves activities related to "
            "the detection, assessment, understanding and prevention "
            "of adverse effects or other medicine-related problems.",

        "Adverse Drug Reactions":
            "An adverse drug reaction is a harmful and unintended "
            "response associated with the use of a medicinal product.",

        "ICSR Reporting":
            "An Individual Case Safety Report documents information "
            "about a suspected adverse reaction in an individual case.",

        "Serious Adverse Events":
            "Seriousness is assessed using regulatory criteria such "
            "as death, life-threatening events, hospitalisation "
            "and other medically important outcomes.",

        "Causality Assessment":
            "Causality assessment evaluates the relationship "
            "between a suspected medicine and an adverse reaction.",

        "Pharmacovigilance in India":
            "India's Pharmacovigilance Programme of India (PvPI) "
            "supports the monitoring of medicine safety."
    }

    st.subheader(topic)
    st.write(descriptions[topic])

    st.info("More learning modules and assessments will be added.")


elif page == "About":

    st.header("About PharmaSentry AI")

    st.write(
        "PharmaSentry AI is an independent academic prototype "
        "focused on pharmacovigilance, medication safety "
        "and pharmacy education."
    )

    st.subheader("Development objectives")

    st.markdown(
        """
        - Evidence-grounded drug safety information
        - ADR case completeness assessment
        - Pharmacovigilance education
        - English and Kannada learning support
        - Research and expert validation
        """
    )

    st.warning(
        "This prototype is for educational and research "
        "development only. It is not a substitute for "
        "professional clinical judgement."
    )

st.divider()

st.caption(
    "PharmaSentry AI | Academic Research Prototype | Version 1.0"
)
