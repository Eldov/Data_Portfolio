## **The Project 3** <br/> 
This project has the goal of creating a data pipeline. </br>


### **Tools** <br/>
Cloud: AWS  
IaC: Terraform  
Storage Method: Data Lake (S3)  
Database: Amazon RDS  
Ingestion: AWS DMS and JSON files in S3  
Processing: Amazon EMR (Spark)  
Loading: Amazon Glue/Athena


### **The Data/Tables** <br/>
We will be working with 3 tables: Customers, Products and Orders.
These are being created in the RDS and the data will be randomised using the [application app-ingestion-sql.py](https://github.com/Eldov/Portfolio/blob/main/Project%203/app-ingestion-sql.py) file


### **The Virtual Environment** <br/>
Before starting with any script or the Cloud itself, I created a virtual environment where I would be free to install the required libs without affecting the global environment.  
~~~
python3 -m venv project3_venv  
~~~
The required libs can be found in the file [requirements.txt](https://github.com/Eldov/Portfolio/blob/main/Project%203/requirements.txt). In order to use it, you should activate the venv first:
~~~
.\project3_venv\Scripts\activate.ps1
~~~
Download the requirements file and then:
~~~
pip install -r requirements.txt
~~~

In case you are using Windows and facing problems activating the venv, make sure you have Set-ExecutionPolicy as Unrestricted.


### **The Terraform** <br/>
We will use Terraform to set all of our infrastructure. From every single bucket to each crawler we may use.  
But! To be able to do that we need to install Terraform itself.  
First, we have to install the aws-cli app:  
You can find the download link in here https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html  
Or, if you're using Windows as I am, you can install using the following command:
~~~
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
~~~

Once that's done, it's time to give it a try! Restart your terminal and use the following command:
~~~
aws configure
~~~
This command will enable you to set your credentials, Access Key ID, Access Key Secret and region, make sure you have them in hand!
To check if it worked, you can use this command (it should list your buckets in S3):
~~~
aws s3 ls
~~~

This is necessary so the Terraform will have your credentials to perform deployments in your account.  
  
Once thats done, download the Terraform here: https://developer.hashicorp.com/terraform/downloads  
Extract the terraform.exe (I put it inside my project3/terraform folder).  
Now we should have the first two .tf files, [main.tf](https://github.com/Eldov/Portfolio/blob/main/Project%203/terraform/main.tf) and [backend.tf](https://github.com/Eldov/Portfolio/blob/main/Project%203/terraform/backend.tf). The first defines the providers and the second where we will be saving our terraform state.  
Create a S3 bucket where you will storage the terraform state, this is the only bucket you will create by hand but it is necessary before we start.  
Once all is done, give the following command a try:
~~~
terraform.exe init
~~~

And you will have it succefully installed.  
Now we can create all our infrastructure, from buckets to instances and once they are done, we can plan/check our architecture with the command:
~~~
terraform plan
~~~
And actually build it with:
~~~
terraform apply
~~~

