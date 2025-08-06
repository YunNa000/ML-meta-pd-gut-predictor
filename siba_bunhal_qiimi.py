import pandas as pd

# 1. 파일 불러오기
manifest = pd.read_csv('manifest_fixed.tsv', sep='\t')

# 2. sample-id에서 숫자 추출 (정렬을 위한 용도)
def extract_numeric(s):
    return int(''.join(filter(str.isdigit, str(s))))

manifest['sample-id-num'] = manifest['sample-id'].apply(extract_numeric)

# 3. 숫자 기준으로 정렬
manifest_sorted = manifest.sort_values(by='sample-id-num').drop(columns='sample-id-num')

# 4. 고유 sample-id 기준으로 절반 나누기
unique_samples = manifest_sorted['sample-id'].drop_duplicates().tolist()
half = len(unique_samples) // 2
samples_part1 = unique_samples[:half]
samples_part2 = unique_samples[half:]

# 5. 각 파트 필터링
manifest_part1 = manifest_sorted[manifest_sorted['sample-id'].isin(samples_part1)]
manifest_part2 = manifest_sorted[manifest_sorted['sample-id'].isin(samples_part2)]

# 6. 저장
manifest_part1.to_csv('manifest_part1.tsv', sep='\t', index=False)
manifest_part2.to_csv('manifest_part2.tsv', sep='\t', index=False)
