"""
Script para demonstrar como simular mudanças nos pinos GPIO durante o desenvolvimento.
Este script mostra como os estados dos pinos podem ser alterados para testar
a funcionalidade de atualização automática dos cacifos.
"""

# Exemplo de como usar no código principal para testar:

# No main.py, você pode adicionar este código para simular mudanças:

"""
# Adicionar ao final da classe LuggageKioskApp:

def simulate_gpio_changes(self):
    '''Simula mudanças nos pinos GPIO para demonstração'''
    import threading
    import time
    
    def change_pins():
        time.sleep(10)  # Esperar 10 segundos
        print("Simulando mudança no PIN 2 para HIGH (Cacifo 001 fica ocupado)")
        if hasattr(GPIO, 'simulate_pin_change'):
            GPIO.simulate_pin_change(2, 1)
        
        time.sleep(5)   # Esperar mais 5 segundos
        print("Simulando mudança no PIN 4 para LOW (Cacifo 002 fica disponível)")
        if hasattr(GPIO, 'simulate_pin_change'):
            GPIO.simulate_pin_change(4, 0)
    
    # Executar em thread separada para não bloquear a UI
    thread = threading.Thread(target=change_pins)
    thread.daemon = True
    thread.start()

# E no método build():
def build(self):
    initialize_gpio()
    
    # Simular mudanças para demonstração
    self.simulate_gpio_changes()
    
    return MainScreenManager()
"""

# Estados iniciais configurados no MockGPIO:
# PIN 2 (Cacifo 001): LOW (0) = DISPONÍVEL (verde)
# PIN 4 (Cacifo 002): HIGH (1) = OCUPADO (vermelho)
# PIN 27 (Cacifo 003): LOW (0) = DISPONÍVEL (verde)
# PIN 10 (Cacifo 004): HIGH (1) = OCUPADO (vermelho)

print("Estados dos cacifos baseados nos pinos GPIO:")
print("PIN 2 = LOW  → Cacifo 001 = DISPONÍVEL (verde)")
print("PIN 4 = HIGH → Cacifo 002 = OCUPADO (vermelho)")
print("PIN 27 = LOW → Cacifo 003 = DISPONÍVEL (verde)")
print("PIN 10 = HIGH → Cacifo 004 = OCUPADO (vermelho)")
print("\nO sistema atualiza automaticamente a cada 2 segundos!")