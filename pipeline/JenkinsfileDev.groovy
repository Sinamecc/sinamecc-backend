pipeline {
  agent any;
  environment {
    DJANGO_SETTINGS_MODULE = "config.settings.ecs_aws"
    DATABASE_HOST = "sinamecc.copuo03vfifp.us-east-2.rds.amazonaws.com"
    DATABASE_NAME = "sinamecc_dev_2020"
    DATABASE_CREDS  = credentials('sinamecc-dev-dba')
    DATABASE_URL    = "postgres://${DATABASE_CREDS}@${DATABASE_HOST}:5432/${DATABASE_NAME}"

    DEFAULT_REGION = "us-east-2"
    BASE_ECR = "973157324549.dkr.ecr.$DEFAULT_REGION.amazonaws.com"
    ENVIRONMENT = "dev"
    APP = "sinamecc-backend"
    ECS_CLUSTER_NAME = "sinamecc-cluster-$ENVIRONMENT"
    ECS_SERVICE_NAME = "$APP-$ENVIRONMENT"
  }

  stages {
    stage("Build and Test") {
      steps {
        withPythonEnv('/bin/python3.7') {
          echo "Step: Upgrading pip"
          sh 'pip install --upgrade pip'

          echo "Step: Updating requirements"
          sh 'pip install -r requirements.txt'

          echo "Step: Running Tests"
          sh 'python manage.py test'

          echo "Step: Running Migrations"
          sh 'python manage.py migrate'
        }
      }
    }

    stage ("Building docker image") {
      steps {
        echo "Step: Building docker image"
        sh 'docker build -t $BASE_ECR/$ENVIRONMENT/$APP:$ENVIRONMENT .'
      }
    }

    stage ("Pushing Images and Updating Service") {
      steps {
        echo "Step: Login ECR"
        sh '/usr/local/bin/aws ecr get-login-password --region $DEFAULT_REGION | docker login --username AWS --password-stdin $BASE_ECR/$ENVIRONMENT/$APP'

        echo "Step: Pushing base image"
        sh 'docker push $BASE_ECR/$ENVIRONMENT/$APP:$ENVIRONMENT'

        echo "Step: Restarting ECS Service"
        sh '/usr/local/bin/aws ecs update-service --cluster $ECS_CLUSTER_NAME --service $ECS_SERVICE_NAME --force-new-deployment'

        echo "Step: Waiting on Service to be healthy"
        sh '/usr/local/bin/aws ecs wait services-stable --cluster $ECS_CLUSTER_NAME --service $ECS_SERVICE_NAME'
      }
    }
  }
}
