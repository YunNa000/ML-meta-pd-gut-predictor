import pandas as pd
from functools import reduce

# 파일 목록
files = [
    "PRJ27564-feature-table.tsv",
    "PRJEB14928-feature-table.tsv",
    "PRJNA381395-feature-table.tsv",
    "PRJNA391524-feature-table.tsv",
    "PRJNA494620-feature-table.tsv"
]

# 첫 줄에 '#' 제거 및 ASV ID 열을 인덱스로 사용
def load_feature_table(filepath):
    df = pd.read_csv(filepath, sep='\t', comment='#', index_col=0)
    return df

# 각 파일을 DataFrame으로 읽기
dfs = [load_feature_table(f) for f in files]

# ASV 기준으로 전체 병합 (union)
merged_df = reduce(lambda left, right: pd.merge(left, right, how='outer', left_index=True, right_index=True), dfs)

# 결측값은 0으로 채움 (존재하지 않은 ASV는 0 count 처리)
merged_df.fillna(0, inplace=True)

# 정수형으로 변환
merged_df = merged_df.astype(int)

# 결과 저장
merged_df.to_csv("merged-feature-table.tsv", sep='\t')

print("✅ 병합 완료: merged-feature-table.tsv 생성됨.")
