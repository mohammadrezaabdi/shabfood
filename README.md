# Shabfood

### Get Started

on your server machine:

clone this repo anywhere you want
```cd``` to the repo directory and run ```make build```

or

just simply run the following commands on your desire directory

```bash
    $ git clone https://sutgl.devopstools.ir/ce/analysisdesign_0001.1/students-teams/Group6/mvp/shabfood.git
    $ cd shabfood/
    $ make build
```

the server is going to be build and run, you can communicate it using the http://shabfood.ir domain

if you've changed the front source code; for updating the static files on nginx, you should rebuild the project by
```bash
    $ make build
```

if you want to run the server and up docker images, just run 
```bash
    $ make run
```

if you want to stop the server, just run 
```bash
    $ make stop
```

if you want to remove server docker images and clean
```bash
    $ make reset
```

if you have changed `/nginx/nginx.conf` file; for updating the nginx's .conf file in docker image, run
```bash
    $ docker exec -it `docker ps | grep nginx | awk '{print$1}'` nginx -s reload
```

`IMPORTANT`: your docker-compose version should be `1.29.2`

### setting up your local DNS
if you are deploying this server on a machine, you need to configure your local DNS, in a way that it returns your machine IP address 
whenever you are using the http://shabfood.ir domain

on your local machine, run:
```bash
   $ sudo echo "<your server ip address>   shabfood.ir" >> /etc/hosts
```  
there, you are good to go!

 just open any browser and start browsing our website or just simply click on http://shabfood.ir
 
### Additional Documents 

[frontend documentation](/front/README.md)

[backend documentation](/backend/README.md)

[database ER and tabled](/backend/db/docs/README.md)