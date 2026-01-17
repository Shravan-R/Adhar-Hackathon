from src.data_loader import load_all_datasets

enrolment_df, biometric_df, demographic_df = load_all_datasets()

print("\n================ ENROLMENT DATA =================")
for col in enrolment_df.columns:
    print(col)

print("\n================ BIOMETRIC DATA =================")
for col in biometric_df.columns:
    print(col)

print("\n================ DEMOGRAPHIC DATA =================")
for col in demographic_df.columns:
    print(col)
