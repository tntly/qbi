# %%
import io
import os
import pandas as pd

# %%
# this will convert vcf to dataframe
def read_vcf(path):
    with open(path, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]
    return pd.read_csv(
        io.StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
               'QUAL': str, 'FILTER': str, 'INFO': str},
        sep='\t'
    ).rename(columns={'#CHROM': 'CHROM'})

# %%
'''
Example search:
1. Find BRCA1 gene on UCSC Genome Browser and get chr17:43044295-43125364 from website
2. Put in parameters of chromosome and start and end location into Defining the range code below
3. On Clinvar website navigate to "FTP" on Home bar
4. Click on "vcf_GRCh38/"
5. Click on "clinvar.vcf.gz" and it will download VCF
6. Unzip the file and use that path below
'''

# ENTER your path to the vcf file
alz_vcf_raw = read_vcf("C:\\Users\\lawfu\\Documents\\Github Hackathon 2025\\clinvar.vcf")

# %%
# show first 5 of dataframe
# print(alz_vcf.head())

# %%
# this will help create a series from ; separators of vcf file
def get_condition(x):
    return x.split(";")[2]

# Define the range you want to find on the gene (chr17:43044295-43125364)
chrom = '19'
start_pos = 44905796
end_pos = 44909393

# Filter the DataFrame to find the region within the range for chr##
alz_vcf = alz_vcf_raw[(alz_vcf_raw['CHROM'] == chrom) & 
                 (alz_vcf_raw['POS'] >= start_pos) & 
                 (alz_vcf_raw['POS'] <= end_pos)]


# %%
# get only INFO column from dataframe
alz_vcf.INFO.map(get_condition)

# %%
counts_conditions = alz_vcf.INFO.map(lambda x: x.split(";")[2]).value_counts()
# count all items in column in INFO
# print(counts_conditions)

# %%
# count all items in column in INFO with just "CLNDN"
counts_conditions = alz_vcf.INFO.map(lambda x: x.split(";")[2] if x.split(";")[2].startswith('CLNDN') else None).value_counts()

# print(counts_conditions)

# %%
# filter out "CLNDN=not_provided","CLNDN=not_specified"
just_conditions = counts_conditions[~counts_conditions.index.isin(["CLNDN=not_provided","CLNDN=not_specified"])]  
# must put .index or it will only filter by the associated value and not the name

# print(just1_conditions)

# %%
# list(map(print, just_conditions.head(5).index))
# for condition in just_conditions.head(5).index:
    # print(condition[6:])

# %%
# just get the top 5 conditions
# top_cond = []
# for condition in just_conditions.head(5).index:
#     top_cond.append(str(condition[6:]))

# print(top_cond)


# dictionary of just conditions and occurances for top 5 for your specific gene
# print(just_conditions.head(5))

top_cond_dict = {str(condition[6:]): just_conditions[condition].item() for condition in just_conditions.head(5).index}

#get total number of variations in chromosome range
total_var = len(alz_vcf)

# Print the dictionary
print(f'Top 5 conditions are: {top_cond_dict}\nOut of the number of varations in this chromosome range: {total_var}')