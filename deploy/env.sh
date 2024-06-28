# !!Require Changes!!:
# =====================
# "GROUP_NAME-APP_NAME" will be used as Chart Name

# refer to GIT Lab project group, use the code within the bracket under group description
# e.g.: for TopicClassification > API > topic-tagging-api the group name will be "topcls".  The GIT project group description is "(topcls) Topic classification projects"
GROUP_NAME=ner

# This will be used for image and K8S module / ingress name
# If GIT Lab project name is different from deployed module on K8S, please use K8S module name instead
APP_NAME=ner-bochk-api

# Update Image Tag if different from any deployed version
IMAGE_TAG=1.0

# Update Chart Tag if different from any deployed version
CHART_VERSION=1.0.0

CHART_DESCRIPTION="NER model for BOCHK"

# Optional, for running deployment script manually
K8S_DEPLOY_NAMESPACE=playground

# Optional, your mail address for notifying(for multiple users: email1,email2,...etc)
MAIL_ADR=test@wisers.com

# Below are predefined. Don't Change unless you know what to achieve
# =====================
CHART_NAME=$GROUP_NAME-$APP_NAME
AILAB_PATH=../docker/ailab
CONFIG_PATH=$CHART_NAME/configs
ROOT_DIR=../../src/
AILAB_DIR=ailab/
# =====================

# !!Require Changes!!:
# =====================

# Copy necessary deployment files to /ailab
# example:
# COPY_TO_AILAB="
# rsync -av $ROOT_DIR/target/actuator-sample-0.0.1-SNAPSHOT.jar ailab/lib/;
# rsync -av $ROOT_DIR/target/classes/application.properties ailab/conf/;
# "
COPY_TO_AILAB="
rsync -av ../../requirements.txt $AILAB_DIR;
rsync -av ../../requirements/ $AILAB_DIR/requirements/;
rsync -av ../../bin/start.sh $AILAB_DIR;
rsync -av ../../configs $AILAB_DIR;
rsync -av $ROOT_DIR $AILAB_DIR/src/;
"

# Copy all necessary files (i.e. config/script) to /configs for creating K8S ConfigMap
# example:
# COPY_TO_CHART_CONFIG="
# cp $AILAB_PATH/start.sh $CONFIG_PATH;
# cp $AILAB_PATH/conf/application.properties $CONFIG_PATH;
# "
COPY_TO_CHART_CONFIG="
cp $AILAB_PATH/configs/configs.yaml.tpl $CONFIG_PATH/tpl/;
cp $AILAB_PATH/configs/logging.conf $CONFIG_PATH/;
"

# appConfigs for swaggerRootPath
SWAGGER_ROOTPATH="/playground/$APP_NAME"

### Set below Variables ONLY for creating Standalone Container on docker Server via docker/run_docker.sh  ###

## Usually define for running on one of DEV servers (ess37~39):

# Set container deployment server
DOCKER_DEPLOY_SERVER="ess76"
# Set docker container name, naming standard: (project|<user_name>)-<app name>
DOCKER_DEPLOY_CONTAINER_NAME="$GITLAB_USER_LOGIN-$APP_NAME"
# Define docker port mappings. multiple mappings can be defined like: "-p 9090:8080 -p 80:80 -p 20000~20005:10000~10005"
DOCKER_DEPLOY_CONTAINER_PORT_PARAMS="-p 13352:8080"
# Optional, set environment variables inside container, i.e. "-e TZ=Asia/Hong_Kong"
DOCKER_ENV_VARS=
# Optional, set volume mount from host to container, i.e. "-v /tmp/dummyfile:/ailab/dummyfile"
DOCKER_VOLUMES_MOUNT=
# Optional, set container start command
DOCKER_CMD=

### Set Postman Testing ###

# Postman collection file name (DEFAULT: postman_collection.json)
POSTMAN_COLLECTION_FILE="postman_collection.json"

# Optional, to override collection's variables from file inside test/collections/variables/ (i.e. playground.json)
POSTMAN_VAR_FILE=ess39.json


### Set Loading Test ###

# The port of tested APP/API (default: 8080)
LOCUST_TEST_API_PORT=8080
# Number of concurrent Locust users (10)
LOCUST_USERS=10
# The rate per second in which users are spawned. (20)
LOCUST_SPAWN_RATE=20
# Stop after the specified amount of time (250s)
LOCUST_RUN_TIME=250s
# enable the web ui of Locust
# LOCUST_WEBUI=false >> disable web ui (auto-run)
# LOCUST_WEBUI=true  >> enable web ui (manually)
LOCUST_WEBUI=false
# When using Locust Web UI, we can set the worker node number
LOCUST_WEBUI_WORKERS=3
# When using Locust autorun, we can set the slave number
LOCUST_SLAVE=3
# if need to upload to S3 bucket (true or false)
UPLOAD_S3=false
ACCOUNT_S3=AKIAO2FJJ25YEOB5LICQ
PASSWORD_S3=/A9dUrncUMFRY+NMwnNkN8J+kMC5c8n3gS3rXBtc

# =====================

# Below are predefined. Don't Change unless you know what to achieve
IMAGE_REPOS=$DK_ESS/$GROUP_NAME-$APP_NAME

RELEASE_NAME=$K8S_DEPLOY_NAMESPACE-$CHART_NAME

HELM_CHART_REPO=http://ess-deploy.wisers.com:8585

CI_REF=${CI_BUILD_REF:-un-known}

CHART_DESCRIPTION="(${CI_REF:0:8}) $CHART_DESCRIPTION"

# check if it's in git tagging flow
if [[ -z "${CI_COMMIT_TAG}" ]]; then
  echo "This is GIT development flow"
  IMAGE_TAG="$IMAGE_TAG-dev"
  CHART_VERSION="$CHART_VERSION-dev"
else
  echo "This is GIT tagging flow, tagName=$CI_COMMIT_TAG"
  if echo $CI_COMMIT_TAG | grep -qE "^stable-.*$" ; then
  	IMAGE_TAG="$IMAGE_TAG-stable"
  	CHART_VERSION="$CHART_VERSION-stable"
  elif echo $CI_COMMIT_TAG | grep -qE "^release-.*$" ; then
 	IMAGE_TAG="$IMAGE_TAG-release"
 	CHART_VERSION="$CHART_VERSION-release"
  else
  	echo "Non-standard tag name: $CI_COMMIT_TAG, please revise!"
  	# exit error to terminiate the ci flow
  	exit 1
  fi
fi


export GROUP_NAME K8S_DEPLOY_NAMESPACE APP_NAME CHART_NAME IMAGE_REPOS IMAGE_TAG RELEASE_NAME CHART_VERSION HELM_CHART_REPO \
CHART_DESCRIPTION DOCKER_DEPLOY_SERVER DOCKER_DEPLOY_CONTAINER_NAME DOCKER_DEPLOY_CONTAINER_PORT_PARAMS CI_REF \
DOCKER_ENV_VARS DOCKER_VOLUMES_MOUNT DOCKER_CMD POSTMAN_COLLECTION_FILE POSTMAN_VAR_FILE \
TEST_NAME COPY_TO_AILAB COPY_TO_CHART_CONFIG MAIL_ADR SWAGGER_ROOTPATH


if command -v dos2unix > /dev/null ; then
  find . -type f | xargs dos2unix -q
fi

# ensure some paths exist
DEPLOY_DIR=$(dirname $(find . -name env.sh))
mkdir -p $DEPLOY_DIR/docker/ailab
mkdir -p $DEPLOY_DIR/k8s/chart/configs/tpl/
#mkdir -p $CONFIG_PATH

### for Harbor using ###
HARBOR_REPO="harbor.wisers.com"
HARBOR_PROJECT_NAME="ailab"
HARBOR_IMAGE_REPOS=$HARBOR_REPO/$HARBOR_PROJECT_NAME/$GROUP_NAME-$APP_NAME
export HARBOR_REPO HARBOR_PROJECT_NAME HARBOR_IMAGE_REPOS

### Set Loading Testing ###
# Host to load test
LOCUST_HOST=http://$APP_NAME.$K8S_DEPLOY_NAMESPACE:$LOCUST_TEST_API_PORT
# loadtest.locust_locustfile -- the name of the locustfile
LOCUST_LOCUSTFILE=locustfile.py


export LOCUST_HOST LOCUST_USERS LOCUST_SPAWN_RATE LOCUST_RUN_TIME LOCUST_LOCUSTFILE LOCUST_WEBUI LOCUST_TEST_API_PORT UPLOAD_S3 LOCUST_WEBUI_WORKERS LOCUST_SLAVE ACCOUNT_S3 PASSWORD_S3
