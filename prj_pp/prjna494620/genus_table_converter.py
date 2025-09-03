from qiime2 import Artifact
import pandas as pd

# 1. 파일 경로
table_fp = 'PRJNA494620-table.qza'
taxonomy_fp = 'taxonomy.qza'

# 2. table 불러오기
table = Artifact.load(table_fp).view(pd.DataFrame)

# 3. table의 index가 SRR 같은 샘플 ID면 전치(transpose) 수행 → ASV가 index가 되도록
if table.index[0].startswith('SRR') or table.index[0].startswith('ERR'):
    print("ASV와 샘플 위치가 반대인 것 같아 전치합니다.")
    table = table.transpose()

# 4. taxonomy 불러오기 (DataFrame → Taxon Series로)
taxonomy_df = Artifact.load(taxonomy_fp).view(pd.DataFrame)
taxonomy_series = taxonomy_df['Taxon']
taxonomy_series.index = taxonomy_df.index

# 5. 공통 feature 추출
common_features = table.index.intersection(taxonomy_series.index)
print(f"매칭되는 feature 수: {len(common_features)} / 전체 {len(table)}")
print("예시 ASV ID:", table.index[:5].tolist())

# 6. 필터링
table = table.loc[common_features]
taxonomy_series = taxonomy_series.loc[common_features]

# 7. Genus 추출 함수
def extract_genus(tax_str):
    if pd.isna(tax_str):
        return 'Unassigned'
    levels = tax_str.split(';')
    for level in levels:
        if level.strip().startswith('g__'):
            genus = level.strip().replace('g__', '')
            return genus if genus else 'Unassigned'
    return 'Unassigned'

# 8. Genus 매핑
genus_map = taxonomy_series.apply(extract_genus)
table['Genus'] = genus_map

# 9. Genus 분포 확인
print("Top Genus counts:")
print(table['Genus'].value_counts().head(10))

# 10. 집계
genus_table = table.groupby('Genus').sum()

# 11. 저장
genus_table.to_csv('genus-feature-table.tsv', sep='\t', index=True, index_label='Genus')
print("genus-feature-table.tsv 저장 완료")
