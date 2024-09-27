// the loop routine runs over and over again forever:
int led = 13;
String msg = "";

void setup() {
    Serial.begin(9600);
    pinMode(led, OUTPUT);
}

void loop() {
    while (Serial.available() > 0) {
        char inChar = (char)Serial.read();
        msg += inChar;

        if (inChar == '\n') {
            msg.trim();
            if (msg == "ON") {
                digitalWrite(led, HIGH);
            } else if (msg == "OFF") {
                digitalWrite(led, LOW);
            }
            msg = "";
        }
    }
}