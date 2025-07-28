from qiime2 import Artifact
import pandas as pd

# 파일명 지정 (해당 PRJ 디렉토리에서 실행)
table_fp = 'PRJXXXXXX-table.qza'
taxonomy_fp = 'taxonomy.qza'

# 불러오기
table = Artifact.load(table_fp).view(pd.DataFrame)  # index: feature (ASV), columns: samples
taxonomy = Artifact.load(taxonomy_fp).view(pd.Series)  # index: feature (ASV), values: taxonomy string

# taxonomy에서 genus만 추출
def extract_genus(tax_str):
    levels = tax_str.split(';')
    for level in levels:
        if level.strip().startswith('g__'):
            return level.strip().replace('g__', '') or 'Unassigned'
    return 'Unassigned'

genus_map = taxonomy.apply(extract_genus)

# ASV → genus 매핑 적용
table['Genus'] = genus_map

# Genus 기준으로 sum aggregation
genus_table = table.groupby('Genus').sum()

# 결과 저장
genus_table.to_csv('genus-feature-table.tsv', sep='\t')
