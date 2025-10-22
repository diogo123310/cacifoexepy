#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar traduções polonesas ao arquivo translations.py
"""

# Traduções polonesas para adicionar
polish_translations = {
    'select_language': 'Wybierz Język:',
    'find_lockers_button': 'Znajdź Szafki',
    'find_lockers_instructions': 'Zielone szafki są dostępne do rezerwacji. Żółty oznacza otwarte drzwi. Czerwony oznacza zajęte. Dotknij zielonej szafki, aby ją zarezerwować.',
    'available_lockers_title': 'Dostępne Szafki',
    'status_available': 'Dostępna',
    'status_occupied': 'Zajęta',
    'status_door_open': 'Drzwi Otwarte',
    'back_to_home': 'Powrót do Strony Głównej',
    'book_locker_title': 'Zarezerwuj Swoją Szafkę',
    'contact_label': 'Informacje Kontaktowe',
    'contact_instruction': 'Wprowadź swoje dane kontaktowe, aby kontynuować. PIN zostanie wygenerowany dla Twojej szafki.',
    'contact_input_label': 'Kontakt:',
    'contact_hint': 'przyklad@email.com lub +48 123 456 789',
    'contact_placeholder': 'przyklad@email.com lub +48 123 456 789',
    'back_button': 'Wstecz',
    'confirm_booking': 'Potwierdź Rezerwację',
    'booking_success': 'Rezerwacja zakończona sukcesem!',
    'locker_booked_success': 'Szafka zarezerwowana pomyślnie!',
    'please_enter_contact': 'Wprowadź prawidłowy kontakt',
    'error': 'Błąd',
    'ok': 'OK',
    'unlock_lockers_title': 'Odblokuj Szafki',
    'contact_pin_title': 'Kontakt i PIN',
    'contact_pin_instruction': 'Wprowadź swój kontakt i PIN, aby odblokować szafkę.',
    'pin_label': 'PIN:',
    'pin_hint': 'Wprowadź swój PIN',
    'unlock_button': 'Odblokuj',
    'invalid_contact_pin': 'Nieprawidłowy kontakt lub PIN',
    'locker_unlocked_success': 'Szafka odblokowana pomyślnie!',
    'refresh_status': 'Odśwież Status',
    'retry': 'Spróbuj Ponownie'
}

# Ler o arquivo translations.py
with open('translations.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Para cada chave, encontrar a linha com 'it': e adicionar 'pl': logo após
for key, polish_text in polish_translations.items():
    # Procurar o padrão: 'key': { ... 'it': 'texto italiano' }
    import re
    
    # Padrão para encontrar a seção da chave
    pattern = rf"'{key}':\s*{{[^}}]*'it':\s*'([^']*)'\s*}}"
    
    def add_polish(match):
        italian_text = match.group(1)
        # Adicionar polonês após italiano
        replacement = match.group(0).replace(
            f"'it': '{italian_text}'",
            f"'it': '{italian_text}',\n                'pl': '{polish_text}'"
        )
        return replacement
    
    content = re.sub(pattern, add_polish, content, flags=re.DOTALL)

# Salvar o arquivo atualizado
with open('translations.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Traduções polonesas adicionadas com sucesso!")
print(f"Total de traduções adicionadas: {len(polish_translations)}")
