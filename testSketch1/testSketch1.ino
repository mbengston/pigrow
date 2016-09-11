//#include <stdlib.h>
#include <dht.h> //dht11 sensor library
#define DELA 1000  // Time between message sends.

#include <MCP3008.h>


// define pin connections
#define CS_PIN 12
#define CLOCK_PIN 9
#define MOSI_PIN 11
#define MISO_PIN 10

// put pins inside MCP3008 constructor
MCP3008 adc(CLOCK_PIN, MOSI_PIN, MISO_PIN, CS_PIN);
dht DHT;
#define DHT11_PIN 7
// int MOISTURE_SENSOR_PIN = A1;
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
      moistureValue = adc.readADC(0);
      Serial.println(moistureValue);

//      iterate thru all channels
//      for (int i=0; i<8; i++) {
//        moistureValue = adc.readADC(i);
//        Serial.println(moistureValue);
//      }
    }
  }
  delay(DELA);
}

