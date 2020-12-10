# FlaskAppUsingRestAPI

# instructions to follow

This application is using python3 compiler.
Please use python3.5 or >3.5
Libraries used 
Flask
Flask-limiter
Pyjwt
Functools

Flask is used to create server 
PyJwt is used  for jwt authentication
Flask-limiter is used for throttling

The Application  will run on the local server and will use Port 5000. Make sure this port is available for communication.

After running the application, open your browser and run localhost:5000/

Enter the login details with enter username:<Anything>  and password:”Password”

It will return a JWT token.

Now you can go to localhost:5000/home?token=<your token>.
It will take you to the home page where you can upload an image file.

The jwt token is necessary for authentication

After selecting and uploading the file it will take you to localhost:5000/upload where you can see the uploaded image.

For both these interfaces I have added a throttling of 5/minute.
If you spam the upload button more than 5 times in a minute then it will show the throttling message.
