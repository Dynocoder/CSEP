/*

The following code reads a string input from the python CLI through the serial port
and then perform some action on it.

*/

String cmd;

void setup() {
  // Baudrate should be same in python and arduino
  Serial.begin(115200);
  pinMode(13, OUTPUT);
}

void loop() {
  while (Serial.available() == 0){

  }
  cmd = Serial.readString();
  Serial.println(cmd);

  if (cmd.equals("on")) {
    digitalWrite(13, HIGH);
  }
  else if (cmd.equals("off")) {
    digitalWrite(13, LOW);
  }
}