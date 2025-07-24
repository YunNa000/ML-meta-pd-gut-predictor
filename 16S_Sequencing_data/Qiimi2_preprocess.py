import pandas as pd
import os
import urllib.request

# 사용자 설정
tsv_path = "data/filereport_read_run_PRJEB27564_tsv.txt"   # ENA에서 받은 tsv 파일 경로
fastq_dir = "data/fastq"                       # FASTQ 저장 디렉토리
manifest_path = "data/manifest.csv"            # manifest 저장 경로 (csv)

os.makedirs(fastq_dir, exist_ok=True)

# TSV 파일 읽기
df = pd.read_csv(tsv_path, sep="\t", encoding="utf-8")
if 'fastq_ftp' not in df.columns or 'run_accession' not in df.columns:
    raise ValueError("필수 컬럼(fastq_ftp, run_accession)이 tsv에 없습니다.")

manifest_lines = ["sample-id,absolute-filepath,direction"]

for idx, row in df.iterrows():
    run_id = row['run_accession']
    fastq_urls = str(row['fastq_ftp']).split(';') if ';' in str(row['fastq_ftp']) else str(row['fastq_ftp']).split(',')

    for i, url in enumerate(fastq_urls):
        direction = 'forward' if i == 0 else 'reverse'
        filename = f"{run_id}_R{i+1}.fastq.gz"
        out_path = os.path.join(fastq_dir, filename)
        abs_path = os.path.abspath(out_path)

        # 다운로드 (이미 있으면 skip)
        if not os.path.exists(out_path):
            print(f"Downloading: ftp://{url}")
            try:
                urllib.request.urlretrieve(f"ftp://{url}", out_path)
            except Exception as e:
                print(f"❌ 다운로드 실패: {url}\n{e}")
                continue

        manifest_lines.append(f"{run_id},{abs_path},{direction}")

# manifest 저장
with open(manifest_path, "w") as f:
    f.write("\n".join(manifest_lines))

print(f"\n✅ 다운로드 완료 및 manifest.csv 생성됨: {manifest_path}")
