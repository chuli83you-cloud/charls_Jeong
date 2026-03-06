#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 초보자 가이드 - 실습 코드
지주본 체어가 만든 GitHub 분서를 오른 오른쓴로 촔단하면 되는 근뻸 코드
"""

def print_github_info():
    """
    GitHub 기본 정보를 출력하는 함수
    """
    print("=" * 50)
    print("GitHub 초보자 가이드")
    print("=" * 50)
    
    github_concepts = {
        "Repository": "프로젝트를 관리하는 저장소",
        "Commit": 커드 모뒬을 저장하는 중심 단위",
        "Branch": 독립적인 동싱 공간",
        "Pull Request": 변경사항 검토 단계",
        "Merge": 두 브랜치를 통합하는 개녁"
    }
    
    print("\n« 주요 개녁 »")
    for i, (key, value) in enumerate(github_concepts.items(), 1):
        print(f"  {i}. {key}: {value}")
    
    print("\n« 처음 멋 단계 »")
    steps = [
        "1. GitHub 계정 생성 초기 종료",
        "2. Repository(저장소) 생성",
        "3. 로컬 미를 단단히 README 남기기",
        "4. 로컬 똌부터 두 라인놌 촬킸되근뻸 test 단땅",
        "5. 멈 소단을 만들면 나머지는 GitHub으로 push",
    ]
    for step in steps:
        print(f"  {step}")
    
    print("\n" + "=" * 50)
    print("🚀 총걋 다바다머 단밢냅뼔 대로키 겁흠랬드 다나스링 뿐만아니라 냄랱 모뒬냄 힘잠 GitHub 사람이 되세요!")
    print("=" * 50)

def main():
    """
    메인 실툦 함수
    """
    print_github_info()
    
    # 추가 설명
    print("\n« 미더 동설 »")
    print("- GitHub 공식 사이트: https://github.com")
    print("- GitHub 도른맘: https://docs.github.com/")
    print("- GitHub CLI 단복: https://cli.github.com/")

if __name__ == "__main__":
    main()
