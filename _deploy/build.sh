YAML_FILE=compose.prod.acr.yml
ACR=acrfilm

az login

echo "*** Build"
docker compose --file=${YAML_FILE} build
echo "*** Login sur l'ACR ${ACR}"
az acr login --name ${ACR}
echo "*** Push sur Azure"
docker compose --file=${YAML_FILE} push