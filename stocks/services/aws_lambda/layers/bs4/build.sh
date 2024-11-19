#!/bin/bash

set -e

LAYER_NAME="beautifulsoup4-layer"
PYTHON_VERSION="python3.10"

# Criar a estrutura necessária para a layer
echo "Creating directory structure for the layer..."
rm -rf build python
mkdir -p python/lib/$PYTHON_VERSION/site-packages

# Instalar o pacote beautifulsoup4 na estrutura correta
echo "Installing beautifulsoup4 into the layer structure..."
pip install beautifulsoup4 -t python/lib/$PYTHON_VERSION/site-packages

# Compactar o conteúdo em um .zip
echo "Zipping the layer..."
zip -r ${LAYER_NAME}.zip python

# Remover diretórios temporários
rm -rf python

echo "Build completed. Output: ${LAYER_NAME}.zip"
