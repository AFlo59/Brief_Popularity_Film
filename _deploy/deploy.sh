#!/bin/bash
YAML_FILE=deploy-aci.yaml

echo "DEPLOIEMENT SUR AZURE..."
az container create --resource-group RG_KUILM --file deploy-aci.yaml