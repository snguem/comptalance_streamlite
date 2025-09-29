
from datetime import datetime
import os
import streamlit as st
from config import Config

# global variable

# Initialisation de l'application
if 'config' not in st.session_state:
    st.session_state.config = Config()
    
config = st.session_state.config
    
if 'current_model_index' not in st.session_state:
    st.session_state.current_model_index = 0

if config.load_excel(st, os.path.join(config.default_excel_folder, config.modeles[0]["file_path"])):
    config.model_choisi()

# Configuration de la page
st.set_page_config(
    page_title="Logiciel d'integration de balances comptable",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin: 1rem 0;
        border-bottom: 2px solid #ff7f0e;
        padding-bottom: 0.5rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


st.markdown('<h1 class="main-header">📊 Comptalance, le logiciel qui facilite l\'integration de vos balance N et N-1</h1>', unsafe_allow_html=True)

# fonctions

# =====================

# Sidebar pour la navigation
with st.sidebar:
    st.markdown("### Navigation")
    page = st.selectbox(
        "Choisir une section:",
        ["🏠 Accueil", "📁 Choisir un model", "📤 Importer les balances"]
    )
    
    st.markdown("---")
    st.markdown("### Informations")
    st.info("Logiciel développé pour l'integration rapide des balances N et N-1")


if page == "🏠 Accueil":
    st.markdown('<div class="section-header">Bienvenue</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 💡 Attention
        
        - Les balances **ne doivent pas** etre dans le meme fichier excel
        - Il ne doit avoir qu'une page(balance N ou N-1) dans le fichier que vous importer
        - Vous devez avoir 2 fichiers excel : celui de la balance N et N-1
        """)
    
    with col2:
        st.markdown("""
        ### 📋 Guide d'utilisation
        
        1. Aller a la section **choisir un modele** en haut a gauche
        2. Choisissez le modele que vous souhaitez
        3. Aller a la section **Importer les Balances** en haut a gauche
        4. **Ajoutez** vos balances (2 fichiers excels)
        5. Revenez a l'acceuil et scroller jusqu'a apercevoir l'etat des fichiers
        6. **Lancer l'integration** et **Exporter le resultat au format excel**
        """)
    
    # Statut des fichiers
    st.markdown('<div class="section-header">État des fichiers</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        modele_status = "✅ Chargé" if config.model_balances_["modele"] else "❌ Non choisi"
        st.metric("Modèle Excel", modele_status)
    
    with col2:
        balance_n_status = "✅ Chargée" if config.model_balances_["baln"] else "❌ Non chargée"
        st.metric("Balance N", balance_n_status)
    
    with col3:
        balance_n1_status = "✅ Chargée" if config.model_balances_["baln_1"] else "❌ Non chargée"
        st.metric("Balance N-1", balance_n1_status)


    if config.model_balances_["modele"] and config.model_balances_["baln"] and config.model_balances_["baln_1"]:
        st.markdown('<div class="section-header">Integration</div>', unsafe_allow_html=True)
        # Bouton pour intégrer les balances
        
        if st.button("🔄 Intégrer les balances au modèle", type="primary"):
            with st.spinner("Traitement en cours..."):
                if config.add_balances_to_modele(st):
                    config.isIntegrated = True
                    config.get_excel_file_download(st)
                    st.info("Les feuilles 'Balance_N' et 'Balance_N-1' ont été ajoutées au modèle")
                else:
                    st.markdown('<div class="warning-box">❌ Erreur lors de l\'intégration des balances</div>', unsafe_allow_html=True)
            # st.success("Terminé!")

    if config.isIntegrated:
        st.markdown('<div class="section-header">Exportation</div>', unsafe_allow_html=True)
        # Bouton pour intégrer les balances
        st.download_button(
            label="📥 Télécharger Excel",
            data=config.excel_data,
            file_name=f"comptabilite_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )
        
        
elif page == "📁 Choisir un model":
    # Interface principale
    st.header("📋 Liste des Modèles Disponibles")
    
    # Création de deux colonnes
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Modeles disponible")
        
        # Liste des modèles avec sélection
        model_names = [model['nom'] for model in config.modeles]
        
        if 'current_model_index' not in st.session_state:
            st.session_state.current_model_index = 0
        
        
        model_choisi = st.radio(
            "djf",
            model_names,
            index=0,
            label_visibility="hidden"
        )
        
        index = config.get_index_model(model_choisi)
        if index!=st.session_state.current_model_index:
            st.session_state.current_model_index = index
            if config.load_excel(st, os.path.join(config.default_excel_folder, config.modeles[index]["file_path"])):
                config.model_choisi()
        
    with col2:
        if config.modeles:
            selected_model = config.modeles[st.session_state.current_model_index]
            
            st.subheader(f"🖼️ Aparcu du {selected_model['nom']}")
            
            # Affichage des images
            if 'imgs' in selected_model and selected_model['imgs']:
                # st.markdown()
                
                # Options d'affichage des images
                show_images = st.checkbox("Afficher les images", value=False)
                
                if show_images:
                    for i, image_name in enumerate(selected_model['imgs']):
                        image_path = os.path.join(config.default_img_path, image_name)
                        
                        st.markdown(f"**Image {i+1}:** {image_name}")
                        
                        config.display_image(st, image_path)
                        st.markdown("---")
            else:
                st.info("Aucune image disponible pour ce modèle")
    
    st.markdown("---")
    

elif page == "📤 Importer les balances":
    config.model_balances_["baln"] = False
    config.model_balances_["baln_1"] = False
    st.markdown('<div class="section-header">Import des balances</div>', unsafe_allow_html=True)
    
    # Upload des balances
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Balance Année N")
        balance_n_file = st.file_uploader(
            "Fichier balance année courante (N):",
            type=['xlsx'],
            key="balance_n_uploader"
        )
        
        if balance_n_file:
            if config.load_excel(st, balance_n_file, 2):
                config.model_balances_["baln"] = True
                st.success("✅ Balance N chargée!")
    
    with col2:
        st.markdown("#### 📊 Balance Année N-1")
        balance_n1_file = st.file_uploader(
            "Fichier balance année précédente (N-1):",
            type=['xlsx'],
            key="balance_n1_uploader"
        )
        
        if balance_n1_file:
            if config.load_excel(st, balance_n1_file, 3):
                config.model_balances_["baln_1"] = True
                st.success("✅ Balance N-1 chargée!")
    
    st.markdown("---")
    

if __name__=="__main__":
    pass