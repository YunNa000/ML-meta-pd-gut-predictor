import pandas as pd
from glob import glob

print("🔍 Step 1: 매핑 테이블 통합 시작")
map_files = glob("mapping_tables/filereport_read_run_*.txt")

maps = []
for f in map_files:
    print(f"  → 파일 로딩 중: {f}")
    df = pd.read_csv(f, sep="\t", low_memory=False)

    run_col = [col for col in df.columns if 'run_accession' in col][0]
    sample_col = [col for col in df.columns if 'sample_accession' in col][0]

    df_sub = df[[run_col, sample_col]].copy()
    df_sub.columns = ["run_id", "sample_id"]
    maps.append(df_sub)

map_df = pd.concat(maps).drop_duplicates().reset_index(drop=True)
run_to_sample = map_df.set_index("run_id")["sample_id"].to_dict()
print(f"✔ Step 1 완료: 매핑 수 {len(map_df)}")

# ───────────────────────────────────────────────

print("🔍 Step 2: feature table 로드")
try:
    feature_df = pd.read_csv("meta-genus-feature-table.tsv", sep="\t", index_col=0, encoding="utf-8")
    print("  → utf-8로 로드 성공")
except UnicodeDecodeError:
    feature_df = pd.read_csv("meta-genus-feature-table.tsv", sep="\t", index_col=0, encoding="ISO-8859-1")
    print("  → ISO-8859-1로 로드 성공")

print("  → 컬럼 수:", feature_df.shape[1])

print("🔍 Step 2-1: run_id 추출 및 sample_id 매핑")
feature_df.columns = feature_df.columns.str.extract(r'([SED]RR\d+)', expand=False)
feature_df.columns = feature_df.columns.map(run_to_sample)
feature_df = feature_df.loc[:, feature_df.columns.notna()]
print(f"✔ Step 2 완료: 매핑된 샘플 수 {feature_df.shape[1]}")

# ───────────────────────────────────────────────

print("🔍 Step 3: feature table transpose 및 중복 처리")
feature_t = feature_df.T
feature_t.index.name = 'sample_id'  # 인덱스 명시
feature_t = feature_t.groupby('sample_id').mean().reset_index()

print("  → feature_t shape:", feature_t.shape)
print("  → sample_id 예시:", feature_t['sample_id'].head().tolist())

# ───────────────────────────────────────────────

print("🔍 Step 4: 메타데이터 로드")
meta_df = pd.read_csv("each_column_pp3.csv")
print("  → meta_df shape:", meta_df.shape)
print("  → sample_id 예시:", meta_df['sample_id'].head().tolist())

# ───────────────────────────────────────────────

print("🔍 Step 4-1: 병합 수행")
merged_df = meta_df.merge(feature_t, on="sample_id", how="inner")
print("✔ 병합 완료 → merged_df shape:", merged_df.shape)

# ───────────────────────────────────────────────

print("🔍 Step 5: 저장")
merged_df.to_csv("merged_metadata_feature2.csv", index=False)
print("✅ 저장 완료: merged_metadata_feature2.csv")

# ───────────────────────────────────────────────

print("✔ 메타데이터 sample 수:", len(meta_df))
print("✔ feature table sample 수:", len(feature_t))
print("✔ 병합 후 sample 수:", len(merged_df))
