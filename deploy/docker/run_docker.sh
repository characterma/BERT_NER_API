#!/bin/sh

# deploy docker, modify the command accordingly

if [[ -z "${DOCKER_DEPLOY_SERVER}" ]]; then
	# run command locally
	echo "[On $(hostname)]: docker run -d $DOCKER_DEPLOY_CONTAINER_PORT_PARAMS $DOCKER_ENV_VARS $DOCKER_VOLUMES_MOUNT --name $DOCKER_DEPLOY_CONTAINER_NAME $IMAGE_REPOS:$IMAGE_TAG $DOCKER_CMD"
	docker run -d $DOCKER_DEPLOY_CONTAINER_PORT_PARAMS $DOCKER_ENV_VARS $DOCKER_VOLUMES_MOUNT --name $DOCKER_DEPLOY_CONTAINER_NAME $IMAGE_REPOS:$IMAGE_TAG $DOCKER_CMD	
else
	# run command remotely
	echo "[On $DOCKER_DEPLOY_SERVER]: docker run -d $DOCKER_DEPLOY_CONTAINER_PORT_PARAMS $DOCKER_ENV_VARS $DOCKER_VOLUMES_MOUNT --name $DOCKER_DEPLOY_CONTAINER_NAME $IMAGE_REPOS:$IMAGE_TAG $DOCKER_CMD"
	
	# if not running via Gitlab CI, this will prompt for login (should not put password here)
	ssh -t developer@$DOCKER_DEPLOY_SERVER docker run -d $DOCKER_DEPLOY_CONTAINER_PORT_PARAMS $DOCKER_ENV_VARS $DOCKER_VOLUMES_MOUNT --name $DOCKER_DEPLOY_CONTAINER_NAME $IMAGE_REPOS:$IMAGE_TAG $DOCKER_CMD
fi	



