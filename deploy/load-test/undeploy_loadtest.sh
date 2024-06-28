#### Below no need to change unless it's necessary


# helm delete, allow extra params, i.e. --purge
helm delete locust-$APP_NAME -n $K8S_DEPLOY_NAMESPACE
