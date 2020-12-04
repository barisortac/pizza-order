Pizza Order API

This project was forked from: `https://github.com/vedant2222/cookiecutter-django-rest`

create project folder (name as you wish, here we say _pizzaorder_)  
`mkdir pizzaorder`  
`cd pizzaorder`

clone project  
`git clone git@github.com:brsrtc/pizza-order.git`  

copy .env.example to .env   
`cd pizza-order/pizzaorder/config`  
`cp .env.example .env`  


**TO RUN WITH DOCKER**  
first create a volume for docker  
`docker volume create --name=pizzaorder_db`  
`docker-compose up`


**TO RUN WITHOUT DOCKER**  
setup virtualenv  
`virtualenv venv_pizza --python=python3`  

activate virtualenv  
`. venv_pizza/bin/activate`  

now you are in virtualenv, install dependencies (requirements)   
`pip install -r requirements.txt`  

edit POSTGRES env variables as you wish  
(if you just use environment in example, 
you need to comment out docker section and uncomment specified part 
_"POSTGRES CONFIGURATION FOR LOCAL DEVELOPMENT"_)  

locate to manage.py, migrate and runserver  
`python manage.py migrate`  
`python manage.py runserver`


****TESTS****  
For now, tests are only written for **order** app, to run these:  
`python manage.py test order `

#### MINI API GUIDE
*****Enums*****  
**pizza** -> `"margarita","marinara","salami"`  
**order status** -> `received,preparing,on_delivery,delivered,canceled,turn_back`   
**pizza size** -> `small, medium, large`   

create customer  
endpoint: `api/customer/`  
method: `POST`  
payload: `{"name": "John"}`  
  
create order  
endpoint: `api/order/`  
method: `POST`  
payload: `{
  "customer_id": "<pk>",
  "order_items": [
    {
      "quantity": 10,
      "pizza": "salami",
      "pizza_size": "small"
    }
  ]
}`  


get order  
endpoint: `api/order/<pk>/`  
method: `get`  

get order list  
endpoint: `api/order/`  
method: `get`    

filter order list  
(ex: filter by status and customer id)  
endpoint: `api/order/?status=received&customer_id=1`  
method: `get`  

edit order  
endpoint: `api/order/<pk>/`  
method: `patch`  
payload: `{"status": "on_delivery"}`  

remove order  
endpoint: `api/order/<pk>/`  
method: `delete`  

add order item  
endpoint: `api/order/item/<pk>/`  
method: `put`  
payload: `[
    {
      "quantity": 10,
      "pizza": "salami",
      "pizza_size": "small"
    }
  ]`  

edit order item  
endpoint: `api/order/item/`  
method: `patch`  
payload: `{"quantity": 2}`  

delete order item  
endpoint: `api/order/item/<pk>/`  
method: `delete`  
  
 
### API Functionalities  
##### Create Order (order pizza):    
- Create pizza by desired flavor (margarita, marinara, salami), the number of pizzas and their size (small, medium, large).  
- Give customer detail in order response.  
- Track status of the order.    
- Create order with the same flavor of pizza but with different sizes multiple times.  
##### Update order:   
- Update the order details by flavours, count, sizes  
- Prevent order update if order status is not in prepared and received.  
- Update status of delivery. 
##### Remove order:    
##### Retrieve an order:**  
- Get order by pk.    
#####List orders:  
- Get all order at once.
- Filter orders by status and customer  


****Improvements for the project (TODO)****
- [ ] Add Authentication
- [ ] Add Swagger
- [ ] Seperate item of OrderItem as an app (for desserts, drinks etc.)
- [ ] Enable to add toppings for pizza
- [ ] Add prices for order items and calculation for order cost
