"""
USB 자동 설정 스크립트
실행하면 자동으로 키를 생성하고 종료됩니다
"""

import ED2

print("="*60)
print("   E.D USB 자동 설정")
print("="*60)
print()

# USB 경로 확인
if not ED2.USB_FOLDER.exists():
    ED2.USB_FOLDER.mkdir(parents=True, exist_ok=True)
    print(f"✓ USB 폴더 생성: {ED2.USB_FOLDER}")

print(f"USB 경로: {ED2.USB_FOLDER}")
print()

# 키 상태 확인
status = ED2.check_usb_status()

if status['has_public_key'] and status['has_private_key']:
    print("✓ USB에 키가 이미 존재합니다")
    print("  (기존 키를 그대로 사용합니다)")
else:
    # 자동으로 키 생성
    print("→ USB에 키 생성 중...")
    ED2.generate_keys_on_usb()

print()
print("="*60)
print("✅ 설정 완료! 이제 D.E.py를 사용할 수 있습니다")
print("="*60)
print()