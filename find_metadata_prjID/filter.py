import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv("dummy_ena_detailed_sample_metadata.csv")  # <-- 파일명에 맞게 수정

# 시작 문자열 조건
prefixes = ["DC", "SC", "DP", "SP"]

# 조건에 맞는 행 필터링
filtered_df = df[df["alias"].str.startswith(tuple(prefixes), na=False)]

# 필요한 컬럼만 추출
result_df = filtered_df[["alias", "project_id", "sample_id"]]

# 결과 출력
print(result_df)

# CSV로 저장
result_df.to_csv("filtered_alias_project_sample.csv", index=False)
