//Arduino UNO Xbee Test Code
#include <SoftwareSerial.h>
SoftwareSerial xbee(0,1);
// above arguments are the pins that the xbee shield connects to

int count = 0;

char c = 'A';
int pingPong = 1;
void setup() {
  Serial.begin(9600);
  Serial.println("Arduino started sending bytes via xbee");

  xbee.begin(9600);
}


void loop() {
//  if (count == 0) {
//    delay(5000);
//  }
//  xbee.println(String(count));
//  Serial.println(String(count));
//  xbee.println(test);
//  Serial.println(test);  
//  count++;
  
  xbee.println(String(c));
  Serial.println(String(c));

// Circular values
  c = c + 1;
  if (c > 'Z') {
    c = 'A';
  }

// Triggers LED on arduino
  if (pingPong == 0) {
    digitalWrite(13, LOW);
  }
  else {
    digitalWrite(13, HIGH);
  }
  pingPong = 1 - pingPong;
  delay(1000);
}
