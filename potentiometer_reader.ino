// Definir os pinos de controle e leitura
const int ALE = 6;       // Conectado ao pino 22 do ADC0808
const int START = 2;     // Conectado ao pino 6 do ADC0808
const int EOC = 3;       // Conectado ao pino 7 do ADC0808
const int OUTPUT_ENABLE = 4; // Conectado ao pino 9 do ADC0808
const int CLOCK = 5;     // Gerado pelo pino D5 no Arduino

// Definir os pinos D0 a D7 como entrada
const int ADC_PINS[] = {0, 1, 2, 3, 4, 5, 6, 7}; // D0 a D7 do ADC0808

void setup() {
  // Definir pinos de controle como saída
  pinMode(ALE, OUTPUT);
  pinMode(START, OUTPUT);
  pinMode(EOC, INPUT);
  pinMode(OUTPUT_ENABLE, OUTPUT);
  pinMode(CLOCK, OUTPUT);
  
  // Definir os pinos D0 a D7 como entrada
  for (int i = 0; i < 8; i++) {
    pinMode(ADC_PINS[i], INPUT);
  }
  
  // Inicializar comunicação serial
  Serial.begin(9600);
  
  // Gerar o clock de 50 kHz (definir o pino CLOCK para alternar)
  digitalWrite(CLOCK, LOW); // Inicializar o clock em LOW
}

void loop() {
  // Iniciar a conversão
  digitalWrite(START, LOW);  // Baixar o pino START
  digitalWrite(START, HIGH); // Subir o pino START (iniciar a conversão)
  
  // Aguardar até que a conversão seja finalizada (EOC ativado)
  while (digitalRead(EOC) == LOW) {
    // Aguarde o pino EOC ativado
  }
  
  // Ler os 8 bits da saída D0 a D7
  int adcValue = 0;
  for (int i = 0; i < 8; i++) {
    adcValue |= digitalRead(ADC_PINS[i]) << i; // Concatena os bits lidos
  }
  
  // Mostrar o valor no monitor serial
  Serial.print("Valor ADC: ");
  Serial.println(adcValue);  // Mostra o valor digitalizado
  
  delay(500);  // Aguardar meio segundo antes da próxima leitura
}
