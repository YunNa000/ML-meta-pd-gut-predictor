import os
import pandas as pd

# 샘플 ID만 추출하기 위해 Windows 경로에서 파일명만 읽어옴
local_data_dir = "yunna02102/wget_fastq"  # Windows에서 fastq 있는 폴더
linux_data_dir = "/home/users/eunseo916/yunna02102/wget_fastq"  # manifest에 들어갈 경로

filenames = sorted(os.listdir(local_data_dir))

forward_reads = [f for f in filenames if f.endswith("_1.fastq.gz")]
manifest_data = []

for fwd in forward_reads:
    sample_id = fwd.replace("_1.fastq.gz", "")
    rev = f"{sample_id}_2.fastq.gz"
    fwd_path = os.path.join(linux_data_dir, fwd)
    rev_path = os.path.join(linux_data_dir, rev)

    if rev in filenames:
        manifest_data.append({
            "sample-id": sample_id,
            "forward-absolute-filepath": fwd_path,
            "reverse-absolute-filepath": rev_path
        })

manifest_df = pd.DataFrame(manifest_data)
manifest_df.to_csv("manifest.tsv", sep="\t", index=False)

print(f"✅ manifest.tsv 생성 완료 — 샘플 수: {len(manifest_df)}")
