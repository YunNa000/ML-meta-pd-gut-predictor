#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pandas as pd
import os

# 처리할 PRJ 리스트
projects = ['prjna391524', 'prjna381395', 'prjeb27564', 'prjeb14928', 'prjna494620']
base_dir = '/home/users/eunseo916/yunna02102/'

merged_table = None

for prj in projects:
    path = os.path.join(base_dir, prj, 'genus-feature-table.tsv')
    df = pd.read_csv(path, sep='\t', index_col=0)
    
    # sample ID에 prefix로 프로젝트명 추가 (겹치지 않게 하기 위해)
    df.columns = [f"{prj}_{col}" for col in df.columns]
    
    # 병합
    if merged_table is None:
        merged_table = df
    else:
        merged_table = merged_table.join(df, how='outer')

# 결측치는 0으로 대체
merged_table = merged_table.fillna(0)

# 저장
merged_table.to_csv('meta-genus-feature-table.tsv', sep='\t')
print("통합 완료: meta-genus-feature-table.tsv 생성됨")
