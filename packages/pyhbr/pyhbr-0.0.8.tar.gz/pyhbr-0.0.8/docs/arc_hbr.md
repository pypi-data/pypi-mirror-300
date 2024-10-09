# ARC HBR Calculation

The ARC HBR score is a concensus-based risk score to identify patients at high bleeding risk. It is formed from a weighted sum of 13 criteria, involving patient characteristics, patient history, laboratory test results, prescriptions information, and planned healthcare activity. This page describes how the ARC HBR score is calculated and assessed in PyHBR.

## Steps to Calculate the ARC HBR Score

Using source data that includes diagnosis/procedure codes, laboratory tests, and prescriptions information, the ARC HBR score can be calculated as follows:

### Preprocessing Steps

Before identifying patients/index events, or calculating the score, some preprocessing is required. This is the section that is likely to require modification if a new data source is used.

1. For diagnosis and procedure codes, add the group they belong to, and drop codes not in any group. Retain the code, the group, and the code position in long format in a table. The following groups are required:
    * `acs`: Diagnosis codes corresponding to acute coronary syndromes (includes myocardial infarction/unstable angina). Used to identify index events.
    * `pci`: Percutaneous coronary intervention codes (e.g. stent implantation). Used to identify index events.
    * `ckd`: Chronic kidney disease: includes N18.5, N18.4, N18.3, N18.2, N18.1. Used as a fall-back in case eGFR is missing.
    * `anaemia`: Used as a fall-back in case Hb measurement is missing.
    * `bleeding`: Used to identify prior bleeding.
    * `cbd`: Chronic bleeding diatheses.
    * `cph`: Cirrhosis with portal hypertension.
    * `cancer_diag`: Used to identify cancer diagnoses.
    * `cancer_proc`: Used to identify cancer therapy.
    * `bavm`: Brain arteriovenous malformation diagnoses.
    * `istroke`: Ischaemic stroke.
    * `ich`: Intracranial haemorrhage.
    * `csurgery`: Cardiac surgery. Used to exclude cardiac surgery for one criterion.
    * `surgery`: All surgery. Used as a proxy for "major surgery" criteria
2. For laboratory results, narrow to the subset of results shown below. Convert all tests to the standard unit used in the ARC definition, and drop the unit from the table. Keep the date/time at which the laboratory sample was collected, and the patient ID (in this data, associated episode is not linked, and must be inferred from the date).
    * `egfr`: Used to assess kidney function (unit: mL/min)
    * `hb`: Haemoglobin, used to assess anaemia (unit: g/dL)
    * `platelets`: Platelet count, used to assess thrombocytopenia (unit: `x10^9/L`)

3. For prescriptions, narrow to the set of medicines shown below. Keep the medicine name, flag for present-on-admission, patient ID, and prescription order date (used to infer link to episode, as above).
    * `oac`: any of warfarin, apixaban, edoxaban, dabigatran, rivaroxaban
    * `nsaid`: any of ibuprofen, naproxen, diclofenac, celecoxib, mefenamic acid, etoricoxib, indomethacin (high-does aspirin excluded for now).

4. For demographics, retain age and gender. This calculation may be postoned until after index events are calculated (for example, if the demographics table contains year of birth instead of age).

NOTE: The `episodes`, `prescriptions`, and `lab_results` tables have `episode_id` as Pandas index. The `demographics` table uses `patient_id` as index. The `episodes` table contains `patient_id` as a column for linking to `demographics`.

#### Link Laboratory Results and Prescriptions to Episodes

In the HIC data, laboratory results and prescriptions do not contain an episode_id; instead, they contain a date/time (either a sample date for laboratory tests or an order date for prescriptions).

To link each test/prescription to an episode, use the episode start and end times. If the sample date/order date falls within the episode start and end time, then it should be associated with that episode.

A complication with this process is that episodes sometimes overlap (i.e. the start time of the next is before the end time of the previous one). This will be solved by associating a test/prescription with the earliest episode containing the time.

### Identify Index Events

Inclusion criteria for calculation of the ARC HBR score is having a hospital visit (spell) where the first episode of the spell contains an ACS diagnosis in the primary position, or a PCI procedure in any position.

The table is indexed by the episode ID, and contains flag columns `acs_index` for `pci_index` for which inclusion condition is satisfied.

NOTE: The `index_event` table is indexed by `episode_id`, and also contains the `patient_id` as a column.

### Calculating the Score

The score is calculated differently for each different class of critera: