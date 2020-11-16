#!/bin/bash
# Creating the script to send metrics to Cloud Watch
cat <<EOF > /etc/init.d/metrics
#!/bin/bash
INSTANCE_ID=\$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
CPU_USAGE_PERCENT=\$(top -b -n1 | grep "Cpu(s)" | awk '{ print \$2 + \$4 }')
FREE_MEM_MB=\$(grep MemFree /proc/meminfo | awk '{ print \$2 / 1024 }')
IO_WAIT=\$(iostat | awk 'NR==4 {print \$4}')
aws cloudwatch put-metric-data --metric-name cpu-usage-percent --dimensions Instance=\${INSTANCE_ID} --namespace "WebServers" --value "\${CPU_USAGE_PERCENT}"
aws cloudwatch put-metric-data --metric-name free-memory-mb --dimensions Instance=\${INSTANCE_ID} --namespace "WebServers" --value "\${FREE_MEM_MB}"
aws cloudwatch put-metric-data --metric-name io-wait --dimensions Instance=\${INSTANCE_ID} --namespace "WebServers" --value "\${IO_WAIT}"
EOF
# Making it executable
chmod 755 /etc/init.d/metrics
# Creating the AWS Client configuration directory
mkdir /root/.aws/
# Setting up the AWS Client to use the Instance Profile
cat  <<EOF > /root/.aws/config
[profile default]
credential_source = Ec2InstanceMetadata
region = eu-west-1
EOF
# Setting up crontab to execute the metrics script every minute
echo '*/1 * * * * root /etc/init.d/metrics' >> /etc/crontab
# Restarting crond
service crond restart
# Creating the chkconfig script for the cloudy container
cat <<EOF > /etc/init.d/cloudy
#!/bin/bash
#
# postgres       Bring up Cloudy
#
# chkconfig: 3 50 50
# description: PostgreSQL Database
case "\$1" in
start)
    docker pull docker.io/apahim/cloudy
    docker run -d --rm --name cloudy -p 8080:8080 docker.io/apahim/cloudy
    ;;
stop)
    docker stop cloudy
    ;;
status)
    docker container ls --filter name=cloudy
    ;;
restart|force-reload)
    cd "$CWD"
    $0 stop
    $0 start
    rc=$?
    ;;
*)
    echo $"Usage: $0 {start|stop|status|restart|force-reload}"
    exit 1
esac
EOF
# Setting the permissions for the postgres script
chmod 755 /etc/init.d/cloudy
# Installing docker
yum install -y docker
# Making sure docker is started on system boot
systemctl start docker
systemctl enable docker
# Allow ec2-user to run docker commands
usermod -aG docker ec2-user
# Setting up the PostgreSQL service
chkconfig cloudy on
# Starting postgres
service cloudy start
