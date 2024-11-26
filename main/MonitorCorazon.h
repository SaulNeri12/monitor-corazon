
/**
	* Define las operaciones necesarias para la interaccion con el modulo 
	* AD8232 de Analog-Devices
	* @author Saul Neri
	*/
class IMonitorCorazon {
	public:
	/**
		* Inicializa el monitor con el pin especificado
		*/
  virtual void iniciar(uint8_t pin) = 0;

	/**
		* Lee la senial analoga proveniente del modulo AD8232
		*/
	virtual void leerSenialAnaloga() = 0;

	/**
		* Lee la senial digital proveniente del modulo AD8232
		*/
  virtual int leerSenialDigital() = 0;
};

/**
	* Obtiene una instancia de una variante de MonitorCorazon que provee
	* lectura simulada sin necesidad de tener el modulo AD8232
	* @author Saul Neri
	*/
class MonitorStub : public IMonitorCorazon {
public:
  void iniciar(uint8_t pin)  override {
    Serial.println("Simulando AD8232...");
  }

  void leerSenialAnaloga() override {
  
	}

  int leerSenialDigital() override {
    // Simulación: el BPM varía aleatoriamente entre 60 y 100 con pequeños cambios
    // Esto simula un cambio de BPM como podría ocurrir en un entorno real
    int bpmChange = random(-3, 4);  // Genera un cambio aleatorio entre -3 y 3 BPM
    bpmActual += bpmChange;

    // Asegúrate de que el BPM esté dentro de un rango razonable
    if (bpmActual < 60) bpmActual = 60;
    if (bpmActual > 100) bpmActual = 100;

    return bpmActual;
  }

	private:
	  //bool lectura = false;  // Variable que simula la señal digital
  	int bpmActual = 75;    // Valor inicial de BPM (puede cambiar aleatoriamente)
};
