#!/bin/sh

{{- if .Values.loadtest.pip_packages }}
pip install --user {{ range .Values.loadtest.pip_packages }}{{ . }} {{ end }}
{{- end }}

mkdir -p /tmp/{{ .Values.groupName }}/{{ .Values.appName }}/{{ .Values.chartVersion }}/locust-reports/
echo "mkdir -p /tmp/{{ .Values.groupName }}/{{ .Values.appName }}/{{ .Values.chartVersion }}/locust-reports/"

WEBUI={{ .Values.locust_webui }}
if [ "$WEBUI" == "false" ]; then
    echo "sh /config/getResources.sh &"
    bash /config/getResources.sh &
fi

echo "[INFO] /usr/local/bin/locust"
/usr/local/bin/locust "$@"

bash /config/upload-nextcloud.sh

UPLOADS3={{ .Values.uploadS3 }}

if [ "$UPLOADS3" == "true" ]; then
    sh /config/upload-rnd-s3.sh
fi

exit 0