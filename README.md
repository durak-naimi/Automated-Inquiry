# Automated-Inquiry

The project aims to utilize Azure AI features to automated customer enquiry system in travel industry (Indian Railway)
Artificial Intelligence can be used to automate Manual enquiry system by featuring Azure AI services.
For the purpose of project we have utilised 3 Azure AI services - Azure Speech, LUIS and QnA maker

The AI powered system aims on 2 objectives.
a. Similar to manually operated system
b. Simple to use

By leveraging Azure Speech and LUIS, first objective has been achieved. As the system takes in input from user in spoken format and using LUIS it correctly utilises the intent of the user such as (GetPlatform, GetTime, GetTrain). The Azure Speech has been trained to recognize the names of Indian Trains using manual recordings and transcript uploaded as "Recordings.zip"

By leveraging QnA maker, second objective is achieved as the system can be updated real time by editing excel sheet (uploaded as KnowledgeBase.xlsx) and uploading it as knowledge base to QnA maker. This process Takes hardly a minute. Moreover the system does not require any coding once it is up and running, data entry is the only requiement which makes it very easy to operate.

Files in the Projects
1. Explaination Video - A 3 minute Demo video explaining the working of a project
2. KnowledgeBase.xslx - Excel file uploaded to QnA maker as Knowledge Base
3. Myrecordings.zip - Custom recording for training azure speech to recognize train name
4. load.py - parsing user input saved in json format and passing it to LUIS
5. main.py - consist of main code of all the three services
6. read.json - to store user input in {"statement":"<user input">} format
7. TrainIntel.json - Trained LUIS export file


How to Install?

1. Install the following modules
   pip install python-decouple
   pip install azure-cognitiveservices-speech
   pip install pytz
   pip install DateTime
   pip install Requests
3. Clone the repository
4. Create Speech Sercive in Azure - enter the key and region in '.env'
5. Go to speech studio -->create custom speech --> upload myrecordings.zip as speech dataset
6. Create luis app in azure using 'Trainintel.json'. Publish and copy paste the luis url ending with 'your query here' in '.env'
7. Create a qna maker app in azure. Import KB using KnowledgeBase.xslx
8. get the url and endpoint key of Qna Maker after publishing from curl request and paste it in '.env'
9. Run main.py
