import pandas as pd
import os

# 사용자 설정
tsv_path = "data/filereport_read_run_PRJNA834801_tsv.txt"  # ENA에서 받은 tsv 경로
output_dir = "data/wget_fastq"                                 # FASTQ 저장 폴더
urls_path = "data/urls_834801.txt"                               # wget용 URL 리스트
manifest_path = "data/manifest_834801.csv"                       # QIIME2 manifest 파일

# 디렉토리 생성
os.makedirs(output_dir, exist_ok=True)

# TSV 로딩
df = pd.read_csv(tsv_path, sep="\t", encoding="utf-8")
if 'fastq_ftp' not in df.columns or 'run_accession' not in df.columns:
    raise ValueError("TSV 파일에 'fastq_ftp' 또는 'run_accession' 컬럼이 없습니다.")

url_lines = []
manifest_lines = ["sample-id,absolute-filepath,direction"]

# FASTQ 링크 및 manifest 생성
for idx, row in df.iterrows():
    run_id = row['run_accession']
    ftp_links = str(row['fastq_ftp']).split(';') if ';' in str(row['fastq_ftp']) else [str(row['fastq_ftp'])]

    for i, ftp_link in enumerate(ftp_links):
        direction = 'forward' if i == 0 else 'reverse'
        filename = f"{run_id}_R{i+1}.fastq.gz"
        abs_path = os.path.abspath(os.path.join(output_dir, filename))
        
        url_lines.append(f"ftp://{ftp_link}")
        manifest_lines.append(f"{run_id},{abs_path},{direction}")

# 파일 저장
with open(urls_path, "w") as f:
    f.write("\n".join(url_lines))

with open(manifest_path, "w") as f:
    f.write("\n".join(manifest_lines))

print(f"✅ URL 리스트 저장: {urls_path}")
print(f"✅ QIIME2 manifest 저장: {manifest_path}")
