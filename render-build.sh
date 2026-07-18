#!/usr/bin/env bash
# Render native-Python build (no Docker). Keeps the install lean:
#  - CPU-only PyTorch (skips ~2GB of CUDA wheels)
#  - xgboost without its nvidia CUDA deps (CPU predict/SHAP don't need them)
#  - pre-download the MiniLM embedding model so the first /chat is instant
set -o errexit

pip install --upgrade pip
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install --no-deps xgboost==3.3.0
pip install -r backend/requirements.txt

python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
