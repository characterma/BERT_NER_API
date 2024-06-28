#!/bin/sh

if [[ -z "${DOCKER_DEPLOY_SERVER}" ]]; then
	# run command locally
	echo "[On $(hostname)]: remove container $DOCKER_DEPLOY_CONTAINER_NAME and image $IMAGE_REPOS:$IMAGE_TAG"

	# delete existing container
	docker rm -f $DOCKER_DEPLOY_CONTAINER_NAME
	# delete existing image, assume only above container was using the image
	docker rmi $IMAGE_REPOS:$IMAGE_TAG

else
	# run command remotely
	echo "[On $DOCKER_DEPLOY_SERVER]: remove container $DOCKER_DEPLOY_CONTAINER_NAME and image $IMAGE_REPOS:$IMAGE_TAG"
	
	# delete existing container
	ssh -t developer@$DOCKER_DEPLOY_SERVER docker rm -f $DOCKER_DEPLOY_CONTAINER_NAME || true
	# delete existing image, assume only above container was using the image
	ssh -t developer@$DOCKER_DEPLOY_SERVER docker rmi $IMAGE_REPOS:$IMAGE_TAG || true

fi
