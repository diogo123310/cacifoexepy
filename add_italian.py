#!/usr/bin/env python3
"""
Script to add Italian translations to all existing translation keys
"""

import re

# Italian translations mapping based on English text
italian_translations = {
    'Automatic Locker System': 'Sistema di Armadietti Automatico',
    'Welcome to the Locker System': 'Benvenuto nel Sistema di Armadietti',
    'Store your luggage safely': 'Conserva i tuoi bagagli in sicurezza',
    'Find available lockers': 'Trova armadietti disponibili',
    'Book a new locker for your bags.': 'Prenota un nuovo armadietto per le tue borse.',
    'Unlock locker': 'Sblocca armadietto',
    'Access your locker with contact and PIN.': 'Accedi al tuo armadietto con contatto e PIN.',
    'Select Language:': 'Seleziona Lingua:',
    'Find Lockers': 'Trova Armadietti',
    'Green lockers are available for booking. Yellow means door open. Red means occupied. Touch a green locker to book it.': 'Gli armadietti verdi sono disponibili per la prenotazione. Giallo significa porta aperta. Rosso significa occupato. Tocca un armadietto verde per prenotarlo.',
    'Available Lockers': 'Armadietti Disponibili',
    'Available': 'Disponibile',
    'Occupied': 'Occupato',
    'Door Open': 'Porta Aperta',
    'Back to Home': 'Torna alla Home',
    'Book Your Locker': 'Prenota il Tuo Armadietto',
    'Contact Information': 'Informazioni di Contatto',
    'Enter your contact details to continue. A PIN will be generated for your locker.': 'Inserisci i tuoi dettagli di contatto per continuare. Verrà generato un PIN per il tuo armadietto.',
    'Contact:': 'Contatto:',
    'email@example.com or +351 123 456 789': 'email@esempio.com o +39 123 456 789',
    'example@email.com or +351 123 456 789': 'esempio@email.com o +39 123 456 789',
    'Back': 'Indietro',
    'Confirm Booking': 'Conferma Prenotazione',
    'Booking completed successfully!': 'Prenotazione completata con successo!',
    'Locker booked successfully!': 'Armadietto prenotato con successo!',
    'Please enter a valid contact': 'Inserisci un contatto valido',
    'Error': 'Errore',
    'OK': 'OK',
    'Unlock Lockers': 'Sblocca Armadietti',
    'Contact and PIN': 'Contatto e PIN',
    'Enter your contact and PIN to unlock your locker.': 'Inserisci il tuo contatto e PIN per sbloccare il tuo armadietto.',
    'PIN:': 'PIN:',
    'Enter your PIN': 'Inserisci il tuo PIN',
    'Unlock': 'Sblocca',
    'Invalid contact or PIN': 'Contatto o PIN non valido',
    'Locker unlocked successfully!': 'Armadietto sbloccato con successo!',
    'Refresh Status': 'Aggiorna Stato',
    'Try Again': 'Riprova'
}

def add_italian_translations():
    """Add Italian translations to the translations.py file"""
    
    # Read the file
    with open('translations.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all translation blocks and add Italian
    def replace_translation_block(match):
        block = match.group(0)
        
        # Check if it already has Italian
        if "'it':" in block:
            return block
        
        # Find the last language (German 'de') line
        de_pattern = r"(\s*'de': '[^']*')\n(\s*})"
        de_match = re.search(de_pattern, block)
        
        if de_match:
            de_line = de_match.group(1)
            closing_brace = de_match.group(2)
            
            # Extract the English translation to map to Italian
            en_pattern = r"'en': '([^']*)',"
            en_match = re.search(en_pattern, block)
            
            if en_match:
                english_text = en_match.group(1)
                italian_text = italian_translations.get(english_text, english_text)  # Fallback to English if not found
                
                # Add Italian translation
                italian_line = f"                'it': '{italian_text}'"
                new_block = block.replace(de_line, f"{de_line},\n{italian_line}")
                return new_block
        
        return block
    
    # Pattern to match translation blocks
    pattern = r"'[^']+': \{\s*(?:'[^']+': '[^']*',?\s*)*\}"
    
    # Replace all translation blocks
    new_content = re.sub(pattern, replace_translation_block, content, flags=re.MULTILINE | re.DOTALL)
    
    # Write back to file
    with open('translations.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Italian translations added successfully!")

if __name__ == "__main__":
    add_italian_translations()