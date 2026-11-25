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
    st.write("Compare reported reactions with the drug database.")

    if drugs.empty:
        st.error("Drug database is not available.")

    else:
        selected_drug = st.selectbox(
            "Select suspected medicine",
            sorted(drugs["Drug_Name"].astype(str).unique()),
            key="screening_drug"
        )

        reaction = st.text_area(
            "Enter reported adverse reactions",
            placeholder="Example: Nausea, vomiting, liver damage"
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
                    "hepatotoxicity": ["liver injury", "hepatic injury"],
                    "diarrhea": ["diarrhoea"],
                    "loose stools": ["diarrhoea", "diarrhea"],
                    "stomach pain": ["abdominal pain"],
                    "feeling sick": ["nausea"],
                    "queasiness": ["nausea"],
                    "emesis": ["vomiting"],
                    "throwing up": ["vomiting"],
                    "skin rash": ["rash"],
                    "itching": ["pruritus"],
                    "hives": ["urticaria"],
                    "head pain": ["headache"],
                    "feeling dizzy": ["dizziness"],
                    "tiredness": ["fatigue"],
                    "weakness": ["asthenia"],
                    "breathlessness": ["dyspnea"],
                    "swelling": ["edema", "oedema"]
                }

                entered_terms = [
                    term.strip().lower()
                    for term in reaction.split(",")
                    if term.strip()
                ]

                st.subheader("Individual ADR Screening Results")

                for term in entered_terms:
                    expanded = {term}
                    expanded.update(aliases.get(term, []))

                    common_found = any(
                        item in common_adr for item in expanded
                    )

                    serious_found = any(
                        item in serious_adr for item in expanded
                    )

                    if serious_found:
                        st.error(
                            f"{term}: Potential serious ADR match"
                        )
                    elif common_found:
                        st.success(
                            f"{term}: Potential common ADR match"
                        )
                    else:
                        st.warning(
                            f"{term}: No direct database match"
                        )

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
