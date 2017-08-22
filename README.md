This is the docker host bootstrap script, which does the following:

1. Configures a docker virtual network
2. Queries Route53 A records and corresponding ECR repository names
3. Pulls images from ECR when a DNS host and repository match is found
4. Initializes each image with corresponding IP address respectively
5. Initializes each image with corresponding hostname respectively
6. Initializes each image with corresponding container name respectively
