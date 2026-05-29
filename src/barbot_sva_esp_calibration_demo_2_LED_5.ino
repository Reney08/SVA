#include <FastLED.h>

#define LED_PIN 8
#define NUM_LEDS 150

CRGB leds[NUM_LEDS];

// ============================
// PINS
// ============================
const int stepPin = 48;
const int dirPin  = 21;
const int enPin   = 47;

const int button1 = 19; // HOME NC
const int button2 = 20; // TEST CONTROL NC
const int killSwitch = 15;

const int recalibBtn = 17; // CALIBRATE
const int testBtn    = 16; // TEST START
const int rainbowBtn = 18;

// ============================
// SETTINGS
// ============================
const int MAX_STEPS = 5120;

const int DEADZONE_LEFT = 8;
const int DEADZONE_RIGHT = 4;
const int FADE_RANGE = 2;

unsigned int stepDelay = 700;

// ============================
// STATE
// ============================
enum State { BOOT, IDLE, TEST, CALIBRATE };
State state = BOOT;

// ============================
// POSITION
// ============================
long steps = 0;

// ============================
// FLAGS
// ============================
bool motorEnabled = true;
bool rainbowMode = false;
uint8_t rainbowHue = 0;

// ============================
// BUTTON EDGE
// ============================
bool lastBtn2 = LOW;
bool lastCalib = LOW;
bool lastRainbow = LOW;

// ============================
// STEP MOTOR
// ============================
void stepMotor(bool dir) {
  digitalWrite(dirPin, dir);

  digitalWrite(stepPin, HIGH);
  delayMicroseconds(stepDelay);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(stepDelay);

  steps += dir ? 1 : -1;
}

// ============================
// KILL SWITCH
// ============================
void handleKillSwitch() {

  static unsigned long t0 = 0;
  static bool pressed = false;
  static bool paused = false;

  bool k = digitalRead(killSwitch);

  if (k == HIGH && !pressed) {
    t0 = millis();
    pressed = true;
  }

  if (k == HIGH && pressed) {

    if (millis() - t0 > 2000) {
      Serial.println("KILL LONG → STOP");
      motorEnabled = false;
      digitalWrite(enPin, HIGH);
      state = IDLE;
      pressed = false;
      paused = false;
      FastLED.clear();
      FastLED.show();
      return;
    }
  }

  if (k == LOW && pressed) {

    if (millis() - t0 < 2000) {
      paused = !paused;
      motorEnabled = !paused;
      digitalWrite(enPin, paused ? HIGH : LOW);
      Serial.println(paused ? "PAUSE ON" : "PAUSE OFF");
    }

    pressed = false;
  }
}

// ============================
// LED UPDATE (SYNC STEP → LED)
// ============================
void updateLEDs() {

  if (rainbowMode) return;

  FastLED.clear();

  int usableLEDs = NUM_LEDS - DEADZONE_LEFT - DEADZONE_RIGHT;
  float ratio = (float)steps / (float)MAX_STEPS;

  int ledPos = DEADZONE_LEFT + (int)(ratio * usableLEDs);

  for (int i = -FADE_RANGE; i <= FADE_RANGE; i++) {

    int idx = ledPos + i;

    if (idx >= 0 && idx < NUM_LEDS) {

      int brightness = 255 - abs(i) * 80;
      if (brightness < 0) brightness = 0;

      leds[idx] = CRGB(0, 0, brightness);
    }
  }

  FastLED.show();
}

// ============================
// RAINBOW
// ============================
void updateRainbow() {

  if (!rainbowMode) return;

  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CHSV(rainbowHue + i * 5, 255, 255);
  }

  FastLED.show();
  rainbowHue++;
}

// ============================
// MOVE UNTIL
// ============================
void moveUntil(bool dir, bool (*stopCondition)()) {

  digitalWrite(enPin, LOW);

  while (!stopCondition()) {

    handleKillSwitch();
    if (!motorEnabled) continue;

    stepMotor(dir);
    updateLEDs();
  }
}

// ============================
// HOME (BUTTON1)
// ============================
void goHome() {

  Serial.println("→ HOME SEARCH");

  digitalWrite(dirPin, false);

  moveUntil(false, []() {
    return digitalRead(button1) == HIGH;
  });

  steps = 0;
  Serial.println("HOME = 0");
}

// ============================
// CALIBRATE BUTTON
// ============================
void calibrate() {
  state = CALIBRATE;
  Serial.println("CALIBRATION");

  goHome();

  state = IDLE;
}

// ============================
// TEST PROGRAM
// ============================
void testProgram() {

  state = TEST;

  Serial.println("TEST START");

  digitalWrite(dirPin, true);

  int target = steps;

  int phase = 0;

  while (true) {

    handleKillSwitch();
    if (!motorEnabled) continue;

    stepMotor(true);
    updateLEDs();

    target++;

    if (target % 500 == 0) {

      Serial.print("STEP: ");
      Serial.println(target);

      delay(2000);

      phase++;

      if (target >= 5000 && digitalRead(button2) == HIGH) {
        Serial.println("BUTTON2 → RETURN HOME");
        break;
      }
    }
  }

  goHome();

  state = IDLE;
}

// ============================
// RAINBOW BUTTON
// ============================
void toggleRainbow() {
  rainbowMode = !rainbowMode;
  Serial.println(rainbowMode ? "RAINBOW ON" : "RAINBOW OFF");

  if (!rainbowMode) {
    FastLED.clear();
    FastLED.show();
  }
}

// ============================
// SETUP
// ============================
void setup() {

  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(120);

  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(enPin, OUTPUT);

  pinMode(button1, INPUT_PULLUP);
  pinMode(button2, INPUT_PULLUP);
  pinMode(killSwitch, INPUT_PULLUP);

  pinMode(recalibBtn, INPUT_PULLUP);
  pinMode(testBtn, INPUT_PULLUP);
  pinMode(rainbowBtn, INPUT_PULLUP);

  Serial.begin(115200);

  digitalWrite(enPin, LOW);

  goHome();

  state = IDLE;
}

// ============================
// LOOP
// ============================
void loop() {

  handleKillSwitch();

  updateRainbow();
  updateLEDs();

  if (state != IDLE) return;

  if (digitalRead(recalibBtn) == HIGH && lastCalib == LOW) {
    calibrate();
  }
  lastCalib = digitalRead(recalibBtn);

  if (digitalRead(testBtn) == HIGH && lastBtn2 == LOW) {
    testProgram();
  }
  lastBtn2 = digitalRead(testBtn);

  if (digitalRead(rainbowBtn) == HIGH && lastRainbow == LOW) {
    toggleRainbow();
  }
  lastRainbow = digitalRead(rainbowBtn);
}