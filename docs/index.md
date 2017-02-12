# Namubufferi


## Features
### LDAP integration
Users are synced from LDAP database to django's database and kept updated.
This is done by periodically calling `manage.py ldap_sync_users`

### Login by magic links
Login is primarily done by magic links sent to email:

1. User enters their email
2. Unique link is sent into their email
3. User can use that link once in the next 15 minutes to login

Good thing is that no password is needed.

### Login by NFC tag
Login by sending link to email is slow.

Problem is solved by allowing users to setup id that they can login with.
This needs some kind of device that acts as akeyboard and quickly types scanned uid.


## REST(like) api
### Products
* __POST__ `product/update/` Update or create product
    - __Requires staff user__
    - Arguments
        - name
        - category
        - price
        - inventory
        - hidden
        - barcode _optional_
    - Returns
        - __201__ Created new product
        - __200__ Updated existing product
        - __400__ Problem with arguments
        - __404__ Other problem
* __PUT__ `product/<id>/barcode/<barcode>/` Assign barcode to product
    - __Requires staff user__
    - Returns
        - __201__ Barcode was created
        - __200__ Barcode was reassigned from another product
        _ __400__ Product was not found
        - __404__ Some other error
* __GET__ `product/barcodes/` List all barcodes in db
    - Returns JSON with barcode->product_id dictionary
* __GET__ `product/barcode/discover/<barcode>` Try to guess product by its barcode
    - Uses external databases to search for product with this barcode
    - __Requires staff user__
    - Returns JSON with attributes:
        - `name`
    - Or __404__ if not found


### Users
* __GET__ `logout/`
* All following have these things in common:
    - On success, they return JSON with:
        - _balance_ The new balance user has
        - _modalMessage_ Message telling what happened in user friendly formatting
        - _message_ Html-message with same message as above
    - They return __404__ on errors
* __POST__ `buy/` Buy product
    - Does not neccessarily need login
    - Arguments
        - product_key
    - Returns
        - JSON
            - _transactionkey_ Key for transaction made
* __POST__ `deposit/` Deposit money to account
    - __Requires login__
    - Arguments
        - euros
        - cents
    - Returns
        - JSON
            - transactionkey
* __POST__ `cancel/` Cancel transaction
    - __Requires login__
    - Arguments
        - transaction_key
    - Returns
        - __204__ If there's problem with rights or transaction already canceled

### History
* __GET__ `history/` List of transactions for user
    - __Requires login__
    - Returns json with transaction-key
        - Contains most recent transactions for user
* __POST__ `receipt/`
    - __Requires login__
    - Arguments
        - transaction_key
    - Returns
        - JSON
            - customer
            - amount
            - timestamp
            - transactionkey
            - canceled
            - product
        - __404__ on errors

### User tags
* __POST__ `tag/auth/` Auth by tag
    - Parameters
        - tag_uid
    - Returns
        - On success
            - JSON with redirect-key to the next location
        - On error
            - JSON with errors-key
        - __404__ on mysterious errors
* __GET__ `tag/` Get tags for current user
    - __Requires login__
    - Returns
        - JSON with taglist-key containing html-list of keys
* __DELETE__ `tag/<uid>/`
    - __Requires login__
    - Parameters:
        - uid
    - Returns
        - __200__ Tag deleted
        - __404__ Other errors
* __POST__ `tag/<uid>/`
    - __Requires login__
    - Parameters:
        - uid
    - Returns
        - __201__ Tag created
        - __409__ Another tag with this uid exists
