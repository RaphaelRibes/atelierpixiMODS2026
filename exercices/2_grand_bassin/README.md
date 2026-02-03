# Le Grand Bassin
Et dans la vrai vie, ça ressemble a quoi un projet pixi ?

## Ramilass
C'est un de nos projet de M2 Bioinformatique réalisé par Mickael Coquerelle, Loïk Galtier et moi même.
Il s'agit d'un assembleur de génome en C++ qui utilise des graphes de De Bruijn.
Ce projet utilise pixi pour gérer ses environements de développement et d'exécution.

Vous pouvez cloner le projet avec:
```shell
git clone https://github.com/MickaelCQ/RaMiLass.git
cd RaMiLass
```

## Déconstruction du projet
On retrouve 4 grands environnements dans RaMiLASS:

### Par défaut (build & run)
C'est l'environnement qui va intéresser l'utilisateur. On va y retrouver les commandes `build` et `start`

1. `pixi run build`

Cette tâche est divisée en deux:
```toml
[tasks._configure]
cmd = "cmake -S $INIT_CWD -B $INIT_CWD/build"
description = "Configure the C++ project using CMake"
inputs = ["$INIT_CWD/CMakeLists.txt"]
outputs = ["$INIT_CWD/build/Makefile"]
```
- `_configure` est une tâche qui configure le projet C++ avec CMake. Le `_` permet à cette tâche de ne pas apparaitre dans `pixi run`.
- `$INIT_CWD` est une variable d'environnement pixi qui pointe vers le répertoire courant d'où est lancé la commande.
- `inputs` et `outputs` sont les fichiers attendus en entrée et en sortie de la tâche. Pixi utilise ces informations pour savoir si la tâche doit être relancée ou si le résultat est déjà à jour. Si ils ne sont pas présent, la tâche s'exécute en envoyant un warning.

```toml
[tasks.build]
cmd = "cmake --build $INIT_CWD/build"
description = "Build the C++ project using CMake"
depends-on = ["_configure"]
inputs = ["$INIT_CWD/src/*", "$INIT_CWD/CMakeLists.txt"]
outputs = ["$INIT_CWD/build/ramilass"]
```
- `depends-on` permet de chaîner des tâches. Ici, la tâche `build` dépend de la tâche `_configure`, qui sera donc exécutée avant.

2. `pixi run start`

```toml
[tasks.start]
args = [
    { "arg" = "file", "default" = "data/reads.fasta" },
    { "arg" = "output", "default" = "reads" },
]
cmd = "$INIT_CWD/build/ramilass $INIT_CWD/{{ file }} $INIT_CWD/output -o {{ output }} --fuse --gfa --debug --max-contig-len 11000 --popping-passes 0"
description = "Run the app"
inputs = ["$INIT_CWD/build/ramilass"]
outputs = ["$INIT_CWD/output/{{ output }}.gfa", "$INIT_CWD/output/{{ output }}.contigs.fasta"]
```
- `args` permet de définir des arguments dynamiques pour la tâche. Ici, on peut passer un fichier d'entrée et un nom de sortie différent à chaque exécution.
  - On défini en premier le nom de l'argument (`"arg" = "file"`)
  - On peut ensuite définir une valeur par défaut si l'argument n'est pas fourni (`"default" = "data/reads.fasta"`).

On peut donc très bien spécifier un autre fichier d'entrée en lançant la commande:
```shell
pixi run start data/other_reads.fasta my_assembly
```

## Conteneuriser
![image](Banner_Gemini_Generated_Image.png)

Le projet est maintenant fini, je veux le partager avec mes collègues bioinformaticiens.
Je vais donc utiliser `pixitainer` pour créer une image singularity/apptainer contenant mon espace de travail pixi.

On va en premier installer `pixitainer`:
```shell
pixi global install -c https://prefix.dev/raphaelribes -c https://prefix.dev/conda-forge pixitainer
```

On peut ensuite regarde ce que ce dernier nous permet de faire:
```shell
pixi containerize --help
Usage: pixi containerize [options]

Pixi extension to containerize a project with Apptainer.
Version: 0.3.3

Options:
  -o, --output OUTPUT       Output image path (default: pixitainer.sif)
  -p, --path PATH           Working directory (source project)
  -s, --seamless            Enable seamless execution
  -e, --env ENV             Specific environment(s) to install (can be used multiple times)
  -q, --quiet               Quiet mode (suppress all output, return 0 on success, 1 on error)
  -v, --verbose             Verbose mode (show full Apptainer build output)
  --base-image IMAGE        Specify base image (default: ubuntu:24.04)
  --pixi-version VERSION    Specify pixi version (default: latest)
  --add-file SRC:DEST       Add a file to the container (format: source:destination)
  --keep-def                Export the .def file (do not delete temporary files)
  --no-install              Do not install any environments
  -h, --help                Show this help message
```

On va en premier construire le projet avec:
```shell
pixi run build
```

On peut donc créer une image apptainer/singularity de notre projet avec la commande:
```shell
pixi containerize -o ramilass.sif\
                  --add-file "$(pwd)/build/ramilass:/opt/conf/build/ramilass"\
                  --seamless --no-install
```

On peut maintenant utiliser l'image `ramilass.sif` pour faire tourner l'assembleur.

```shell
apptainer run --bind $(pwd)/../.:$(pwd)/../. ramilass.sif start
```
