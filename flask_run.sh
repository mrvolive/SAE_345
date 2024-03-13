#!/bin/bash

# Chemin du fichier à la racine
file_path="./sae_s2.env"

# Vérifier si le fichier existe
if [ ! -f "$file_path" ]; then
    # Créer le fichier s'il n'existe pas
    touch "$file_path"

    # Ajouter le contenu au fichier
    # shellcheck disable=SC2129
    echo "HOST=\"localhost\"" >> "$file_path"
    echo "LOGIN=\"login\"" >> "$file_path"
    echo "PASSWORD=\"password\"" >> "$file_path"
    echo "DATABASE=\"BDD_login_sae\"" >> "$file_path"

    echo "Le fichier $file_path a été créé avec succès."
fi


flask --debug  --app app  run   --host 0.0.0.0