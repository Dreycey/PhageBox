#include <PhageBox.h> 

void setup()
{
    Serial.begin(9600);
    init_phagebox();
}

void loop() 
{
    start_phagebox();
}
