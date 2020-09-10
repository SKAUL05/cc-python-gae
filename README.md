# CodeComp Python Player


### Guide to deploy to Google App Engine using Github Actions

1. Setting up Google Cloud Project (skip if you already have a GCP Project)
-  Go to [Google Cloud](https://cloud.google.com/) and click on 'Get Started for FREE'.
-  Login using your gmail account, choose your country, accept terms and conditions and click Continue.
-  In the next step, fill your details, like account type, Name, Address, credit card details, tax information, etc. If you have old Gmail account and all the information is already there it would take it and you might not have to fill all the details.
-  After filling all the details click on "Start my free trial".
-  Google will setup your cloud account and in few seconds your Google Cloud Platform account will be ready to start deploying applications on it. It will look like below:

2. Creating Service Account and store credentials in Github

- Creating Service Account and provide owner access
  - Go to **Navigation Menu(Top left Corner) > IAM & Admin > Service Accounts**
  - Click on **Create Service Account**
  - Under **Service Account Details** provide service account **name** and **description** of your choice and click on **Create**
  - Under **Service Account Permissions** select **Project > Owner** Role and click on **Continue**
  - Keep **User Access Section** unchanged and click on **Continue**
