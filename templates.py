"""
Clinical note templates with PHI placeholder slots.

Placeholder naming convention maps to HIPAA Safe Harbor identifiers:
  {patient_name}, {patient_first}, {patient_last}   — names
  {provider_name}, {provider_first}, {provider_last} — provider names
  {dob}                                              — date of birth
  {admission_date}, {discharge_date}                 — encounter dates
  {appointment_date}, {procedure_date}               — encounter dates
  {phone}, {fax}                                     — telephone/fax numbers
  {email}                                            — email addresses
  {ssn}                                              — Social Security numbers
  {mrn}                                              — medical record numbers
  {street_address}, {city}, {state}, {zip_code}      — geographic data
  {full_address}                                     — combined address
  {health_plan_number}                               — health plan beneficiary numbers
  {account_number}                                   — account numbers
  {license_number}, {dea_number}                     — certificate/license numbers
  {device_id}                                        — device identifiers
  {url}                                              — web URLs
  {ip_address}                                       — IP addresses
"""

TEMPLATES = [
    {
        "type": "Progress Note",
        "text": (
            "PROGRESS NOTE\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "Date: {appointment_date}  Provider: {provider_name}\n"
            "Phone: {phone}  Health Plan #: {health_plan_number}\n\n"
            "SUBJECTIVE:\n"
            "{patient_first} is a 54-year-old presenting for follow-up of hypertension and "
            "type 2 diabetes mellitus. Patient reports overall improved energy since last visit. "
            "Blood glucose readings at home have been in the 130–160 mg/dL range fasting. "
            "Denies chest pain, shortness of breath, or lower extremity edema. "
            "Reports occasional headaches, approximately twice per week, relieved with acetaminophen.\n\n"
            "OBJECTIVE:\n"
            "BP 138/84 mmHg, HR 72 bpm, RR 16, Temp 98.4°F, SpO2 98% on room air, Wt 214 lbs.\n"
            "General: Alert and oriented, no acute distress.\n"
            "Cardiovascular: Regular rate and rhythm, no murmurs.\n"
            "Extremities: No edema.\n\n"
            "ASSESSMENT/PLAN:\n"
            "1. Hypertension — continue lisinopril 10 mg daily; encourage sodium restriction.\n"
            "2. Type 2 diabetes — continue metformin 1000 mg BID; recheck HbA1c in 3 months.\n"
            "3. Headaches — likely tension-type; continue PRN acetaminophen.\n\n"
            "Follow-up in 3 months or sooner if symptoms worsen.\n\n"
            "Electronically signed: {provider_name}, MD  License #: {license_number}"
        ),
    },
    {
        "type": "Discharge Summary",
        "text": (
            "DISCHARGE SUMMARY\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "Account #: {account_number}  Health Plan #: {health_plan_number}\n"
            "Admission Date: {admission_date}  Discharge Date: {discharge_date}\n"
            "Attending Physician: {provider_name}, MD\n\n"
            "ADMITTING DIAGNOSIS: Community-acquired pneumonia, right lower lobe.\n\n"
            "HOSPITAL COURSE:\n"
            "{patient_first} {patient_last} is a 67-year-old male admitted through the Emergency "
            "Department with a 4-day history of productive cough, fever to 102.1°F, and right-sided "
            "pleuritic chest pain. Chest X-ray confirmed right lower lobe infiltrate. Blood cultures "
            "drawn on admission grew Streptococcus pneumoniae. Patient was started on ceftriaxone "
            "1 g IV daily and azithromycin 500 mg IV daily. Transitioned to oral amoxicillin-clavulanate "
            "on day 3 after clinical improvement. Oxygen requirement resolved by day 2.\n\n"
            "DISCHARGE CONDITION: Stable, afebrile x 48 hours.\n\n"
            "DISCHARGE MEDICATIONS:\n"
            "- Amoxicillin-clavulanate 875/125 mg PO BID x 5 days\n"
            "- Guaifenesin 400 mg PO q4h PRN cough\n\n"
            "DISCHARGE INSTRUCTIONS:\n"
            "Return to ED for fever >101°F, worsening shortness of breath, or hemoptysis.\n"
            "Follow up with primary care in 7–10 days.\n\n"
            "Discharge address: {full_address}\n"
            "Contact phone: {phone}\n\n"
            "Attending: {provider_name}, MD  DEA #: {dea_number}"
        ),
    },
    {
        "type": "History and Physical",
        "text": (
            "HISTORY AND PHYSICAL\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "Date: {admission_date}  Admitting Provider: {provider_name}, MD\n"
            "Address: {street_address}, {city}, {state} {zip_code}\n"
            "Phone: {phone}  Email: {email}\n\n"
            "CHIEF COMPLAINT: Severe abdominal pain x 12 hours.\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "{patient_first} is a 38-year-old female with a history of cholelithiasis who presents "
            "with acute onset of severe right upper quadrant pain radiating to the right shoulder, "
            "associated with nausea and two episodes of vomiting. Pain began approximately 2 hours "
            "after a fatty meal. Denies fever or jaundice.\n\n"
            "PAST MEDICAL HISTORY: Cholelithiasis, GERD, seasonal allergies.\n"
            "SURGICAL HISTORY: Appendectomy (2009).\n"
            "MEDICATIONS: Omeprazole 20 mg daily, cetirizine 10 mg daily.\n"
            "ALLERGIES: Penicillin (hives).\n"
            "SOCIAL HISTORY: Non-smoker, occasional alcohol, employed as schoolteacher.\n"
            "FAMILY HISTORY: Father with CAD; mother with type 2 diabetes.\n\n"
            "REVIEW OF SYSTEMS: Positive for nausea, vomiting, RUQ pain. Negative for fever, "
            "jaundice, changes in stool or urine color.\n\n"
            "PHYSICAL EXAM:\n"
            "Vitals: BP 122/78, HR 98, Temp 98.8°F, RR 18, SpO2 99%.\n"
            "Abdomen: Tender RUQ with positive Murphy's sign. No rebound or guarding.\n\n"
            "ASSESSMENT/PLAN: Acute cholecystitis. Admit for surgical consult and IV antibiotics.\n\n"
            "SSN: {ssn}\n"
            "Signed: {provider_name}, MD  License #: {license_number}"
        ),
    },
    {
        "type": "Radiology Report",
        "text": (
            "RADIOLOGY REPORT\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "Exam Date: {procedure_date}  Account #: {account_number}\n"
            "Ordering Provider: {provider_name}, MD\n"
            "Interpreting Radiologist: {provider_first} {provider_last}, MD\n\n"
            "EXAMINATION: CT Abdomen and Pelvis with contrast.\n\n"
            "CLINICAL INDICATION: Right lower quadrant pain, rule out appendicitis.\n\n"
            "TECHNIQUE: Axial images were acquired through the abdomen and pelvis following "
            "administration of 100 mL IV contrast. Oral contrast was administered.\n\n"
            "FINDINGS:\n"
            "Liver: Normal size and attenuation. No focal lesions.\n"
            "Gallbladder: Small calculi present; no wall thickening or pericholecystic fluid.\n"
            "Pancreas: Normal in size and morphology.\n"
            "Spleen: Unremarkable.\n"
            "Kidneys: Bilateral kidneys normal in size. No hydronephrosis. No calculi.\n"
            "Appendix: Dilated to 11 mm in diameter with periappendiceal fat stranding and a "
            "2 mm appendicolith at the base. Findings consistent with acute appendicitis.\n"
            "Bowel: No obstruction.\n"
            "Lymph nodes: No significant adenopathy.\n\n"
            "IMPRESSION:\n"
            "1. Acute appendicitis with appendicolith. Surgical consultation recommended.\n"
            "2. Cholelithiasis without evidence of acute cholecystitis.\n\n"
            "Report electronically signed by {provider_first} {provider_last}, MD\n"
            "License #: {license_number}  Fax: {fax}"
        ),
    },
    {
        "type": "Lab Report",
        "text": (
            "LABORATORY REPORT\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "Collected: {procedure_date}  Account #: {account_number}\n"
            "Ordering Provider: {provider_name}, MD\n"
            "Health Plan #: {health_plan_number}\n\n"
            "SPECIMEN: Venous blood\n\n"
            "COMPLETE METABOLIC PANEL:\n"
            "Sodium:       138 mEq/L     (136–145)  Normal\n"
            "Potassium:    4.1 mEq/L     (3.5–5.0)  Normal\n"
            "Chloride:     101 mEq/L     (98–107)   Normal\n"
            "CO2:          24 mEq/L      (22–29)    Normal\n"
            "BUN:          18 mg/dL      (7–25)     Normal\n"
            "Creatinine:   1.0 mg/dL     (0.6–1.2)  Normal\n"
            "eGFR:         >60                       Normal\n"
            "Glucose:      214 mg/dL     (70–99)    HIGH\n"
            "Calcium:      9.4 mg/dL     (8.5–10.5) Normal\n"
            "Total Protein: 7.2 g/dL    (6.3–8.2)  Normal\n"
            "Albumin:      4.0 g/dL      (3.5–5.0)  Normal\n"
            "Total Bilirubin: 0.6 mg/dL (0.2–1.2)  Normal\n"
            "AST:          28 U/L        (10–40)    Normal\n"
            "ALT:          32 U/L        (7–56)     Normal\n"
            "Alk Phos:     88 U/L        (44–147)   Normal\n\n"
            "HbA1c:        8.4%                      HIGH (target <7.0% for diabetics)\n\n"
            "Interpreting provider: {provider_name}, MD\n"
            "Device ID: {device_id}\n"
            "Results portal: {url}"
        ),
    },
    {
        "type": "Referral Letter",
        "text": (
            "REFERRAL LETTER\n\n"
            "Date: {appointment_date}\n\n"
            "To: Cardiology Department\n"
            "From: {provider_name}, MD\n"
            "License #: {license_number}  DEA #: {dea_number}\n"
            "Fax: {fax}\n\n"
            "RE: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "Address: {street_address}, {city}, {state} {zip_code}\n"
            "Phone: {phone}  Email: {email}\n\n"
            "Dear Cardiology Colleague,\n\n"
            "I am referring {patient_first} {patient_last}, a 61-year-old male with a 15-year history "
            "of hypertension and newly diagnosed hyperlipidemia, for evaluation of exertional chest "
            "tightness. He reports substernal pressure with moderate exertion (climbing two flights of "
            "stairs) that resolves with rest. He denies rest pain, diaphoresis, or syncope. "
            "ECG performed in my office showed non-specific ST-T wave changes in leads V4–V6. "
            "Resting echocardiogram showed EF 55%, mild LV hypertrophy.\n\n"
            "Current medications include amlodipine 10 mg daily, atorvastatin 40 mg nightly, "
            "and aspirin 81 mg daily. He has no known drug allergies.\n\n"
            "I would appreciate your evaluation and stress testing as clinically appropriate. "
            "Please feel free to contact me at {phone} or fax records to {fax}.\n\n"
            "Thank you for your care of {patient_first}.\n\n"
            "Sincerely,\n"
            "{provider_name}, MD"
        ),
    },
    {
        "type": "Prescription",
        "text": (
            "PRESCRIPTION\n\n"
            "Prescriber: {provider_name}, MD\n"
            "License #: {license_number}  DEA #: {dea_number}\n"
            "Address: {street_address}, {city}, {state} {zip_code}\n"
            "Phone: {phone}  Fax: {fax}\n"
            "Date: {appointment_date}\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "Address: {full_address}\n"
            "Health Plan #: {health_plan_number}\n\n"
            "Rx:\n"
            "Hydrocodone/Acetaminophen 5/325 mg tablets\n"
            "Sig: Take 1 tablet by mouth every 6 hours as needed for moderate to severe pain\n"
            "Disp: #20 (twenty) tablets\n"
            "Refills: 0\n\n"
            "Indication: Post-operative pain management following right knee arthroscopy.\n\n"
            "Do not fill if altered. DEA Schedule II controlled substance.\n\n"
            "Prescriber signature: {provider_name}, MD\n"
            "Electronic prescription transmitted to pharmacy."
        ),
    },
    {
        "type": "Operative Note",
        "text": (
            "OPERATIVE NOTE\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "Account #: {account_number}  Date of Procedure: {procedure_date}\n"
            "Surgeon: {provider_name}, MD  License #: {license_number}\n"
            "Anesthesiologist: Dr. Chen, MD\n\n"
            "PREOPERATIVE DIAGNOSIS: Acute appendicitis.\n"
            "POSTOPERATIVE DIAGNOSIS: Acute appendicitis confirmed.\n"
            "PROCEDURE PERFORMED: Laparoscopic appendectomy.\n"
            "ANESTHESIA: General endotracheal.\n"
            "ESTIMATED BLOOD LOSS: 15 mL.\n"
            "SPECIMENS: Appendix sent to pathology.\n"
            "COMPLICATIONS: None.\n\n"
            "OPERATIVE REPORT:\n"
            "The patient was taken to the operating room and placed supine on the operating table. "
            "General anesthesia was induced without difficulty. The abdomen was prepped and draped "
            "in the usual sterile fashion. A 12 mm trocar was introduced at the umbilicus under "
            "direct visualization. Pneumoperitoneum was established to 15 mmHg. Two additional "
            "5 mm trocars were placed in the suprapubic and left lower quadrant positions.\n\n"
            "The appendix was identified in the right lower quadrant, grossly inflamed with "
            "periappendiceal erythema. No perforation was noted. The mesoappendix was divided "
            "using the LigaSure device. The base of the appendix was secured with two endoloops "
            "and the appendix transected. The specimen was placed in an endobag and extracted "
            "through the umbilical port site.\n\n"
            "The abdomen was irrigated with 500 mL warm saline. Hemostasis confirmed. "
            "Trocars removed under direct visualization. Fascial defects closed. Skin closed "
            "with subcuticular sutures.\n\n"
            "Patient tolerated procedure well. Transferred to PACU in stable condition.\n\n"
            "Surgeon: {provider_name}, MD  DEA #: {dea_number}"
        ),
    },
    {
        "type": "Nursing Note",
        "text": (
            "NURSING NOTE\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "Date/Time: {admission_date} 14:30  Unit: 4 North Medical-Surgical\n"
            "Nurse: {provider_first} {provider_last}, RN  License #: {license_number}\n\n"
            "ASSESSMENT:\n"
            "{patient_first} is alert and oriented x 3. Reports pain 4/10 at rest, 7/10 with "
            "movement, describing it as sharp in the right lower quadrant. Last analgesic dose "
            "was administered at 12:00. IV site right forearm — patent, no signs of infiltration "
            "or phlebitis. Foley catheter in place draining clear yellow urine, 75 mL/hour.\n\n"
            "Vital Signs:\n"
            "BP 118/74 mmHg  HR 84 bpm  RR 16  Temp 99.1°F  SpO2 97% on 2L NC\n\n"
            "INTERVENTIONS:\n"
            "- Repositioned patient for comfort; elevated HOB 30 degrees.\n"
            "- Administered morphine 2 mg IV as ordered at 14:15; pain reassessed at 14:45, "
            "patient reports pain 2/10.\n"
            "- Encouraged incentive spirometry q1h while awake; patient performed 10 reps "
            "to 1200 mL volume.\n"
            "- Ambulated patient to bathroom with assistance; tolerated without dizziness.\n"
            "- IV fluids: NS at 75 mL/hr running as ordered.\n\n"
            "PLAN:\n"
            "Continue post-operative monitoring. Pain management per order set. "
            "Advance diet as tolerated per surgeon orders. Notify MD for temp >101°F, "
            "HR >110, or SpO2 <94%.\n\n"
            "Device ID (IV pump): {device_id}\n"
            "Phone contact: {phone}"
        ),
    },
    {
        "type": "Consultation Note",
        "text": (
            "CONSULTATION NOTE\n\n"
            "Consulting Service: Nephrology\n"
            "Consulting Physician: {provider_name}, MD  License #: {license_number}\n"
            "Date of Consultation: {appointment_date}\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "Health Plan #: {health_plan_number}  Account #: {account_number}\n"
            "Email: {email}\n\n"
            "REASON FOR CONSULTATION: Acute kidney injury, creatinine rise from baseline 1.1 "
            "to 2.8 mg/dL over 48 hours in setting of contrast administration.\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "{patient_last} is a 72-year-old female with CKD stage 3 (baseline Cr 1.1), "
            "type 2 diabetes, and hypertension admitted for NSTEMI. She received IV contrast "
            "for cardiac catheterization two days prior. Urine output has remained adequate "
            "at >0.5 mL/kg/hr. She is hemodynamically stable.\n\n"
            "PHYSICAL EXAM:\n"
            "BP 146/88, HR 76. No signs of volume overload. Trace lower extremity edema bilaterally.\n\n"
            "RELEVANT LABS:\n"
            "BMP today: Creatinine 2.8, BUN 42, K+ 4.6, HCO3 20.\n"
            "Urinalysis: Muddy brown casts consistent with ATN.\n\n"
            "IMPRESSION AND PLAN:\n"
            "1. Contrast-induced nephropathy / ATN — hold nephrotoxins, maintain euvolemia, "
            "IV fluids at 75 mL/hr, repeat BMP in 24 hours.\n"
            "2. Avoid further contrast agents until renal function recovers.\n"
            "3. Renal dosing adjustments: hold metformin, adjust lisinopril dose.\n"
            "4. Dialysis not indicated at this time. Will follow daily.\n\n"
            "Thank you for this interesting consultation.\n\n"
            "{provider_name}, MD — Nephrology\n"
            "Phone: {phone}  Fax: {fax}"
        ),
    },
    {
        "type": "Emergency Department Note",
        "text": (
            "EMERGENCY DEPARTMENT NOTE\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "Account #: {account_number}  Arrival: {admission_date}\n"
            "ED Physician: {provider_name}, MD  License #: {license_number}\n"
            "Phone: {phone}\n\n"
            "TRIAGE CHIEF COMPLAINT: Chest pain and shortness of breath.\n"
            "TRIAGE ACUITY: ESI Level 2\n\n"
            "HISTORY:\n"
            "{patient_first} is a 58-year-old male with known CAD (stents x2, 2021) and "
            "hypertension presenting with 2-hour history of substernal chest pressure radiating "
            "to the left arm, associated with diaphoresis and mild shortness of breath. "
            "Onset at rest. Denies pleuritic pain or cough.\n\n"
            "EXAM:\n"
            "BP 158/96 right arm, HR 102, RR 20, SpO2 94% RA (improved to 98% on 2L NC), "
            "Temp 98.6°F. Diaphoretic. Mild JVD. S3 gallopheard. Crackles bilateral bases.\n\n"
            "WORKUP:\n"
            "12-lead ECG: ST elevations in II, III, aVF — inferior STEMI pattern.\n"
            "Troponin I: 2.4 ng/mL (reference <0.04).\n"
            "CXR: Mild pulmonary vascular congestion.\n\n"
            "TREATMENT:\n"
            "Aspirin 325 mg PO, heparin IV bolus and infusion, ticagrelor 180 mg PO. "
            "Cardiology activated. Cath lab team on standby.\n\n"
            "DISPOSITION: Admitted to CCU for emergent cardiac catheterization.\n\n"
            "Address on file: {street_address}, {city}, {state} {zip_code}\n"
            "Health Plan #: {health_plan_number}  SSN: {ssn}"
        ),
    },
    {
        "type": "Pathology Report",
        "text": (
            "PATHOLOGY REPORT\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "Accession #: {account_number}  Procedure Date: {procedure_date}\n"
            "Submitting Physician: {provider_name}, MD  License #: {license_number}\n"
            "Pathologist: Dr. Rivera, MD\n\n"
            "SPECIMEN: Appendix, laparoscopic appendectomy.\n\n"
            "CLINICAL HISTORY: 38-year-old female with acute appendicitis.\n\n"
            "GROSS DESCRIPTION:\n"
            "Received is a vermiform appendix measuring 7.5 cm in length and up to 1.5 cm in "
            "diameter. The serosal surface is erythematous with focal fibrinous exudate. "
            "On sectioning, the lumen is occluded by a 0.4 cm fecalith. The mucosa is "
            "congested and focally ulcerated.\n\n"
            "MICROSCOPIC DESCRIPTION:\n"
            "Sections show acute suppurative appendicitis with transmural neutrophilic infiltration "
            "and periappendiceal fat necrosis. A fecalith is identified at the base. "
            "No perforation is identified. No dysplasia or malignancy is seen.\n\n"
            "DIAGNOSIS:\n"
            "Appendix: Acute suppurative appendicitis with fecalith. No perforation. "
            "Surgical margins not applicable. Pathologic staging: not applicable.\n\n"
            "Electronically signed: Dr. Rivera, MD\n"
            "Report transmitted to: {provider_name}, MD  Fax: {fax}\n"
            "Patient contact: {email}"
        ),
    },
    {
        "type": "Physical Therapy Note",
        "text": (
            "PHYSICAL THERAPY NOTE\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "Date: {appointment_date}  Visit #: 4 of 12\n"
            "Therapist: {provider_name}, PT, DPT  License #: {license_number}\n"
            "Health Plan #: {health_plan_number}\n\n"
            "DIAGNOSIS: Right rotator cuff repair, status post-surgery {procedure_date}.\n\n"
            "SUBJECTIVE:\n"
            "{patient_first} reports pain level 3/10 at rest, 5/10 with overhead activity. "
            "States sleep is disrupted approximately 2x/night due to shoulder discomfort. "
            "Able to perform ADLs independently with modifications. Working from home and "
            "reports difficulty typing for extended periods.\n\n"
            "OBJECTIVE:\n"
            "ROM (active): Flexion 95°, Abduction 80°, ER 30°, IR 55°.\n"
            "Strength (MMT): Deltoid 4/5, supraspinatus 3+/5, infraspinatus 3/5.\n"
            "Special tests: Positive Neer sign, negative Hawkins-Kennedy.\n"
            "Posture: Forward head, rounded shoulders.\n\n"
            "TREATMENT PROVIDED:\n"
            "- Ultrasound to posterior capsule (1 MHz, 1.0 W/cm², 5 min)\n"
            "- Codman pendulum exercises 3x50 reps\n"
            "- Scapular stabilization exercises: rows, retraction\n"
            "- Supine passive ER stretching\n"
            "- Patient education: posture correction, activity modification\n\n"
            "PLAN:\n"
            "Continue current protocol. Progress to active-assisted ROM exercises next visit. "
            "Home exercise program reviewed and updated. Next appointment in 3 days.\n\n"
            "Contact: {phone}  Email: {email}"
        ),
    },
    {
        "type": "Mental Health Note",
        "text": (
            "MENTAL HEALTH PROGRESS NOTE\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "Date: {appointment_date}  Session #: 8\n"
            "Provider: {provider_name}, LCSW  License #: {license_number}\n"
            "Health Plan #: {health_plan_number}\n"
            "Telehealth session. Patient IP address on file: {ip_address}\n\n"
            "DIAGNOSIS: Major depressive disorder, recurrent, moderate (F33.1).\n\n"
            "SUBJECTIVE:\n"
            "{patient_first} presents via telehealth. Reports moderate improvement in mood over "
            "the past two weeks since medication adjustment by psychiatrist. PHQ-9 score today: "
            "11 (baseline: 18). Continues to endorse low energy, difficulty concentrating, and "
            "reduced motivation. Denies current suicidal ideation, plan, or intent. Last SI "
            "episode was 6 weeks ago (passive, no intent — safety plan in place).\n\n"
            "Sleep improved from 4 hours to 5–6 hours nightly. Appetite remains decreased "
            "but has been eating at least 2 meals/day. No alcohol or substance use.\n\n"
            "OBJECTIVE:\n"
            "Appearance: Neat, appropriate. Affect: Mildly constricted but reactive. "
            "Speech: Normal rate and rhythm. Thought content: No psychosis. Insight: Good.\n\n"
            "INTERVENTIONS:\n"
            "Cognitive behavioral techniques: Identified automatic negative thought pattern "
            "(catastrophizing regarding employment). Challenged and reframed with evidence. "
            "Behavioral activation: Reviewed activity schedule; patient committed to daily "
            "15-minute walk.\n\n"
            "PLAN:\n"
            "Continue weekly CBT sessions. Safety plan reviewed. Emergency contact {phone} on file. "
            "Coordinate with prescribing psychiatrist. Next session {appointment_date}.\n\n"
            "Email: {email}  Address: {street_address}, {city}, {state} {zip_code}"
        ),
    },
    {
        "type": "Immunization Record",
        "text": (
            "IMMUNIZATION RECORD\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "SSN: {ssn}  Health Plan #: {health_plan_number}\n"
            "Address: {full_address}  Phone: {phone}\n\n"
            "Provider: {provider_name}, MD  License #: {license_number}\n"
            "Practice Portal: {url}\n\n"
            "IMMUNIZATION HISTORY:\n\n"
            "Vaccine                  Date Administered  Lot #       Site    Route\n"
            "Influenza (IIV4)         {appointment_date} FL2024-8821 L Delt  IM\n"
            "COVID-19 (mRNA booster)  {procedure_date}   CV4-992341  R Delt  IM\n"
            "Tdap                     2022-03-15         TD22-44102  L Delt  IM\n"
            "Pneumococcal (PPSV23)    2021-11-08         PN21-33291  R Delt  IM\n"
            "Hepatitis B (3rd dose)   2020-06-22         HB20-11099  L Delt  IM\n"
            "Shingrix dose 2          2023-09-10         SH23-76120  R Delt  IM\n\n"
            "ADVERSE REACTIONS: None on record.\n\n"
            "NEXT DUE:\n"
            "- Annual influenza vaccine: Due next October\n"
            "- Pneumococcal (PCV15/20): Due age 65\n\n"
            "VIS given: Yes. Patient consent documented: Yes.\n\n"
            "Administering nurse: {provider_first} {provider_last}, RN\n"
            "Device ID (scanner): {device_id}"
        ),
    },
    {
        "type": "Telemedicine Note",
        "text": (
            "TELEMEDICINE VISIT NOTE\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "Date: {appointment_date}  Platform: Secure Video\n"
            "Provider: {provider_name}, MD  License #: {license_number}  DEA #: {dea_number}\n"
            "Patient IP Address: {ip_address}\n"
            "Patient email: {email}  Phone: {phone}\n\n"
            "VISIT TYPE: Follow-up — Anxiety disorder.\n\n"
            "CONSENT: Patient verbally consented to telehealth visit and was informed of the "
            "limitations of remote evaluation.\n\n"
            "SUBJECTIVE:\n"
            "{patient_first} reports stable anxiety symptoms this week. GAD-7 score 9 (last visit: 13). "
            "Buspirone 10 mg BID started 4 weeks ago — reports tolerating well with modest benefit. "
            "Continues to practice mindfulness techniques. Denies panic attacks in past 2 weeks. "
            "Work stress remains elevated. Sleeping 7 hours nightly.\n\n"
            "OBJECTIVE:\n"
            "Video exam limited. Patient appears calm, well-groomed. Speech clear and goal-directed. "
            "No apparent psychomotor agitation. Denies SI/HI.\n\n"
            "ASSESSMENT/PLAN:\n"
            "1. Generalized anxiety disorder — improved. Continue buspirone, titrate to 15 mg BID.\n"
            "2. Refer to cognitive behavioral therapy if not already engaged.\n"
            "3. Lab work ordered: TSH and CMP to rule out medical contributors.\n\n"
            "Prescription sent electronically to pharmacy on file.\n"
            "Follow-up in 4 weeks via telemedicine.\n\n"
            "Health Plan #: {health_plan_number}  Account #: {account_number}\n"
            "Patient portal: {url}"
        ),
    },
    {
        "type": "Medical Equipment Order",
        "text": (
            "DURABLE MEDICAL EQUIPMENT ORDER\n\n"
            "Ordering Physician: {provider_name}, MD\n"
            "License #: {license_number}  NPI: 1234567890\n"
            "Address: {street_address}, {city}, {state} {zip_code}\n"
            "Phone: {phone}  Fax: {fax}\n"
            "Date: {appointment_date}\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "Address: {full_address}\n"
            "Phone: {phone}  Health Plan #: {health_plan_number}\n\n"
            "EQUIPMENT ORDERED:\n"
            "Item: Continuous Positive Airway Pressure (CPAP) device with humidifier\n"
            "HCPCS Code: E0601\n"
            "ICD-10 Diagnosis: G47.33 — Obstructive sleep apnea\n"
            "Pressure setting: Auto CPAP 5–15 cmH2O\n"
            "Device ID to be assigned upon dispensing: {device_id}\n\n"
            "CLINICAL JUSTIFICATION:\n"
            "Patient underwent attended polysomnography on {procedure_date}. AHI: 28 events/hour. "
            "Oxygen nadir: 82%. Meets Medicare criteria for OSA. Prior non-invasive therapy "
            "with positional modifications was unsuccessful. CPAP titration study shows optimal "
            "pressure of 9 cmH2O.\n\n"
            "LENGTH OF NEED: 13 months (ongoing).\n\n"
            "Prescribing Physician Signature: {provider_name}, MD\n"
            "DEA #: {dea_number}"
        ),
    },
    {
        "type": "Transfer Summary",
        "text": (
            "TRANSFER SUMMARY\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "SSN: {ssn}  Account #: {account_number}\n"
            "Transferring Facility: St. Mary's Hospital\n"
            "Receiving Facility: Regional Rehabilitation Center\n"
            "Transfer Date: {discharge_date}  Admission Date: {admission_date}\n"
            "Attending: {provider_name}, MD  License #: {license_number}\n\n"
            "REASON FOR TRANSFER: Skilled nursing facility care following ischemic stroke.\n\n"
            "HOSPITAL COURSE SUMMARY:\n"
            "{patient_first} {patient_last} is a 79-year-old right-handed male admitted on "
            "{admission_date} with acute onset right-sided weakness and expressive aphasia. "
            "MRI brain confirmed left MCA territory ischemic stroke. IV tPA administered "
            "within 90 minutes of symptom onset. Post-tPA course notable for good neurologic "
            "improvement; right arm weakness improved from 0/5 to 3/5, speech improved from "
            "near-absent to halting but intelligible.\n\n"
            "ACTIVE DIAGNOSES:\n"
            "1. Ischemic stroke, left MCA territory\n"
            "2. Hypertension\n"
            "3. Atrial fibrillation (newly diagnosed on telemetry)\n\n"
            "DISCHARGE MEDICATIONS:\n"
            "Apixaban 5 mg PO BID, atorvastatin 80 mg nightly, lisinopril 10 mg daily, "
            "aspirin 81 mg daily (hold pending anticoagulation decisions).\n\n"
            "FUNCTIONAL STATUS AT TRANSFER:\n"
            "Ambulates 10 feet with walker and min assist. ADLs requiring mod assist. "
            "Dysphagia — pureed diet / nectar-thick liquids per SLP.\n\n"
            "Contact: {phone}  Address: {full_address}\n"
            "Health Plan #: {health_plan_number}"
        ),
    },
    {
        "type": "Death Summary",
        "text": (
            "DEATH SUMMARY\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "SSN: {ssn}  Account #: {account_number}\n"
            "Admission Date: {admission_date}  Date of Death: {discharge_date}\n"
            "Attending Physician: {provider_name}, MD  License #: {license_number}\n\n"
            "CAUSE OF DEATH:\n"
            "Immediate: Septic shock\n"
            "Underlying: Metastatic pancreatic adenocarcinoma\n"
            "Contributing: Acute respiratory failure, disseminated intravascular coagulation\n\n"
            "CLINICAL SUMMARY:\n"
            "{patient_first} {patient_last} was a 68-year-old female with stage IV pancreatic "
            "adenocarcinoma on palliative gemcitabine/nab-paclitaxel, admitted on {admission_date} "
            "with febrile neutropenia and bacteremia (E. coli, ESBL-producing). Despite broad-spectrum "
            "antibiotics (meropenem, micafungin), she developed progressive septic shock with "
            "multiorgan failure. Given her advanced malignancy and patient-stated wishes, goals "
            "of care were revised to comfort-focused on hospital day 3 in consultation with "
            "palliative care and family. She expired peacefully at 03:14 on {discharge_date} "
            "with family present.\n\n"
            "AUTOPSY: Declined by family.\n\n"
            "Death certificate completed by: {provider_name}, MD\n"
            "Next of kin notified: Yes\n"
            "Address: {full_address}  Phone: {phone}\n"
            "Health Plan #: {health_plan_number}"
        ),
    },
    {
        "type": "Insurance Pre-Authorization",
        "text": (
            "INSURANCE PRE-AUTHORIZATION REQUEST\n\n"
            "Date: {appointment_date}\n"
            "Requesting Provider: {provider_name}, MD\n"
            "License #: {license_number}  DEA #: {dea_number}\n"
            "Address: {street_address}, {city}, {state} {zip_code}\n"
            "Phone: {phone}  Fax: {fax}\n\n"
            "Patient: {patient_name}  DOB: {dob}  MRN: {mrn}\n"
            "SSN: {ssn}  Health Plan #: {health_plan_number}\n"
            "Account #: {account_number}\n"
            "Email: {email}  Phone: {phone}\n\n"
            "REQUESTED SERVICE:\n"
            "Procedure: Total right knee arthroplasty\n"
            "CPT Code: 27447\n"
            "ICD-10 Diagnosis: M17.11 — Primary osteoarthritis, right knee\n"
            "Proposed Procedure Date: {procedure_date}\n"
            "Facility: Northside Orthopedic Surgery Center\n\n"
            "CLINICAL JUSTIFICATION:\n"
            "{patient_first} {patient_last} is a 71-year-old male with a 5-year history of "
            "progressive right knee osteoarthritis. He has failed conservative management "
            "including physical therapy (12 sessions), corticosteroid injections x3, and "
            "NSAID therapy. Recent X-rays show Kellgren-Lawrence grade 4 changes with bone-on-bone "
            "articulation. Patient experiences pain 8/10 limiting ambulation to less than one block. "
            "Functional limitation significantly impacts quality of life and activities of daily living.\n\n"
            "SUPPORTING DOCUMENTATION ATTACHED:\n"
            "- Office notes x3 documenting conservative treatment failure\n"
            "- Radiograph report ({procedure_date})\n"
            "- Physical therapy discharge summary\n\n"
            "Provider portal submission: {url}\n"
            "Provider IP for submission: {ip_address}\n\n"
            "Signature: {provider_name}, MD"
        ),
    },
]
