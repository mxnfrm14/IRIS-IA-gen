
# IRIS-IA-gen

Bienvenue dans le projet **IRIS-IA-gen**. Ce projet vise à simplifier l'utilisation de modèles IA en fournissant des instructions claires pour l'installation et l'utilisation. 

## Installation

Pour installer le modèle, suivez ces étapes :

1. Installez le package `huggingface-hub` :
   ```bash
   pip install huggingface-hub
   ```

2. Testez l'installation avec la commande suivante :
   ```bash
   huggingface-cli --help
   ```

### Résolution des problèmes

Si la commande ci-dessus ne fonctionne pas, vous devrez peut-être ajouter `huggingface-cli` au `PATH`.

#### Ajouter `huggingface-cli` au `PATH`

1. **Localisez votre dossier Python Scripts** :
   Sous Windows, le répertoire `Scripts` de votre installation Python contient des exécutables comme `huggingface-cli`. Pour trouver ce dossier, exécutez la commande suivante :
   ```bash
   python -m site --user-base
   ```
   Cela renverra un chemin similaire à :
   ```
   C:\Users\VotreNomUtilisateur\AppData\Roaming\Python\Python39\Scripts
   ```

2. **Ajoutez ce dossier au `PATH`** :
   - Ouvrez les **Paramètres système avancés**.
   - Cliquez sur **Variables d'environnement**.
   - Sous **Variables système**, sélectionnez la variable `PATH` et cliquez sur **Modifier**.
   - Ajoutez un nouveau chemin en collant le chemin du dossier `Scripts` que vous avez trouvé précédemment.
   - Cliquez sur **OK** pour enregistrer les modifications.

3. **Redémarrez le terminal** :
   Après avoir ajouté le chemin, redémarrez votre terminal et essayez à nouveau d'exécuter la commande :
   ```bash
   huggingface-cli --help
   ```

## Utilisation

Pour télécharger le modèle, utilisez la commande suivante :
```bash
huggingface-cli download Qwen/Qwen2.5-3B-Instruct-GGUF qwen2.5-3b-instruct-q5_k_m.gguf --local-dir ./Models --local-dir-use-symlinks False
```

## Installation de Llama

Entrez cette commande pour cloner :
```bash
git clone https://github.com/ggerganov/llama.cpp
```
Pour utiliser **Llama**, il est nécessaire d'installer Visual Studio 2022. Vous pouvez le télécharger à l'adresse suivante : [Visual Studio 2022](https://visualstudio.microsoft.com/fr/visual-cpp-build-tools/).

### Ajout des requirements C++

Optionnel : Installer Visual Studio avec les outils de build

1. Téléchargez et installez Visual Studio depuis le [site de Visual Studio](https://visualstudio.microsoft.com/).
2. Pendant l'installation, sélectionnez l'option **Desktop development with C++**.
3. Une fois installé, ouvrez **Developer Command Prompt for Visual Studio** pour avoir accès à `cl.exe` (le compilateur C/C++ de Visual Studio).
4. Retournez dans le répertoire du projet `llama.cpp` et relancez la commande `make` depuis le terminal de développement Visual Studio.

### Relancer la compilation

Après avoir installé les outils de développement et les avoir ajoutés à votre environnement, revenez dans le répertoire de votre projet `llama.cpp` et relancez la commande suivante :
```bash
make llama-cli
```

faire 
```bash
pip install llama-cpp-python
```

Merci d'avoir consulté ce projet ! Si vous avez des questions ou des suggestions, n'hésitez pas à ouvrir une issue.
