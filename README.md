# Installation

Run `pip install -r requirements.txt`

# Usage

`ansible-playbook site.yml`

# Access to RDS

## SSH tunnel through bastion

`ssh -i ~/.ssh/ansible_ec2.pem -N -L 5432:abc.rds.amazonaws.com:5432 ec2-user@xyz.compute.amazonaws.com`

* first occurrence of `5432` is the target port on your local machine
* `abc.rds.amazonaws.com:5432` is the hostname of RDS instance with postgres port
* `xyz.compute.amazonaws.com` is the hostname of the bastion node

## Connecting to RDS

Use your favorite PostgreSQL client and point it to `localhost:5432`, for example:

`psql -U ChosenOne -h localhost postgres`
