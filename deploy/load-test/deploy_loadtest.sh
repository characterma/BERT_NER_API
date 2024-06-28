#!/bin/sh

# Verify variable values
env | grep -E 'K8S_DEPLOY_NAMESPACE|APP_NAME|LOCUST_HOST|LOCUST_USERS|LOCUST_SPAWN_RATE|LOCUST_RUN_TIME|LOCUST_LOCUSTFILE|LOCUST_WEBUI|GROUP_NAME|CHART_VERSION|UPLOAD_S3|LOCUST_WEBUI_WORKERS|LOCUST_SLAVE|ACCOUNT_S3|PASSWORD_S3'

mkdir -p locust/locustfiles/example/
cp -r ../../load-test/*  locust/locustfiles/example/

helm install --namespace $K8S_DEPLOY_NAMESPACE --set appName=$APP_NAME --set k8sNamespace=$K8S_DEPLOY_NAMESPACE \
--set groupName=$GROUP_NAME --set chartVersion=$CHART_VERSION --set nameOverride=locust-$APP_NAME --set fullnameOverride=locust-$APP_NAME \
--set locust_host=$LOCUST_HOST --set locust_users=$LOCUST_USERS --set locust_spawn_rate=$LOCUST_SPAWN_RATE --set locust_run_time=$LOCUST_RUN_TIME \
--set locust_locustfile=$LOCUST_LOCUSTFILE --set locust_webui=$LOCUST_WEBUI --set locust_webui_workers=$LOCUST_WEBUI_WORKERS \
--set locust_slave=$LOCUST_SLAVE  --set uploadS3=$UPLOAD_S3 --set accountS3=$ACCOUNT_S3 --set passwordS3=$PASSWORD_S3 locust-$APP_NAME ./locust

echo "helm install --namespace $K8S_DEPLOY_NAMESPACE --set appName=$APP_NAME --set k8sNamespace=$K8S_DEPLOY_NAMESPACE 
--set groupName=$GROUP_NAME --set chartVersion=$CHART_VERSION --set nameOverride=locust-$APP_NAME --set fullnameOverride=locust-$APP_NAME 
--set locust_host=$LOCUST_HOST --set locust_users=$LOCUST_USERS --set locust_spawn_rate=$LOCUST_SPAWN_RATE --set locust_run_time=$LOCUST_RUN_TIME 
--set locust_locustfile=$LOCUST_LOCUSTFILE --set locust_webui=$LOCUST_WEBUI --set locust_webui_workers=$LOCUST_WEBUI_WORKERS 
--set locust_slave=$LOCUST_SLAVE  --set uploadS3=$UPLOAD_S3 --set accountS3=$ACCOUNT_S3 --set passwordS3=$PASSWORD_S3 locust-$APP_NAME ./locust"
