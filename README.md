### Web-Shop-Product-Management

Web shop system to manage and control products price by applying Increase or Decrease as per Stock quantity

## How it works

simple web shop system that allow authenticated user to get list of products or specific product, update them and adjust price as per stock quantity dynamically from DB

- if stock quantity is 0, them price actually not adjust and remain the same as original 
- if stock quantity <= 5, them price adjust and increase by 5%
- if stock price > 5, them price dynamically adjust and decrease by 7%
## Schema
- `Users` table include users info like `username` and `password`
- `Products` table include product info like `name`, `description`, `stock_quantity` and `price`
	- Constraints
			- `Users` table `username` field must be `unique`
			- `Users` `id` unique , include index and auto generated
			- `Products` table `stock_quantity` must be >= `0`
			- `Products` table `price` must be > `0.0`
			- `Products` `id` unique , include index and auto generated
## API End Points 
|  HTTP Method| url  | Description|
|--|--|-|
|  POST| /api/products/ | create new product|
| GET| /api/products/| list of products with their price adjusted as per stock quantity | 
|GET} | /api/products/{`PRODUCT_ID`}| get specific product data,also price adjusted as per stock quantity|
| PUT | /api/products/{`PRODUCT_ID`}| update product data| 
|POST | /api/users/register | create new user|
|POST | /api/users/login/ | login with username and password |
| GET | /docs | Swagger docs for apis| 

## API Testing 
- `/docs` open swagger API which can be used for testing 
- [postman collection](https://api.postman.com/collections/6749950-55e0a4c0-cf3f-48e9-8903-89571c2bacbf?access_key=PMAT-01JP0VYV9QGF7CPJBJWBJ3KSNM) include API testing  

## How to Operate 
-	Prerequesists 
	-	 machine with python `v3.12`  
	-	 `sqlite3` installed as DB 
	- python library `poetry` for project management 
	- git as version control 
- Steps to Operate 
	- clone project repo from Github `git clone https://github.com/BakrFrag/Web-Shop-Product-Management`
	- move to project folder `cd Web-Shop-Product-Management`
	- create `.env` file at root folder and set `env variables` with their values 
	- create virtual env and activate project `poetry shell` 
	- install requirements from `pyproject.toml` `poetry add`
	- run local web server for dev or test `python src/app.py`
	- now application is listening and process requests on local host port `8000`
## ENV variables 
| Name | Description |
|--|--|
|  ALGORITHM| algorithm used |
|SECRET_KEY | used for password hashing| 

### Application 
- Application is based upon python `v3.12` with `fastapi` and `sqlite3` as DB 
- `Rate Limit` is apply globally over all end points with rate limit `20/minute`
- stream logging is used and make informative logging statements 
- `SECRETS` as managed by `python-decouple` library and read as `env variable`
- for `dev` purposes , sqlite3 as `RDBMS` 
- `requirements.txt` include all requirements and libraries for application 
- `routers` are applied on `Users` and `Products` , all routers are aggregated in `app.py` 
- asynchronous is used over all application , allow much more faster 



 