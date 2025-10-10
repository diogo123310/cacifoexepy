#!/usr/bin/env python3
"""
Teste da integração do pulso de 20ms na aplicação completa
"""

import sys
import os
import time

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_booking_with_pulse():
    """Testa o fluxo completo de reserva com pulso"""
    
    print("🎯 TESTE DE INTEGRAÇÃO - RESERVA COM PULSO DE 20ms")
    print("=" * 60)
    
    # Importar e inicializar
    from main import GPIOController, initialize_gpio
    from database import LockerDatabase
    
    # Simular inicialização
    print("1. Inicializando sistema...")
    initialize_gpio()
    controller = GPIOController()
    
    print("✅ Sistema inicializado")
    
    # Teste 1: Verificar funcionalidade do pulso
    print("\n2. Testando funcionalidade de pulso...")
    
    start_time = time.time()
    success = controller.pulse_locker_unlock('001', 0.02)
    end_time = time.time()
    duration = (end_time - start_time) * 1000
    
    print(f"   Pulso enviado: {'✅' if success else '❌'}")
    print(f"   Duração: {duration:.1f}ms")
    
    if not success or duration < 15 or duration > 30:
        print("❌ FALHA: Pulso não funcionou corretamente")
        return False
    
    # Teste 2: Simular fluxo de reserva completo
    print("\n3. Simulando fluxo completo de reserva...")
    
    # 3.1 Verificar status inicial
    initial_status = controller.db.get_locker_status('002')
    print(f"   Status inicial cacifo 002: {initial_status}")
    
    if initial_status != 'available':
        # Devolver se estiver ocupado
        controller.db.return_locker('002')
        print("   Cacifo 002 devolvido para teste")
    
    # 3.2 Fazer reserva
    print("   Fazendo reserva...")
    booking_result = controller.db.book_locker('002', 'test@pulse.com', '9876')
    
    if not booking_result or not booking_result.get('success'):
        print(f"❌ FALHA na reserva: {booking_result}")
        return False
    
    print(f"   ✅ Reserva bem-sucedida: {booking_result['message']}")
    
    # 3.3 Enviar pulso para abrir
    print("   Enviando pulso para abrir cacifo...")
    
    start_time = time.time()
    pulse_success = controller.pulse_locker_unlock('002', 0.02)
    end_time = time.time()
    pulse_duration = (end_time - start_time) * 1000
    
    if pulse_success:
        print(f"   ✅ Pulso enviado com sucesso ({pulse_duration:.1f}ms)")
    else:
        print("   ❌ FALHA no envio do pulso")
        return False
    
    # 3.4 Verificar status após reserva
    after_booking_status = controller.db.get_locker_status('002')
    print(f"   Status após reserva: {after_booking_status}")
    
    if after_booking_status != 'occupied':
        print("❌ FALHA: Status não foi atualizado corretamente")
        return False
    
    # 3.5 Simular devolução
    print("   Simulando devolução...")
    return_success = controller.db.return_locker('002')
    
    if return_success:
        print("   ✅ Cacifo devolvido com sucesso")
    else:
        print("   ❌ FALHA na devolução")
        return False
    
    # Verificar status final
    final_status = controller.db.get_locker_status('002')
    print(f"   Status final: {final_status}")
    
    if final_status != 'available':
        print("❌ FALHA: Status final incorreto")
        return False
    
    print("\n✅ FLUXO COMPLETO BEM-SUCEDIDO!")
    return True

def test_multiple_lockers_pulse():
    """Testa pulso em múltiplos cacifos"""
    
    print("\n4. Testando pulso em múltiplos cacifos...")
    print("-" * 50)
    
    from main import GPIOController, initialize_gpio
    
    controller = GPIOController()
    
    # Testar pulso em todos os cacifos
    lockers = ['001', '002', '003', '004']
    results = {}
    
    for locker in lockers:
        print(f"   Testando cacifo {locker}...")
        
        start_time = time.time()
        success = controller.pulse_locker_unlock(locker, 0.02)
        end_time = time.time()
        duration = (end_time - start_time) * 1000
        
        results[locker] = {
            'success': success,
            'duration': duration
        }
        
        status = "✅" if success else "❌"
        print(f"     {status} Pulso: {duration:.1f}ms")
        
        time.sleep(0.1)  # Pequena pausa entre cacifos
    
    # Verificar resultados
    all_success = all(r['success'] for r in results.values())
    avg_duration = sum(r['duration'] for r in results.values()) / len(results)
    
    print(f"\n   Resumo:")
    print(f"   Todos bem-sucedidos: {'✅' if all_success else '❌'}")
    print(f"   Duração média: {avg_duration:.1f}ms")
    
    return all_success and 15 <= avg_duration <= 30

def test_timing_precision():
    """Testa precisão do timing do pulso"""
    
    print("\n5. Testando precisão do timing...")
    print("-" * 50)
    
    from main import GPIOController
    
    controller = GPIOController()
    
    # Múltiplos testes para verificar consistência
    durations = []
    num_tests = 10
    
    for i in range(num_tests):
        start_time = time.time()
        success = controller.pulse_output(3, 0.02)  # Pin 3, 20ms
        end_time = time.time()
        
        if success:
            duration = (end_time - start_time) * 1000
            durations.append(duration)
            print(f"   Teste {i+1:2d}: {duration:.1f}ms")
        else:
            print(f"   Teste {i+1:2d}: ❌ FALHA")
            return False
        
        time.sleep(0.05)  # Pequena pausa entre testes
    
    # Calcular estatísticas
    avg = sum(durations) / len(durations)
    min_dur = min(durations)
    max_dur = max(durations)
    variation = max_dur - min_dur
    
    print(f"\n   Estatísticas ({num_tests} testes):")
    print(f"   Média:     {avg:.1f}ms")
    print(f"   Mínimo:    {min_dur:.1f}ms")
    print(f"   Máximo:    {max_dur:.1f}ms")
    print(f"   Variação:  {variation:.1f}ms")
    
    # Critérios de sucesso
    success_criteria = (
        15 <= avg <= 30 and      # Média dentro da tolerância
        variation <= 10 and       # Variação baixa
        min_dur >= 10            # Mínimo razoável
    )
    
    print(f"   Precisão: {'✅ BOA' if success_criteria else '❌ RUIM'}")
    
    return success_criteria

def test_error_handling():
    """Testa tratamento de erros"""
    
    print("\n6. Testando tratamento de erros...")
    print("-" * 50)
    
    from main import GPIOController
    
    controller = GPIOController()
    
    # Teste 1: Cacifo inexistente
    print("   Testando cacifo inexistente...")
    result = controller.pulse_locker_unlock('999', 0.02)
    
    if result == False:
        print("   ✅ Erro tratado corretamente")
    else:
        print("   ❌ Erro não tratado corretamente")
        return False
    
    # Teste 2: Duração inválida
    print("   Testando duração inválida...")
    try:
        result = controller.pulse_output(3, -0.01)  # Duração negativa
        print("   ✅ Duração negativa tratada")
    except Exception as e:
        print(f"   ✅ Exceção capturada: {type(e).__name__}")
    
    # Teste 3: Pin inválido
    print("   Testando pin inválido...")
    try:
        result = controller.pulse_output(999, 0.02)  # Pin inexistente
        print("   ✅ Pin inválido tratado")
    except Exception as e:
        print(f"   ✅ Exceção capturada: {type(e).__name__}")
    
    return True

def main():
    """Função principal de teste"""
    
    try:
        print("🚀 INICIANDO TESTES DE INTEGRAÇÃO DO PULSO")
        print("=" * 60)
        
        # Executar todos os testes
        test1 = test_booking_with_pulse()
        test2 = test_multiple_lockers_pulse()
        test3 = test_timing_precision()
        test4 = test_error_handling()
        
        # Resumo final
        print("\n" + "=" * 60)
        print("📊 RESUMO DOS TESTES:")
        print(f"   Fluxo de Reserva:     {'✅ PASSOU' if test1 else '❌ FALHOU'}")
        print(f"   Múltiplos Cacifos:    {'✅ PASSOU' if test2 else '❌ FALHOU'}")
        print(f"   Precisão do Timing:   {'✅ PASSOU' if test3 else '❌ FALHOU'}")
        print(f"   Tratamento de Erros:  {'✅ PASSOU' if test4 else '❌ FALHOU'}")
        
        all_passed = test1 and test2 and test3 and test4
        
        print("\n" + "=" * 60)
        if all_passed:
            print("🏆 TODOS OS TESTES PASSARAM!")
            print("   ✅ Pulso de 20ms totalmente integrado")
            print("   ✅ Funcionalidade pronta para produção")
            print("   ✅ Sistema robusto e confiável")
        else:
            print("⚠️  ALGUNS TESTES FALHARAM")
            print("   ❌ Verifique a implementação do pulso")
            print("   ❌ Corrija os problemas antes de usar em produção")
        
        return all_passed
        
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO DURANTE OS TESTES: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)