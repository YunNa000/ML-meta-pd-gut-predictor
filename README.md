# AI-driven Gut Microbiome Analysis for Early Parkinson’s Detection

## Overview  
This repository contains the code and analysis pipeline developed during my **KAIST KAM Lab internship (Summer 2025)**.  
The project investigates the gut microbiome of Parkinson’s disease (PD) patients and controls using **integrative 16S rRNA sequencing data analysis**, with the goal of identifying **reproducible microbial biomarkers** and building **machine learning models for prediction**.  

## Motivation  
Parkinson’s disease is often preceded by gastrointestinal symptoms, indicating a strong connection with the **gut–brain axis**. However, previous studies have produced inconsistent results due to dataset heterogeneity and the limitations of linear models.  
This project addresses these challenges by:  
- Integrating and harmonizing multiple publicly available datasets  
- Applying both **linear and non-linear models** for interpretability and predictive power  
- Proposing candidate microbial taxa that can be extended to **wet-lab validation**  

## Data  
- **Samples:** 653 stool samples (PD vs Control)  
- **Features:** 1,137 genus-level abundance profiles  
- **Sources:** ENA public projects (PRJEB14928, PRJEB27564, PRJNA391524, PRJNA494620, PRJEB30615) + -Zenodo metadata (Boktor et al., Wallen et al.)- 
- **Preprocessing:**  
  - QIIME2 (DADA2 denoising, taxonomy assignment)  
  - Aggregation to genus level, relative abundance transformation  
  - -ComBat batch correction based on project_id-

## Analysis Pipeline  
1. **Exploratory Data Analysis (EDA)**  
   - UMAP visualization: overlap between PD and Control → motivates non-linear modeling  
   - Alpha diversity (Shannon): no significant difference (p=0.7119)  
   - Beta diversity (Bray-Curtis + PERMANOVA): significant community structure differences (p=0.003)  

2. **Feature Selection**  
   - Lasso logistic regression (5-fold CV, ROC AUC-based)  

3. **Modeling**  
   - XGBoost (η=0.03, max_depth=4, subsample=0.8, colsample_bytree=0.8)  
   - Performance: ROC AUC=0.79, PR AUC=0.78, Brier score=0.19  

4. **Interpretability**  
   - SHAP values for non-linear feature interpretation  
   - Linear SHAP + coefficient sign alignment for robust validation  
   - Biological mapping of protective vs risk-associated bacteria  

## Key Findings  
- **Protective taxa (↓ in PD):** SCFA/butyrate producers (Agathobacter, Ruminococcus, Bifidobacterium, etc.)  
- **Risk-associated taxa (↑ in PD):** Akkermansia, UBA1819, other pathogenic/barrier-damaging genera  
- Non-linear SHAP interpretation revealed **interaction effects** missed by linear models  


## Requirements & How to Run  
- Python 3.10+  
- Conda environment (`pdgut`)  
- Main dependencies: `qiime2`, `scikit-learn`, `xgboost`, `shap`

## Next Steps
- Extend dataset integration (16S + shotgun metagenomics)
- Analyze PD progression stages (early vs advanced PD)
- Collaborate with wet-lab teams for experimental validation of candidate taxa




------>>>------
KAISTNUERO | ML-driven Meta-Analysis of the Gut Microbiome in Body-First Parkinson’s Disease

- Data
16S rRNA 기반 microbiome 데이터 (e.g. ENA)
MetaData: 건강상태, 지역, 성별, sequencing method 등

- Reference
Machine learning-based meta-analysis reveals gut microbiome alterations associated with Parkinson’s disease (Romano et al., 2023)

- Log
* 2025-07-21
    - ENA 기반 메타데이터 수집 파이프라인 구현
        ENA 포털에서 PRJ/PRJNA 형식의 프로젝트 코드 입력 시, SHOW COLUMN SELECTION을 통해 메타데이터 열 중 SAMPLE ACCESSION (SAMN%07d 형식)을 확인하고, 이를 기반으로 JSON 형식(sample_accessions.json)의 샘플 목록 수집 스크립트(prj2meta.py) 작성
        수집된 SAMN 코드들을 기반으로 ENA XML 포맷 링크에 접속해, 태그 기반으로 메타데이터 추출 및 CSV 파일화 (fetchmeta.py) → ena_detailed_sample_metadata.csv 생성

    - 파일 설명
        prj2meta.py: ENA 프로젝트 코드(PRJNAxxxxx)를 기반으로 SAMN ID 목록(JSON) 수집
        fetchmeta.py: SAMN ID를 기반으로 XML 파싱 → CSV 변환
        ena_detailed_sample_metadata.csv: 샘플별 상세 메타데이터가 포함된 최종 결과 CSV

* 2025-07-23
    - 논문 제공 16S 메타데이터에서 실제 ENA project_id와 매칭되는 align만 필터링
        논문 메타데이터에는 DC-01, DC001 같이 동일 실험을 가리키는 여러 형태 존재
        ENA 메타데이터에서는 DC001, DP001 등의 %03d 형식만 존재하므로 이를 기준으로 일치 여부 확인
        정제된 align 정보는 find_meta-pd-gut-predictor/alias_split/에 저장

    - 실제 논문에서 활용 가능한 align과 ENA 메타데이터의 매칭 결과 정리
        전체 align 중 일치하는 subset만 남겨 분석 대상 확정

    - 16S FASTQ 병렬 다운로드 진행
        16S_Sequencing_data/data/fastq/ 내 각 run_accession 별로 paired-end FASTQ 파일 다운로드
        리눅스 wget 병렬 처리 방식 사용하여 속도 향상
        다운로드 완료 후 QIIME2 입력용 manifest.csv 작성 예정

    - 메타데이터 XML 파싱 정제 스크립트 개선
        meta2csv.py 작성하여 다양한 태그(ex. title, scientific_name, host, env_material 등)를 선택적으로 추출
        결측/중복 제거 및 의미 있는 feature만 유지하도록 구성
        샘플 기반 분석 가능하도록 컬럼 정리된 형태로 저장
