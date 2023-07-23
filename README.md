# API Routes
1. First, create your venv with pipenv command utilizing the pipfile which contains related libraries.
   ```console
       PS: > pipenv install
   ```
3. Make migrations
   ```console
       PS: >  python manage.py makemigrations
       PS: >  python manage.py migrate
   ```
2. The database is not populated, you may do it, first create an admin with the following command.
   ```console
       PS: > python manage.py createsuperuser
   ```
4. You may use either admin panel or related endpoints listed below with suitable payloads in order to populate the rest of the database; such as, menu-items,  users, and assigning user roles such as manager or delivery_crew, and customer. All users should be authenticated.
5. Run the server.
```console
    PS: > python manage.py runserver.
```
**Capabilities:**
1. The admin and manager can assign previously added users to the manager group with a *username* payload using POST method.
    - /api/groups/manager/users  
2. The admin and manager can access the manager group users with GET method, list all users.
    - /api/groups/manager/users  
3. The admin and manager can remove the user with a UserId from the manager group users with DELETE method using detail-view.
    - /api/groups/manager/users/{userId} 
4. The admin can add new menu items with POST method.
    - /api/menu-items
5. The admin can add categories.
    - /api/categories
6. Managers can update the item of the day by changing only the *featured* field of a specific menu-item with PATCH method.
    - /api/menu-items/{menuItem}
7. Managers can assign users to the delivery crew with POST method.
    - /api/groups/delivery-crew/users
8. Managers can assign specific orders to the delivery crew by changing the *delivery_crew* field of the *Order* table with PATCH method.
    - /api/orders/{orderId}
9. The delivery crew can access orders only assigned to them with GET method.
    - /api/orders
10. The delivery crew can update an order as delivered by changing the *status* field of the *Order* table.
    - /api/orders/{orderId}
11. Customers can register with a username and password payload using the POST method. The djoser automatically handles it with a suitable endpoint.
    - /api/users
12. Customers can log in using their username and password as payloads and get access tokens with the POST method.
    - /api/token/login
13. Customers can browse all categories with GET method.
    - /api/categories
14. Customers can browse all the menu items at once with GET method.
    - /api/menu-items 
15. Customers can browse menu items by category with GET method.
    - /api/menu-items/?search={categoryName}
    <br>or,
    - /api/menu-items/?category={categoryId}
    <br>or, 
    - /api/menu-items/?category__title={categoryTitle}
16. Customers can paginate menu items with GET method.
    - /api/menu-items/?page=3
17. Customers can sort menu items by price with GET method
    - /api/menu-items/?ordering=price
18. Customers can add menu items to the cart with a payload of menuitem={menuitemId} and quantity by using PATCH method.
    - /api/cart/menu-items
19. Customers can access only their own items in the cart with GET method. 
    - /api/cart/menu-items
20. Customers can place orders with a POST request to the endpoint, which will erase the cart item.
    - /api/orders
21. Customers can browse their own orders with GET method.
    - /api/orders
A summary of API Endpoints:
+ User Registration and Token Generation endpoints, exploiting djoser library.
    - /api/users
    - /api/users/users/me/  
    - /api/token/login/  
+ Menu Item management endpoints:
    -	/api/menu-items  
    -	/api/menu-items/{menuItem}  
+ User group management endpoints:
    - /api/groups/manager/users
    - /api/groups/manager/users/{userId}
    - /api/groups/delivery-crew/users
    - /api/groups/delivery-crew/users/{userId}
+ Cart management endpoints:
    - /api/cart/menu-items
+ Order management endpoints:
    - /api/orders
    - /api/orders/{orderId}
