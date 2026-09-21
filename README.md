# aws-ec2-django-nginx-deployment
Deploying a Django web application on AWS EC2 using Gunicorn, Nginx, Application Load Balancer and Auto Scaling.


# AWS EC2 Django Nginx Deployment

A hands-on AWS deployment project demonstrating how to deploy a Django web application on Amazon EC2 using Gunicorn and Nginx, with AWS networking, Application Load Balancer and Auto Scaling.

## 🚀 Project Overview

This project demonstrates the deployment of a Django application on AWS using a production-style web server architecture.

The application is deployed on Amazon EC2 and served through Gunicorn and Nginx. An AWS Application Load Balancer is used to distribute incoming HTTP traffic to the EC2 application instances.

The project also includes Auto Scaling configuration to allow the application tier to scale based on demand.

## 🏗️ Architecture

```text
                         Internet
                            |
                            |
                    Application Load
                       Balancer
                            |
                 +----------+----------+
                 |                     |
                 v                     v
              EC2 #1                EC2 #2
                 |                     |
                 |                     |
              Nginx                 Nginx
                 |                     |
                 v                     v
             Gunicorn              Gunicorn
                 |                     |
                 v                     v
              Django                Django
                 |                     |
                 +----------+----------+
                            |
                            v
                    PostgreSQL / RDS
```

### Application Flow

```text
Client
   |
   v
AWS Application Load Balancer
   |
   v
Nginx :80
   |
   v
Gunicorn :8000
   |
   v
Django Application
   |
   v
PostgreSQL Database
```

## 🛠️ Technologies Used

### Application

* Python
* Django
* PostgreSQL
* Gunicorn

### AWS

* Amazon EC2
* Application Load Balancer
* Auto Scaling Group
* VPC
* Security Groups
* IAM
* Amazon RDS PostgreSQL
* Amazon S3

### Web / Linux

* Nginx
* Amazon Linux
* Linux system administration
* systemd

## 🔧 Implementation

### 1. AWS Infrastructure

Created the AWS networking and compute infrastructure required to host the Django application.

Implemented:

* VPC
* Public and private subnets
* Route tables
* Security groups
* EC2 instances
* Application Load Balancer
* Target Group
* Auto Scaling Group

### 2. Django Deployment

Deployed the Django application to an EC2 instance.

The application environment was configured with:

* Python
* Python virtual environment
* Django
* Gunicorn
* PostgreSQL connectivity
* Environment-based configuration

### 3. Gunicorn

Configured Gunicorn as the application server responsible for running the Django application.

Example:

```bash
gunicorn --bind 0.0.0.0:8000 config.wsgi:application
```

Gunicorn runs the Django application on port `8000`.

### 4. Nginx

Configured Nginx as the web server and reverse proxy in front of Gunicorn.

```text
Client
   |
   v
Nginx :80
   |
   v
Gunicorn :8000
   |
   v
Django
```

Nginx handles incoming HTTP requests and forwards application requests to Gunicorn.

### 5. Application Load Balancer

Configured an AWS Application Load Balancer to distribute traffic to the Django application instances.

Configured:

* ALB
* Listener
* Target Group
* Health Check
* EC2 target registration

The target group forwards traffic to the Django/Gunicorn application.

### 6. Auto Scaling

Configured an Auto Scaling Group to manage the EC2 application instances.

The architecture allows additional application instances to be launched when required while keeping the application behind the Application Load Balancer.

### 7. Database

Configured the Django application to connect to PostgreSQL using environment-based database configuration.

Example configuration:

```text
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
```

This keeps database credentials outside the application source code.

### 8. Static Files

Configured Django static-file handling using:

```bash
python manage.py collectstatic
```

Static files can be served separately from application requests using Nginx or Amazon S3.

## 🔐 Security

Implemented AWS security controls using Security Groups.

The intended traffic flow is:

```text
Internet
   |
   v
ALB :80
   |
   v
EC2 :80
   |
   v
Gunicorn :8000
```

The application server does not need to expose Gunicorn directly to the public internet.

Database access is restricted to the application tier rather than allowing unrestricted internet access.

## 🩺 Health Checks

Configured the ALB Target Group to monitor the health of the Django application.

The ALB periodically sends HTTP health-check requests to the application target.

```text
ALB
 |
 | HTTP Health Check
 v
EC2 :8000 / Application
 |
 +---- HTTP 200 ----> Healthy
```

## 🐛 Troubleshooting Experience

During deployment, several real-world AWS and application issues were investigated and resolved.

### ALB Health Check

The ALB initially reported unhealthy targets.

Investigated:

* Security Group rules
* Target Group configuration
* Application port
* Django `ALLOWED_HOSTS`
* Health-check path
* Gunicorn availability

### Django Static Files

The application initially returned an incorrect response when loading CSS through the ALB.

Investigated:

* Django `STATIC_URL`
* `STATIC_ROOT`
* `collectstatic`
* Nginx static-file configuration
* Response content type
* S3/static-file architecture

### AWS Connectivity

Investigated connectivity between AWS components including:

* EC2
* ALB
* Application ports
* Security Groups
* AWS Systems Manager

These troubleshooting activities helped validate the complete request path from the load balancer to the Django application.

## 📁 Project Structure

```text
aws-ec2-django-nginx-deployment/
│
├── django-app/
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   ├── templates/
│   └── ...
│
├── nginx/
│   └── django.conf
│
├── systemd/
│   └── django.service
│
├── scripts/
│   └── deployment.sh
│
└── README.md
```

## 🎯 What I Learned

Through this project I gained hands-on experience with:

* Deploying Django applications on AWS EC2
* Linux server administration
* Gunicorn application serving
* Nginx reverse proxy configuration
* AWS Application Load Balancer
* Target Groups and health checks
* Auto Scaling Groups
* AWS VPC networking
* Security Groups
* PostgreSQL connectivity
* Django production configuration
* Static-file management
* AWS Systems Manager
* Troubleshooting application and infrastructure connectivity

## 🔮 Future Improvements

Planned improvements for this project include:

* Serve static files with S3 & Cloudfront instead of nginx
* Containerize the Django application using Docker
* Push the image to Amazon ECR
* Deploy the container using Amazon ECS
* Deploy the application to Amazon EKS
* Automate infrastructure using Terraform
* Implement CI/CD using GitHub Actions
* Add centralized logging and monitoring
* Add HTTPS using ACM and the Application Load Balancer

## 📌 Project Goal

The goal of this project is to demonstrate practical experience deploying and operating a Python Django application on AWS using commonly used cloud, Linux and DevOps technologies.
