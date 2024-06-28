# Webhook or Token.
WEBHOOK_URL=https://wisers.webhook.office.com/webhookb2/354d6653-9f05-437a-834d-15fa4d0976db@ed439e7b-498b-4ff9-83d6-23e6e01abbdb/IncomingWebhook/beaf89a87e004c319431ed206eabbefe/3d8807ac-49ca-4dfd-9095-25a40bff656d
if [[ "${WEBHOOK_URL}" == "" ]]
then
  echo "No webhook_url specified."
  exit 1
fi
shift

# Title .
TITLE="$CHART_NAME:$CHART_VERSION is finisned"
if [[ "${TITLE}" == "" ]]
then
  echo "No title specified."
  exit 1
fi
shift

# Color.
COLOR=ff0000
if [[ "${COLOR}" == "" ]]
then
  echo "No status specified."
  exit 1
fi
shift

# Text.
TEXT="$CHART_NAME:$CHART_VERSION is finisned. Now you can check it on our k8s."
if [[ "${TEXT}" == "" ]]
then
  echo "No text specified."
  exit 1
fi

# Convert formating.
MESSAGE=$( echo ${TEXT} | sed 's/"/\"/g' | sed "s/'/\'/g" )
JSON="{\"title\": \"${TITLE}\", \"themeColor\": \"${COLOR}\", \"text\": \"${MESSAGE}\" }"

# Post to Microsoft Teams.
curl -H "Content-Type: application/json" -d "${JSON}" "${WEBHOOK_URL}"

# Sent email
if [ ! -n "$MAIL_ADR" ]; then
  echo "Subject: $CHART_NAME-$CHART_VERSION is finisned"
else
  ssh -t developer@ess-deploy "echo 'Subject: $CHART_NAME-$CHART_VERSION is finisned' | /usr/sbin/sendmail -f gitlab-cicd@wisers.com -v $MAIL_ADR"
fi