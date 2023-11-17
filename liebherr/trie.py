import os
import shutil

def move_files_to_root_folder(root_folder):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            root_path = os.path.join(root_folder, filename)

            # S'assurer que le fichier n'est pas déjà à la racine
            if dirpath != root_folder:
                # Déplacer le fichier à la racine
                # Utiliser 'shutil.move' pour déplacer les fichiers
                shutil.move(file_path, root_path)
                print(f"Fichier déplacé : {file_path} -> {root_path}")

# Chemin du dossier 'Done'
root_folder_path = 'Done'
move_files_to_root_folder(root_folder_path)