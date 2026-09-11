#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input

# Download the open-source multilingual Argos model during the build so the
# first visitor does not have to wait for a large model download.
python - <<'PY'
import os, urllib.request
import argostranslate.package

model_dir = os.path.abspath(os.getenv("ARGOS_MODEL_DIR", ".argos"))
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "translate-fairseq_m2m_100_418M.argosmodel")
url = "https://data.argosopentech.com/argospm/v2/translate-fairseq_m2m_100_418M.argosmodel"
if not os.path.exists(model_path):
    print("Downloading Argos multilingual model...")
    urllib.request.urlretrieve(url, model_path)
print("Installing Argos multilingual model...")
try:
    argostranslate.package.install_from_path(model_path)
except Exception as exc:
    print(f"Argos model may already be installed: {exc}")
PY
