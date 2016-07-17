//#include <stdlib.h>
#include <dht.h> //dht11 sensor library
#define DELA 5000  // Time between message sends.
dht DHT;
#define DHT11_PIN 7
int MOISTURE_SENSOR_PIN = A1;
int moistureValue = 0;


void setup() {
  Serial.begin(9600);
}
void loop() {
  int chk = DHT.read11(DHT11_PIN);
  moistureValue = analogRead(MOISTURE_SENSOR_PIN);
  Serial.print("DHT11 Temperature = ");
  Serial.println(DHT.temperature);
  Serial.print("DHT11 Humidity = ");
  Serial.println(DHT.humidity);
  Serial.print("Moisture Value = ");
  Serial.println(moistureValue);
  delay(DELA);
}
