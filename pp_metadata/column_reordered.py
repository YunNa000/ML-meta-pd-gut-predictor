import pandas as pd

df = pd.read_csv("merged_columns.csv", encoding="ISO-8859-1")

# 1. 그룹별 컬럼 리스트 정의
id_cols = ["sample_id", "alias", "project_id", "center_name", "title", "description"]
exp_cols = [
    "scientific_name", "organism", "ENA-CHECKLIST", "collection_date", "ENA-FIRST-PUBLIC",
    "sequencing method", "ENA-LAST-UPDATE", "investigation type", "project name",
    "environment (material)", "collection_method"
]
clinical_cols = [col for col in df.columns if col not in id_cols + exp_cols]  # 나머지

# 2. 새로운 컬럼 순서
ordered_cols = id_cols + exp_cols + clinical_cols
ordered_cols = [col for col in ordered_cols if col in df.columns]  # 실제 존재하는 컬럼만

# 3. 컬럼 순서 재정렬
df = df[ordered_cols]

# 4. 저장
df.to_csv("metadata_column_reordered.csv", index=False)
print("✅ 컬럼 순서 정리 완료 → metadata_column_reordered.csv")
