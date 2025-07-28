import os
import requests
from nicegui import ui
from dotenv import load_dotenv

# Charge les variables d'environnement à partir d'un fichier .env pour le développement local
load_dotenv() 

# --- CONFIGURATION API ---
# Récupère les identifiants depuis les variables d'environnement
CLIENT_ID = os.environ.get("FT_CLIENT_ID")
CLIENT_SECRET = os.environ.get("FT_CLIENT_SECRET")
API_TOKEN = None

# --- LOGIQUE API ---
def get_access_token():
    """Récupère un token d'accès auprès de l'API France Travail."""
    global API_TOKEN
    if not CLIENT_ID or not CLIENT_SECRET:
        print("ERREUR : Variables d'environnement FT_CLIENT_ID et FT_CLIENT_SECRET non définies.")
        return False
    
    auth_url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'client_credentials', 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'scope': 'api_offresdemploiv2 o2dsoffre'}
    
    try:
        response = requests.post(auth_url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        API_TOKEN = response.json()['access_token']
        print("Token obtenu avec succès au démarrage.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Échec critique de l'obtention du token au démarrage : {e}")
        API_TOKEN = None
        return False

# --- DÉFINITION DE LA PAGE ET DE L'INTERFACE UTILISATEUR ---
@ui.page('/')
def main_page():
    with ui.row().classes('w-full justify-center'):
        ui.label('Data Collector').classes('text-3xl font-bold my-4')

    # Zone pour les filtres de recherche
    with ui.row().classes('w-full items-end gap-4 justify-center'):
        input_metier = ui.input(label='Métier recherché', placeholder='Ex: Développeur web').classes('w-60')
        input_departement = ui.input(label='Département', placeholder='Ex: 75').classes('w-28')
        select_contrat = ui.select(
            options={'CDI': 'CDI', 'CDD': 'CDD', 'MIS': 'Intérim'}, 
            label='Type de contrat', 
            value='CDI'
        ).classes('w-40')
        select_limit = ui.select(options={10: '10', 20: '20', 30: '30'}, label='Résultats', value=10).classes('w-24')
        ui.button('Rechercher', on_click=lambda: search_jobs())

    results_area = ui.column().classes('w-full max-w-4xl mx-auto gap-10 mt-6')

    # --- FONCTION DE RECHERCHE ---
    async def search_jobs():
        """Fonction appelée par le bouton pour interroger l'API et afficher les résultats."""
        if not input_metier.value:
            ui.notification("Veuillez entrer un métier ou un code ROME.", color='warning')
            return

        results_area.clear()
        with results_area:
            ui.spinner(size='lg', color='primary').classes('self-center')

        if not API_TOKEN:
            if not get_access_token():
                results_area.clear()
                ui.notification("Erreur d'authentification avec l'API.", color='negative')
                return

        api_url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
        headers = {'Authorization': f'Bearer {API_TOKEN}'}
        params = {
            'typeContrat': select_contrat.value,
            'range': f'0-{select_limit.value - 1}'
        }
        
        if input_metier.value:
            params['motsCles'] = input_metier.value
        if input_departement.value:
            params['departement'] = input_departement.value

        try:
            response = requests.get(api_url, headers=headers, params=params, timeout=20)
            
            # Gestion du token expiré (code 401)
            if response.status_code == 401:
                print("Token expiré, tentative de renouvellement automatique...")
                get_access_token()
                headers['Authorization'] = f'Bearer {API_TOKEN}'
                response = requests.get(api_url, headers=headers, params=params, timeout=20)
            
            response.raise_for_status()
            
            results_area.clear()
            # Gestion du cas "aucune offre trouvée" (code 204)
            if response.status_code == 204:
                with results_area:
                    ui.label("Aucune offre trouvée pour cette recherche.").classes('text-center text-gray-500')
                return

            offres = response.json().get('resultats', [])
            with results_area:
                ui.label(f"{len(offres)} offres trouvées.").classes('text-center font-semibold mb-2')
                for offre in offres:
                    with ui.card().classes('w-full hover:shadow-lg transition'):
                        ui.label(offre.get('intitule')).classes('font-bold text-lg')
                        if offre.get('entreprise') and offre.get('entreprise').get('nom'):
                            ui.label(f"Entreprise : {offre.get('entreprise').get('nom')}")
                        if offre.get('lieuTravail'):
                            ui.label(f"Lieu : {offre.get('lieuTravail').get('libelle')}")
                        
                        ui.chip(offre.get('typeContratLibelle', 'N/A'), color='blue-600', text_color='white')
                        
                        if offre.get('origineOffre', {}).get('urlOrigine'):
                             ui.link('Voir l\'offre originale', offre.get('origineOffre').get('urlOrigine'), new_tab=True).classes('mt-2')
        except requests.exceptions.RequestException as e:
            results_area.clear()
            ui.notification(f"Erreur lors de la communication avec l'API : {e}", color='negative')
            if e.response is not None:
                 print(f"--- ERREUR API : {e.response.text} ---")

# --- DÉMARRAGE DE L'APPLICATION ---
get_access_token()
port = int(os.environ.get('PORT', 8080))
ui.run(host='0.0.0.0', port=port, title="Data Collector")