# YottosShopifyApp

- Create a Python virtual environment.

    virtualenv  -p python3.5 env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e "."
    
- Activate virtualenv in console

    source env/bin/activate



mysql -u root -p
CREATE DATABASE shopify CHARACTER SET utf8;
CREATE USER 'shopify_yottos'@'%' IDENTIFIED BY 'shopify_yottos';
GRANT ALL PRIVILEGES ON * . * TO 'shopify_yottos'@'%';
FLUSH PRIVILEGES;

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'vthjdbyu';
FLUSH PRIVILEGES;

./webp-convert.sh yottos_shopify/static/images/


ssh root@205.196.80.10