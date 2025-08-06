import pandas as pd

# 1. 데이터 불러오기
df = pd.read_csv("merged_16smeta.csv", encoding='ISO-8859-1')

# 2. 삭제 대상: 결측률 100% 컬럼만
missing_ratio = df.isna().mean()
drop_candidates = missing_ratio[missing_ratio == 1.0].index.tolist()

# 3. 컬럼 제거
df_cleaned = df.drop(columns=drop_candidates)

# 4. 결과 저장 (선택)
df_cleaned.to_csv("metadata_only_empty_dropped.csv", index=False)

# 5. 로그 출력
print(f"삭제된 빈 칼럼 수: {len(drop_candidates)}")
print("삭제된 컬럼 목록:", drop_candidates)
