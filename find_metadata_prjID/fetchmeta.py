import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import xml.etree.ElementTree as ET

# JSON 파일 경로
json_file = "sample_accessions.json"  # 현재 디렉토리에 위치해야 함

# 결과 저장용 리스트
all_metadata = []

# JSON 파일 로딩
with open(json_file, 'r') as f:
    project_samples = json.load(f)

# ENA XML API 기반 메타데이터 수집 함수
def extract_sample_metadata_xml(sample_id):
    url = f"https://www.ebi.ac.uk/ena/browser/api/xml/{sample_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.text)

        # SAMPLE 노드 파싱
        sample_elem = root.find(".//SAMPLE")
        metadata = {"sample_id": sample_id}

        if sample_elem is not None:
            metadata["alias"] = sample_elem.attrib.get("alias")
            metadata["center_name"] = sample_elem.attrib.get("center_name")

            # 기본 필드
            title = sample_elem.findtext("TITLE")
            metadata["title"] = title

            sci_name = sample_elem.findtext("SAMPLE_NAME/SCIENTIFIC_NAME")
            metadata["scientific_name"] = sci_name

            common_name = sample_elem.findtext("SAMPLE_NAME/COMMON_NAME")
            metadata["common_name"] = common_name

            description = sample_elem.findtext("DESCRIPTION")
            metadata["description"] = description

            # ATTRIBUTE 태그 파싱
            for attr in sample_elem.findall(".//SAMPLE_ATTRIBUTE"):
                tag = attr.findtext("TAG")
                value = attr.findtext("VALUE")
                if tag and value:
                    metadata[tag] = value

        return metadata

    except Exception as e:
        print(f"{sample_id} XML 조회 실패: {e}")
        return {"sample_id": sample_id, "error": str(e)}

# 전체 프로젝트 반복 (자동 크롤링)
for project_id, sample_list in project_samples.items():
    print(f"\n{project_id} 처리 중... 총 {len(sample_list)}개 샘플")
    for sid in sample_list:
        metadata = extract_sample_metadata_xml(sid)
        metadata['project_id'] = project_id
        all_metadata.append(metadata)
        time.sleep(1.5)  # 서버 과부하 방지용 대기

# DataFrame으로 변환 및 저장
output_path = "ena_detailed_sample_metadata.csv"
df = pd.DataFrame(all_metadata)
df.to_csv(output_path, index=False)

print(f"\n모든 메타데이터 저장 완료 → {output_path}")
