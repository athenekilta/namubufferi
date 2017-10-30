# Namubufferi
Namubufferi is a small e-commerce app for handling a small
store with mainly cash payments.

## Features
### Login
#### by magic links
1. User enters their email
2. Unique link is sent into their email
3. User can use that link once in the next 15 minutes to login

Good thing is that no password is needed, bad thing is that this is
slow method for the user.

#### by NFC tag
Problem is solved by allowing users to setup id that they can login with.
This needs some kind of device that acts as a keyboard and quickly types scanned uid.
This uid is then recognized and used for login.

Fast for user, but needs special hardware. (Or atleast
special app for normal hardware. Mobile browsers seem not to
supply api for nfc readers)


