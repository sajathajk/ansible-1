# Installation

Run `pip install -r requirements.txt`

Put the ansible_ec2.pem to ~/.ssh/ansible_ec2.pem and chown it to 0400

# Access to RDS

## SSH tunnel through bastion

`ssh -i ~/.ssh/ansible_ec2.pem -N -L 5432:abc.rds.amazonaws.com:5432 ec2-user@xyz.compute.amazonaws.com`

* first occurrence of `5432` is the target port on your local machine
* `abc.rds.amazonaws.com:5432` is the hostname of RDS instance with postgres port
* `xyz.compute.amazonaws.com` is the hostname of the bastion node

## Connecting to RDS

Use your favorite PostgreSQL client and point it to `localhost:5432`, for example:

`psql -U ChosenOne -h localhost postgres`

# Access to EMR

## Start EMR cluster

    ansible-playbook -i inventories/dev/ playbooks/emr.yml

## Socks proxy to a running EMR cluster

    aws emr socks --cluster-id $(aws emr list-clusters --active --output=json | jq -r '.Clusters[0].Id') --key-pair-file ~/.ssh/ansible_ec2.pem

## Stop the EMR cluster

    aws emr terminate-clusters --cluster-ids $(aws emr list-clusters --active --output=json | jq -r '.Clusters[0].Id')