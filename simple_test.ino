/*
 * Simple Analog Read Test
 * 
 * This basic sketch tests if your Arduino can read any analog value at all.
 */

void setup() {
  // Start serial communication
  Serial.begin(9600);
  
  // Wait for serial port to connect
  while (!Serial) {
    ; // wait for serial port to connect
  }
  
  Serial.println("Simple Analog Read Test");
  Serial.println("----------------------");
  Serial.println("Testing if A0 can read any values at all");
}

void loop() {
  // Read the analog value
  int sensorValue = analogRead(A0);
  
  // Print the value
  Serial.print("A0 reading: ");
  Serial.println(sensorValue);
  
  // Wait a bit
  delay(500);
}
