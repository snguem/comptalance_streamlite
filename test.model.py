import streamlit as st
import json
import os
from pathlib import Path
import pandas as pd
from PIL import Image

# Configuration de la page
st.set_page_config(
    page_title="Gestionnaire de Modèles Excel",
    page_icon="📊",
    layout="wide"
)

def load_models_config(json_path):
    """Charge la configuration des modèles depuis le fichier JSON"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Fichier JSON non trouvé: {json_path}")
        return {}
    except json.JSONDecodeError:
        st.error("Erreur dans le format du fichier JSON")
        return {}

def check_file_exists(file_path):
    """Vérifie si un fichier existe"""
    return os.path.exists(file_path)

def display_image(image_path):
    """Affiche une image avec gestion d'erreur"""
    try:
        if check_file_exists(image_path):
            image = Image.open(image_path)
            st.image(image, use_container_width=True)
            return True
        else:
            st.warning(f"Image non trouvée: {image_path}")
            return False
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'image: {str(e)}")
        return False

def main():
    st.title("📊 Gestionnaire de Modèles Excel")
    st.markdown("---")
    
    # Chemins par défaut
    default_images_folder = "models_images"
    default_json_file = "models.json"
    
    # Chargement de la configuration
    config = load_models_config(default_json_file)
    
    if not config :
        st.error("Configuration invalide ou vide")
        return
    
    modeles = config
    
    if not modeles:
        st.warning("Aucun modèle trouvé dans la configuration")
        return
    
    # Interface principale
    st.header("📋 Liste des Modèles Disponibles")
    
    # Création de deux colonnes
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Modèles")
        
        # Liste des modèles avec sélection
        model_names = [model['nom'] for model in modeles]
        
        if 'selected_model_index' not in st.session_state:
            st.session_state.selected_model_index = 0
        
        # Affichage de la liste des modèles
        for i, model in enumerate(modeles):
            excel_path = os.path.join("models_excel", model['file_path'])
            excel_exists = check_file_exists(excel_path)
            
            # Indicateur de statut
            status_icon = "✅" if excel_exists else "❌"
            
            # Bouton pour sélectionner le modèle
            if st.button(f"{status_icon} {model['nom']}", key=f"model_{i}"):
                st.session_state.selected_model_index = i
            
            # Affichage de la description si disponible
            if 'description' in model and model['description']:
                st.caption(model['description'])
            
            st.markdown("---")
    
    with col2:
        if modeles:
            selected_model = modeles[st.session_state.selected_model_index]
            
            st.subheader(f"📊 {selected_model['nom']}")
            
            
            st.write(f"**Fichier Excel:** {selected_model['file_path']}")
            
            # Affichage des images
            if 'imgs' in selected_model and selected_model['imgs']:
                st.markdown("### 🖼️ Images du modèle")
                
                # Options d'affichage des images
                show_images = st.checkbox("Afficher les images", value=False)
                
                if show_images:
                    for i, image_name in enumerate(selected_model['imgs']):
                        image_path = os.path.join(default_images_folder, image_name)
                        
                        st.markdown(f"**Image {i+1}:** {image_name}")
                        
                        if display_image(image_path):
                            # Bouton de téléchargement de l'image
                            try:
                                with open(image_path, 'rb') as f:
                                    st.download_button(
                                        label=f"📥 Télécharger {image_name}",
                                        data=f.read(),
                                        file_name=image_name,
                                        key=f"download_img_{i}"
                                    )
                            except:
                                pass
                        
                        st.markdown("---")
            else:
                st.info("Aucune image disponible pour ce modèle")
    
    # Footer avec informations
    st.markdown("---")

if __name__ == "__main__":
    main()