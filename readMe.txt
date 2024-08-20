                                   " This project is create for Track user's Income and Expenses "
                          ------------------------------------------------------------------------------

Database's Table Level:
-------------------------
level1: user, custom_field
level2: wallet(user:FK)
level3: account(wallet:FK, custom_field:M to M), client(wallet:FK, custom_field:M to M), category(wallet:FK, custom_field:M to M)
level4: transaction(account:FK, client:FK, category:M to M, custom_field:M to M)


Task:
--------------------------------
- create user, custom_field, wallet, account, client, category,transaction  models
- custom_field contains fields(like text, radio, select etc..,) with values in json format
- user have multiple wallets(1 to M relationships). foreign key.
- account, client, category models have multiple wallets(1 to M relationships). foreign key.
- account, client, category models have multiple custom_field(M to M relationships).
- transaction have multiple accounts, client(1 to M relationships). foreign key.
- transaction have multiple custom_field(M to M relationships).
- all records are stored in encryption format in DB when user get data at that time data is decrypted.

functionally:
--------------
- user registration with firstname, lastname, email, phone & password. email and phone must be unique.
- when user object is created then wallet object is automatically created with containing user_id, wallet_name = user.firstname, description=user.firstname, color=white
- user login and retuning JWT token (using simple-jwt library). if user profile is deleted than user can't perform login.
- logged-in user can create/update/delete/get/list a wallets.
- logged-in user can update/delete their profile. if user delete their profile than also disable wallets related to that user.
- logged-in user can create/update/delete/get/list an accounts, client, category model.
- logged-in user can create/update/delete/get/list a transaction model.
- when user create/update account, client, category model at that time check user's entered wallet field isDelete=False.
- add validation for all field.
- validation: in transaction model user entered incomeorexpense type at that time check user's entered category_type list
               if in list user select income type category than user have to select income type in transaction model, same as for expense.


Notes: Postmen collection is present for the purpose of getting information about the user, custom field, wallet, account,
        client, category, transaction API'S.(how APIs work with data)


Run Project:
---------------
---------------
1. create your virtual environment using "python3 -m venv venv".
2. activate virtual environment.
3. install project requirements using "pip install -r requirements.txt".
4. create your .env file and add project related environment variables.
5. run makemigrations command to generate migration files using "python manage.py makemigrations".
6. apply the changes in database using "python manage.py migrate".
7. create super user(admin) using "python manage.py createsuperuser".
8. run server to access endpoints using "python manage.py runserver".

