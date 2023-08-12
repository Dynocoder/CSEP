/*
The program reads the switch state and then passes it through the serial port where it is grabbed by python 
*/

int switchState = 0;

void setup() {
  // Baudrate should be same in python and arduino.
  Serial.begin(115200);
  pinMode(2, INPUT);

}

void loop() {
  // put your main code here, to run repeatedly:

  switchState = digitalRead(2);
  Serial.println(switchState);
  delay(100);
  
}
