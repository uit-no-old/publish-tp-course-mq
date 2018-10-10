**10.10.2018 - Øyvind - MOVED TO https://github.com/uit-no/publish-tp-course-mq**


# Publish TP-course changes to RabbitMQ

python 3.6

## Installation/setup tp-canvas.uit.no

#### Install python 3.6

Add repo:  
`sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm`

Update yum:  
`sudo yum update`

Download and install python:  
`sudo yum install -y python36u python36u-libs python36u-devel python36u-pip`

Upgrade pip:  
`sudo pip3.6 --proxy http://swproxy.uit.no:3128 install --upgrade pip`

install packages:  
`sudo pip3.6 --proxy http://swproxy.uit.no:3128 install pika requests`

#### Checkout script
`git clone git@bitzer.uit.no:sua/publish-tp-course-mq.git /home/sua/publish-tp-course-mq`

#### Setup Crontab
`crontab -e`

Insert into crontab file:
```
MQ_USER=[insert username]
MQ_PASS=[insert password]

* * * * * /bin/bash -l -c 'cd /home/sua/publish-tp-course-mq && python3.6 publish_tp_course.py'
```
