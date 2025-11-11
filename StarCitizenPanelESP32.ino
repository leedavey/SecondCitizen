
#include <Arduino.h>
#include <BleGamepad.h>

// Pin definitions
//const int squareLedPin = 17;    // Red LED connected to PWM pin 9
const int redLedPin = 21;    // Red LED connected to PWM pin 9
const int yellowLedPin = 16; // Yellow LED connected to PWM pin 10

// Brightness levels
const int redBrightness = 8;    // Red LED brightness (0-255)
const int yellowBrightness = 16; // Yellow LED brightness (0-255)

unsigned long previousMillis = 0;
int durationRY = 100;

//If using more than 4 buttons, declare them here and change below NUM_BUTTONS
#define BUTTON_PIN1 12  // GPIO12
#define BUTTON_PIN2 14  // GPIO14
#define BUTTON_PIN3 27  // GPIO27
#define BUTTON_PIN4 26  // GPIO26

//Number of buttons connected. You can connect more and change it here
#define NUM_BUTTONS 4

BleGamepad bleGamepad ("Star Citizen Panel", "SCPanel", 100);

//JOYSTICKS (Swap pins if directions are inverted)
#define VRX_JOYSTICK 15
#define VRY_JOYSTICK 4

//If only Y axis is inverted, switch this true/false
#define INVERT_Y false
#define INVERT_X true

int buttonPins[NUM_BUTTONS] = { BUTTON_PIN1, BUTTON_PIN2, BUTTON_PIN3, BUTTON_PIN4 };

/*Default library buttons. If you have specific button values, add them here
On Android, mapping is as follows
BUTTON_1 - A
BUTTON_2 - B
BUTTON_4 - X
BUTTON_5 - Y
*/
int buttons[NUM_BUTTONS] = { BUTTON_1, BUTTON_2, BUTTON_4, BUTTON_5 };

uint16_t VrxReading = 0;
uint16_t VryReading = 0;
uint16_t VrxValue = 0;
uint16_t VryValue = 0;

void setup() {
//  Serial.begin(115200);
  // initialize the push-button pins as an pull-up input
  pinMode(BUTTON_PIN1, INPUT_PULLUP);
  pinMode(BUTTON_PIN2, INPUT_PULLUP);
  pinMode(BUTTON_PIN3, INPUT_PULLUP);
  pinMode(BUTTON_PIN4, INPUT_PULLUP);

  // Set LED pins as outputs
//  pinMode(squareLedPin, OUTPUT);
  pinMode(redLedPin, OUTPUT);
  pinMode(yellowLedPin, OUTPUT);
  
  // Initialize random seed
  randomSeed(analogRead(0));

  bleGamepad.begin();
}

void loop() {

  // LED control
//  digitalWrite(squareLedPin, HIGH);
  unsigned long currentMillis = millis();
  
  if (currentMillis - previousMillis >= durationRY) {
    // save the last time you blinked the LED
    previousMillis = currentMillis;
    durationRY = random(1000, 4001);
    // Randomly choose which LED to turn on (0 = red, 1 = yellow, 2 = both, 3 = none)
    int ledChoice = random(4);
  
    // Turn off both LEDs initially
    analogWrite(redLedPin, 0);
    analogWrite(yellowLedPin, 0);
  
    // Turn on selected LED(s)
    if (ledChoice == 0) {
      analogWrite(redLedPin, redBrightness);
    } else if (ledChoice == 1) {
      analogWrite(yellowLedPin, yellowBrightness);
    } else if (ledChoice == 2) {
      analogWrite(redLedPin, redBrightness);
      analogWrite(yellowLedPin, yellowBrightness);
    }
  }

  if (bleGamepad.isConnected()) {

    VrxReading = analogRead(VRX_JOYSTICK);
    VryReading = analogRead(VRY_JOYSTICK);

    VrxValue = map(VrxReading, 4095, 0, 0, 32737);
    VryValue = map(VryReading, 4095, 0, 0, 32737);

    if (INVERT_Y) {
      VryValue = 32737 - VryValue;
      if (VryValue < 0)
        VryValue = -VryValue;
    }
    if (INVERT_X) {
      VrxValue = 32737 - VrxValue;
      if (VrxValue < 0)
        VrxValue = -VrxValue;
    }

    bleGamepad.setLeftThumb(VrxValue, VryValue);

    for (int i = 0; i < NUM_BUTTONS; i++) {
      if (!digitalRead(buttonPins[i])) {
        bleGamepad.press(buttons[i]);
      } else {
        bleGamepad.release(buttons[i]);
      }
    }
  }
}