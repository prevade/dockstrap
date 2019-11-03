#!/usr/bin/python

import boto3
import os
import sys

# Route53, ECR, and EC2 client objects
r53_client = boto3.client('route53')
ecr_client = boto3.client('ecr')

# Route53 configuration paramters
r53_hostedzoneid = 'Z3SDCG6L1NXBOI'
r53_resourcerecordsets = r53_client.list_resource_record_sets(HostedZoneId=r53_hostedzoneid)

# ECR configuration paramters
ecr_registryid = '935044474330'
ecr_uri = ecr_registryid + ".dkr.ecr.us-east-1.amazonaws.com/"

# Login to ECR
ecr_client.get_authorization_token()

# Docker configuration parameters
docker_subnet = "172.28.0.0/16"
docker_network = "prevade0"

# Query ECR for repository names
ecr_reg = ecr_client.describe_repositories(registryId=ecr_registryid)

# Create Docker subnet
os.system("docker network create --subnet %s %s" % (docker_subnet,docker_network))

# Map ECR repository name to corresponding Route53 FQDN A record
for resourcerecordsets in r53_resourcerecordsets['ResourceRecordSets']:
        for repositories in ecr_reg['repositories']:
                fqdn = str(resourcerecordsets['Name'])[:-1]
                docker_address = str(resourcerecordsets['ResourceRecords'][0]['Value'])

                # Pull image and initialize container with corresponding IP when FQDN and repository name match
                if fqdn == repositories['repositoryName']:
                        os.system("docker pull %s.dkr.ecr.us-east-1.amazonaws.com/%s" % (ecr_registryid, fqdn))
                        os.system("docker run -dit --restart always --ip %s --network %s --hostname %s --name %s %s%s" % (docker_address, docker_network, fqdn, fqdn, ecr_uri, fqdn))
                        break
