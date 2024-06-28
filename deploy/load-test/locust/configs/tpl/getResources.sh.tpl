#!/bin/bash
# https://github.com/eldada/kubernetes-scripts

# UNCOMMENT this line to enable debugging
# set -xv

## Get resources requests and limits per container in a Kubernetes cluster.

OUT=/tmp/{{ .Values.groupName }}/{{ .Values.appName }}/{{ .Values.chartVersion }}/locust-reports/resources.csv
HEADERS=true
CONSOLE_ONLY=false
RUN_TIME=$(echo "{{ .Values.locust_run_time }}" | sed -r 's/s//g')

######### Functions #########
errorExit () {
    echo -e "\nERROR: $1\n"
    exit 1
}

# Test connection to a cluster by kubectl
testConnection () {
    kubectl get pods > /dev/null || errorExit "[Debug] Connection to k8s cluster failed"
}

getRequestsAndLimits () {
    local time=
    local data=
    local namespace=
    local pod=
    local container=
    local cpu_request=
    local mem_request=
    local cpu_limit=
    local mem_limit=
    local cpu_usage=
    local memory_usage=
    local line=
    local final_line=
    local sleep_time=
    local loop_num=

    sleep_time={{ .Values.locust_spawn_rate }}
    loop_num=$((${RUN_TIME}/{{ .Values.locust_spawn_rate }}))

    echo "[Debug] kubectl get pods -n {{ .Values.k8sNamespace }} -o json | jq -r '.items[] | .metadata.namespace + "," + .metadata.name + "," + (.spec.containers[] | .name + "," + .resources.requests.cpu + "," + .resources.requests.memory + "," + .resources.limits.cpu + "," + .resources.limits.memory)' | grep {{ .Values.appName }} | grep -v locust"
    data=$(kubectl get pods -n {{ .Values.k8sNamespace }} -o json | jq -r '.items[] | .metadata.namespace + "," + .metadata.name + "," + (.spec.containers[] | .name + "," + .resources.requests.cpu + "," + .resources.requests.memory + "," + .resources.limits.cpu + "," + .resources.limits.memory)' | grep {{ .Values.appName }} | grep -v locust | grep -v istio-proxy )

    # Backup OUT file if already exists
    [ -f "${OUT}" ] && [ "$CONSOLE_ONLY" == "false" ] && cp -f "${OUT}" "${OUT}.$(date +"%Y-%m-%d_%H:%M:%S")"

    # Prepare header for output CSV
    if [ "${HEADERS}" == true ]; then
        echo "Time,Namespace,Pod,Container,CPU request,CPU Usage,Memory request,Memory Usage,CPU limit,Memory limit" > "${OUT}"
    else
        echo -n "" > "${OUT}"
    fi

    local OLD_IFS=${IFS}
    IFS=$'\n'

    for i in $(seq 1 $loop_num); do
        for l in ${data}; do
            time=$(date +"%T")
            namespace=$(echo "${l}" | awk -F, '{print $1}')
            pod=$(echo "${l}" | awk -F, '{print $2}')
            container=$(echo "${l}" | awk -F, '{print $3}')
            cpu_request=$(echo "${l}" | awk -F, '{print $4}')
            mem_request=$(echo "${l}" | awk -F, '{print $5}')
            cpu_limit=$(echo "${l}" | awk -F, '{print $6}')
            mem_limit=$(echo "${l}" | awk -F, '{print $7}')

            # Adding pod and container actual usage with pod top data
            line=$(kubectl top pod -n ${namespace} ${pod} --containers | grep " ${container} ")

            cpu_usage=$(echo "${line}" | awk '{print $3}')
            memory_usage=$(echo "${line}" | awk '{print $4}')

            final_line=${time},${namespace},${pod},${container},${cpu_request},${cpu_usage},${mem_request},${memory_usage},${cpu_limit},${mem_limit}

            echo "${final_line}" | tee -a "${OUT}"
        done
        sleep $sleep_time
    done
    IFS=${OLD_IFS}
}

main () {
    sleep 5
    testConnection
    getRequestsAndLimits
}

######### Main #########

main "$@"