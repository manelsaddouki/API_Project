# Rest-API 
This project is part of the Web Service class, focusing on the assigned theme of 'Politics.' The objective is to design and implement an API centered around a political topic.

For my project, I chose to develop an API that manages funds allocated by countries to address specific issues such as the effect of war (e.g., Palestine/Ukraine), responses to natural disasters (e.g., Morocco), or limiting the impacts of climate change (e.g., Brazil).

As part of this project, I have created a prototype for the front end. Now, we have a user-friendly interface that facilitates interaction with the API. The live version of my web service is accessible at [https://lossanddamagefunds.onrender.com/](https://lossanddamagefunds.onrender.com/).

The development process involved various libraries and tools:

- **For the backend and development:** Python served as the primary programming language, supported by several libraries such as Flask, Flask-Smorest, Migrate (from Flask-Migrate), JWTManager (Flask-JWT), Secrets, Passlib.hash, SQLAlchemy (from Flask-SQLAlchemy), Flask.Views, and Schemas. For testing, Insomnia and Postman were employed. Plus, Swagger was employed for documentation and other APIs have been integrated.
- **For the frontend and deployment:** HTML, CSS, and JavaScript were the languages used. Gunicorn was the library of choice for server deployment. Render, ElephantSQL, and pgAdmin4 (PostgreSQL) were tools implemented for deployment and production database manipulation.
