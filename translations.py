#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Tradução Multi-idioma para o CacifoExe
Suporte para: Português, Inglês, Espanhol, Francês, Alemão, Italiano
"""

class TranslationManager:
    def __init__(self):
        self.current_language = 'en'  # Idioma padrão: Inglês
        self.translations = {
            # === HOME SCREEN ===
            'app_title': {
                'pt': 'Sistema Automático de Cacifos',
                'en': 'Automatic Locker System',
                'es': 'Sistema de Casilleros Automático',
                'fr': 'Système de Casiers Automatique',
                'de': 'Automatisches Schließfachsystem',
                'it': 'Sistema di Armadietti Automatico'
            },
            'home_title': {
                'pt': 'Bem-vindo ao Sistema de Cacifos',
                'en': 'Welcome to the Locker System', 
                'es': 'Bienvenido al Sistema de Casilleros',
                'fr': 'Bienvenue au Système de Casiers',
                'de': 'Willkommen im Schließfachsystem',
                'it': 'Benvenuto nel Sistema di Armadietti'
            },
            'home_subtitle': {
                'pt': 'Guarde as suas bagagens com segurança',
                'en': 'Store your luggage safely',
                'es': 'Guarde su equipaje de forma segura', 
                'fr': 'Rangez vos bagages en sécurité',
                'de': 'Bewahren Sie Ihr Gepäck sicher auf',
                'it': 'Conserva i tuoi bagagli in sicurezza'
            },
            'find_lockers_title': {
                'pt': 'Encontrar cacifos disponíveis',
                'en': 'Find available lockers',
                'es': 'Encontrar casilleros disponibles',
                'fr': 'Trouver des casiers disponibles', 
                'de': 'Verfügbare Schließfächer finden',
                'it': 'Trova armadietti disponibili'
            },
            'find_lockers_desc': {
                'pt': 'Reserve um novo cacifo para as suas bagagens.',
                'en': 'Book a new locker for your bags.',
                'es': 'Reserve un nuevo casillero para sus maletas.',
                'fr': 'Réservez un nouveau casier pour vos bagages.',
                'de': 'Buchen Sie ein neues Schließfach für Ihr Gepäck.',
                'it': 'Prenota un nuovo armadietto per le tue borse.'
            },
            'unlock_locker_title': {
                'pt': 'Desbloquear cacifo',
                'en': 'Unlock locker',
                'es': 'Desbloquear casillero',
                'fr': 'Déverrouiller le casier',
                'de': 'Schließfach öffnen',
                'it': 'Sblocca armadietto'
            },
            'unlock_locker_desc': {
                'pt': 'Aceda ao seu cacifo com contacto e PIN.',
                'en': 'Access your locker with contact and PIN.',
                'es': 'Acceda a su casillero con contacto y PIN.',
                'fr': 'Accédez à votre casier avec contact et PIN.',
                'de': 'Greifen Sie auf Ihr Schließfach mit Kontakt und PIN zu.',
                'it': 'Accedi al tuo armadietto con contatto e PIN.'
            },
            
            # === LANGUAGE SELECTION ===
            'select_language': {
                'pt': 'Selecionar Idioma:',
                'en': 'Select Language:',
                'es': 'Seleccionar Idioma:',
                'fr': 'Sélectionner la Langue:',
                'de': 'Sprache Wählen:',
                'it': 'Seleziona Lingua:'
            },
            
            # === FIND LOCKERS SCREEN ===
            'find_lockers_button': {
                'pt': 'Encontrar Cacifos',
                'en': 'Find Lockers',
                'es': 'Encontrar Casilleros',
                'fr': 'Trouver Casiers',
                'de': 'Schließfächer Finden',
                'it': 'Trova Armadietti'
            },
            'find_lockers_instructions': {
                'pt': 'Cacifos verdes estão disponíveis para reserva. Amarelo significa porta aberta. Vermelho significa ocupado. Toque num cacifo verde para reservá-lo.',
                'en': 'Green lockers are available for booking. Yellow means door open. Red means occupied. Touch a green locker to book it.',
                'es': 'Los casilleros verdes están disponibles para reservar. Amarillo significa puerta abierta. Rojo significa ocupado. Toca un casillero verde para reservarlo.',
                'fr': 'Les casiers verts sont disponibles pour réservation. Jaune signifie porte ouverte. Rouge signifie occupé. Touchez un casier vert pour le réserver.',
                'de': 'Grüne Schließfächer sind für die Buchung verfügbar. Gelb bedeutet Tür offen. Rot bedeutet besetzt. Berühren Sie ein grünes Schließfach, um es zu buchen.',
                'it': 'Gli armadietti verdi sono disponibili per la prenotazione. Giallo significa porta aperta. Rosso significa occupato. Tocca un armadietto verde per prenotarlo.'
            },
            'available_lockers_title': {
                'pt': 'Cacifos Disponíveis',
                'en': 'Available Lockers',
                'es': 'Casilleros Disponibles',
                'fr': 'Casiers Disponibles',
                'de': 'Verfügbare Schließfächer',
                'it': 'Armadietti Disponibili'
            },
            'status_available': {
                'pt': 'Disponível',
                'en': 'Available',
                'es': 'Disponible',
                'fr': 'Disponible',
                'de': 'Verfügbar',
                'it': 'Disponibile'
            },
            'status_occupied': {
                'pt': 'Ocupado',
                'en': 'Occupied',
                'es': 'Ocupado',
                'fr': 'Occupé',
                'de': 'Besetzt',
                'it': 'Occupato'
            },
            'status_door_open': {
                'pt': 'Porta Aberta',
                'en': 'Door Open',
                'es': 'Puerta Abierta',
                'fr': 'Porte Ouverte',
                'de': 'Tür Offen',
                'it': 'Porta Aperta'
            },
            'back_to_home': {
                'pt': 'Voltar ao Início',
                'en': 'Back to Home',
                'es': 'Volver al Inicio',
                'fr': 'Retour à l\'Accueil',
                'de': 'Zurück zum Start',
                'it': 'Torna alla Home'
            },
            
            # === BOOKING SCREEN ===
            'book_locker_title': {
                'pt': 'Reserve o Seu Cacifo',
                'en': 'Book Your Locker',
                'es': 'Reserve su Casillero',
                'fr': 'Réservez votre Casier',
                'de': 'Ihr Schließfach Buchen',
                'it': 'Prenota il Tuo Armadietto'
            },
            'contact_label': {
                'pt': 'Informações de Contacto',
                'en': 'Contact Information',
                'es': 'Información de Contacto',
                'fr': 'Informations de Contact',
                'de': 'Kontaktinformationen',
                'it': 'Informazioni di Contatto'
            },
            'contact_instruction': {
                'pt': 'Introduza os seus dados de contacto para continuar. Será gerado um PIN para o seu cacifo.',
                'en': 'Enter your contact details to continue. A PIN will be generated for your locker.',
                'es': 'Introduzca sus datos de contacto para continuar. Se generará un PIN para su casillero.',
                'fr': 'Entrez vos coordonnées pour continuer. Un PIN sera généré pour votre casier.',
                'de': 'Geben Sie Ihre Kontaktdaten ein, um fortzufahren. Eine PIN wird für Ihr Schließfach generiert.',
                'it': 'Inserisci i tuoi dettagli di contatto per continuare. Verrà generato un PIN per il tuo armadietto.'
            },
            'contact_label_short': {
                'pt': 'Contacto:',
                'en': 'Contact:',
                'es': 'Contacto:',
                'fr': 'Contact:',
                'de': 'Kontakt:',
                'it': 'Contatto:'
            },
            'contact_hint': {
                'pt': 'exemplo@email.com ou +351 123 456 789',
                'en': 'example@email.com or +351 123 456 789',
                'es': 'ejemplo@email.com o +34 123 456 789',
                'fr': 'exemple@email.com ou +33 123 456 789',
                'de': 'beispiel@email.com oder +49 123 456 789',
                'it': 'esempio@email.com o +39 123 456 789'
            },
            'contact_placeholder': {
                'pt': 'exemplo@email.com ou +351 123 456 789',
                'en': 'example@email.com or +351 123 456 789',
                'es': 'ejemplo@email.com o +34 123 456 789',
                'fr': 'exemple@email.com ou +33 123 456 789',
                'de': 'beispiel@email.com oder +49 123 456 789',
                'it': 'esempio@email.com o +39 123 456 789'
            },
            'back_button': {
                'pt': 'Voltar',
                'en': 'Back',
                'es': 'Atrás',
                'fr': 'Retour',
                'de': 'Zurück',
                'it': 'Indietro'
            },
            'confirm_booking': {
                'pt': 'Confirmar Reserva',
                'en': 'Confirm Booking',
                'es': 'Confirmar Reserva',
                'fr': 'Confirmer la Réservation',
                'de': 'Buchung Bestätigen',
                'it': 'Conferma Prenotazione'
            },
            'booking_success': {
                'pt': 'Reserva realizada com sucesso!',
                'en': 'Booking completed successfully!',
                'es': '¡Reserva realizada con éxito!',
                'fr': 'Réservation effectuée avec succès!',
                'de': 'Buchung erfolgreich abgeschlossen!',
                'it': 'Prenotazione completata con successo!'
            },
            'locker_booked': {
                'pt': 'Cacifo reservado com sucesso!',
                'en': 'Locker booked successfully!',
                'es': '¡Casillero reservado con éxito!',
                'fr': 'Casier réservé avec succès!',
                'de': 'Schließfach erfolgreich gebucht!',
                'it': 'Armadietto prenotato con successo!'
            },
            'invalid_contact': {
                'pt': 'Por favor, introduza um contacto válido',
                'en': 'Please enter a valid contact',
                'es': 'Por favor, introduzca un contacto válido',
                'fr': 'Veuillez saisir un contact valide',
                'de': 'Bitte geben Sie einen gültigen Kontakt ein',
                'it': 'Inserisci un contatto valido'
            },
            'error': {
                'pt': 'Erro',
                'en': 'Error',
                'es': 'Error',
                'fr': 'Erreur',
                'de': 'Fehler',
                'it': 'Errore'
            },
            'ok': {
                'pt': 'OK',
                'en': 'OK',
                'es': 'OK',
                'fr': 'OK',
                'de': 'OK',
                'it': 'OK'
            },
            
            # === UNLOCK SCREEN ===
            'unlock_lockers_title': {
                'pt': 'Desbloquear Cacifos',
                'en': 'Unlock Lockers',
                'es': 'Desbloquear Casilleros',
                'fr': 'Déverrouiller Casiers',
                'de': 'Schließfächer Öffnen',
                'it': 'Sblocca Armadietti'
            },
            'contact_pin_title': {
                'pt': 'Contacto e PIN',
                'en': 'Contact and PIN',
                'es': 'Contacto y PIN',
                'fr': 'Contact et PIN',
                'de': 'Kontakt und PIN',
                'it': 'Contatto e PIN'
            },
            'unlock_instruction': {
                'pt': 'Introduza o seu contacto e PIN para desbloquear o seu cacifo.',
                'en': 'Enter your contact and PIN to unlock your locker.',
                'es': 'Introduzca su contacto y PIN para desbloquear su casillero.',
                'fr': 'Entrez votre contact et PIN pour déverrouiller votre casier.',
                'de': 'Geben Sie Ihren Kontakt und PIN ein, um Ihr Schließfach zu öffnen.',
                'it': 'Inserisci il tuo contatto e PIN per sbloccare il tuo armadietto.'
            },
            'pin_label': {
                'pt': 'PIN:',
                'en': 'PIN:',
                'es': 'PIN:',
                'fr': 'PIN:',
                'de': 'PIN:',
                'it': 'PIN:'
            },
            'pin_hint': {
                'pt': 'Introduza o seu PIN',
                'en': 'Enter your PIN',
                'es': 'Introduzca su PIN',
                'fr': 'Entrez votre PIN',
                'de': 'Geben Sie Ihre PIN ein',
                'it': 'Inserisci il tuo PIN'
            },
            'unlock_button': {
                'pt': 'Desbloquear',
                'en': 'Unlock',
                'es': 'Desbloquear',
                'fr': 'Déverrouiller',
                'de': 'Öffnen',
                'it': 'Sblocca'
            },
            'invalid_credentials': {
                'pt': 'Contacto ou PIN inválidos',
                'en': 'Invalid contact or PIN',
                'es': 'Contacto o PIN inválidos',
                'fr': 'Contact ou PIN invalides',
                'de': 'Ungültiger Kontakt oder PIN',
                'it': 'Contatto o PIN non valido'
            },
            'locker_unlocked': {
                'pt': 'Cacifo desbloqueado com sucesso!',
                'en': 'Locker unlocked successfully!',
                'es': '¡Casillero desbloqueado con éxito!',
                'fr': 'Casier déverrouillé avec succès!',
                'de': 'Schließfach erfolgreich geöffnet!',
                'it': 'Armadietto sbloccato con successo!'
            },
            'refresh_button': {
                'pt': 'Atualizar Estado',
                'en': 'Refresh Status',
                'es': 'Actualizar Estado',
                'fr': 'Actualiser le Statut',
                'de': 'Status Aktualisieren',
                'it': 'Aggiorna Stato'
            },
            'try_again_button': {
                'pt': 'Tentar Novamente',
                'en': 'Try Again',
                'es': 'Intentar de Nuevo',
                'fr': 'Essayer à Nouveau',
                'de': 'Erneut Versuchen',
                'it': 'Riprova'
            }
        }
        
        # Idiomas suportados com informações de display
        self.supported_languages = {
            'pt': {'name': 'Português', 'flag': '🇵🇹', 'code': 'PT'},
            'en': {'name': 'English', 'flag': '🇬🇧', 'code': 'EN'}, 
            'es': {'name': 'Español', 'flag': '🇪🇸', 'code': 'ES'},
            'fr': {'name': 'Français', 'flag': '🇫🇷', 'code': 'FR'},
            'de': {'name': 'Deutsch', 'flag': '🇩🇪', 'code': 'DE'},
            'it': {'name': 'Italiano', 'flag': '🇮🇹', 'code': 'IT'}
        }
    
    def set_language(self, language_code):
        """Alterar o idioma atual"""
        if language_code in self.supported_languages:
            self.current_language = language_code
            print(f"Idioma alterado para: {self.supported_languages[language_code]['name']}")
            return True
        return False
    
    def get_text(self, key):
        """Obter texto traduzido para uma chave específica"""
        if key in self.translations:
            translation = self.translations[key]
            if self.current_language in translation:
                return translation[self.current_language]
            else:
                # Fallback para inglês se a tradução não existir
                return translation.get('en', key)
        return key
    
    def get_current_language(self):
        """Obter o idioma atual"""
        return self.current_language
    
    def get_language_info(self, lang_code=None):
        """Obter informações de um idioma específico ou atual"""
        if lang_code is None:
            lang_code = self.current_language
        return self.supported_languages.get(lang_code, {})
    
    def get_all_languages(self):
        """Obter todos os idiomas suportados"""
        return self.supported_languages

# Instância global para facilitar o acesso
translator = TranslationManager()