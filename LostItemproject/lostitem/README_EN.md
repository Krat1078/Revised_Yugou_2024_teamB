# LostItem APP function

students log in, register lost items, send emails, and delete registered items.

学生のログイン、遺失物の登録、メールの送信、登録した物の削除などを備えている。


# Backend API interface

## 1. Homepage (Index)
URL: /
Method: GET
Description: Returns the homepage of the site.
## 2. Password Reset
URL: /restartPassword/
Method: POST
Description: Initiates the password reset process by sending a reset link to the user's email.
## 3. Login
URL: /login/
Method: POST
Description: Logs in a user with their username and password. Redirects based on user type (admin or regular user).
## 4. Logout
URL: /logout/
Method: POST
Description: Logs out the currently authenticated user and ends the session.
## 5. Sign Up
URL: /signup/
Method: POST
Description: Allows a new user to register by providing their username, email, and password.
