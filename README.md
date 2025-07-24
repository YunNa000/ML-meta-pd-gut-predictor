# meta-pd-gut-predictor
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