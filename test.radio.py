import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Checkboxes et Radios Streamlit",
    page_icon="☑️",
    layout="wide"
)

st.title("☑️ Checkboxes et Boutons Radio avec Streamlit")
st.markdown("---")

# ========================================
# SECTION 1: CHECKBOXES SIMPLES
# ========================================
st.header("1️⃣ Checkboxes Simples")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Checkboxes basiques")
    
    # Checkbox simple
    agree = st.checkbox("J'accepte les conditions d'utilisation")
    
    # Checkbox avec valeur par défaut
    notifications = st.checkbox("Recevoir des notifications", value=True)
    
    # Checkbox avec clé personnalisée
    newsletter = st.checkbox("S'abonner à la newsletter", key="newsletter_checkbox")
    
    # Checkbox avec aide
    analytics = st.checkbox(
        "Activer l'analytics", 
        help="Permet de collecter des statistiques d'usage"
    )
    
    # Affichage des résultats
    if agree:
        st.success("✅ Conditions acceptées")
    if notifications:
        st.info("🔔 Notifications activées")
    if newsletter:
        st.info("📧 Newsletter activée")
    if analytics:
        st.info("📊 Analytics activé")

with col2:
    st.subheader("Checkboxes multiples")
    
    # Groupe de checkboxes liées
    st.write("**Fonctionnalités à activer:**")
    
    features = {}
    features['export_pdf'] = st.checkbox("Export PDF")
    features['export_excel'] = st.checkbox("Export Excel")
    features['auto_save'] = st.checkbox("Sauvegarde automatique")
    features['backup'] = st.checkbox("Sauvegarde cloud")
    features['sharing'] = st.checkbox("Partage en équipe")
    
    # Compte des fonctionnalités activées
    active_features = sum(features.values())
    st.metric("Fonctionnalités activées", active_features)
    
    # Liste des fonctionnalités activées
    if active_features > 0:
        st.write("**Fonctionnalités sélectionnées:**")
        for feature, is_active in features.items():
            if is_active:
                st.write(f"• {feature.replace('_', ' ').title()}")

st.markdown("---")

# ========================================
# SECTION 2: BOUTONS RADIO SIMPLES
# ========================================
st.header("2️⃣ Boutons Radio Simples")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Radio basique")
    
    # Radio simple
    genre = st.radio(
        "Quel est votre genre préféré ?",
        ("Comédie", "Drame", "Action", "Science-fiction")
    )
    st.write(f"Vous avez choisi: **{genre}**")
    
    # Radio horizontal
    difficulty = st.radio(
        "Niveau de difficulté:",
        ("Facile", "Moyen", "Difficile"),
        horizontal=True
    )
    
    # Affichage conditionnel basé sur la sélection
    if difficulty == "Facile":
        st.success("🟢 Bon choix pour débuter!")
    elif difficulty == "Moyen":
        st.warning("🟡 Un bon équilibre!")
    else:
        st.error("🔴 Pour les experts!")

with col2:
    st.subheader("Radio avec index")
    
    # Radio avec index par défaut
    transport = st.radio(
        "Moyen de transport préféré:",
        ("🚗 Voiture", "🚆 Train", "✈️ Avion", "🚲 Vélo"),
        index=1  # Train sélectionné par défaut
    )
    
    # Radio avec clé personnalisée
    theme = st.radio(
        "Thème de l'interface:",
        ("🌞 Clair", "🌙 Sombre", "🎨 Auto"),
        key="theme_selector"
    )
    
    st.write(f"Transport: {transport}")
    st.write(f"Thème: {theme}")

st.markdown("---")

# ========================================
# SECTION 3: EXEMPLES AVANCÉS
# ========================================
st.header("3️⃣ Exemples Avancés")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Sélection conditionnelle")
    
    # Checkbox principal qui contrôle d'autres options
    enable_advanced = st.checkbox("Activer les options avancées")
    
    if enable_advanced:
        st.write("**Options avancées:**")
        
        # Options qui n'apparaissent que si la case principale est cochée
        debug_mode = st.checkbox("Mode debug", disabled=False)
        verbose_logs = st.checkbox("Logs détaillés", disabled=False)
        performance_monitor = st.checkbox("Monitoring performance", disabled=False)
        
        # Radio conditionnel
        if debug_mode:
            debug_level = st.radio(
                "Niveau de debug:",
                ("Minimal", "Standard", "Détaillé"),
                horizontal=True
            )
            st.info(f"Debug {debug_level.lower()} activé")
    else:
        st.info("Cochez la case ci-dessus pour voir les options avancées")

with col2:
    st.subheader("Validation de formulaire")
    
    # Simuler un formulaire avec validation
    st.write("**Formulaire d'inscription:**")
    
    # Checkboxes obligatoires
    accept_terms = st.checkbox("J'accepte les conditions générales *")
    accept_privacy = st.checkbox("J'accepte la politique de confidentialité *")
    
    # Checkbox optionnel
    marketing = st.checkbox("J'accepte de recevoir des e-mails marketing")
    
    # Radio obligatoire
    account_type = st.radio(
        "Type de compte: *",
        ("Personnel", "Professionnel", "Entreprise")
    )
    
    # Validation
    form_valid = accept_terms and accept_privacy and account_type
    
    if st.button("S'inscrire", disabled=not form_valid):
        if form_valid:
            st.success("✅ Inscription réussie!")
            st.balloons()
        else:
            st.error("❌ Veuillez remplir tous les champs obligatoires (*)")
    
    if not form_valid:
        st.caption("* Champs obligatoires")

st.markdown("---")

# ========================================
# SECTION 4: USAGE AVEC SESSION STATE
# ========================================
st.header("4️⃣ Utilisation avec Session State")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Persistance des données")
    
    # Initialisation du session state si nécessaire
    if 'persistent_checkboxes' not in st.session_state:
        st.session_state.persistent_checkboxes = {
            'option1': False,
            'option2': True,
            'option3': False
        }
    
    if 'persistent_radio' not in st.session_state:
        st.session_state.persistent_radio = "Option A"
    
    st.write("**Options persistantes:**")
    
    # Checkboxes avec session state
    for i in range(1, 4):
        key = f'option{i}'
        st.session_state.persistent_checkboxes[key] = st.checkbox(
            f"Option persistante {i}",
            value=st.session_state.persistent_checkboxes[key],
            key=f"persistent_cb_{i}"
        )
    
    # Radio avec session state
    st.session_state.persistent_radio = st.radio(
        "Choix persistant:",
        ("Option A", "Option B", "Option C"),
        index=["Option A", "Option B", "Option C"].index(st.session_state.persistent_radio),
        key="persistent_radio"
    )

with col2:
    st.subheader("État actuel")
    
    st.write("**Checkboxes persistantes:**")
    for key, value in st.session_state.persistent_checkboxes.items():
        icon = "✅" if value else "❌"
        st.write(f"{icon} {key}: {value}")
    
    st.write(f"**Radio persistant:** {st.session_state.persistent_radio}")
    
    # Bouton pour réinitialiser
    if st.button("🔄 Réinitialiser tout"):
        st.session_state.persistent_checkboxes = {
            'option1': False,
            'option2': False,
            'option3': False
        }
        st.session_state.persistent_radio = "Option A"
        st.experimental_rerun()

st.markdown("---")

# ========================================
# SECTION 5: STYLES ET APPARENCE
# ========================================
st.header("5️⃣ Personnalisation avec CSS")

# CSS personnalisé pour styliser les éléments
st.markdown("""
<style>
.custom-checkbox {
    background-color: #f0f2f6;
    padding: 10px;
    border-radius: 5px;
    margin: 5px 0;
}

.highlight-radio {
    background: linear-gradient(90deg, #ff6b6b, #feca57);
    padding: 15px;
    border-radius: 10px;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Style personnalisé")
    
    st.markdown('<div class="custom-checkbox">', unsafe_allow_html=True)
    custom_check = st.checkbox("Checkbox avec style personnalisé")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if custom_check:
        st.markdown('<div class="highlight-radio">Checkbox activée avec style!</div>', 
                   unsafe_allow_html=True)

with col2:
    st.subheader("Métriques basées sur sélections")
    
    # Exemples de métriques dynamiques
    options_selected = sum([
        st.checkbox("Métrique 1", key="metric1"),
        st.checkbox("Métrique 2", key="metric2"), 
        st.checkbox("Métrique 3", key="metric3")
    ])
    
    st.metric(
        label="Options sélectionnées",
        value=options_selected,
        delta=options_selected - 1 if options_selected > 1 else None
    )

# ========================================
# RÉSUMÉ DES SYNTAXES
# ========================================
st.markdown("---")
st.header("📝 Résumé des syntaxes")

st.code("""
# CHECKBOXES
checkbox = st.checkbox("Label")                    # Checkbox simple
checkbox = st.checkbox("Label", value=True)        # Avec valeur par défaut
checkbox = st.checkbox("Label", key="unique_key")  # Avec clé
checkbox = st.checkbox("Label", help="Aide")       # Avec texte d'aide
checkbox = st.checkbox("Label", disabled=True)     # Désactivé

# BOUTONS RADIO  
radio = st.radio("Question", ("Option1", "Option2"))           # Radio simple
radio = st.radio("Question", options, index=1)                 # Avec index par défaut
radio = st.radio("Question", options, horizontal=True)         # Horizontal
radio = st.radio("Question", options, key="unique_key")        # Avec clé
radio = st.radio("Question", options, disabled=True)           # Désactivé

# AVEC SESSION STATE
if 'key' not in st.session_state:
    st.session_state.key = False
st.session_state.key = st.checkbox("Label", value=st.session_state.key)
""", language="python")

st.success("🎉 Vous maîtrisez maintenant les checkboxes et radios Streamlit!")