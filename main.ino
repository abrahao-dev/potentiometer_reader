// Pinos do DAC R-2R (saídas digitais)
const int DAC_D0 = 13;  // LSB
const int DAC_D1 = 12;
const int DAC_D2 = 11;
const int DAC_D3 = 10;  // MSB

// Pinos de controle do ADC0808
const int ALE_PIN = 6;      // Address Latch Enable
const int START_PIN = 2;    // Start Conversion
const int EOC_PIN = 3;      // End of Conversion
const int OE_PIN = 4;       // Output Enable
const int CLOCK_PIN = 5;    // Clock Input

// Pino de entrada do ADC0808 (apenas D7)
const int ADC_D7 = A1;      // Bit mais significativo (MSB)

void setup() {
  // Inicializa comunicação serial
  Serial.begin(9600);
  while (!Serial) {
    ; // Aguarda porta serial conectar
  }
  delay(1000);  // Aguarda estabilização

  // Configura pinos do DAC como saída
  pinMode(DAC_D0, OUTPUT);
  pinMode(DAC_D1, OUTPUT);
  pinMode(DAC_D2, OUTPUT);
  pinMode(DAC_D3, OUTPUT);

  // Configura pinos de controle do ADC
  pinMode(ALE_PIN, OUTPUT);
  pinMode(START_PIN, OUTPUT);
  pinMode(EOC_PIN, INPUT);
  pinMode(OE_PIN, OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);
  
  // Configura pino de dados do ADC como entrada
  pinMode(ADC_D7, INPUT);

  // Estado inicial
  digitalWrite(ALE_PIN, LOW);
  digitalWrite(START_PIN, LOW);
  digitalWrite(OE_PIN, LOW);

  Serial.println("\nDAC R-2R 4 bits -> ADC0808");
  Serial.println("-------------------------");
  delay(1000);  // Aguarda antes de começar
}

// Gera clock para o ADC0808
void clockPulse() {
  digitalWrite(CLOCK_PIN, HIGH);
  delayMicroseconds(5);
  digitalWrite(CLOCK_PIN, LOW);
  delayMicroseconds(5);
}

// Define valor digital no DAC (0-15)
void setDACValue(byte value) {
  digitalWrite(DAC_D0, value & 0x01);
  digitalWrite(DAC_D1, (value >> 1) & 0x01);
  digitalWrite(DAC_D2, (value >> 2) & 0x01);
  digitalWrite(DAC_D3, (value >> 3) & 0x01);
}

// Lê bit D7 do ADC0808
bool readADC() {
  // Inicia conversão
  digitalWrite(ALE_PIN, HIGH);
  digitalWrite(START_PIN, HIGH);
  delayMicroseconds(5);
  digitalWrite(START_PIN, LOW);
  digitalWrite(ALE_PIN, LOW);
  
  // Aguarda fim da conversão
  while (digitalRead(EOC_PIN) == LOW) {
    clockPulse();
  }

  // Lê apenas D7
  digitalWrite(OE_PIN, HIGH);
  delayMicroseconds(5);
  bool d7 = digitalRead(ADC_D7);
  digitalWrite(OE_PIN, LOW);

  return d7;
}

void loop() {
  static int lastDacValue = -1;  // Para controlar a mudança de valor
  static unsigned long lastChangeTime = 0;
  
  // Gera clock contínuo
  clockPulse();

  // Atualiza a cada 1 segundo
  if (millis() - lastChangeTime >= 1000) {
    lastDacValue++;
    if (lastDacValue >= 16) {
      lastDacValue = 0;
      Serial.println("\n--- Reiniciando sequência ---\n");
    }

    // Define valor no DAC
    setDACValue(lastDacValue);

    // Lê valor do ADC (apenas D7)
    bool adcBit = readADC();

    // Mostra resultados
    Serial.print("DAC: ");
    Serial.print(lastDacValue);
    Serial.print(" (");
    
    // Mostra bits do DAC
    for (int i = 3; i >= 0; i--) {
      Serial.print((lastDacValue >> i) & 0x01);
    }
    
    Serial.print(") -> ADC D7: ");
    Serial.print(adcBit);
    
    // Calcula tensão aproximada do DAC (0-5V)
    float voltage = (lastDacValue * 5.0) / 15.0;
    Serial.print(" (");
    Serial.print(voltage, 2);
    Serial.println("V)");

    lastChangeTime = millis();
  }
}