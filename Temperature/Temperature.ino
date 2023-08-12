/* Create by Camilo Robledo
*/

#include "max6675.h"

// Amplifier's declaration

int thermoDO = 4;
int thermoCS = 5;
int thermoCLK = 6;

MAX6675 thermocouple(thermoCLK, thermoCS, thermoDO);

char fromPython;

void setup() {

    Serial.begin(9600);  // Serial Setup

    Serial.println("MAX6675 test");
    // wait for MAX chip to stabilize
  delay(500);
}

void loop() {
  
  if (Serial.available() > 0) {

    fromPython = Serial.read();

    if(fromPython == 'g'){
      
      Serial.println(thermocouple.readCelsius());

    }
  
  }
}
