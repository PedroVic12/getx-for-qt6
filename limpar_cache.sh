#!/bin/bash

# Encontra todos os diretórios chamados __pycache__ e os remove
find . -type d -name "__pycache__" -exec rm -rf {} +

echo "Limpeza de __pycache__ concluída!"

