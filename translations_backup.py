#!/usr/bin/e             self.translations = {
            # === HOME SCREEN ===
            'app_title': {
                'pt': 'Sistema Automático de Cacifos',
                'en': 'Automatic Locker System',
                'es': 'Sistema de Casilleros Automático',
                'fr': 'Système de Casiers Automatique',
                'de': 'Automatisches Schließfachsystem',
                'it': 'Sistema di Armadietti Automatico'
            },pp_title': {
                'pt': 'Sistema Automático de Cacifos',
                'en': 'Automatic Locker System',
                'es': 'Sistema de Casilleros Automático',
                'fr': 'Système de Casiers Automatique',
                'de': 'Automatisches Schließfachsystem',
                'it': 'Sistema di Armadietti Automatico'
            },on3
# -*- coding: utf-8 -*-
"""
Sistema de Tradução Multi-idioma para o CacifoExe
Suporte para: Português, Inglês, Espanhol, Francês, Alemão
"""

class TranslationManager:
    def __init__(self):
        self.current_language = 'pt'  # Idioma padrão: Português
        self.translations = {
            # === HOME SCREEN ===
            'app_title': {
                'pt': 'Sistema de Cacifos Automático',
                'en': 'Automatic Locker System',
                'es': 'Sistema de Casilleros Automático',
                'fr': 'Système de Casiers Automatique',
                'de': 'Automatisches Schließfachsystem'
            },
            'home_title': {
                'pt': 'Bem-vindo ao Sistema de Cacifos',
                'en': 'Welcome to the Locker System', 
                'es': 'Bienvenido al Sistema de Casilleros',
                'fr': 'Bienvenue au Système de Casiers',
                'de': 'Willkommen im Schließfachsystem'
            },
            'home_subtitle': {
                'pt': 'Guarde as suas bagagens com segurança',
                'en': 'Store your luggage safely',
                'es': 'Guarde su equipaje de forma segura', 
                'fr': 'Rangez vos bagages en sécurité',
                'de': 'Bewahren Sie Ihr Gepäck sicher auf'
            },
            'find_lockers_title': {
                'pt': 'Encontrar cacifos disponíveis',
                'en': 'Find available lockers',
                'es': 'Encontrar casilleros disponibles',
                'fr': 'Trouver des casiers disponibles', 
                'de': 'Verfügbare Schließfächer finden'
            },
            'find_lockers_desc': {
                'pt': 'Reserve um novo cacifo para as suas bagagens.',
                'en': 'Book a new locker for your bags.',
                'es': 'Reserve un nuevo casillero para sus maletas.',
                'fr': 'Réservez un nouveau casier pour vos bagages.',
                'de': 'Buchen Sie ein neues Schließfach für Ihr Gepäck.'
            },
            'unlock_locker_title': {
                'pt': 'Desbloquear cacifo',
                'en': 'Unlock locker',
                'es': 'Desbloquear casillero',
                'fr': 'Déverrouiller le casier',
                'de': 'Schließfach öffnen'
            },
            'unlock_locker_desc': {
                'pt': 'Aceda ao seu cacifo com contacto e PIN.',
                'en': 'Access your locker with contact and PIN.',
                'es': 'Acceda a su casillero con contacto y PIN.',
                'fr': 'Accédez à votre casier avec contact et PIN.',
                'de': 'Greifen Sie auf Ihr Schließfach mit Kontakt und PIN zu.'
            },
            
            # === LANGUAGE SELECTION ===
            'select_language': {
                'pt': 'Selecionar Idioma:',
                'en': 'Select Language:',
                'es': 'Seleccionar Idioma:',
                'fr': 'Sélectionner la Langue:',
                'de': 'Sprache Wählen:'
            },
            
            # === FIND LOCKERS SCREEN ===
            'find_lockers_header': {
                'pt': 'Encontrar Cacifos',
                'en': 'Find Lockers',
                'es': 'Encontrar Casilleros',
                'fr': 'Trouver des Casiers',
                'de': 'Schließfächer Finden'
            },
            'find_lockers_instructions': {
                'pt': 'Cacifos verdes estão disponíveis para reserva. Amarelo significa porta aberta. Vermelho significa ocupado. Toque num cacifo verde para reservá-lo.',
                'en': 'Green lockers are available for booking. Yellow means door is open. Red means occupied. Touch a green locker to book it.',
                'es': 'Los casilleros verdes están disponibles para reserva. Amarillo significa puerta abierta. Rojo significa ocupado. Toque un casillero verde para reservarlo.',
                'fr': 'Les casiers verts sont disponibles pour la réservation. Jaune signifie porte ouverte. Rouge signifie occupé. Touchez un casier vert pour le réserver.',
                'de': 'Grüne Schließfächer sind für die Buchung verfügbar. Gelb bedeutet Tür offen. Rot bedeutet besetzt. Berühren Sie ein grünes Schließfach, um es zu buchen.'
            },
            'available_lockers': {
                'pt': 'Cacifos Disponíveis',
                'en': 'Available Lockers',
                'es': 'Casilleros Disponibles', 
                'fr': 'Casiers Disponibles',
                'de': 'Verfügbare Schließfächer'
            },
            'locker_available': {
                'pt': 'Disponível',
                'en': 'Available',
                'es': 'Disponible',
                'fr': 'Disponible',
                'de': 'Verfügbar'
            },
            'locker_occupied': {
                'pt': 'Ocupado',
                'en': 'Occupied',
                'es': 'Ocupado',
                'fr': 'Occupé',
                'de': 'Besetzt'
            },
            'locker_door_open': {
                'pt': 'Porta Aberta',
                'en': 'Door Open',
                'es': 'Puerta Abierta',
                'fr': 'Porte Ouverte',
                'de': 'Tür Offen'
            },
            'back_to_home': {
                'pt': 'Voltar ao Início',
                'en': 'Back to Home',
                'es': 'Volver al Inicio',
                'fr': 'Retour à l\'Accueil',
                'de': 'Zurück zum Start'
            },
            
            # === CONTACT PIN SCREEN ===
            'book_locker_title': {
                'pt': 'Reservar o Seu Cacifo',
                'en': 'Book Your Locker',
                'es': 'Reservar Su Casillero',
                'fr': 'Réserver Votre Casier',
                'de': 'Ihr Schließfach Buchen'
            },
            'contact_info': {
                'pt': 'Informações de Contacto',
                'en': 'Contact Information',
                'es': 'Información de Contacto',
                'fr': 'Informations de Contact',
                'de': 'Kontaktinformationen'
            },
            'contact_instruction': {
                'pt': 'Introduza as suas informações de contacto para continuar. Será gerado um PIN para o seu cacifo.',
                'en': 'Enter your contact information to proceed. A PIN will be generated for your locker.',
                'es': 'Ingrese su información de contacto para continuar. Se generará un PIN para su casillero.',
                'fr': 'Saisissez vos informations de contact pour continuer. Un PIN sera généré pour votre casier.',
                'de': 'Geben Sie Ihre Kontaktdaten ein, um fortzufahren. Eine PIN wird für Ihr Schließfach generiert.'
            },
            'contact_label': {
                'pt': 'Contacto:',
                'en': 'Contact:',
                'es': 'Contacto:',
                'fr': 'Contact:',
                'de': 'Kontakt:'
            },
            'contact_hint': {
                'pt': 'exemplo@email.com ou +351 123 456 789',
                'en': 'example@email.com or +44 123 456 789',
                'es': 'ejemplo@email.com o +34 123 456 789',
                'fr': 'exemple@email.com ou +33 123 456 789',
                'de': 'beispiel@email.com oder +49 123 456 789'
            },
            'contact_placeholder': {
                'pt': 'exemplo@email.com ou +351 123 456 789',
                'en': 'example@email.com or +44 123 456 789',
                'es': 'ejemplo@email.com o +34 123 456 789',
                'fr': 'exemple@email.com ou +33 123 456 789',
                'de': 'beispiel@email.com oder +49 123 456 789'
            },
            'locker_selected': {
                'pt': 'Cacifo Selecionado:',
                'en': 'Selected Locker:',
                'es': 'Casillero Seleccionado:',
                'fr': 'Casier Sélectionné:',
                'de': 'Ausgewähltes Schließfach:'
            },
            'confirm_booking': {
                'pt': 'Confirmar Reserva',
                'en': 'Confirm Booking',
                'es': 'Confirmar Reserva',
                'fr': 'Confirmer la Réservation',
                'de': 'Buchung Bestätigen'
            },
            'booking_success': {
                'pt': 'Reserva realizada com sucesso!',
                'en': 'Booking completed successfully!',
                'es': '¡Reserva realizada con éxito!',
                'fr': 'Réservation effectuée avec succès!',
                'de': 'Buchung erfolgreich abgeschlossen!'
            },
            'your_pin': {
                'pt': 'O seu PIN é:',
                'en': 'Your PIN is:',
                'es': 'Su PIN es:',
                'fr': 'Votre PIN est:',
                'de': 'Ihre PIN ist:'
            },
            'remember_pin': {
                'pt': 'Guarde este PIN para desbloquear o seu cacifo.',
                'en': 'Save this PIN to unlock your locker.',
                'es': 'Guarde este PIN para desbloquear su casillero.',
                'fr': 'Sauvegardez ce PIN pour déverrouiller votre casier.',
                'de': 'Speichern Sie diese PIN, um Ihr Schließfach zu öffnen.'
            },
            
            # === UNLOCK LOCKER SCREEN ===
            'unlock_locker_header': {
                'pt': 'Desbloquear Cacifo',
                'en': 'Unlock Locker',
                'es': 'Desbloquear Casillero',
                'fr': 'Déverrouiller le Casier',
                'de': 'Schließfach Öffnen'
            },
            'pin_label': {
                'pt': 'PIN (4 dígitos):',
                'en': 'PIN (4 digits):',
                'es': 'PIN (4 dígitos):',
                'fr': 'PIN (4 chiffres):',
                'de': 'PIN (4 Ziffern):'
            },
            'pin_placeholder': {
                'pt': 'Introduza o seu PIN de 4 dígitos',
                'en': 'Enter your 4-digit PIN',
                'es': 'Ingrese su PIN de 4 dígitos',
                'fr': 'Entrez votre PIN à 4 chiffres',
                'de': 'Geben Sie Ihre 4-stellige PIN ein'
            },
            'unlock_button': {
                'pt': 'Desbloquear Cacifo',
                'en': 'Unlock Locker',
                'es': 'Desbloquear Casillero',
                'fr': 'Déverrouiller le Casier',
                'de': 'Schließfach Öffnen'
            },
            'unlock_instruction': {
                'pt': 'Introduza as suas informações de contacto e PIN de 4 dígitos para aceder ao seu cacifo.',
                'en': 'Enter your contact information and 4-digit PIN to access your locker.',
                'es': 'Ingrese su información de contacto y PIN de 4 dígitos para acceder a su casillero.',
                'fr': 'Entrez vos informations de contact et votre PIN à 4 chiffres pour accéder à votre casier.',
                'de': 'Geben Sie Ihre Kontaktdaten und 4-stellige PIN ein, um auf Ihr Schließfach zuzugreifen.'
            },
            
            # === SUCCESS MESSAGES ===
            'locker_opened_title': {
                'pt': 'Cacifo Aberto',
                'en': 'Locker Opened',
                'es': 'Casillero Abierto',
                'fr': 'Casier Ouvert',
                'de': 'Schließfach Geöffnet'
            },
            'locker_opened_success': {
                'pt': 'foi aberto com sucesso!',
                'en': 'opened successfully!',
                'es': '¡abierto con éxito!',
                'fr': 'ouvert avec succès!',
                'de': 'erfolgreich geöffnet!'
            },
            'locker_opened_instruction': {
                'pt': 'Pode agora colocar ou retirar os seus pertences. O cacifo fechará automaticamente quando terminar.',
                'en': 'You can now place or remove your belongings. The locker will close automatically when you finish.',
                'es': 'Ahora puede colocar o retirar sus pertenencias. El casillero se cerrará automáticamente cuando termine.',
                'fr': 'Vous pouvez maintenant placer ou retirer vos affaires. Le casier se fermera automatiquement lorsque vous aurez terminé.',
                'de': 'Sie können jetzt Ihre Gegenstände hineinlegen oder herausnehmen. Das Schließfach schließt sich automatisch, wenn Sie fertig sind.'
            },
            
            # === ERROR MESSAGES ===
            'error_title': {
                'pt': 'Erro',
                'en': 'Error',
                'es': 'Error',
                'fr': 'Erreur',
                'de': 'Fehler'
            },
            'error_fields_required': {
                'pt': 'Por favor, introduza contacto e PIN',
                'en': 'Please enter both contact and PIN',
                'es': 'Por favor, ingrese contacto y PIN',
                'fr': 'Veuillez entrer le contact et le PIN',
                'de': 'Bitte geben Sie Kontakt und PIN ein'
            },
            'error_pin_format': {
                'pt': 'O PIN deve ter exatamente 4 dígitos',
                'en': 'PIN must be exactly 4 digits',
                'es': 'El PIN debe tener exactamente 4 dígitos',
                'fr': 'Le PIN doit avoir exactement 4 chiffres',
                'de': 'PIN muss genau 4 Ziffern haben'
            },
            'error_incorrect_credentials': {
                'pt': 'Contacto ou PIN incorreto, ou nenhuma reserva ativa',
                'en': 'Incorrect contact or PIN, or no active booking',
                'es': 'Contacto o PIN incorrecto, o ninguna reserva activa',
                'fr': 'Contact ou PIN incorrect, ou aucune réservation active',
                'de': 'Falscher Kontakt oder PIN, oder keine aktive Buchung'
            },
            'try_again': {
                'pt': 'Tentar Novamente',
                'en': 'Try Again',
                'es': 'Intentar de Nuevo',
                'fr': 'Réessayer',
                'de': 'Erneut Versuchen'
            },
            
            # === LOCKER STATUS ===
            'status_available': {
                'pt': 'Disponível',
                'en': 'Available',
                'es': 'Disponible',
                'fr': 'Disponible',
                'de': 'Verfügbar'
            },
            'status_door_open': {
                'pt': 'Porta Aberta',
                'en': 'Door Open',
                'es': 'Puerta Abierta',
                'fr': 'Porte Ouverte',
                'de': 'Tür Offen'
            },
            'status_occupied': {
                'pt': 'Ocupado',
                'en': 'Occupied',
                'es': 'Ocupado',
                'fr': 'Occupé',
                'de': 'Besetzt'
            },
            
            # === BUTTONS ===
            'back_button': {
                'pt': 'Voltar',
                'en': 'Back',
                'es': 'Volver',
                'fr': 'Retour',
                'de': 'Zurück'
            },
            'refresh_button': {
                'pt': 'Atualizar Estado',
                'en': 'Refresh Status',
                'es': 'Actualizar Estado',
                'fr': 'Actualiser État',
                'de': 'Status Aktualisieren'
            },
            'try_again_button': {
                'pt': 'Tentar Novamente',
                'en': 'Try Again',
                'es': 'Intentar de Nuevo',
                'fr': 'Réessayer',
                'de': 'Erneut Versuchen'
            },
            
            # === GENERAL UI ===
            'cancel': {
                'pt': 'Cancelar',
                'en': 'Cancel',
                'es': 'Cancelar',
                'fr': 'Annuler',
                'de': 'Abbrechen'
            },
            'continue': {
                'pt': 'Continuar',
                'en': 'Continue',
                'es': 'Continuar',
                'fr': 'Continuer',
                'de': 'Weiter'
            },
            'ok': {
                'pt': 'OK',
                'en': 'OK',
                'es': 'OK',
                'fr': 'OK',
                'de': 'OK'
            },
            'close': {
                'pt': 'Fechar',
                'en': 'Close',
                'es': 'Cerrar',
                'fr': 'Fermer',
                'de': 'Schließen'
            }
        }
        
        # Idiomas suportados com bandeiras
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
    
    def get_text(self, key, **kwargs):
        """Obter texto traduzido"""
        if key in self.translations:
            text = self.translations[key].get(self.current_language, 
                                           self.translations[key].get('pt', key))
            # Suporte para formatação de texto
            if kwargs:
                try:
                    return text.format(**kwargs)
                except:
                    return text
            return text
        return key
    
    def get_current_language(self):
        """Obter idioma atual"""
        return self.current_language
    
    def get_language_info(self, lang_code):
        """Obter informações do idioma"""
        return self.supported_languages.get(lang_code, {})
    
    def get_all_languages(self):
        """Obter todos os idiomas suportados"""
        return self.supported_languages

# Instância global do gestor de traduções
translation_manager = TranslationManager()

def get_text(key, **kwargs):
    """Função de conveniência para obter textos traduzidos"""
    return translation_manager.get_text(key, **kwargs)

def set_language(language_code):
    """Função de conveniência para alterar idioma"""
    return translation_manager.set_language(language_code)

def get_current_language():
    """Função de conveniência para obter idioma atual"""
    return translation_manager.get_current_language()