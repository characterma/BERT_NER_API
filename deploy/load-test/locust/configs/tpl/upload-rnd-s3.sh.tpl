#!/bin/sh

echo "start upload-report!!!"

/usr/local/bin/mc alias set minio {{ .Values.S3Url }} {{ .Values.accountS3 }} {{ .Values.passwordS3 }} --api S3v4
echo "mc alias set minio {{ .Values.S3Url }} {{ .Values.accountS3 }} {{ .Values.passwordS3 }} --api S3v4"

# copy the file to s3 server for serving spark deployment
for filename in /tmp/{{ .Values.groupName }}/{{ .Values.appName }}/{{ .Values.chartVersion }}/locust-reports/*; do
    echo "- Uploading file: $filename"
    /usr/local/bin/mc cp $filename minio/ai-test-report/{{ .Values.appName }}/{{ .Values.chartVersion }}/locust-reports/
done

# check it should not be empty
echo "mc ls minio/ai-test-report/{{ .Values.appName }}/{{ .Values.chartVersion }}/locust-reports/"
/usr/local/bin/mc ls minio/ai-test-report/{{ .Values.appName }}/{{ .Values.chartVersion }}/locust-reports/
