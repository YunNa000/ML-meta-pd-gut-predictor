import pandas as pd
import re
import os

# CSV 불러오기
df = pd.read_csv("filtered_alias_project_sample.csv")  # 파일명 수정

# prefix 목록
prefixes = ["DC", "DP", "SP", "SC"]

# 저장 디렉토리
output_dir = "./alias_split"
os.makedirs(output_dir, exist_ok=True)

# left (기형) 저장할 리스트
left_rows = []

# 각 prefix별 처리
for prefix in prefixes:
    # 정규식: 정확히 PREFIX + 3자리 숫자
    valid_pattern = re.compile(rf"^{prefix}\d{{3}}$")

    # 해당 prefix로 시작하는 행만 필터링
    sub_df = df[df["alias"].str.startswith(prefix, na=False)].copy()

    # 유효한 형식만 추출
    valid_df = sub_df[sub_df["alias"].str.match(valid_pattern)]
    invalid_df = sub_df[~sub_df["alias"].str.match(valid_pattern)]

    # 유효한 alias 정렬 & 저장
    valid_df = valid_df.sort_values("alias")
    valid_df.to_csv(f"{output_dir}/{prefix}.csv", index=False)

    # invalid는 모두 left로 누적
    left_rows.append(invalid_df)

# 모든 invalid alias 하나로 합쳐서 left.csv로 저장
if left_rows:
    left_df = pd.concat(left_rows)
    left_df.to_csv(f"{output_dir}/left.csv", index=False)
    print(f"left.csv 저장됨 ({len(left_df)}개)")
else:
    print("left.csv 저장 안됨 (모든 alias가 유효한 포맷)")
