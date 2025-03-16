
#------------------------------IMPORT LIBRARIES-------------------------------------------------

import pandas as pd
import numpy as np

#------------------------------READ FILES WITH PANDAS--------------------------------------------

ParameterTable = pd.read_csv("https://raw.githubusercontent.com/NikoletaPantelidou/Language-data-complexity/refs/heads/main/parameters.csv")
ValueTable = pd.read_csv("https://raw.githubusercontent.com/NikoletaPantelidou/Language-data-complexity/refs/heads/main/values.csv" , on_bad_lines='skip')

#-------------------------------BINARIZE PARAMETERS--------------------------------------------

def make_binary_ParameterTable(ParameterTable, keep_multi_state_features=True, keep_raw_binary=False):
    binarised_feats = [
        "GB024a", "GB024b", "GB025a", "GB025b", "GB065a", "GB065b",
        "GB130a", "GB130b", "GB193a", "GB193b", "GB203a", "GB203b"
    ]

    if keep_raw_binary and all(feat in ParameterTable['ID'].values for feat in binarised_feats):
        return ParameterTable.copy()

    parameter_binary = pd.DataFrame({
        "ID": ["GB024", "GB024", "GB025", "GB025", "GB065", "GB065",
               "GB130", "GB130", "GB193", "GB193", "GB203", "GB203"],
        "ID_binary": binarised_feats,
        "Grambank_ID_desc_binary": [
            "GB024a NUMOrder_Num-N", "GB024b NUMOrder_N-Num",
            "GB025a DEMOrder_Dem-N", "GB025b DEMOrder_N-Dem",
            "GB065a POSSOrder_PSR-PSD", "GB065b POSSOrder_PSD-PSR",
            "GB130a IntransOrder_SV", "GB130b IntransOrder_VS",
            "GB193a ANMOrder_ANM-N", "GB193b ANMOrder_N-ANM",
            "GB203a UQOrder_UQ-N", "GB203b UQOrder_N-UQ"
        ],
        "Name_binary": [
            "Is the order of the numeral and noun Num-N?",
            "Is the order of the numeral and noun N-Num?",
            "Is the order of the adnominal demonstrative and noun Dem-N?",
            "Is the order of the adnominal demonstrative and noun N-Dem?",
            "Is the pragmatically unmarked order of adnominal possessor noun and possessed noun PSR-PSD?",
            "Is the pragmatically unmarked order of adnominal possessor noun and possessed noun PSD-PSR?",
            "Is the pragmatically unmarked order of S and V in intransitive clauses S-V?",
            "Is the pragmatically unmarked order of S and V in intransitive clauses V-S?",
            "Is the order of the adnominal property word (ANM) and noun ANM-N?",
            "Is the order of the adnominal property word (ANM) and noun N-ANM?",
            "Is the order of the adnominal collective universal quantifier (UQ) and noun UQ-N?",
            "Is the order of the adnominal collective universal quantifier (UQ) and noun N-UQ?"
        ],
        "Word_Order_binary": [0, 1, 0, 1, 0, 1, None, None, 0, 1, 0, 1],
        "Binary_Multistate": ["Binarised"] * 12
    })

    multistate_features = {"GB024", "GB025", "GB065", "GB130", "GB193", "GB203"}

    ParameterTable_new = ParameterTable.merge(parameter_binary, on="ID", how="outer")

    ParameterTable_new["ID"] = ParameterTable_new["ID_binary"].combine_first(ParameterTable_new["ID"])
    ParameterTable_new["Name"] = ParameterTable_new["Name_binary"].combine_first(ParameterTable_new["Name"])
    ParameterTable_new["Grambank_ID_desc"] = ParameterTable_new["Grambank_ID_desc_binary"].combine_first(ParameterTable_new["Grambank_ID_desc"])
    ParameterTable_new["Word_Order"] = ParameterTable_new["Word_Order_binary"].combine_first(ParameterTable_new["Word_Order"])

    ParameterTable_new = ParameterTable_new.drop(columns=["ID_binary", "Name_binary", "Grambank_ID_desc_binary", "Word_Order_binary"])

    ParameterTable_new["Binary_Multistate"] = ParameterTable_new["ID"].apply(
        lambda x: "Multi" if x in multistate_features else "Binary"
    )

    if not keep_multi_state_features:
        ParameterTable_new = ParameterTable_new[~ParameterTable_new["ID"].isin(multistate_features)]

    return ParameterTable_new

##----------------------------BINARIZE VALUES -------------------------------------------------



def binarise_GBXXX_to_GBXXXa_without_zero(values):
    if "0" in values.values:
        raise ValueError("Feature contains zero-values which are not permitted.")
    return values.replace({"1": "1", "2": "0", "3": "1", "?": "?", np.nan: np.nan})

def binarise_GBXXX_to_GBXXXb_without_zero(values):
    if "0" in values.values:
        raise ValueError("Feature contains zero-values which are not permitted.")
    return values.replace({"1": "0", "2": "1", "3": "1", "?": "?", np.nan: np.nan})

def binarise_GBXXX_to_GBXXXa_with_zero(values):
    return values.replace({"0": "0", "1": "1", "2": "0", "3": "1", "?": "?", np.nan: np.nan})

def binarise_GBXXX_to_GBXXXb_with_zero(values):
    return values.replace({"0": "0", "1": "0", "2": "1", "3": "1", "?": "?", np.nan: np.nan})

def gb_recode(values, oldvariable, newvariable, func):
    subset = values[values["Parameter_ID"] == oldvariable].copy()
    subset["Parameter_ID"] = newvariable
    subset["ID"] = newvariable + "-" + subset["Language_ID"]
    subset["Value"] = func(subset["Value"])
    subset["Code_ID"] = subset["Parameter_ID"] + "-" + subset["Value"].astype(str)
    return pd.concat([values, subset], ignore_index=True)

def make_binary_ValueTable(values, keep_multistate=False, keep_raw_binary=True, trim_to_only_raw_binary=False):
    multistate_parameters = ["GB024", "GB025", "GB065", "GB130", "GB193", "GB203"]
    binary_parameters = ["GB024a", "GB024b", "GB025a", "GB025b", "GB065a", "GB065b", "GB130a", "GB130b", "GB193a", "GB193b", "GB203a", "GB203b"]

    if trim_to_only_raw_binary:
        values = values[~values["Parameter_ID"].isin(multistate_parameters)]
        if not any(values["Parameter_ID"].isin(binary_parameters)):
            raise ValueError("There is no raw binary coding at all.")
    else:
        if not keep_raw_binary:
            values = values[~values["Parameter_ID"].isin(binary_parameters)]
        else:
            values_raw_binary = values[values["Parameter_ID"].isin(binary_parameters)]

        values = gb_recode(values, 'GB024', 'GB024a', binarise_GBXXX_to_GBXXXa_without_zero)
        values = gb_recode(values, 'GB024', 'GB024b', binarise_GBXXX_to_GBXXXb_without_zero)
        values = gb_recode(values, 'GB025', 'GB025a', binarise_GBXXX_to_GBXXXa_without_zero)
        values = gb_recode(values, 'GB025', 'GB025b', binarise_GBXXX_to_GBXXXb_without_zero)
        values = gb_recode(values, 'GB065', 'GB065a', binarise_GBXXX_to_GBXXXa_without_zero)
        values = gb_recode(values, 'GB065', 'GB065b', binarise_GBXXX_to_GBXXXb_without_zero)
        values = gb_recode(values, 'GB130', 'GB130a', binarise_GBXXX_to_GBXXXa_without_zero)
        values = gb_recode(values, 'GB130', 'GB130b', binarise_GBXXX_to_GBXXXb_without_zero)
        values = gb_recode(values, 'GB193', 'GB193a', binarise_GBXXX_to_GBXXXa_with_zero)
        values = gb_recode(values, 'GB193', 'GB193b', binarise_GBXXX_to_GBXXXb_with_zero)
        values = gb_recode(values, 'GB203', 'GB203a', binarise_GBXXX_to_GBXXXa_with_zero)
        values = gb_recode(values, 'GB203', 'GB203b', binarise_GBXXX_to_GBXXXb_with_zero)

        if keep_raw_binary:
            values = values[~values.set_index(["Language_ID", "Parameter_ID"]).index.isin(values_raw_binary.set_index(["Language_ID", "Parameter_ID"]).index)]
            values = pd.concat([values, values_raw_binary], ignore_index=True)

        if not keep_multistate:
            values = values[~values["Parameter_ID"].isin(multistate_parameters)]

    return values

#-----------------------------------FUSION SCORE-------------------------------------------------


def calculate_fusion_scores(parameters_url, values_url):
    # Load the data from the provided URLs
    parameters = pd.read_csv(parameters_url)
    values = pd.read_csv(values_url,on_bad_lines='skip', sep=',')
    if "GB203b" not in values["Parameter_ID"].values:
        values = make_binary_ValueTable(values)

    if "GB203b" not in parameters["ID"].values:
         parameters = make_binary_ParameterTable(parameters)

    # Filter parameters to include only those with Fusion weight of 1
    fusion_params = parameters[parameters['Fusion'] == 1]

    # Merge values with fusion parameters to focus only on relevant features
    merged_data = values.merge(fusion_params, left_on='Parameter_ID', right_on='ID')
    merged_data['Value'] = pd.to_numeric(merged_data['Value'], errors='coerce')

    # Create a pivot table with languages as rows and parameters as columns
    pivot_table = merged_data.pivot_table(index='Language_ID', columns='Parameter_ID', values='Value', aggfunc='first')

    # Calculate the percentage of missing data for each language
    missing_data_percentage = pivot_table.isnull().mean(axis=1)

    # Increase threshold to allow more missing data if necessary
    filtered_languages = pivot_table[missing_data_percentage <= 0.5]  # Adjusted threshold to 50%

    # Calculate the percentage of missing data for each language
    missing_data_percentage = pivot_table.isnull().mean(axis=1)

    # Filter out languages with more than 60% missing data
    filtered_languages = pivot_table[missing_data_percentage <= 0.6]

    # Calculate the Fusion score as the mean of available (non-missing) values for each language
    fusion_scores = filtered_languages.mean(axis=1)

    return fusion_scores

# URLs of the CSV files
parameters_url = 'https://raw.githubusercontent.com/NikoletaPantelidou/Language-data-complexity/refs/heads/main/parameters.csv'
values_url ='https://raw.githubusercontent.com/NikoletaPantelidou/Language-data-complexity/refs/heads/main/values.csv'

# Calculate Fusion scores
fusion_scores = calculate_fusion_scores(parameters_url, values_url)

# Display the Fusion scores
print(fusion_scores)

#--------------------------------INFORMATIVITY SCORE---------------------------------------------


def calculate_informativity(values_url, parameters_url):

    # Load the data from the provided URLs
    parameters = pd.read_csv(parameters_url)
    values = pd.read_csv(values_url,on_bad_lines='skip', sep=',' )
    # Merge ValueTable with Informativity categories from ParameterTable

    parameters.columns = parameters.columns.str.strip()

    # Merge using correct column names
    values = values.merge(parameters[['ID', 'Informativity']],
                      left_on="Parameter_ID", right_on="ID",
                      how="left")

    # Drop redundant "ID" column after merging
    # The merge creates 'ID_x', 'ID_y' columns. Drop 'ID_y' which came from parameters DataFrame.
    # values = values.drop(columns=["ID"])  # Original line causing the error
    values = values.drop(columns=['ID_y']) # Drop the 'ID_y' column instead of 'ID'
    # Rename the "ID_x" column back to "ID" for consistency
    values = values.rename(columns={'ID_x': 'ID'})

    # Drop redundant "ID" column after merging
    values = values.drop(columns=["ID"])  # Ignore if not present


    # Drop missing Informativity values (features without a category are ignored)
    values = values.dropna(subset=['Informativity'])

    # Convert values to numeric, replacing "?" or invalid entries with NaN
    values['Value'] = pd.to_numeric(values['Value'], errors='coerce') # Changed 'value' to 'Value'

    # Filter out rows where value is NaN (missing data)
    values = values.drop(columns=["ID"], errors="ignore")

    # Step 1: Check if a language has at least one '1' in each Informativity group
    informativity_check = values.groupby(["Language_ID", "Informativity"])["Value"].max().reset_index()

    # Step 2: If max value in a group is 1, it counts as marked
    informativity_check["Marked"] = (informativity_check["Value"] == 1).astype(int)

    # Step 3: Count marked categories per language
    marked_counts = informativity_check.groupby("Language_ID")["Marked"].sum().reset_index(name="Marked_Categories")

    # Step 4: Count total relevant categories per language (groups with at least one feature)
    total_counts = informativity_check.groupby("Language_ID")["Informativity"].nunique().reset_index(name="Total_Categories")

    # Step 5: Compute informativity score = (Marked_Categories / Total_Categories)
    result_df = marked_counts.merge(total_counts, on="Language_ID")
    result_df["Informativity"] = result_df["Marked_Categories"] / result_df["Total_Categories"]

    return result_df

parameters_url = 'https://raw.githubusercontent.com/NikoletaPantelidou/Language-data-complexity/refs/heads/main/parameters.csv'
values_url = 'https://raw.githubusercontent.com/NikoletaPantelidou/Language-data-complexity/refs/heads/main/values.csv'
informativity_scores = calculate_informativity(values_url, parameters_url)

# Print full table
print(informativity_scores[0:])

#---------------------------------------------END------------------------------------------------