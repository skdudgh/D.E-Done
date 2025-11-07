"""
키 상태 진단 스크립트 (USB 전용 버전)
암호화/복호화 문제 해결용
"""

import ED2
import os
from pathlib import Path

print("="*70)
print("   E.D 키 상태 진단 (USB 전용 모드)")
print("="*70)
print()

# 1. USB 상태 확인
print("📌 1. USB 상태")
print("-"*70)
status = ED2.check_usb_status()
print(f"USB 연결: {'✅ 예' if status['connected'] else '❌ 아니오'}")
print(f"USB 경로: {ED2.USB_FOLDER}")
print(f"  → 존재 여부: {'✅ 있음' if ED2.USB_FOLDER.exists() else '❌ 없음'}")
print()
print(f"USB 공개키: {'✅ 있음' if status['has_public_key'] else '❌ 없음'}")
if status['has_public_key']:
    print(f"  → 경로: {ED2.USB_PUBLIC_KEY}")
print()
print(f"USB 개인키: {'✅ 있음' if status['has_private_key'] else '❌ 없음'}")
if status['has_private_key']:
    print(f"  → 경로: {ED2.USB_PRIVATE_KEY}")
print()
print(f"USB 암호화 파일: {'✅ 있음' if status['has_encrypted_file'] else '❌ 없음'}")
if status['has_encrypted_file']:
    print(f"  → 경로: {ED2.USB_ENCRYPTED_FILE}")
print()

# 2. 로컬 작업 파일 상태
print("📌 2. 로컬 작업 파일 상태")
print("-"*70)
print(f"ED.txt: {'✅ 있음' if ED2.ed_path.exists() else '❌ 없음'}")
if ED2.ed_path.exists():
    try:
        with open(ED2.ed_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line.startswith("[ENCODING:"):
                print(f"  → 암호화된 파일입니다")
            else:
                print(f"  → 평문 파일입니다 (첫 줄: {first_line[:30]}...)")
    except Exception as e:
        print(f"  → 읽기 오류: {e}")

print(f"Output.txt: {'✅ 있음' if ED2.output_path.exists() else '❌ 없음'}")
print(f"Decrypt.txt: {'✅ 있음' if ED2.copy_txt_path.exists() else '❌ 없음'}")
print()

# 3. USB 키 쌍 테스트
print("📌 3. USB 키 쌍 일치 테스트")
print("-"*70)

test_message = "TEST_MESSAGE_12345"

# USB 키 쌍 테스트
if status['has_public_key'] and status['has_private_key']:
    try:
        import rsa
        pub = ED2.load_public_key()
        priv = ED2.load_private_key()
        encrypted = rsa.encrypt(test_message.encode(), pub)
        decrypted = rsa.decrypt(encrypted, priv).decode()
        if decrypted == test_message:
            print("✅ USB 키 쌍: 정상 (암호화/복호화 가능)")
            print(f"  → 공개키: {ED2.USB_PUBLIC_KEY.name}")
            print(f"  → 개인키: {ED2.USB_PRIVATE_KEY.name}")
        else:
            print("❌ USB 키 쌍: 복호화 결과 불일치")
    except Exception as e:
        print(f"❌ USB 키 쌍: 테스트 실패 - {e}")
elif status['has_public_key']:
    print("⚠️ USB 키 쌍: 공개키만 있음 (암호화는 가능, 복호화 불가)")
elif status['has_private_key']:
    print("⚠️ USB 키 쌍: 개인키만 있음 (복호화는 가능, 암호화 불가)")
else:
    print("❌ USB 키 쌍: 없음 (암호화/복호화 불가)")
print()

# 4. 문제 진단 및 해결책
print("📌 4. 진단 결과 및 해결책")
print("-"*70)

problems = []

# 문제 1: USB 연결 안 됨
if not status['connected']:
    problems.append({
        'problem': 'USB 폴더가 존재하지 않습니다',
        'solution': f'{ED2.USB_FOLDER}를 만들거나 USB를 연결하세요'
    })

# 문제 2: USB에 키가 없음
if status['connected'] and not (status['has_public_key'] and status['has_private_key']):
    problems.append({
        'problem': 'USB에 키가 완전하지 않습니다',
        'solution': 'D.E.py를 다시 실행하면 자동으로 키가 생성됩니다'
    })

# 문제 3: 암호화 파일이 있지만 키가 없음
if status['has_encrypted_file'] and not status['has_private_key']:
    problems.append({
        'problem': '암호화된 파일은 있지만 복호화 키가 없습니다',
        'solution': '암호화할 때 사용한 USB가 맞는지 확인하세요'
    })

if not problems:
    print("✅ 문제가 발견되지 않았습니다!")
    print()
    if status['has_public_key'] and status['has_private_key']:
        print("암호화/복호화가 정상적으로 작동해야 합니다.")
    else:
        print("D.E.py를 실행하면 키가 자동으로 생성됩니다.")
else:
    for i, p in enumerate(problems, 1):
        print(f"\n❌ 문제 {i}: {p['problem']}")
        print(f"   💡 해결책: {p['solution']}")

print()
print("="*70)
print()

# 5. 빠른 수정 옵션
print("📌 5. 빠른 수정 옵션")
print("-"*70)
print("[1] USB에 새 키 생성 (기존 키 삭제)")
print("[2] USB 폴더 생성")
print("[3] USB 상태만 확인 (수정 안 함)")
print()

choice = input("선택 (1-3): ").strip()

if choice == "1":
    confirm = input("\n⚠️ 기존 키를 삭제하면 이전에 암호화한 파일을 복호화할 수 없습니다.\n계속하시겠습니까? (y/n): ")
    if confirm.lower() == 'y':
        # 기존 키 삭제
        if ED2.USB_PUBLIC_KEY.exists():
            ED2.USB_PUBLIC_KEY.unlink()
            print("✓ 공개키 삭제")
        if ED2.USB_PRIVATE_KEY.exists():
            ED2.USB_PRIVATE_KEY.unlink()
            print("✓ 개인키 삭제")
        
        # 새 키 생성
        print("\n→ 새 키 생성 중...")
        if ED2.generate_keys_on_usb():
            print("✅ 새 키 생성 완료!")
    else:
        print("취소되었습니다")

elif choice == "2":
    try:
        ED2.USB_FOLDER.mkdir(parents=True, exist_ok=True)
        print(f"✅ USB 폴더 생성: {ED2.USB_FOLDER}")
        print("\n이제 D.E.py를 실행하면 키가 자동으로 생성됩니다")
    except Exception as e:
        print(f"❌ 폴더 생성 실패: {e}")

elif choice == "3":
    print("\n상태만 확인했습니다")
else:
    print("잘못된 선택입니다")

print()
print("="*70)
print()

# 6. 추가 정보
print("📌 6. 추가 정보")
print("-"*70)
print("💡 정상 작동 조건:")
print("   - USB 폴더 존재: ✅")
print("   - USB 공개키 존재: ✅")
print("   - USB 개인키 존재: ✅")
print("   - USB 키 쌍 테스트: 정상")
print()
print("💡 두 컴퓨터에서 사용하려면:")
print("   1. 같은 USB를 두 컴퓨터에서 사용하세요")
print("   2. USB의 키 파일(public.pem, private.pem)을 삭제하지 마세요")
print("   3. 암호화한 컴퓨터와 다른 컴퓨터에서 복호화할 수 있습니다")
print()
print("="*70)

input("\n완료! Enter를 눌러 종료하세요...")