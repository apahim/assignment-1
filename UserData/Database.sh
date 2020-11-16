#!/bin/bash
# Adding the VIP
cat <<EOF > /etc/sysconfig/network-scripts/ifcfg-eth0:0
DEVICE=eth0:0
IPADDR=10.10.10.10
NETMASK=255.255.255.0
ONBOOT=yes
EOF
# Bringing the new VIP up
ifup eth0:0
# Installing docker
yum install -y docker
# Making sure docker is started on system boot
systemctl start docker
systemctl enable docker
# Allow ec2-user to run docker commands
usermod -aG docker ec2-user
# Directory to mount the PostgreSQL data NFS volume
mkdir /data
# Creating the chkconfig script for the PostgreSQL container
cat <<EOF > /etc/init.d/postgres
#!/bin/bash
#
# postgres       Bring up PostgreSQL
#
# chkconfig: 3 50 50
# description: PostgreSQL Database
case "\$1" in
start)
    mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport ${DatabaseEFS}.efs.${AWS::Region}.amazonaws.com:/ /data
    docker run -d --restart=always --name postgres -p 5432:5432 -v /data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres postgres
    ;;
stop)
    umount /data
    docker stop postgres
    docker rm postgres
    ;;
status)
    docker container ls --filter name=postgres
    ;;
*)
    echo $"Usage: $0 {start|stop|status|restart|force-reload}"
    exit 1
esac
EOF
# Setting the permissions for the postgres script
chmod 755 /etc/init.d/postgres
# Setting up the PostgreSQL service
chkconfig postgres on
# Starting postgres
service postgres start