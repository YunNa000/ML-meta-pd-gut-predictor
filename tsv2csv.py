import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# --- 0. TSV → CSV 변환 ---
df_tsv = pd.read_csv("meta-genus-feature-table.tsv", sep="\t")  # 파일명은 필요에 맞게 수정
df_tsv.to_csv("merged_genus.csv", index=False)  # 이거

# --- 1. 샘플 & OTU 수 요약 ---
df = pd.read_csv("merged_genus.csv", index_col=0)
n_otus = df.shape[0]
n_samples = df.shape[1]
print(f"OTU (genus) 수: {n_otus}, 샘플 수: {n_samples}")

# --- 2. Alpha diversity (Shannon Index) ---
def shannon_entropy(row):
    p = row[row > 0] / row.sum()
    return -(p * np.log(p)).sum()

shannon = df.T.apply(shannon_entropy, axis=1)
shannon.to_csv("shannon_index.csv") # 이거

# --- 3. Feature sparsity (각 genus가 얼마나 희소한가) ---
sparsity = (df == 0).sum(axis=1) / df.shape[1]
sparsity.to_csv("genus_sparsity.csv")   # 이거 

# --- 4. PCA (2D) ---
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X = df.T.replace(0, np.nan).fillna(0)
X_pca = pca.fit_transform(X)
pca_df = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
pca_df.to_csv("pca_projection.csv", index=False) # 이거  총 4개 
