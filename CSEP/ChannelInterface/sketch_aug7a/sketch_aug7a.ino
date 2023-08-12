#include "max6675.h"
#include <HX711_ADC.h>
#if defined(ESP8266)|| defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif

// Pinouts:
// Temperature Sensor pinouts
int thermoDO = 4;
int thermoCS = 5;
int thermoCLK = 6;

// LoadCell Pinouts: 
const int HX711_dout = 2; //mcu > HX711 dout pin
const int HX711_sck = 3; //mcu > HX711 sck pin

int channelLength = 6; // length of a channel substring: [c100] = 6;
const int channelCount = 4;
String channels[channelCount];
String readings[channelCount];
const int calVal_eepromAdress = 0;
boolean loadCellDataReady = false;

MAX6675 thermocouple(thermoCLK, thermoCS, thermoDO); // Initializing the thermocouple.
HX711_ADC LoadCell(HX711_dout, HX711_sck); // Initializing the LoadCell

void setup() {
  Serial.begin(9600);
  delay(500);

  LoadCell.begin();

  float calibrationValue;

// This will fetch the load cell calibration value from the eeprom
#if defined(ESP8266)|| defined(ESP32)
  EEPROM.begin(512); // uncomment this if you use ESP8266/ESP32 and want to fetch the calibration value from eeprom
#endif
  EEPROM.get(calVal_eepromAdress, calibrationValue); // uncomment this if you want to fetch the calibration value from eeprom

  // Tare will be performed when the loadcell is started.
  unsigned long stabilizingtime = 2000; // preciscion right after power-up can be improved by adding a few seconds of stabilizing time
  boolean _tare = true; //set this to false if you don't want tare to be performed in the next step
  LoadCell.start(stabilizingtime, _tare);

  // If the Loadcell fails to start
  if (LoadCell.getTareTimeoutFlag()) {
  Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
  while (1);
  }
  // On Successful loadcell start
  else {
    LoadCell.setCalFactor(calibrationValue); // set calibration value (float)
    Serial.println("Startup is complete");
  }

}

void loop() {
  // put your main code here, to run repeatedly:
  char arr[50];

  // [[c1t0], [c2l0], [c300], [c400]]

  if (LoadCell.update()) loadCellDataReady = true;

  if (Serial.available() > 0) {

    String channelData = Serial.readString();
    Serial.println(channelData);
    getChannelRequest(channelData);
    processChannelRequests();
  }

  for (String i: readings) {
    Serial.println(i);
  }

}

/*
Method to separate the data String into channels and store them in the channels array.
*/
void getChannelRequest(String channelData) {
  channelData.toLowerCase();
  int firstIndex = 1;
  int lastIndex = 7;
  for (int i = 0; i < channelCount; i++) {
    channels[i] = channelData.substring(firstIndex, lastIndex);
    firstIndex = lastIndex + 2;
    lastIndex = firstIndex + channelLength;
  }
}

/*
Method to process the channel requests stored in the channels array and call the required methods to return the data.
"t" - temperature reading.
"l" - LoadCell Reading.
  "lc" - Loadcell Calibration.
*/
void processChannelRequests() {
  for (int i = 0; i < channelCount; i++) {
    // if (channels[i][2] == "0") {return;}
    // Thermocouple
    if (channels[i][2] == "t") {
      Serial.println("Getting Thermocouple Reading");
      readings[i] = String(readThermocouple());
    }
    // Load Cell 
    else if (channels[i][2] == "l") {
      if (loadCellDataReady) {
          // Load Cell Read Value
        if (channels[i][3] == "0") {
          Serial.println("Getting Load Cell Reading");
          readLoadCell();
        }
        // Load Cell calibrate
        // else if (channels[i][3] == "c") {
        //   calibrateLoadCell();
        // }
      }

    }
  }
}


// *********************** Thermocouple Methods ***********************
/* Method to read thermocouple value */
float readThermocouple() {
  return thermocouple.readCelsius();
}


// ********************** Load Cell Methods ***********************
/* Method to calibrate the load cell */
// void calibrateLoadCell() {
//   Serial.println("***");
//   Serial.println("Start calibration:");
//   Serial.println("Place the load cell an a level stable surface.");
//   Serial.println("Remove any load applied to the load cell.");
//   Serial.println("Send 't' from serial monitor to set the tare offset.");

//   boolean _resume = false;
//   while (_resume == false) {
//     LoadCell.update();
//     if (Serial.available() > 0) {
//       if (Serial.available() > 0) {
//         char inByte = Serial.read();
//         if (inByte == 't') LoadCell.tareNoDelay();
//       }
//     }
//     if (LoadCell.getTareStatus() == true) {
//       Serial.println("Tare complete");
//       _resume = true;
//     }
//   }

//   Serial.println("Now, place your known mass on the loadcell.");
//   Serial.println("Then send the weight of this mass (i.e. 100.0) from serial monitor.");

//   float known_mass = 0;
//   _resume = false;
//   while (_resume == false) {
//     LoadCell.update();
//     if (Serial.available() > 0) {
//       known_mass = Serial.parseFloat();
//       if (known_mass != 0) {
//         Serial.print("Known mass is: ");
//         Serial.println(known_mass);
//         _resume = true;
//       }
//     }
//   }

//   LoadCell.refreshDataSet(); //refresh the dataset to be sure that the known mass is measured correct
//   float newCalibrationValue = LoadCell.getNewCalibration(known_mass); //get the new calibration value

//   Serial.print("New calibration value has been set to: ");
//   Serial.print(newCalibrationValue);
//   Serial.println(", use this as calibration value (calFactor) in your project sketch.");
//   Serial.print("Save this value to EEPROM adress ");
//   Serial.print(calVal_eepromAdress);
//   Serial.println("? y/n");

//   _resume = false;
//   while (_resume == false) {
//     if (Serial.available() > 0) {
//       char inByte = Serial.read();
//       if (inByte == 'y') {
// #if defined(ESP8266)|| defined(ESP32)
//         EEPROM.begin(512);
// #endif
//         EEPROM.put(calVal_eepromAdress, newCalibrationValue);
// #if defined(ESP8266)|| defined(ESP32)
//         EEPROM.commit();
// #endif
//         EEPROM.get(calVal_eepromAdress, newCalibrationValue);
//         Serial.print("Value ");
//         Serial.print(newCalibrationValue);
//         Serial.print(" saved to EEPROM address: ");
//         Serial.println(calVal_eepromAdress);
//         _resume = true;

//       }
//       else if (inByte == 'n') {
//         Serial.println("Value not saved to EEPROM");
//         _resume = true;
//       }
//     }
//   }

//   Serial.println("End calibration");
//   Serial.println("***");
//   Serial.println("To re-calibrate, send 'r' from serial monitor.");
//   Serial.println("For manual edit of the calibration value, send 'c' from serial monitor.");
//   Serial.println("***");
// }

/* Method to read Load cell value */
float readLoadCell() {
  return LoadCell.getData();
}
