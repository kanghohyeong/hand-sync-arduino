import serial
import time

ser = serial.Serial('/dev/tty.usbmodem1301', 9600)  # 포트 번호는 본인 환경에 맞게 변경
time.sleep(2)  # 아두이노 초기화 시간

try:
    while True:
        cmd = input("손을 펴려면 'o', 쥐려면 'c' 입력: ")
        if cmd in ['open', 'close']:
            ser.write(cmd.encode())
        else:
            print("잘못된 입력. 'o' 또는 'c'만 입력하세요.")
except KeyboardInterrupt:
    print("종료합니다.")
finally:
    ser.close()