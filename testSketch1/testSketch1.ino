//#include <stdlib.h>
#include <dht.h> //dht11 sensor library
#define DELA 1000  // Time between message sends.
dht DHT;
#define DHT11_PIN 7
int MOISTURE_SENSOR_PIN = A1;
int moistureValue = 0;

void setup() {
  Serial.begin(9600);
}
void loop()
{
  if (Serial.available())
  {
    int chk = DHT.read11(DHT11_PIN);
    char ch = Serial.read();
    if (ch == '1')
    {
      Serial.println(DHT.temperature);
    }
    else if (ch == '2')
    {
      Serial.println(DHT.humidity);
    }
    else if (ch == '3')
    {
      moistureValue = analogRead(MOISTURE_SENSOR_PIN);
      Serial.println(moistureValue);
    }
  }
  delay(DELA);
}
