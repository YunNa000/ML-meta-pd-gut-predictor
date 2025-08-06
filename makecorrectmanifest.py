import pandas as pd
import os

# 입력 파일 경로
input_csv = 'manifest.csv'
output_tsv = 'manifest.tsv'

# 지정할 새로운 경로 (마지막 / 포함)
new_base_path = '/home/users/eunseo916/yunna02102/fastq/'

# CSV 읽기
df = pd.read_csv(input_csv)

# 파일명만 추출 + 리눅스용 이름으로 교체
df['filename'] = df['absolute-filepath'].apply(lambda x: os.path.basename(x)
                                                .replace('_R1', '_1')
                                                .replace('_R2', '_2'))

# 새 절대경로 만들기
df['new_path'] = new_base_path + df['filename']

# 방향별로 나누고 병합
forward = df[df['direction'] == 'forward'][['sample-id', 'new_path']].rename(columns={'new_path': 'forward-absolute-filepath'})
reverse = df[df['direction'] == 'reverse'][['sample-id', 'new_path']].rename(columns={'new_path': 'reverse-absolute-filepath'})

# sample-id 기준 병합
manifest = pd.merge(forward, reverse, on='sample-id', how='inner')

# TSV 저장
manifest.to_csv(output_tsv, sep='\t', index=False)
