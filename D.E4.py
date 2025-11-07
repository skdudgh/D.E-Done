import ED2
import pygame
import os
import shutil
pygame.init()

"""
1. window pixel [1000, 600] / [1500, 800]
"""

screen_width = 1000
screen_height = 600
caption = "E.D"
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(caption)

WHITE = pygame.Color("#FFFFFF")
BLACK = pygame.Color("#000000")
BLUE = pygame.Color("#0000FF")
RED = pygame.Color("#FF0000")
GREEN = pygame.Color("#00FF00")
PALE_GREEN = pygame.Color("#98FB98")
YELLOW = pygame.Color("#FFFF00")

#image
path = os.path.dirname(__file__)
image = os.path.join(path, "image")
button = os.path.join(path, "button")
information = os.path.join(path, "information")

Original_txtFile = os.path.join(information, "ED.txt")
Copy_txtFile = r'E:\D.E File\Decrypt.txt'
Output_txtFile = os.path.join(information, "Output.txt")

background = pygame.image.load(os.path.join(image, 'background.png'))
background = pygame.transform.scale(background, (screen_width, screen_height))

enc_background = pygame.image.load(os.path.join(image, 'encryption.png'))
enc_background = pygame.transform.scale(enc_background, (screen_width, screen_height))

dec_background = pygame.image.load(os.path.join(image, 'decryption.png'))
dec_background = pygame.transform.scale(dec_background, (screen_width, screen_height))

lock1 = pygame.image.load(os.path.join(image, 'lock1.png'))
lock1 = pygame.transform.scale(lock1, (100, 100))
pygame.display.set_icon(lock1)

Original_blue = pygame.image.load(os.path.join(button, 'blue.png'))
blue = pygame.transform.scale(Original_blue, (400, 100))
blue_rect = blue.get_rect()
blue_size= blue.get_size()
blue_x = (screen_width / 4) - (blue.get_width() / 2)
blue_y = (screen_height / 2) - (blue.get_height() / 2)

Original_orange = pygame.image.load(os.path.join(button, 'orange.png'))
orange = pygame.transform.scale(Original_orange, (400, 100))
orange_rect = orange.get_rect()
orange_size= orange.get_size()
orange_x = (screen_width / 1.32) - (orange.get_width() / 2)
orange_y = (screen_height / 2) - (orange.get_height() / 2)

Original_green = pygame.image.load(os.path.join(button, 'green.png'))
green = pygame.transform.scale(Original_green, (400, 100))
green_rect = green.get_rect()
green_size= green.get_size()
green_x = (screen_width / 2) - (green.get_width() / 2)
green_y = (screen_height / 1.5) - (green.get_height() / 2)

Original_pink = pygame.image.load(os.path.join(button, 'pink.png'))
pink = pygame.transform.scale(Original_pink, (400, 100))
pink_rect = pink.get_rect()
pink_size= pink.get_size()
pink_x = (screen_width / 2) - (pink.get_width() / 2)
pink_y = (screen_height / 1.5) - (pink.get_height() / 2)

Original_textImg = pygame.image.load(os.path.join(image, 'textImg.png'))
textImg = pygame.transform.scale(Original_textImg, (65, 75))
textImg_rect = textImg.get_rect()
textImg_size= textImg.get_size()
textImg_x = (blue_x + (blue.get_width() / 2)) - (textImg.get_width() / 2)
textImg_y = (blue_y + (blue.get_height() / 2)) - (textImg.get_height() / 2)

Original_textImg2 = pygame.image.load(os.path.join(image, 'textImg2.png'))
textImg2 = pygame.transform.scale(Original_textImg2, (65, 75))
textImg2_rect = textImg2.get_rect()
textImg2_size= textImg2.get_size()
textImg2_x = (orange_x + (orange.get_width() / 2)) - (textImg2.get_width() / 2)
textImg2_y = (orange_y + (orange.get_height() / 2)) - (textImg2.get_height() / 2)

Original_textImg_E = pygame.image.load(os.path.join(image, 'textImg_Encrypt.png'))
textImg_E = pygame.transform.scale(Original_textImg_E, (65, 75))
textImg_E_rect = textImg_E.get_rect()
textImg_E_size= textImg_E.get_size()
textImg_E_x = (blue_x + (blue.get_width() / 2)) - (textImg_E.get_width() / 2)
textImg_E_y = (blue_y + (blue.get_height() / 2)) - (textImg_E.get_height() / 2)

Original_textImg2_D = pygame.image.load(os.path.join(image, 'textImg2_Decrypt.png'))
textImg2_D = pygame.transform.scale(Original_textImg2_D, (65, 75))
textImg2_D_rect = textImg2_D.get_rect()
textImg2_D_size= textImg2_D.get_size()
textImg2_D_x = (pink_x + (pink.get_width() / 2)) - (textImg2_D.get_width() / 2)
textImg2_D_y = (pink_y + (pink.get_height() / 2)) - (textImg2_D.get_height() / 2)

Original_back = pygame.image.load(os.path.join(image, 'back.png'))
back_E = pygame.transform.scale(Original_back, (135, 135))
back_E_rect = back_E.get_rect()
back_size= back_E.get_size()
back_E_x = (screen_width / 1.13) - (back_E.get_width() / 2)
back_E_y = (screen_height / 1.2) - (back_E.get_height() / 2)

back_D = pygame.transform.scale(Original_back, (135, 135))
back_D_rect = back_D.get_rect()
back_D_size= back_D.get_size()
back_D_x = (screen_width / 1.13) - (back_D.get_width() / 2)
back_D_y = (screen_height / 1.2) - (back_D.get_height() / 2)

#text
font = pygame.font.SysFont(None, 50)
font_small = pygame.font.SysFont(None, 30, bold=False, italic=True)

encryption = font.render("Encryption", True, YELLOW)
encryption_rect = encryption.get_rect()
encryption_size = encryption.get_size()
encryption_x = (blue_x + (blue.get_width() / 2)) - (encryption.get_width() / 2)
encryption_y = (blue_y + (blue.get_height() / 2)) - (encryption.get_height() / 2)

decryption = font.render("Decryption", True, BLUE)
decryption_rect = decryption.get_rect()
decryption_size = decryption.get_size()
decryption_x = (orange_x + (orange.get_width() / 2)) - (decryption.get_width() / 2)
decryption_y = (orange_y + (orange.get_height() / 2)) - (decryption.get_height() / 2)

info = font.render("Info", True, PALE_GREEN)
info_rect = info.get_rect()
info_size = info.get_size()

main = True
enc = False
dec = False

blank = ""

active = False
openfile = False

def connection():
    """암호화 화면에서 나갈 때: USB 파일 동기화"""
    shutil.copy(Original_txtFile, Copy_txtFile)
    
    # USB에 암호화 파일이 있으면 Copy_txtFile에 복사
    if ED2.USB_ENCRYPTED_FILE.exists():
        try:
            shutil.copy(ED2.USB_ENCRYPTED_FILE, Copy_txtFile)
            print("✓ USB → 로컬 동기화")
        except Exception as e:
            print(f"⚠ 동기화 실패: {e}")

def output():
    shutil.copy(Copy_txtFile, Output_txtFile)

def original():
    global blue, blue_x, blue_y, green, green_x, green_y, orange, orange_x, orange_y, pink, pink_x, pink_y
    blue = pygame.transform.scale(Original_blue, (400, 100))
    green = pygame.transform.scale(Original_green, (400, 100))
    orange = pygame.transform.scale(Original_orange, (400, 100))
    pink = pygame.transform.scale(Original_pink, (400, 100))

    blue_x = (screen_width / 4) - (blue.get_width() / 2)
    blue_y = (screen_height / 2) - (blue.get_height() / 2)
    green_x = (screen_width / 2) - (green.get_width() / 2)
    green_y = (screen_height / 1.5) - (green.get_height() / 2)
    orange_x = (screen_width / 1.32) - (orange.get_width() / 2)
    orange_y = (screen_height / 2) - (orange.get_height() / 2)
    pink_x = (screen_width / 2) - (pink.get_width() / 2)
    pink_y = (screen_height / 1.5) - (pink.get_height() / 2)

def clear():
    global background, back, back_x, back_y,Original_blue, blue, blue_x, blue_y, Original_orange, orange, orange_x, orange_y, decryption, decryption_x, decryption_y, encryption, encryption_x, encryption_y
    original()
    screen.blit(background, (0, 0))
    blue = pygame.transform.scale(Original_blue, (400, 100))
    screen.blit(blue, (blue_x, blue_y))
    orange = pygame.transform.scale(Original_orange, (400, 100))
    screen.blit(orange, (orange_x, orange_y))
    screen.blit(decryption, (decryption_x, decryption_y))
    screen.blit(encryption, (encryption_x, encryption_y))

def draw_usb_status():
    """화면에 USB 연결 상태 표시"""
    usb_status_font = pygame.font.SysFont(None, 22)
    
    status = ED2.check_usb_status()
    
    if status['connected']:
        # USB 연결됨
        status_text = "USB: "
        if status['has_private_key']:
            status_text += "Full Mode (Enc+Dec)"  # 암호화+복호화 모두 가능
            status_color = GREEN
        elif status['has_public_key']:
            status_text += "Transfer Mode"  # 다른 컴퓨터로 전송용
            status_color = YELLOW
        else:
            status_text += "Empty"
            status_color = PALE_GREEN
    else:
        status_text = "USB: Not Connected"
        status_color = RED
    
    status_surface = usb_status_font.render(status_text, True, status_color)
    screen.blit(status_surface, (10, screen_height - 30))

def encrypt():
    global Original_blue, blue, blue_x, blue_y, Original_green, green, green_x, green_y, textImg, textImg_x, textImg_y, textImg_E, textImg_E_x, textImg_E_y
    screen.blit(enc_background, (0, 0))
    blue = pygame.transform.scale(Original_blue, (200, 100))
    blue_x, blue_y = 20, 20
    textImg_x = (blue_x + (blue.get_width() / 2)) - (textImg.get_width() / 2)
    textImg_y = (blue_y + (blue.get_height() / 2)) - (textImg.get_height() / 2)
    green = pygame.transform.scale(Original_green, (200, 100))
    green_x, green_y = 20, (blue_y + blue.get_height()) + 80
    textImg_E_x = (green_x + (green.get_width() / 2)) - (textImg_E.get_width() / 2)
    textImg_E_y = (green_y + (green.get_height() / 2)) - (textImg_E.get_height() / 2)
    screen.blit(blue, (blue_x, blue_y))
    screen.blit(textImg, (textImg_x, textImg_y))
    screen.blit(green, (green_x, green_y))
    screen.blit(textImg_E, (textImg_E_x, textImg_E_y))
    screen.blit(back_E, (back_E_x, back_E_y))
    draw_usb_status()  # USB 상태 표시


def decrypt():
    global Original_orange, orange, orange_x, orange_y, Original_pink, pink, pink_x, pink_y, textImg2, textImg2_x, textImg2_y, textImg2_D, textImg2_D_x, textImg2_D_y
    screen.blit(dec_background, (0, 0))
    orange = pygame.transform.scale(Original_orange, (200, 100))
    orange_x, orange_y = 20, 20
    textImg2_x = (orange_x + (orange.get_width() / 2)) - (textImg2.get_width() / 2)
    textImg2_y = (orange_y + (orange.get_height() / 2)) - (textImg2.get_height() / 2)
    pink = pygame.transform.scale(Original_pink, (200, 100))
    pink_x, pink_y = 20, (orange_y + orange.get_height()) + 80
    textImg2_D_x = (pink_x + (pink.get_width() / 2)) - (textImg2_D.get_width() / 2)
    textImg2_D_y = (pink_y + (pink.get_height() / 2)) - (textImg2_D.get_height() / 2)
    screen.blit(orange, (orange_x, orange_y))
    screen.blit(textImg2, (textImg2_x, textImg2_y))
    screen.blit(pink, (pink_x, pink_y))
    screen.blit(textImg2_D, (textImg2_D_x, textImg2_D_y))
    screen.blit(back_D, (back_D_x, back_D_y))
    draw_usb_status()  # USB 상태 표시


mouse_x, mouse_y = pygame.mouse.get_pos()
openfile = False

outputFile_exist = os.path.exists(Output_txtFile)
Isoutput = False
dec_text = "[DECODING:utf-8]\n"
lineChange = "\n"

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.button == 1:
                if main  == True and enc == False and dec == False:
                    if (blue_x <= mouse_x <= blue_x + blue.get_width()) and (blue_y <= mouse_y <= blue_y + blue.get_height()):
                        main = False
                        dec = False
                        enc = True
                        screen.fill(BLACK)
                        print("Encryption")
                    if (orange_x <= mouse_x <= orange_x + orange.get_width()) and (orange_y <= mouse_y <= orange_y + orange.get_height()):
                        main = False
                        enc = False
                        dec = True
                        screen.fill(BLACK)
                        print("Decryption")

            # ==================== 암호화 버튼 클릭 ====================
            if event.button == 1:
                if enc:
                    # 파일 열기 버튼 (textImg)
                    if (textImg_x <= mouse_x <= textImg_x + textImg.get_width()) and \
                       (textImg_y <= mouse_y <= textImg_y + textImg.get_height()):
                        openfile = True
                        print("📝 파일 편집 모드")
                    
                    # 암호화 실행 버튼 (textImg_E)
                    if (textImg_E_x <= mouse_x <= textImg_E_x + textImg_E.get_width()) and \
                       (textImg_E_y <= mouse_y <= textImg_E_y + textImg_E.get_height()):
                        # USB 키로 암호화 (항상)
                        usb_status = ED2.check_usb_status()
                        
                        if usb_status['has_public_key']:
                            print("🔑 USB 공개키로 암호화")
                            ED2.encrypt()
                        else:
                            print("❌ USB에 공개키가 없습니다! setup_usb.py를 실행하세요")
                        
                        if ED2.ed_path.exists():
                            os.startfile(Original_txtFile)

            # ==================== 복호화 버튼 클릭 ====================
            if event.button == 1:
                if dec:
                    # USB에서 파일 가져오기 버튼 (textImg2)
                    if (textImg2_x <= mouse_x <= textImg2_x + textImg2.get_width()) and \
                       (textImg2_y <= mouse_y <= textImg2_y + textImg2.get_height()):
                        print("📥 USB에서 암호화 파일 가져오기 시도...")
                        if ED2.import_from_usb():
                            print("✓ USB에서 파일 가져오기 완료")
                            os.startfile(Copy_txtFile)  # 가져온 암호화 파일 보기
                        else:
                            print("✗ USB에 암호화 파일 없음")
                    
                    # 복호화 실행 버튼 (textImg2_D)
                    if (textImg2_D_x <= mouse_x <= textImg2_D_x + textImg2.get_width()) and \
                       (textImg2_D_y <= mouse_y <= textImg2_D_y + textImg2.get_height()):
                        print("🔓 복호화 시작...")
                        
                        # USB 상태 확인
                        usb_status = ED2.check_usb_status()
                        
                        # 자동 복호화: 로컬 키 시도 → 실패 시 USB 키 시도
                        success = False
                        
                        # 1단계: 로컬 개인키로 시도
                        if ED2.decrypt(use_usb_key=False):
                            print("✓ 로컬 키로 복호화 성공!")
                            success = True
                        # 2단계: 실패 시 USB 개인키로 시도
                        elif usb_status['connected'] and usb_status['has_private_key']:
                            print("→ USB 개인키로 재시도...")
                            if ED2.decrypt(use_usb_key=True):
                                print("✓ USB 키로 복호화 성공!")
                                success = True
                        
                        if success:
                            os.startfile(Output_txtFile)
                            Isoutput = True
                        else:
                            print("✗ 복호화 실패")
                            print("  → 로컬 개인키와 USB 개인키 모두 실패")
                            print("  → 다른 컴퓨터에서 암호화된 파일일 수 있습니다")

            # ==================== 뒤로가기 버튼 ====================
            if event.button == 1:
                if enc:
                    if (back_E_x <= mouse_x <= back_E_x + back_E.get_width()) and (back_E_y <= mouse_y <= back_E_y + back_E.get_height()):
                        original()
                        connection()
                        enc, main = False, True
                if dec:
                    if (back_D_x <= mouse_x <= back_D_x + back_D.get_width()) and (back_D_y <= mouse_y <= back_D_y + back_D.get_height()):
                        original()
                        dec, main = False, True
                        Isoutput = True
                        output()

        # ==================== Output 처리 ====================
        if Isoutput:
            with open(Output_txtFile, 'w', encoding='utf-8') as f:
                f.write(dec_text + lineChange + ED2.decrypted_text)
                print("OUTPUT 저장 완료")
                Isoutput = False

        # ==================== 파일 열기 처리 ====================
        if openfile:
            os.startfile(os.path.join(information, "ED.txt"))
            with open(os.path.join(information, "ED.txt"), 'w', encoding='utf-8') as file:
                file.write(blank)
            with open(os.path.join(information, "OutPut.txt"), 'w', encoding='utf-8') as file:
                file.write(blank)
            openfile = False

    # ==================== 화면 렌더링 ====================
    if main == True and enc == False and dec == False:
        clear()

    if enc == True and main == False and dec == False:
        encrypt()

    if dec == True and main == False and enc == False:
        decrypt()

    pygame.display.update()
    
pygame.quit()