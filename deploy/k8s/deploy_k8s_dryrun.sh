#!/bin/sh

# Auto-rename the chart folder according to CHART_NAME defined in env.sh
if [ -d "$CHART_NAME" ]; then
	echo "Folder $CHART_NAME found."
elif [ -d "chart" ]; then
	echo "Rename folder /chart to /$CHART_NAME as defined."
	mv chart $CHART_NAME
else
	echo "No expected chart folder found, pls check."
	exit 1
fi

# Define paths
AILAB_PATH=../docker/ailab
CONFIG_PATH=$CHART_NAME/configs/
mkdir -p $CONFIG_PATH
#rm -rf $CONFIG_PATH/*

sh -c "$COPY_TO_CHART_CONFIG" #define in env.sh

# Verify variable values
env | grep -E 'K8S_DEPLOY_NAMESPACE|APP_NAME|IMAGE_REPOS|IMAGE_TAG|RELEASE_NAME|CHART_NAME|CHART_VERSION|CI_REF|SWAGGER_ROOTPATH'

# Replace chart name, version and description in Chart.yaml 
sed -i 's/\[\[\[CHART_DESCRIPTION\]\]\]/'"$CHART_DESCRIPTION"'/g' $CHART_NAME/Chart.yaml
sed -i 's/\[\[\[CHART_NAME\]\]\]/'"$CHART_NAME"'/g' $CHART_NAME/Chart.yaml
sed -i 's/\[\[\[CHART_VERSION\]\]\]/'"$CHART_VERSION"'/g' $CHART_NAME/Chart.yaml

sed -i 's/\[\[\[APP_NAME\]\]\]/'"$APP_NAME"'/g' $CHART_NAME/values.yaml
sed -i 's/\[\[\[IMAGE_REPOS\]\]\]/'"$(echo $IMAGE_REPOS | sed -e 's/[\/&]/\\&/g')"'/g' $CHART_NAME/values.yaml
sed -i 's/\[\[\[IMAGE_TAG\]\]\]/'"$IMAGE_TAG"'/g' $CHART_NAME/values.yaml
sed -i 's/\[\[\[CI_REF\]\]\]/'"$CI_REF"'/g' $CHART_NAME/values.yaml
sed -i 's/\[\[\[SWAGGER_ROOTPATH\]\]\]/'"$(echo $SWAGGER_ROOTPATH | sed -e 's/[\/&]/\\&/g')"'/g' $CHART_NAME/values.yaml

# update chart dependencies
helm dep up ./$CHART_NAME

if [ "$1" == "upgrade" ]; then
   echo "helm upgrade --set ciBuildRef=$CI_REF --set appName=$APP_NAME --set imageRepository=$IMAGE_REPOS --set imageTag=$IMAGE_TAG 
   -i --namespace $K8S_DEPLOY_NAMESPACE $RELEASE_NAME --debug --dry-run ./$CHART_NAME"
   helm upgrade --set ciBuildRef=$CI_REF --set appName=$APP_NAME --set imageRepository=$IMAGE_REPOS --set imageTag=$IMAGE_TAG \
   -i --namespace $K8S_DEPLOY_NAMESPACE $RELEASE_NAME --debug --dry-run ./$CHART_NAME
else
   echo "helm install --set ciBuildRef=$CI_REF --set appName=$APP_NAME --set imageRepository=$IMAGE_REPOS --set imageTag=$IMAGE_TAG 
   --namespace $K8S_DEPLOY_NAMESPACE $RELEASE_NAME --dry-run --debug ./$CHART_NAME"
   helm install --set ciBuildRef=$CI_REF --set appName=$APP_NAME --set imageRepository=$IMAGE_REPOS --set imageTag=$IMAGE_TAG \
    --namespace $K8S_DEPLOY_NAMESPACE $RELEASE_NAME --dry-run --debug ./$CHART_NAME
fi


