## start setup with
docker-compose up -d --build
# on newer setup : 
## migrate/superuser
docker exec -it <django-container-id> python manage.py migrate
docker exec -it <django-container-id> python manage.py createsuperuser


-------------
## standalone setup cmds
docker build -t munchmate-app .

# standalone sql. use stronger password for setup
docker run --name mysql-db -e MYSQL_ROOT_PASSWORD=rootpass -e MYSQL_DATABASE=munchmate_db -e MYSQL_USER=munchuser -e MYSQL_PASSWORD=munchpass -p 3306:3306 -d mysql:latest

# root user only
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=your_root_password -p 3306:3306 -d mysql:latest


## preloading recipe table
docker cp recipes_preloaded.sql mysql-db:/tmp/recipes_preloaded.sql
docker exec -it mysql-db bash -c "mysql -u root -p'test123' munchmate < /tmp/recipes_preloaded.sql"


# or access your docker sql
docker exec -it mysql-db mysql -u root -p"password"

# manually add the docker container to a network
sudo docker network connect munchmate_default munchmate-web-1



# ubuntu setup
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable --now docker


# simulate api endpoint can be triggered from the browser console by
fetch("base_url/api/simulate/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        count: 5
    })
})
.then(response => response.json())
.then(data => console.log("Success:", data))
.catch(error => console.error("Error:", error));