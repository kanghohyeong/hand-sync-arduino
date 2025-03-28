#include <Arduino.h>
#include <Servo.h>

#define SERVO_PIN 9

Servo servo;

int target_angle = 0;
int current_angle = 0;

void setup()
{
    servo.attach(SERVO_PIN);
    Serial.begin(9600);
    servo.write(0);
    Serial.println("ready");
}

void loop()
{
    if (Serial.available())
    {
        String input = Serial.readStringUntil('\n');
        input.trim();

        Serial.print("arduino receive message: ");
        Serial.println(input);

        // TODO : 입력값이 숫자인지 확인
        for (int i = 0; i < input.length(); i++)
        {
            if (!isdigit(input[i]))
            {
                Serial.println("please input number");
                return;
            }
        }
        // TODO : 입력값이 0~180 사이의 값인지 확인하고, 그렇지 않으면 에러 메시지를 출력하고 다음 입력을 받도록 수정
        int input_num = input.toInt();
        if (input_num < 0 || input_num > 90)
        {
            Serial.println("please input between 0~90 ");
            return;
        }

        target_angle = input_num;
        Serial.print("target angle: ");
        Serial.println(target_angle);
    }

    // TODO : 현재 각도에서 목표 각도까지 서보 모터를 움직이는 코드를 작성
    int step_angle;

    if (current_angle < target_angle)
    {
        step_angle = min(current_angle + 10, target_angle);
    }
    else
    {
        step_angle = max(current_angle - 10, target_angle);
    }

    Serial.print("step_angle: ");
    Serial.println(step_angle);

    servo.write(step_angle);
    current_angle = step_angle;

    delay(100);
    Serial.println("ready");;
}