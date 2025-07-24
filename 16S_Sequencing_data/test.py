import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

tsv_path = "feature-table.tsv"  # 같은 폴더에 있어야 함

# Windows용 나눔고딕 (또는 Malgun Gothic)
matplotlib.rc('font', family='Malgun Gothic')  # 또는 'NanumGothic' if installed
matplotlib.rcParams['axes.unicode_minus'] = False

# 헤더 줄 건너뛰기
with open(tsv_path, "r") as f:
    lines = f.readlines()

header_index = next(i for i, line in enumerate(lines) if not line.startswith("#"))
df = pd.read_csv(tsv_path, sep="\t", skiprows=header_index, index_col=0)

# taxonomy 컬럼 제거
if "taxonomy" in df.columns:
    df.drop(columns=["taxonomy"], inplace=True)

df = df.T

# 출력
print("샘플 수:", df.shape[0])
print("ASV 수:", df.shape[1])
print("샘플당 비어있지 않은 ASV (median):", (df > 0).sum(axis=1).median())

# 히스토그램
sns.histplot((df > 0).sum(axis=1), bins=20, kde=True)
plt.title("Nonzero ASVs per sample")
plt.xlabel("ASV 개수")
plt.ylabel("샘플 수")
plt.tight_layout()
plt.show()

# 가장 많이 나온 ASV 10개
df.sum(axis=0).sort_values(ascending=False).head(10).plot(kind='bar')
plt.title("Top 10 Abundant ASVs")
plt.ylabel("Total Abundance")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
