#!/usr/bin/env python3
"""
GDD 완성도 검증 스크립트

GDD 마크다운 파일을 분석하여 필수 섹션이 포함되어 있는지,
내용이 충분한지 검증합니다.
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple, Dict

class GDDValidator:
    # 1페이지 GDD 필수 섹션
    ONEPAGE_REQUIRED_SECTIONS = [
        "게임 개요",
        "핵심 경험",
        "핵심 메커니즘",
        "비주얼",
        "기술 스택",
    ]

    # 풀 GDD 필수 섹션
    FULL_GDD_REQUIRED_SECTIONS = [
        "게임 개요",
        "핵심 경험",
        "게임플레이 메커니즘",
        "게임 시스템",
        "비주얼",
        "UI/UX",
        "기술 사양",
    ]

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()

        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def detect_gdd_type(self) -> str:
        """GDD 타입 감지 (1페이지 vs 풀 GDD)"""
        if "목차" in self.content or len(self.content) > 5000:
            return "full"
        return "onepage"

    def extract_sections(self) -> List[str]:
        """문서에서 헤딩 섹션 추출"""
        # # 헤딩 또는 ## 헤딩 찾기
        headings = re.findall(r'^#{1,2}\s+(.+)$', self.content, re.MULTILINE)
        return [h.strip() for h in headings]

    def check_required_sections(self, gdd_type: str) -> bool:
        """필수 섹션 존재 확인"""
        sections = self.extract_sections()
        required = (self.ONEPAGE_REQUIRED_SECTIONS if gdd_type == "onepage"
                   else self.FULL_GDD_REQUIRED_SECTIONS)

        all_present = True
        for req_section in required:
            found = any(req_section in section for section in sections)
            if not found:
                self.errors.append(f"필수 섹션 누락: '{req_section}'")
                all_present = False

        return all_present

    def check_placeholders(self) -> bool:
        """템플릿 플레이스홀더가 그대로 남아있는지 확인"""
        placeholders = [
            r'\[게임 제목\]',
            r'\[날짜\]',
            r'\[이름\]',
            r'\[예:',
            r'\[설명\]',
            r'TODO',
            r'FIXME',
        ]

        has_placeholders = False
        for placeholder in placeholders:
            matches = re.findall(placeholder, self.content, re.IGNORECASE)
            if matches:
                self.warnings.append(
                    f"플레이스홀더 발견 ({len(matches)}개): {placeholder}"
                )
                has_placeholders = True

        return has_placeholders

    def check_content_depth(self) -> Dict[str, int]:
        """각 섹션의 내용 충분성 확인"""
        # 섹션별 단어 수 계산
        sections = re.split(r'^#{1,2}\s+(.+)$', self.content, flags=re.MULTILINE)
        section_lengths = {}

        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                section_name = sections[i].strip()
                section_content = sections[i + 1].strip()
                # 한글, 영문 단어 수 카운트
                word_count = len(re.findall(r'[가-힣]+|\b\w+\b', section_content))
                section_lengths[section_name] = word_count

        # 너무 짧은 섹션 경고
        for section, word_count in section_lengths.items():
            if word_count < 20:
                self.warnings.append(
                    f"섹션이 너무 짧음: '{section}' ({word_count}단어)"
                )

        return section_lengths

    def check_pixijs_specific(self) -> bool:
        """PixiJS 특화 내용 확인"""
        pixijs_keywords = [
            'PixiJS',
            'PIXI.Application',
            '스프라이트',
            'sprite',
            'texture',
            'FPS',
            '프레임',
        ]

        found_keywords = []
        for keyword in pixijs_keywords:
            if keyword.lower() in self.content.lower():
                found_keywords.append(keyword)

        if not found_keywords:
            self.warnings.append(
                "PixiJS 특화 내용이 부족합니다. "
                "기술 스택 섹션에 PixiJS 관련 내용을 추가하세요."
            )
            return False

        self.info.append(f"PixiJS 관련 키워드 발견: {', '.join(found_keywords)}")
        return True

    def check_core_loop(self) -> bool:
        """게임 루프 설명 확인"""
        loop_patterns = [
            r'게임\s*루프',
            r'core\s*loop',
            r'→.*→',  # 화살표로 연결된 루프
            r'\[행동\].*\[결과\]',
        ]

        has_loop = False
        for pattern in loop_patterns:
            if re.search(pattern, self.content, re.IGNORECASE):
                has_loop = True
                break

        if not has_loop:
            self.warnings.append(
                "게임 루프(Core Loop) 설명이 명확하지 않습니다. "
                "플레이어가 반복하는 핵심 행동을 화살표로 표현하세요."
            )

        return has_loop

    def check_version_info(self) -> bool:
        """버전 정보 확인"""
        version_patterns = [
            r'버전.*\d+\.\d+',
            r'version.*\d+\.\d+',
            r'최종\s*수정일',
            r'작성자',
        ]

        found_version = False
        for pattern in version_patterns:
            if re.search(pattern, self.content, re.IGNORECASE):
                found_version = True
                break

        if not found_version:
            self.warnings.append(
                "버전 정보(버전, 최종 수정일, 작성자)가 없습니다. "
                "문서 추적을 위해 추가하세요."
            )

        return found_version

    def validate(self) -> Tuple[bool, str]:
        """전체 검증 실행"""
        print(f"🔍 GDD 검증 중: {self.file_path.name}\n")

        # GDD 타입 감지
        gdd_type = self.detect_gdd_type()
        type_name = "1페이지 GDD" if gdd_type == "onepage" else "풀 GDD"
        print(f"📄 문서 타입: {type_name}")
        print(f"📏 문서 길이: {len(self.content):,} 자\n")

        # 검증 실행
        self.check_required_sections(gdd_type)
        self.check_placeholders()
        section_lengths = self.check_content_depth()
        self.check_pixijs_specific()
        self.check_core_loop()
        self.check_version_info()

        # 결과 출력
        passed = len(self.errors) == 0

        if self.errors:
            print("❌ 오류 (반드시 수정 필요):")
            for error in self.errors:
                print(f"   • {error}")
            print()

        if self.warnings:
            print("⚠️  경고 (권장 수정):")
            for warning in self.warnings:
                print(f"   • {warning}")
            print()

        if self.info:
            print("ℹ️  정보:")
            for info in self.info:
                print(f"   • {info}")
            print()

        # 섹션별 통계
        if section_lengths:
            print("📊 섹션별 단어 수:")
            for section, count in sorted(section_lengths.items(),
                                         key=lambda x: x[1], reverse=True)[:5]:
                print(f"   • {section}: {count}단어")
            print()

        # 최종 결과
        if passed:
            if self.warnings:
                status = "✅ 검증 통과 (경고 있음)"
            else:
                status = "✅ 완벽! 검증 통과"
        else:
            status = "❌ 검증 실패"

        print("=" * 60)
        print(f"{status}")
        print("=" * 60)

        return passed, type_name


def main():
    if len(sys.argv) < 2:
        print("사용법: python validate_gdd.py <GDD_파일.md>")
        print("\n예시:")
        print("  python validate_gdd.py game-design-doc.md")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        validator = GDDValidator(file_path)
        passed, gdd_type = validator.validate()
        sys.exit(0 if passed else 1)

    except FileNotFoundError as e:
        print(f"❌ 오류: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
