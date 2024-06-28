#!/bin/sh

cd /tmp/{{ .Values.groupName }}/

UPLOAD_FOLDER={{ .Values.appName }}

#### NO NEED TO CHANGE BELOW ####

SPEC_LOGIN="spec:spec0000"

create_remote_folder()
{
    BASE_URL=$1
    FOLDER=$2

    # check if folder exists, otherwise create one
    #if [[ $(curl -X PROPFIND -H "Depth: $DEPTH" -u $SPEC_LOGIN "$BASE_URL" | grep "/$FOLDER") ]]; then
    if curl -u $SPEC_LOGIN --output /dev/null --silent --head --fail "$BASE_URL/$FOLDER"; then
        echo "Folder $FOLDER already exists"
    else
        echo "Folder $FOLDER not found, create it"
        curl -u $SPEC_LOGIN -X MKCOL "$BASE_URL/$FOLDER"
    fi
}


# loop through upload folder to upload files/directories
upload_files()
{
    BASE_URL=$1
    FOLDER=$2
    DEPTH=1
    for file in $FOLDER/*; do

        if ! [ "$(ls -A $file)" ]; then continue; fi

        if [[ -d "$file" && ! -L "$file" ]]; then
            echo "$file is a directory, create remote directory";

            foldername=$(basename "$file")

            create_remote_folder $BASE_URL $file

            upload_files $BASE_URL $file

        else
            echo "found file with name: $file"

            filename=$(basename "$file")
            curl -u $SPEC_LOGIN -X DELETE "$BASE_URL/$file"
            curl -u $SPEC_LOGIN -T $file "$BASE_URL/$file"
        fi

    done
}


OWN_CLOUD_SPEC_URL="http://ess-repos01.wisers.com:10000/remote.php/dav/files/spec/Spec"

create_remote_folder $OWN_CLOUD_SPEC_URL $UPLOAD_FOLDER
upload_files $OWN_CLOUD_SPEC_URL $UPLOAD_FOLDER
