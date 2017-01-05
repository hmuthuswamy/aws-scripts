yum install -y epel-release
yum install -y ansible
echo "localhost ansible_connection=local" >> /etc/ansible/hosts
mkdir /etc/ansible/templates
mkdir /etc/ansible/group_vars
echo "document_root: /apps/hello-http/html" > /etc/ansible/group_vars/all
############
echo "Running ansible playbook to setup httpd"
echo " "
echo " "
cd /etc/ansible; ansible-playbook -i hosts site.yml
echo "Testing hello.html"
echo " "
echo " "
echo " "
echo " "
curl -vl https://localhost/hello.html -k
