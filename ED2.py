import rsa
import chardet
from pathlib import Path
import base64
import shutil
import os

# ==================== 경로 설정 ====================
# USB 경로 설정 (로컬 키는 사용하지 않음)
USB_FOLDER = Path("E:/D.E File")  # USB 드라이브 경로
USB_FOLDER.mkdir(parents=True, exist_ok=True)

USB_PUBLIC_KEY = USB_FOLDER / "public.pem"  # USB에 저장될 공개키
USB_PRIVATE_KEY = USB_FOLDER / "private.pem"  # USB에 저장될 개인키
USB_ENCRYPTED_FILE = USB_FOLDER / "Encrypted.txt"  # USB에 저장될 암호화 파일

# 로컬 파일 경로 (작업용)
base_path = Path(__file__).parent / "information"
base_path.mkdir(exist_ok=True)
ed_path = base_path / "ED.txt"  # 암호화/복호화 대상 파일
output_path = base_path / "Output.txt"  # 복호화 결과 파일
copy_txt_path = base_path / "Decrypt.txt"  # 복호화 결과 임시 파일

# 전역 변수
decrypted_text = ""


# ==================== 키 관리 함수 ====================
def generate_keys_on_usb():
    """USB에 직접 RSA 키 쌍 생성"""
    if not USB_PUBLIC_KEY.exists() or not USB_PRIVATE_KEY.exists():
        print("→ USB에 새 키 쌍 생성 중...")
        pub_key, priv_key = rsa.newkeys(1024)
        
        USB_FOLDER.mkdir(parents=True, exist_ok=True)
        
        with open(USB_PUBLIC_KEY, 'wb') as f:
            f.write(pub_key.save_pkcs1('PEM'))
        with open(USB_PRIVATE_KEY, 'wb') as f:
            f.write(priv_key.save_pkcs1('PEM'))
        
        print(f"✓ USB에 RSA 키 생성 완료")
        print(f"  공개키: {USB_PUBLIC_KEY}")
        print(f"  개인키: {USB_PRIVATE_KEY}")
        return True
    else:
        print("✓ USB에 키가 이미 존재합니다")
        return True

def load_public_key():
    """USB의 공개키 불러오기"""
    if not USB_PUBLIC_KEY.exists():
        raise FileNotFoundError(f"USB에 공개키가 없습니다: {USB_PUBLIC_KEY}\n'python setup_usb.py'를 먼저 실행하세요")
    
    with open(USB_PUBLIC_KEY, 'rb') as f:
        return rsa.PublicKey.load_pkcs1(f.read())

def load_private_key():
    """USB의 개인키 불러오기"""
    if not USB_PRIVATE_KEY.exists():
        raise FileNotFoundError(f"USB에 개인키가 없습니다: {USB_PRIVATE_KEY}\n'python setup_usb.py'를 먼저 실행하세요")
    
    with open(USB_PRIVATE_KEY, 'rb') as f:
        return rsa.PrivateKey.load_pkcs1(f.read())


# ==================== 인코딩 감지 ====================
def detect_encoding(file_path):
    """파일 인코딩 자동 감지"""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding'], raw_data


# ==================== 암호화 함수 ====================
def encrypt(use_usb_key=True):
    """
    ED.txt 파일을 USB 공개키로 암호화하고 USB로 복사
    
    Args:
        use_usb_key (bool): 항상 True (USB 키만 사용)
    """
    print(f"\n[암호화 시작]")
    
    # 1. USB 키 확인
    if not USB_PUBLIC_KEY.exists():
        print("✗ USB에 공개키가 없습니다!")
        print("  → 'python setup_usb.py'를 먼저 실행하세요")
        return False
    
    # 2. 파일 존재 확인
    if not ed_path.exists():
        print("✗ ED.txt 파일이 없습니다")
        return False

    # 3. 파일 읽기 및 인코딩 감지
    encoding, raw_data = detect_encoding(ed_path)
    try:
        content = raw_data.decode(encoding)
    except Exception as e:
        print(f"✗ 인코딩 오류: {e}")
        return False

    if not content.strip():
        print("✗ 암호화할 내용이 없습니다")
        return False

    print(f"→ 원본 내용: {len(content)} 문자")

    # 4. USB 공개키로 암호화
    try:
        public_key = load_public_key()
        print(f"→ USB 공개키 사용: {USB_PUBLIC_KEY.name}")
    except Exception as e:
        print(f"✗ 공개키 로드 실패: {e}")
        return False

    # 5. 블록 단위 암호화
    content_bytes = content.encode(encoding)
    max_length = 117  # RSA 1024비트 최대 암호화 크기
    encrypted_blocks = []

    for i in range(0, len(content_bytes), max_length):
        block = content_bytes[i:i+max_length]
        try:
            encrypted_block = rsa.encrypt(block, public_key)
            encrypted_blocks.append(base64.b64encode(encrypted_block).decode('ascii'))
        except Exception as e:
            print(f"✗ 암호화 오류: {e}")
            return False

    print(f"→ 암호화 블록: {len(encrypted_blocks)}개")

    # 6. 암호화된 데이터 저장 (ED.txt에 덮어쓰기)
    encrypted_content = f"[ENCODING:{encoding}]\n\n"
    for block in encrypted_blocks:
        encrypted_content += block + '\n'
    
    with open(ed_path, 'w', encoding='utf-8') as f:
        f.write(encrypted_content)
    
    print(f"✓ 암호화 완료: {ed_path}")

    # 7. USB로 복사
    try:
        shutil.copy(ed_path, USB_ENCRYPTED_FILE)
        print(f"✓ USB에 저장: {USB_ENCRYPTED_FILE}")
        return True
    except Exception as e:
        print(f"⚠ USB 복사 실패: {e}")
        print("  (암호화는 완료되었으나 USB에 복사하지 못했습니다)")
        return True  # 암호화는 성공


# ==================== 복호화 함수 ====================
def decrypt(use_usb_key=True):
    """
    ED.txt의 암호화된 내용을 USB 개인키로 복호화
    
    Args:
        use_usb_key (bool): 항상 True (USB 키만 사용)
    """
    global decrypted_text
    
    print(f"\n[복호화 시작]")
    
    # 1. USB 키 확인
    if not USB_PRIVATE_KEY.exists():
        print("✗ USB에 개인키가 없습니다!")
        print("  → 'python setup_usb.py'를 먼저 실행하세요")
        return False
    
    # 2. 파일 존재 확인
    if not ed_path.exists():
        print("✗ ED.txt 파일이 없습니다")
        return False

    # 3. 암호화된 파일 읽기
    try:
        with open(ed_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"✗ 파일 읽기 오류: {e}")
        return False

    # 4. 인코딩 정보 추출
    if not lines or not lines[0].startswith("[ENCODING:"):
        print("✗ 인코딩 정보를 찾을 수 없습니다 (암호화된 파일이 아님)")
        return False

    encoding = lines[0].strip()[10:-1]  # "[ENCODING:UTF-8]" → "UTF-8"
    encrypted_blocks = [line.strip() for line in lines[2:] if line.strip()]

    if not encrypted_blocks:
        print("✗ 암호화된 데이터가 없습니다")
        return False

    print(f"→ 암호화 블록: {len(encrypted_blocks)}개")

    # 5. USB 개인키로 복호화
    try:
        private_key = load_private_key()
        print(f"→ USB 개인키 사용: {USB_PRIVATE_KEY.name}")
    except Exception as e:
        print(f"✗ 개인키 로드 실패: {e}")
        return False

    decrypted_bytes = b''
    for idx, block in enumerate(encrypted_blocks):
        try:
            encrypted_block = base64.b64decode(block)
            decrypted_bytes += rsa.decrypt(encrypted_block, private_key)
        except Exception as e:
            print(f"✗ {idx+1}번째 블록 복호화 실패: {e}")
            print(f"  → 다른 키로 암호화된 파일일 수 있습니다")
            return False

    # 6. 디코딩
    try:
        decrypted_text = decrypted_bytes.decode(encoding)
    except Exception as e:
        print(f"✗ 디코딩 오류: {e}")
        return False

    # 7. 결과 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(decrypted_text)
    
    with open(copy_txt_path, 'w', encoding='utf-8') as f:
        f.write(decrypted_text)
    
    print(f"✓ 복호화 완료!")
    print(f"  → {output_path}")
    print(f"  → {copy_txt_path}")
    
    return True


# ==================== USB 파일 관리 ====================
def import_from_usb():
    """USB의 암호화된 파일을 로컬(ED.txt)로 복사"""
    try:
        if not USB_ENCRYPTED_FILE.exists():
            print(f"✗ USB에 암호화된 파일이 없습니다: {USB_ENCRYPTED_FILE}")
            return False
        
        shutil.copy(USB_ENCRYPTED_FILE, ed_path)
        print(f"✓ USB에서 파일 가져오기 완료: {ed_path}")
        return True
    except Exception as e:
        print(f"✗ USB에서 가져오기 실패: {e}")
        return False

def check_usb_status():
    """USB 연결 및 키 상태 확인"""
    status = {
        'connected': USB_FOLDER.exists(),
        'has_public_key': USB_PUBLIC_KEY.exists(),
        'has_private_key': USB_PRIVATE_KEY.exists(),
        'has_encrypted_file': USB_ENCRYPTED_FILE.exists()
    }
    return status


# ==================== 초기화 ====================
# 프로그램 시작 시 USB에 키가 없으면 자동 생성
try:
    if not (USB_PUBLIC_KEY.exists() and USB_PRIVATE_KEY.exists()):
        print("\n" + "="*60)
        print("   🔑 USB 키 자동 생성")
        print("="*60)
        generate_keys_on_usb()
        print("="*60)
        print()
    else:
        print("\n✓ USB 키 로드 완료")
        print(f"  공개키: {USB_PUBLIC_KEY.name}")
        print(f"  개인키: {USB_PRIVATE_KEY.name}")
except Exception as e:
    print(f"\n⚠️ USB 초기화 오류: {e}")
    print(f"  USB 경로: {USB_FOLDER}")
    print(f"  USB가 올바르게 연결되었는지 확인하세요")

# 전역 변수 초기화 (D.E.py 호환용)
try:
    public_key = load_public_key()
    private_key = load_private_key()
except Exception as e:
    print(f"⚠️ 키 로드 실패: {e}")
    public_key = None
    private_key = None