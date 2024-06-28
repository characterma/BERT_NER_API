set -e
curl -X POST -H "Content-Type:application/json" \
-H "Authorization:eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiIxMDgiLCJuYW1lIjoic2hlbSIsInVzZXJuYW1lIjoic2hlbSIsInJvbGUiOiJkZXZlbG9wZXIiLCJyYW5kb20iOjIzODk2Mjk2MjExMDQ0NDY0ODMsInVhcF9lbnYiOiJ1YXQiLCJpc3MiOiJ1YXAgZG1nciIsInN1YiI6ImFjY2VzcyBjb250cm9sIiwiaWF0IjoxNjM3MzAzODE1LCJleHAiOjI1NTYxMTUxOTl9.hOCz6QhP568ZEDDFiq71mMTqiYz1YJIGnA0eHCjItZM" \
-d '{
    "_root": {
        "app_description": "'"$CHART_DESCRIPTION"'",
        "app_name": "'$APP_NAME'",
        "ci_ref": "'$CI_REF'",
        "git_url": "'$CI_REPOSITORY_URL'",
        "group_name": "'$GROUP_NAME'",
        "image": "'$IMAGE_REPOS'",
        "image_create_time": "",
        "image_tag": "'$IMAGE_TAG'",
        "version": "'$CI_BUILD_TAG'"
    }
}' \
http://ess72.wisers.com/uap-uat/datamgr-data-cud-api/api/restful/object/UapApiInventory/US?jobid=447&idtype=string
set +e
sleep 5