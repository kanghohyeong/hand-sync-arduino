#include <Arduino.h>
#include <Servo.h>

#define SERVO_PIN 9
#define TIG_PIN 3
#define ECHO_PIN 2

const int open_angle = 0;
const int close_angle = 80;

bool is_tagged = false;

Servo servo;

// put function declarations here:
int get_distance_mm();
void open_hand();
void close_hand();

void setup()
{
  // put your setup code here, to run once:
  servo.attach(SERVO_PIN);
  Serial.begin(9600);
  pinMode(TIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  servo.write(0);
}

void loop()
{
  // put your main code here, to run repeatedly:
  int distance = get_distance_mm();
  
  // Serial.println(distance);
  // Serial.println(is_tagged);
  delay(500);

  if (is_tagged)
  {
    if (distance > 200)
    {
      is_tagged = false;
    }

    return;
  }

  if (!is_tagged)
  {
    if (distance < 50)
    {
      is_tagged = true;

      close_hand();
      delay(3000);
      open_hand();
    }
  }
}

// put function definitions here:
int get_distance_mm()
{
  digitalWrite(TIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TIG_PIN, LOW);
  return pulseIn(ECHO_PIN, HIGH) * 340 / 2 / 1000;
}

void open_hand()
{
  for (int i = close_angle; i >= open_angle; i--)
  {
    servo.write(i);
    delay(15);
  }
}

void close_hand()
{
  for (int i = open_angle; i <= close_angle; i++)
  {
    servo.write(i);
    delay(15);
  }
}
