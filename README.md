# bootstrap.py

This is the docker host bootstrap script, it does the following:

1. Configures a docker virtual network
2. Queries Route53 A records and ECR repository names
3. Pulls ECR images when a DNS host name and repository name match
4. Runs each image with corresponding IP address, hostname, and container name
