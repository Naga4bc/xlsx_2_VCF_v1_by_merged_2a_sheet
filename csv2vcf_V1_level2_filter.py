
'''
#This is renamed and level2 filter added 

import pandas as pd
import csv

# Step 1: Read data
sample_df = pd.read_csv('23may_leve2csv.csv')

# Step 2: Map column names
column_mapping = {
    '#CHROM': '#CHROM',
    'POS': 'POS',
    'REF': 'REF',
    'ID': 'ID',
    'ALT': 'ALT',
    'QUAL': 'QUAL',
    'filters': 'FILTER'
}

sample_df = sample_df.rename(columns=column_mapping)

# Create the INFO column with renamed sub-fields
info_columns = {
    'BAM_Total_Depth': 'Bam_Total_Count',
    'BAM_REF_Depth': 'Bam_Ref_Depth',
    'BAM_ALT_Depth': 'Bam_Alt_Depth',
    'PCT_BAM_ALT_Depth': 'BAM_Alt_Dept_Percen',
    'SYMBOL': 'Gene',
    'HGVSp_VEP': 'P_Dot',
    'CLIN_SIG': 'Clinvar_Clinsig'
}

def format_info(row):
    info_pairs = [f"Filter=Level_2a"]  # here we want specify the level2 or level2a 
    for old_col, new_col in info_columns.items():
        if pd.notna(row[old_col]):
            info_pairs.append(f"{new_col}={row[old_col]}")
    return ';'.join(info_pairs)

sample_df['INFO'] = sample_df.apply(format_info, axis=1)

# Add columns 
sample_df['QUAL'] = '.'
sample_df['FORMAT'] = '.'
sample_df['FILTER'] = 'Pass'
sample_df['ID'] = '.'

required_columns = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']
sample_df = sample_df[required_columns]

# Step 3: Sort the DataFrame based on chromosome and position
def custom_sort(chr_str):
    if chr_str.startswith('chr'):
        try:
            chr_num = int(chr_str[3:])
            if chr_num <= 22:
                return chr_num
            elif chr_num == 23:
                return 'X'
            elif chr_num == 24:
                return 'Y'
        except ValueError:
            pass
    return chr_str

sample_df['chr_num'] = sample_df['#CHROM'].apply(custom_sort)
sample_df = sample_df.sort_values(by=['chr_num', 'POS']).drop(columns=['chr_num'])

# Additional lines for both CSV and VCF files
additional_lines = ['##fileformat=VCFv4.2']

# Step 4: Write to VCF
output_vcf_file = '23may_leve2csv_level2.vcf'
with open(output_vcf_file, 'w') as f:
    for line in additional_lines:
        f.write(line + '\n')
    f.write('\t'.join(required_columns) + '\n')
    for _, row in sample_df.iterrows():
        f.write('\t'.join(str(row[col]) for col in required_columns) + '\n')

print(f"Final VCF file '{output_vcf_file}' created successfully.")
'''

##############################################################################################################
'''
## sheet eduthukuthu pandas pothum enna ella filesum handles pannum 
import pandas as pd

# Step 1: Read  Excel
file_path = 'X43AH-F1-D-L2-FEV2F2both-S1_vepAnn_Mod_v1.xlsx'
sheet_names = ['Level_2', 'Level_2a']

# Read both sheets into DataFrames
df_level_2 = pd.read_excel(file_path, sheet_name=sheet_names[0])
df_level_2['Filter_Sheet'] = 'Level_2'  # Add a column to identify sheet

df_level_2a = pd.read_excel(file_path, sheet_name=sheet_names[1])
df_level_2a['Filter_Sheet'] = 'Level_2a'  

# Combine the two DataFrames
combined_df = pd.concat([df_level_2, df_level_2a])

# Step 2: Map column names
column_mapping = {
    '#CHROM': '#CHROM',
    'POS': 'POS',
    'REF': 'REF',
    'ID': 'ID',
    'ALT': 'ALT',
    'QUAL': 'QUAL',
    'filters': 'FILTER'
}

combined_df = combined_df.rename(columns=column_mapping)

# Create the INFO column with renamed sub-fields
info_columns = {
    'BAM_Total_Depth': 'Bam_Total_Count',
    'BAM_REF_Depth': 'Bam_Ref_Depth',
    'BAM_ALT_Depth': 'Bam_Alt_Depth',
    'PCT_BAM_ALT_Depth': 'BAM_Alt_Dept_Percen',
    'SYMBOL': 'Gene',
    'HGVSp_VEP': 'P_Dot',
    'CLIN_SIG': 'Cling_Sig',
    'clinvar_clnsig':'Clinvar_Clinsig'
}

def format_info(row):
    filter_value = f"Filter={row['Filter_Sheet']}"
    info_pairs = [filter_value]  # Add the constant INFO field based on the sheet
    for old_col, new_col in info_columns.items():
        if pd.notna(row[old_col]):
            info_pairs.append(f"{new_col}={row[old_col]}")
    return ';'.join(info_pairs)

combined_df['INFO'] = combined_df.apply(format_info, axis=1)

# Add columns 
combined_df['QUAL'] = '.'
combined_df['FORMAT'] = '.'
combined_df['FILTER'] = 'Pass'
combined_df['ID'] = '.'

required_columns = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']
combined_df = combined_df[required_columns]

# Step 3: Sort the DataFrame based on chromosome and position
def custom_sort(chr_str):
    if chr_str.startswith('chr'):
        try:
            chr_num = int(chr_str[3:])
            if chr_num <= 22:
                return chr_num
            elif chr_num == 23:
                return 'X'
            elif chr_num == 24:
                return 'Y'
        except ValueError:
            pass
    return chr_str

combined_df['chr_num'] = combined_df['#CHROM'].apply(custom_sort)
combined_df = combined_df.sort_values(by=['chr_num', 'POS']).drop(columns=['chr_num'])

# Additional lines for both CSV and VCF files
additional_lines = ['##fileformat=VCFv4.2']

# Step 4: Write to VCF
output_vcf_file = 'X43AH-F1-D-L2-FEV2F2both.vcf'
with open(output_vcf_file, 'w') as f:
    for line in additional_lines:
        f.write(line + '\n')
    f.write('\t'.join(required_columns) + '\n')
    for _, row in combined_df.iterrows():
        f.write('\t'.join(str(row[col]) for col in required_columns) + '\n')

print(f"Final VCF file '{output_vcf_file}' created successfully.")
'''
"""
import pandas as pd

# Step 1: Read  Excel
file_path = 'XEWCJ-B-D-SE8-S1_vepAnn_Mod_v1.xlsx'
sheet_names = ['Merged_2_n_2a']

# Read both sheets into DataFrames
df_level_2 = pd.read_excel(file_path, sheet_name=sheet_names[0])
df_level_2['Filter_Sheet'] = 'Merged_2_n_2a'  # Add a column to identify sheet

# Combine the two DataFrames
combined_df = pd.concat([df_level_2,])

# Step 2: Map column names
column_mapping = {
    '#CHROM': '#CHROM',
    'POS': 'POS',
    'REF': 'REF',
    'ID': 'ID',
    'ALT': 'ALT',
    'QUAL': 'QUAL',
    'filters': 'FILTER'
}

combined_df = combined_df.rename(columns=column_mapping)

# Create the INFO column with renamed sub-fields
info_columns = {
    'BAM_Total_Depth': 'Bam_Total_Count',
    'BAM_REF_Depth': 'Bam_Ref_Depth',
    'BAM_ALT_Depth': 'Bam_Alt_Depth',
    'PCT_BAM_ALT_Depth': 'BAM_Alt_Dept_Percen',
    'SYMBOL': 'Gene',
    'HGVSp_VEP': 'P_Dot',
    'CLIN_SIG': 'Cling_Sig',
    'clinvar_clnsig':'Clinvar_Clinsig',
    'Level':'Filter',
    'gnomAD_exomes_SAS_AF':'gAD_E_SAS',
    'gnomAD_exomes_EAS_AF':'gAD_E_EAS',
    'gnomAD_genomes_EAS_AF':'gAD_G_SAS',
    'gnomAD_genomes_SAS_AF':'gAD_G_EAS'
}

def format_info(row):
    info_pairs = []  # Initialize an empty list for info pairs
    for old_col, new_col in info_columns.items():
        if pd.notna(row[old_col]):
            info_pairs.append(f"{new_col}={row[old_col]}")
    return ';'.join(info_pairs)

combined_df['INFO'] = combined_df.apply(format_info, axis=1)

# Add columns 
combined_df['QUAL'] = '.'
combined_df['FORMAT'] = '.'
combined_df['FILTER'] = 'Pass'
combined_df['ID'] = '.'

required_columns = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']
combined_df = combined_df[required_columns]

# Step 3: Sort the DataFrame based on chromosome and position
def custom_sort(chr_str):
    if chr_str.startswith('chr'):
        try:
            chr_num = int(chr_str[3:])
            if chr_num <= 22:
                return chr_num
            elif chr_num == 23:
                return 'X'
            elif chr_num == 24:
                return 'Y'
        except ValueError:
            pass
    return chr_str

combined_df['chr_num'] = combined_df['#CHROM'].apply(custom_sort)
combined_df = combined_df.sort_values(by=['chr_num', 'POS']).drop(columns=['chr_num'])

# Additional lines for both CSV and VCF files
additional_lines = ['##fileformat=VCFv4.2']

# Step 4: Write to VCF
output_vcf_file = 'XEWCJ-B-D-SE8-S1_vepAnn_Mod_v1.vcf'
with open(output_vcf_file, 'w') as f:
    for line in additional_lines:
        f.write(line + '\n')
    f.write('\t'.join(required_columns) + '\n')
    for _, row in combined_df.iterrows():
        f.write('\t'.join(str(row[col]) for col in required_columns) + '\n')

print(f"Final VCF file '{output_vcf_file}' created successfully.")
"""
################################################ input file directory

import os
import pandas as pd

directory_path = '/home/naga/filter_merged_2na'

# Column mapping
column_mapping = {
    '#CHROM': '#CHROM',
    'POS': 'POS',
    'REF': 'REF',
    'ID': 'ID',
    'ALT': 'ALT',
    'QUAL': 'QUAL',
    'filters': 'FILTER'
}

info_columns = {
    'BAM_Total_Depth': 'Bam_Total_Count',
    'BAM_REF_Depth': 'Bam_Ref_Depth',
    'BAM_ALT_Depth': 'Bam_Alt_Depth',
    'PCT_BAM_ALT_Depth': 'BAM_Alt_Dept_Percen',
    'SYMBOL': 'Gene',
    'HGVSp_VEP': 'P_Dot',
    'CLIN_SIG': 'Cling_Sig',
    'clinvar_clnsig':'Clinvar_Clinsig',
    'Level':'Filter',
    'gnomAD_exomes_SAS_AF':'gAD_E_SAS',
    'gnomAD_exomes_EAS_AF':'gAD_E_EAS',
    'gnomAD_genomes_EAS_AF':'gAD_G_SAS',
    'gnomAD_genomes_SAS_AF':'gAD_G_EAS'
}

def format_info(row):
    info_pairs = []
    for old_col, new_col in info_columns.items():
        if pd.notna(row[old_col]):
            info_pairs.append(f"{new_col}={row[old_col]}")
    return ';'.join(info_pairs)

def custom_sort(chr_str):
    if chr_str.startswith('chr'):
        try:
            chr_num = int(chr_str[3:])
            if chr_num <= 22:
                return chr_num
            elif chr_num == 23:
                return 'X'
            elif chr_num == 24:
                return 'Y'
        except ValueError:
            pass
    return chr_str

# Process  .xlsx 
for file_name in os.listdir(directory_path):
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(directory_path, file_name)
        output_vcf_file = os.path.join(directory_path, file_name.replace('.xlsx', '.vcf'))
        
        # Read the sheet
        sheet_names = ['Merged_2_n_2a']
        df_level_2 = pd.read_excel(file_path, sheet_name=sheet_names[0])
        df_level_2['Filter_Sheet'] = 'Merged_2_n_2a'
        
        combined_df = pd.concat([df_level_2,])
        
        combined_df = combined_df.rename(columns=column_mapping)
        
        # Create the INFO column
        combined_df['INFO'] = combined_df.apply(format_info, axis=1)
        
        # Add required columns
        combined_df['QUAL'] = '.'
        combined_df['FORMAT'] = '.'
        combined_df['FILTER'] = 'Pass'
        combined_df['ID'] = '.'
        
        # Select and sort required columns
        required_columns = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']
        combined_df = combined_df[required_columns]
        
        combined_df['chr_num'] = combined_df['#CHROM'].apply(custom_sort)
        combined_df = combined_df.sort_values(by=['chr_num', 'POS']).drop(columns=['chr_num'])
        
        # Additional lines for VCF file
        additional_lines = ['##fileformat=VCFv4.2']
        
        # Write to VCF file
        with open(output_vcf_file, 'w') as f:
            for line in additional_lines:
                f.write(line + '\n')
            f.write('\t'.join(required_columns) + '\n')
            for _, row in combined_df.iterrows():
                f.write('\t'.join(str(row[col]) for col in required_columns) + '\n')
        
        print(f"Final VCF file '{output_vcf_file}' created successfully.")
