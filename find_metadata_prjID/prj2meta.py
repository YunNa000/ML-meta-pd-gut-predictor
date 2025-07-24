import os
import pandas as pd
import json

# 메타데이터 폴더 경로
metadata_dir = "D:/dummy_meta-pd-gut-predictor/metadata"

# 결과 저장 파일
output_json = os.path.join(metadata_dir, "sample_accessions.json")

# 결과 저장용 dict
all_accessions = {}

# 폴더 내 모든 txt 파일 순회
for filename in os.listdir(metadata_dir):
    if filename.endswith(".txt") and filename.startswith("filereport_read_run_"):
        file_path = os.path.join(metadata_dir, filename)
        try:
            df = pd.read_csv(file_path, sep='\t', low_memory=False)
            if 'sample_accession' not in df.columns:
                print(f"'sample_accession' 컬럼 없음: {filename}")
                continue

            project_id = filename.split("_")[3]  
            samples = df['sample_accession'].dropna().unique().tolist()
            all_accessions[project_id] = samples
            print(f"{project_id}: {len(samples)}개 sample 수집")

        except Exception as e:
            print(f"파일 읽기 실패: {filename} - {e}")

# JSON 저장
with open(output_json, "w") as f:
    json.dump(all_accessions, f, indent=4)

print(f"\n완료: {output_json}에 저장됨")
