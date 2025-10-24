#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Tradução Multi-idioma para o CacifoExe
Suporte para: Português, Inglês, Espanhol, Francês, Alemão, Italiano, Polonês
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
                'it': 'Sistema di Armadietti Automatico',
                'pl': 'Automatyczny System Szafek'
            },
            'home_title': {
                'pt': 'Bem-vindo ao Sistema de Cacifos',
                'en': 'Welcome to the Locker System', 
                'es': 'Bienvenido al Sistema de Casilleros',
                'fr': 'Bienvenue au Système de Casiers',
                'de': 'Willkommen im Schließfachsystem',
                'it': 'Benvenuto nel Sistema di Armadietti',
                'pl': 'Witamy w Systemie Szafek'
            },
            'home_subtitle': {
                'pt': 'Guarde as suas bagagens com segurança',
                'en': 'Store your luggage safely',
                'es': 'Guarde su equipaje de forma segura', 
                'fr': 'Rangez vos bagages en sécurité',
                'de': 'Bewahren Sie Ihr Gepäck sicher auf',
                'it': 'Conserva i tuoi bagagli in sicurezza',
                'pl': 'Przechowuj swój bagaż bezpiecznie'
            },
            'find_lockers_title': {
                'pt': 'Encontrar cacifos disponíveis',
                'en': 'Find available lockers',
                'es': 'Encontrar casilleros disponibles',
                'fr': 'Trouver des casiers disponibles', 
                'de': 'Verfügbare Schließfächer finden',
                'it': 'Trova armadietti disponibili',
                'pl': 'Znajdź dostępne szafki'
            },
            'find_lockers_desc': {
                'pt': 'Reserve um novo cacifo para as suas bagagens.',
                'en': 'Book a new locker for your bags.',
                'es': 'Reserve un nuevo casillero para sus maletas.',
                'fr': 'Réservez un nouveau casier pour vos bagages.',
                'de': 'Buchen Sie ein neues Schließfach für Ihr Gepäck.',
                'it': 'Prenota un nuovo armadietto per le tue borse.',
                'pl': 'Zarezerwuj nową szafkę na swoje torby.'
            },
            'unlock_locker_title': {
                'pt': 'Desbloquear cacifo',
                'en': 'Unlock locker',
                'es': 'Desbloquear casillero',
                'fr': 'Déverrouiller le casier',
                'de': 'Schließfach öffnen',
                'it': 'Sblocca armadietto',
                'pl': 'Odblokuj szafkę'
            },
            'unlock_locker_desc': {
                'pt': 'Aceda ao seu cacifo com contacto e PIN.',
                'en': 'Access your locker with contact and PIN.',
                'es': 'Acceda a su casillero con contacto y PIN.',
                'fr': 'Accédez à votre casier avec contact et PIN.',
                'de': 'Greifen Sie auf Ihr Schließfach mit Kontakt und PIN zu.',
                'it': 'Accedi al tuo armadietto con contatto e PIN.',
                'pl': 'Uzyskaj dostęp do szafki za pomocą kontaktu i PIN-u.'
            },
            'how_it_works_title': {
                'pt': 'Como funciona',
                'en': 'How it works',
                'es': 'Cómo funciona',
                'fr': 'Comment ça marche',
                'de': 'Wie es funktioniert',
                'it': 'Come funziona',
                'pl': 'Jak to działa'
            },
            'how_it_works_desc': {
                'pt': 'Aprenda a usar os nossos cacifos.',
                'en': 'Learn how to use our lockers.',
                'es': 'Aprenda a usar nuestros casilleros.',
                'fr': 'Apprenez à utiliser nos casiers.',
                'de': 'Erfahren Sie, wie Sie unsere Schließfächer nutzen.',
                'it': 'Impara a usare i nostri armadietti.',
                'pl': 'Dowiedz się, jak korzystać z naszych szafek.'
            },
            'pricing_title': {
                'pt': 'Preços',
                'en': 'Pricing',
                'es': 'Precios',
                'fr': 'Tarifs',
                'de': 'Preise',
                'it': 'Prezzi',
                'pl': 'Cennik'
            },
            'pricing_desc': {
                'pt': 'Consulte as nossas tarifas e planos.',
                'en': 'View our rates and plans.',
                'es': 'Consulte nuestras tarifas y planes.',
                'fr': 'Consultez nos tarifs et forfaits.',
                'de': 'Sehen Sie unsere Tarife und Pläne.',
                'it': 'Visualizza le nostre tariffe e piani.',
                'pl': 'Zobacz nasze stawki i plany.'
            },
            'pricing_subtitle': {
                'pt': 'POUPE DINHEIRO: PAGUE POR CACIFO, NÃO POR MALA!',
                'en': 'SAVE MONEY: PAY PER LOCKER, NOT PER BAG!',
                'es': '¡AHORRE DINERO: PAGUE POR CASILLERO, NO POR BOLSA!',
                'fr': 'ÉCONOMISEZ: PAYEZ PAR CASIER, PAS PAR SAC!',
                'de': 'GELD SPAREN: ZAHLEN SIE PRO SCHLIEFACH, NICHT PRO TASCHE!',
                'it': 'RISPARMIA: PAGA PER ARMADIETTO, NON PER BORSA!',
                'pl': 'OSZCZĘDZAJ: PŁAĆ ZA SZAFKĘ, NIE ZA TORBĘ!'
            },
            
            # === HOW IT WORKS ===
            'how_it_works_subtitle': {
                'pt': 'Siga estes passos simples para usar o nosso sistema:',
                'en': 'Follow these simple steps to use our system:',
                'es': 'Siga estos pasos simples para usar nuestro sistema:',
                'fr': 'Suivez ces étapes simples pour utiliser notre système:',
                'de': 'Befolgen Sie diese einfachen Schritte, um unser System zu nutzen:',
                'it': 'Segui questi semplici passaggi per utilizzare il nostro sistema:',
                'pl': 'Wykonaj te proste kroki, aby korzystać z naszego systemu:'
            },
            'step1_title': {
                'pt': 'Reserve o seu cacifo',
                'en': 'Book your locker',
                'es': 'Reserve su casillero',
                'fr': 'Réservez votre casier',
                'de': 'Buchen Sie Ihr Schließfach',
                'it': 'Prenota il tuo armadietto',
                'pl': 'Zarezerwuj swoją szafkę'
            },
            'step1_description': {
                'pt': 'No local: Use o ecrã táctil no local de armazenamento para fazer a sua reserva.\nPague: Complete o pagamento com cartão de crédito.',
                'en': 'On-site: Use the touchscreen at the storage location to make your booking.\nPay: Complete the payment with a credit card.',
                'es': 'En el sitio: Use la pantalla táctil en la ubicación de almacenamiento para hacer su reserva.\nPague: Complete el pago con tarjeta de crédito.',
                'fr': 'Sur place: Utilisez l\'écran tactile à l\'emplacement de stockage pour faire votre réservation.\nPayez: Complétez le paiement avec une carte de crédit.',
                'de': 'Vor Ort: Verwenden Sie den Touchscreen am Lagerort, um Ihre Buchung vorzunehmen.\nBezahlen: Schließen Sie die Zahlung mit einer Kreditkarte ab.',
                'it': 'In loco: Usa il touchscreen nella posizione di stoccaggio per effettuare la prenotazione.\nPaga: Completa il pagamento con una carta di credito.',
                'pl': 'Na miejscu: Użyj ekranu dotykowego w lokalizacji przechowywania, aby dokonać rezerwacji.\nZapłać: Dokończ płatność kartą kredytową.'
            },
            'step2_title': {
                'pt': 'Deposite a sua bagagem',
                'en': 'Deposit your baggage',
                'es': 'Deposite su equipaje',
                'fr': 'Déposez vos bagages',
                'de': 'Hinterlegen Sie Ihr Gepäck',
                'it': 'Deposita i tuoi bagagli',
                'pl': 'Złóż swój bagaż'
            },
            'step2_description': {
                'pt': 'O sistema atribuir-lhe-á um cacifo e abrirá para si.\nColoque as suas malas dentro do cacifo e feche a porta.',
                'en': 'The system will assign you a locker and open it for you.\nPlace your bags inside the locker and close the door.',
                'es': 'El sistema le asignará un casillero y lo abrirá para usted.\nColoque sus bolsas dentro del casillero y cierre la puerta.',
                'fr': 'Le système vous attribuera un casier et l\'ouvrira pour vous.\nPlacez vos sacs dans le casier et fermez la porte.',
                'de': 'Das System weist Ihnen ein Schließfach zu und öffnet es für Sie.\nLegen Sie Ihre Taschen in das Schließfach und schließen Sie die Tür.',
                'it': 'Il sistema ti assegnerà un armadietto e lo aprirà per te.\nMetti le tue borse all\'interno dell\'armadietto e chiudi la porta.',
                'pl': 'System przydzieli Ci szafkę i otworzy ją dla Ciebie.\nWłóż swoje torby do szafki i zamknij drzwi.'
            },
            'step3_title': {
                'pt': 'Reabra e retire a sua bagagem',
                'en': 'Reopen and retrieve your baggage',
                'es': 'Reabra y retire su equipaje',
                'fr': 'Rouvrez et récupérez vos bagages',
                'de': 'Öffnen Sie erneut und holen Sie Ihr Gepäck ab',
                'it': 'Riapri e ritira i tuoi bagagli',
                'pl': 'Otwórz ponownie i odbierz swój bagaż'
            },
            'step3_description': {
                'pt': 'Para recolher as suas malas, use o seu smartphone ou o ecrã táctil no local e insira o seu código do cacifo.',
                'en': 'To collect your bags, use your smartphone or the touchscreen at the location and enter your locker code.',
                'es': 'Para recoger sus bolsas, use su smartphone o la pantalla táctil en la ubicación e ingrese su código de casillero.',
                'fr': 'Pour récupérer vos sacs, utilisez votre smartphone ou l\'écran tactile à l\'emplacement et entrez votre code de casier.',
                'de': 'Um Ihre Taschen abzuholen, verwenden Sie Ihr Smartphone oder den Touchscreen am Standort und geben Sie Ihren Schließfachcode ein.',
                'it': 'Per ritirare le tue borse, usa il tuo smartphone o il touchscreen nella posizione e inserisci il codice del tuo armadietto.',
                'pl': 'Aby odebrać swoje torby, użyj swojego smartfona lub ekranu dotykowego w lokalizacji i wprowadź kod swojej szafki.'
            },
            
            # === LANGUAGE SELECTION ===
            'select_language': {
                'pt': 'Selecionar Idioma:',
                'en': 'Select Language:',
                'es': 'Seleccionar Idioma:',
                'fr': 'Sélectionner la Langue:',
                'de': 'Sprache Wählen:',
                'it': 'Seleziona Lingua:',
                'pl': 'Wybierz Język:'
            },
            
            # === FIND LOCKERS SCREEN ===
            'find_lockers_button': {
                'pt': 'Encontrar Cacifos',
                'en': 'Find Lockers',
                'es': 'Encontrar Casilleros',
                'fr': 'Trouver Casiers',
                'de': 'Schließfächer Finden',
                'it': 'Trova Armadietti',
                'pl': 'Znajdź Szafki'
            },
            'find_lockers_instructions': {
                'pt': 'Cacifos verdes estão disponíveis para reserva. Amarelo significa porta aberta. Vermelho significa ocupado. Toque num cacifo verde para reservá-lo.',
                'en': 'Green lockers are available for booking. Yellow means door open. Red means occupied. Touch a green locker to book it.',
                'es': 'Los casilleros verdes están disponibles para reservar. Amarillo significa puerta abierta. Rojo significa ocupado. Toca un casillero verde para reservarlo.',
                'fr': 'Les casiers verts sont disponibles pour réservation. Jaune signifie porte ouverte. Rouge signifie occupé. Touchez un casier vert pour le réserver.',
                'de': 'Grüne Schließfächer sind für die Buchung verfügbar. Gelb bedeutet Tür offen. Rot bedeutet besetzt. Berühren Sie ein grünes Schließfach, um es zu buchen.',
                'it': 'Gli armadietti verdi sono disponibili per la prenotazione. Giallo significa porta aperta. Rosso significa occupato. Tocca un armadietto verde per prenotarlo.',
                'pl': 'Zielone szafki są dostępne do rezerwacji. Żółty oznacza otwarte drzwi. Czerwony oznacza zajęte. Dotknij zielonej szafki, aby ją zarezerwować.'
            },
            'available_lockers_title': {
                'pt': 'Cacifos Disponíveis',
                'en': 'Available Lockers',
                'es': 'Casilleros Disponibles',
                'fr': 'Casiers Disponibles',
                'de': 'Verfügbare Schließfächer',
                'it': 'Armadietti Disponibili',
                'pl': 'Dostępne Szafki'
            },
            'status_available': {
                'pt': 'Disponível',
                'en': 'Available',
                'es': 'Disponible',
                'fr': 'Disponible',
                'de': 'Verfügbar',
                'it': 'Disponibile',
                'pl': 'Dostępna'
            },
            'status_occupied': {
                'pt': 'Ocupado',
                'en': 'Occupied',
                'es': 'Ocupado',
                'fr': 'Occupé',
                'de': 'Besetzt',
                'it': 'Occupato',
                'pl': 'Zajęta'
            },
            'status_door_open': {
                'pt': 'Porta Aberta',
                'en': 'Door Open',
                'es': 'Puerta Abierta',
                'fr': 'Porte Ouverte',
                'de': 'Tür Offen',
                'it': 'Porta Aperta',
                'pl': 'Drzwi Otwarte'
            },
            'back_to_home': {
                'pt': 'Voltar ao Início',
                'en': 'Back to Home',
                'es': 'Volver al Inicio',
                'fr': 'Retour à l\'Accueil',
                'de': 'Zurück zum Start',
                'it': 'Torna alla Home',
                'pl': 'Powrót do Strony Głównej'
            },
            
            # === BOOKING SCREEN ===
            'book_locker_title': {
                'pt': 'Reserve o Seu Cacifo',
                'en': 'Book Your Locker',
                'es': 'Reserve su Casillero',
                'fr': 'Réservez votre Casier',
                'de': 'Ihr Schließfach Buchen',
                'it': 'Prenota il Tuo Armadietto',
                'pl': 'Zarezerwuj Swoją Szafkę'
            },
            'contact_label': {
                'pt': 'Informações de Contacto',
                'en': 'Contact Information',
                'es': 'Información de Contacto',
                'fr': 'Informations de Contact',
                'de': 'Kontaktinformationen',
                'it': 'Informazioni di Contatto',
                'pl': 'Informacje Kontaktowe'
            },
            'contact_instruction': {
                'pt': 'Introduza os seus dados de contacto para continuar. Será gerado um PIN para o seu cacifo.',
                'en': 'Enter your contact details to continue. A PIN will be generated for your locker.',
                'es': 'Introduzca sus datos de contacto para continuar. Se generará un PIN para su casillero.',
                'fr': 'Entrez vos coordonnées pour continuer. Un PIN sera généré pour votre casier.',
                'de': 'Geben Sie Ihre Kontaktdaten ein, um fortzufahren. Eine PIN wird für Ihr Schließfach generiert.',
                'it': 'Inserisci i tuoi dettagli di contatto per continuare. Verrà generato un PIN per il tuo armadietto.',
                'pl': 'Wprowadź swoje dane kontaktowe, aby kontynuować. PIN zostanie wygenerowany dla Twojej szafki.'
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
                'it': 'esempio@email.com o +39 123 456 789',
                'pl': 'przyklad@email.com lub +48 123 456 789'
            },
            'contact_placeholder': {
                'pt': 'exemplo@email.com ou +351 123 456 789',
                'en': 'example@email.com or +351 123 456 789',
                'es': 'ejemplo@email.com o +34 123 456 789',
                'fr': 'exemple@email.com ou +33 123 456 789',
                'de': 'beispiel@email.com oder +49 123 456 789',
                'it': 'esempio@email.com o +39 123 456 789',
                'pl': 'przyklad@email.com lub +48 123 456 789'
            },
            'back_button': {
                'pt': 'Voltar',
                'en': 'Back',
                'es': 'Atrás',
                'fr': 'Retour',
                'de': 'Zurück',
                'it': 'Indietro',
                'pl': 'Wstecz'
            },
            'confirm_booking': {
                'pt': 'Confirmar Reserva',
                'en': 'Confirm Booking',
                'es': 'Confirmar Reserva',
                'fr': 'Confirmer la Réservation',
                'de': 'Buchung Bestätigen',
                'it': 'Conferma Prenotazione',
                'pl': 'Potwierdź Rezerwację'
            },
            'booking_success': {
                'pt': 'Reserva realizada com sucesso!',
                'en': 'Booking completed successfully!',
                'es': '¡Reserva realizada con éxito!',
                'fr': 'Réservation effectuée avec succès!',
                'de': 'Buchung erfolgreich abgeschlossen!',
                'it': 'Prenotazione completata con successo!',
                'pl': 'Rezerwacja zakończona sukcesem!'
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
                'it': 'Errore',
                'pl': 'Błąd'
            },
            'ok': {
                'pt': 'OK',
                'en': 'OK',
                'es': 'OK',
                'fr': 'OK',
                'de': 'OK',
                'it': 'OK',
                'pl': 'OK'
            },
            
            # === ADDITIONAL BOOKING FIELDS ===
            'name_label': {
                'pt': 'Nome:',
                'en': 'Name:',
                'es': 'Nombre:',
                'fr': 'Nom:',
                'de': 'Name:',
                'it': 'Nome:',
                'pl': 'Imię:'
            },
            'name_placeholder': {
                'pt': 'Digite o seu nome completo',
                'en': 'Enter your full name',
                'es': 'Ingrese su nombre completo',
                'fr': 'Entrez votre nom complet',
                'de': 'Geben Sie Ihren vollständigen Namen ein',
                'it': 'Inserisci il tuo nome completo',
                'pl': 'Wprowadź swoje pełne imię'
            },
            'email_label': {
                'pt': 'Email:',
                'en': 'Email:',
                'es': 'Correo:',
                'fr': 'Email:',
                'de': 'E-Mail:',
                'it': 'Email:',
                'pl': 'Email:'
            },
            'email_placeholder': {
                'pt': 'exemplo@email.com',
                'en': 'example@email.com',
                'es': 'ejemplo@email.com',
                'fr': 'exemple@email.com',
                'de': 'beispiel@email.com',
                'it': 'esempio@email.com',
                'pl': 'przyklad@email.com'
            },
            'phone_label': {
                'pt': 'Número de Telemóvel:',
                'en': 'Phone Number:',
                'es': 'Número de Teléfono:',
                'fr': 'Numéro de Téléphone:',
                'de': 'Telefonnummer:',
                'it': 'Numero di Telefono:',
                'pl': 'Numer Telefonu:'
            },
            'phone_placeholder': {
                'pt': '123 456 789',
                'en': '123 456 789',
                'es': '123 456 789',
                'fr': '123 456 789',
                'de': '123 456 789',
                'it': '123 456 789',
                'pl': '123 456 789'
            },
            'birth_date_label': {
                'pt': 'Data de Nascimento:',
                'en': 'Date of Birth:',
                'es': 'Fecha de Nacimiento:',
                'fr': 'Date de Naissance:',
                'de': 'Geburtsdatum:',
                'it': 'Data di Nascita:',
                'pl': 'Data Urodzenia:'
            },
            'day_placeholder': {
                'pt': 'Dia',
                'en': 'Day',
                'es': 'Día',
                'fr': 'Jour',
                'de': 'Tag',
                'it': 'Giorno',
                'pl': 'Dzień'
            },
            'month_placeholder': {
                'pt': 'Mês',
                'en': 'Month',
                'es': 'Mes',
                'fr': 'Mois',
                'de': 'Monat',
                'it': 'Mese',
                'pl': 'Miesiąc'
            },
            'year_placeholder': {
                'pt': 'Ano',
                'en': 'Year',
                'es': 'Año',
                'fr': 'Année',
                'de': 'Jahr',
                'it': 'Anno',
                'pl': 'Rok'
            },
            'fill_all_fields': {
                'pt': 'Preencha todos os campos para continuar. Será gerado um PIN para o seu cacifo.',
                'en': 'Fill all fields to continue. A PIN will be generated for your locker.',
                'es': 'Complete todos los campos para continuar. Se generará un PIN para su casillero.',
                'fr': 'Remplissez tous les champs pour continuer. Un PIN sera généré pour votre casier.',
                'de': 'Füllen Sie alle Felder aus, um fortzufahren. Eine PIN wird für Ihr Schließfach generiert.',
                'it': 'Compila tutti i campi per continuare. Verrà generato un PIN per il tuo armadietto.',
                'pl': 'Wypełnij wszystkie pola, aby kontynuować. PIN zostanie wygenerowany dla Twojej szafki.'
            },
            'invalid_name': {
                'pt': 'Por favor, introduza um nome válido',
                'en': 'Please enter a valid name',
                'es': 'Por favor, introduzca un nombre válido',
                'fr': 'Veuillez saisir un nom valide',
                'de': 'Bitte geben Sie einen gültigen Namen ein',
                'it': 'Inserisci un nome valido',
                'pl': 'Wprowadź prawidłowe imię'
            },
            'invalid_email': {
                'pt': 'Por favor, introduza um email válido',
                'en': 'Please enter a valid email',
                'es': 'Por favor, introduzca un email válido',
                'fr': 'Veuillez saisir un email valide',
                'de': 'Bitte geben Sie eine gültige E-Mail ein',
                'it': 'Inserisci un email valido',
                'pl': 'Wprowadź prawidłowy email'
            },
            'invalid_phone': {
                'pt': 'Por favor, introduza um número de telefone válido',
                'en': 'Please enter a valid phone number',
                'es': 'Por favor, introduzca un número de teléfono válido',
                'fr': 'Veuillez saisir un numéro de téléphone valide',
                'de': 'Bitte geben Sie eine gültige Telefonnummer ein',
                'it': 'Inserisci un numero di telefono valido',
                'pl': 'Wprowadź prawidłowy numer telefonu'
            },
            'invalid_birth_date': {
                'pt': 'Por favor, selecione uma data de nascimento válida',
                'en': 'Please select a valid birth date',
                'es': 'Por favor, seleccione una fecha de nacimiento válida',
                'fr': 'Veuillez sélectionner une date de naissance valide',
                'de': 'Bitte wählen Sie ein gültiges Geburtsdatum',
                'it': 'Seleziona una data di nascita valida',
                'pl': 'Wybierz prawidłową datę urodzenia'
            },
            
            # === UNLOCK SCREEN ===
            'unlock_lockers_title': {
                'pt': 'Desbloquear Cacifos',
                'en': 'Unlock Lockers',
                'es': 'Desbloquear Casilleros',
                'fr': 'Déverrouiller Casiers',
                'de': 'Schließfächer Öffnen',
                'it': 'Sblocca Armadietti',
                'pl': 'Odblokuj Szafki'
            },
            'contact_pin_title': {
                'pt': 'Contacto e PIN',
                'en': 'Contact and PIN',
                'es': 'Contacto y PIN',
                'fr': 'Contact et PIN',
                'de': 'Kontakt und PIN',
                'it': 'Contatto e PIN',
                'pl': 'Kontakt i PIN'
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
                'it': 'PIN:',
                'pl': 'PIN:'
            },
            'pin_hint': {
                'pt': 'Introduza o seu PIN',
                'en': 'Enter your PIN',
                'es': 'Introduzca su PIN',
                'fr': 'Entrez votre PIN',
                'de': 'Geben Sie Ihre PIN ein',
                'it': 'Inserisci il tuo PIN',
                'pl': 'Wprowadź swój PIN'
            },
            'unlock_button': {
                'pt': 'Desbloquear',
                'en': 'Unlock',
                'es': 'Desbloquear',
                'fr': 'Déverrouiller',
                'de': 'Öffnen',
                'it': 'Sblocca',
                'pl': 'Odblokuj'
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
                'it': 'Armadietto sbloccato con successo!',
                'pl': 'Szafka została pomyślnie odblokowana!'
            },
            'thank_you_message': {
                'pt': 'Obrigado pela sua escolha!',
                'en': 'Thank you for your choice!',
                'es': '¡Gracias por tu elección!',
                'fr': 'Merci pour votre choix!',
                'de': 'Vielen Dank für Ihre Wahl!',
                'it': 'Grazie per la tua scelta!',
                'pl': 'Dziękujemy za wybór!'
            },
            'come_back_soon': {
                'pt': 'Volte sempre!',
                'en': 'Come back soon!',
                'es': '¡Vuelve pronto!',
                'fr': 'Revenez bientôt!',
                'de': 'Kommen Sie bald wieder!',
                'it': 'Torna presto!',
                'pl': 'Wróć wkrótce!'
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
            'it': {'name': 'Italiano', 'flag': '🇮🇹', 'code': 'IT'},
            'pl': {'name': 'Polski', 'flag': '🇵🇱', 'code': 'PL'}
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