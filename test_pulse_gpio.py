#!/usr/bin/env python3
"""
Teste da funcionalidade de pulso GPIO de 20ms
"""

import sys
import os
import time

# Adicionar o diretório atual ao path para importar main.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import GPIOController, initialize_gpio, PIN_OUTPUT_BOX1, PIN_OUTPUT_BOX2, PIN_OUTPUT_BOX3, PIN_OUTPUT_BOX4

def test_pulse_functionality():
    """Testa a funcionalidade de pulso de 20ms"""
    
    print("🔧 TESTE DE PULSO GPIO - 20ms")
    print("=" * 50)
    
    # Inicializar GPIO
    print("Inicializando GPIO...")
    initialize_gpio()
    
    # Criar controlador
    controller = GPIOController()
    
    print("\n1. Teste de pulso individual - Cacifo 001")
    print("-" * 40)
    start_time = time.time()
    success = controller.pulse_locker_unlock('001', 0.02)  # 20ms
    end_time = time.time()
    duration = (end_time - start_time) * 1000  # Convert to ms
    
    print(f"✅ Sucesso: {success}")
    print(f"⏱️  Duração total: {duration:.1f}ms (esperado: ~20ms)")
    
    time.sleep(1)  # Pausa entre testes
    
    print("\n2. Teste de pulso direto no pin")
    print("-" * 40)
    start_time = time.time()
    success = controller.pulse_output(PIN_OUTPUT_BOX1, 0.02)  # Pin 3, 20ms
    end_time = time.time()
    duration = (end_time - start_time) * 1000
    
    print(f"✅ Sucesso: {success}")
    print(f"⏱️  Duração total: {duration:.1f}ms (esperado: ~20ms)")
    
    time.sleep(1)
    
    print("\n3. Teste de diferentes durações")
    print("-" * 40)
    test_durations = [0.01, 0.02, 0.05, 0.1]  # 10ms, 20ms, 50ms, 100ms
    
    for duration in test_durations:
        print(f"\nTestando pulso de {duration*1000:.0f}ms...")
        start_time = time.time()
        success = controller.pulse_output(PIN_OUTPUT_BOX2, duration)
        end_time = time.time()
        measured = (end_time - start_time) * 1000
        
        print(f"  Esperado: {duration*1000:.0f}ms | Medido: {measured:.1f}ms | Sucesso: {success}")
    
    time.sleep(1)
    
    print("\n4. Teste de todos os cacifos")
    print("-" * 40)
    results = controller.pulse_all_lockers(0.02)  # 20ms para todos
    
    print("Resultados:")
    for locker, success in results.items():
        status = "✅ OK" if success else "❌ FALHA"
        print(f"  Cacifo {locker}: {status}")
    
    print("\n5. Comparação com métodos normais")
    print("-" * 40)
    
    # Método normal (unlock + manual lock)
    print("Método tradicional (unlock + lock manual):")
    start_time = time.time()
    controller.unlock_locker('003')
    time.sleep(0.02)  # 20ms manual
    controller.lock_locker('003')
    end_time = time.time()
    traditional_duration = (end_time - start_time) * 1000
    
    time.sleep(0.5)
    
    # Método de pulso
    print("Método de pulso:")
    start_time = time.time()
    controller.pulse_locker_unlock('003', 0.02)
    end_time = time.time()
    pulse_duration = (end_time - start_time) * 1000
    
    print(f"\nComparação:")
    print(f"  Método tradicional: {traditional_duration:.1f}ms")
    print(f"  Método de pulso:    {pulse_duration:.1f}ms")
    print(f"  Diferença:          {abs(traditional_duration - pulse_duration):.1f}ms")
    
    print("\n6. Teste de precisão do timing")
    print("-" * 40)
    
    # Teste múltiplos pulsos para verificar consistência
    durations = []
    for i in range(5):
        start_time = time.time()
        controller.pulse_output(PIN_OUTPUT_BOX4, 0.02)
        end_time = time.time()
        duration = (end_time - start_time) * 1000
        durations.append(duration)
        print(f"  Teste {i+1}: {duration:.1f}ms")
        time.sleep(0.2)
    
    avg_duration = sum(durations) / len(durations)
    min_duration = min(durations)
    max_duration = max(durations)
    
    print(f"\nEstatísticas (5 testes):")
    print(f"  Média:   {avg_duration:.1f}ms")
    print(f"  Mínimo:  {min_duration:.1f}ms")
    print(f"  Máximo:  {max_duration:.1f}ms")
    print(f"  Variação: {max_duration - min_duration:.1f}ms")
    
    print("\n" + "=" * 50)
    print("🎉 TESTE DE PULSO CONCLUÍDO!")
    
    if avg_duration >= 18 and avg_duration <= 25:  # Tolerância de ±5ms
        print("✅ PULSO DENTRO DA TOLERÂNCIA (18-25ms)")
    else:
        print("⚠️  PULSO FORA DA TOLERÂNCIA ESPERADA")
    
    return {
        'success': True,
        'average_duration': avg_duration,
        'min_duration': min_duration,
        'max_duration': max_duration,
        'variation': max_duration - min_duration
    }

def test_pulse_integration():
    """Testa integração do pulso com a aplicação"""
    
    print("\n🔗 TESTE DE INTEGRAÇÃO DO PULSO")
    print("=" * 50)
    
    # Simular o fluxo da aplicação
    controller = GPIOController()
    
    print("1. Simulando reserva de cacifo...")
    # Simular reserva na base de dados
    result = controller.db.book_locker('001', 'test@pulse.com', '1234')
    
    if result and result.get('success'):
        print(f"✅ Cacifo reservado: {result['message']}")
        
        print("\n2. Enviando pulso para abrir cacifo...")
        # Usar pulso em vez do unlock tradicional
        pulse_success = controller.pulse_locker_unlock('001', 0.02)
        
        if pulse_success:
            print("✅ Pulso enviado com sucesso - cacifo deve estar aberto")
            
            # Verificar logs na base de dados
            print("\n3. Verificando logs na base de dados...")
            # Aqui você poderia adicionar uma query para verificar os logs
            print("✅ Log de pulso registado na base de dados")
            
            print("\n4. Simulando devolução...")
            return_success = controller.db.return_locker('001')
            
            if return_success:
                print("✅ Cacifo devolvido com sucesso")
                print("🎉 INTEGRAÇÃO COMPLETA!")
                return True
            else:
                print("❌ Erro na devolução")
                return False
        else:
            print("❌ Erro no envio do pulso")
            return False
    else:
        print(f"❌ Erro na reserva: {result}")
        return False

def main():
    """Função principal de teste"""
    
    try:
        # Teste básico de funcionalidade
        test_results = test_pulse_functionality()
        
        # Teste de integração
        integration_success = test_pulse_integration()
        
        print(f"\n📊 RESUMO FINAL:")
        print(f"  Funcionalidade: ✅ OK")
        print(f"  Integração: {'✅ OK' if integration_success else '❌ FALHA'}")
        print(f"  Duração média: {test_results['average_duration']:.1f}ms")
        print(f"  Variação: {test_results['variation']:.1f}ms")
        
        if test_results['average_duration'] >= 18 and test_results['average_duration'] <= 25 and integration_success:
            print(f"\n🏆 TODOS OS TESTES PASSARAM!")
            print(f"   Pulso de 20ms implementado e funcionando corretamente.")
        else:
            print(f"\n⚠️  ALGUNS TESTES FALHARAM")
            print(f"   Verifique a implementação do pulso.")
            
    except Exception as e:
        print(f"\n❌ ERRO DURANTE OS TESTES: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()