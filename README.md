## Inspiration
Everyday twenty-two people die waiting for a transplant. Around 65% of organs are rejected by centers while 10% of accepted organs are not used in transplants. Rejections occur due to low confidence from doctors about compatibility, time spent waiting for decisions being made, and human error. This $34B industry is missing many chances at saving lives and money. UNOS stores data for the thousands of transplants that occur and current medical charts have hundreds of data points on patients. This seemed like a perfect opportunity to let machines solve this problem.  

## What it does
Our system takes in donor and recipient medical data and predicts the viability of a transplant succeeding. The model was trained with synthetic data based on worldwide organ transplant trends. We have a system for both UNOS (and other administrators) and doctors to predict the chances of success (using many data points such as antibodies, blood type, age, ethnicity, distance, etc.) 

## How we built it
We used keras to iterate and improve our deep learning model quickly. To generate the synthetic data we used python. The frontend was built using angular and react.

## Challenges we ran into
Our product is centered around historic data related to organ transplants, and the biggest challenge that we faced was gaining access to this information. Since this is a highly regulated field, the government and organizations involved in organ transplants tend to keep this information highly confidential. However, in order to replicate original trends, we created synthetic data based on factual information, and used these probabilities to populate our data set. 

## Accomplishments that we're proud of
Working together to solve real world problems. 

#Prizes

##Information overload 
We use a deep learning model to organize transplant data to make it univerally accesible and useful for transplant clinicians. 

##Head in the clouds 
We use the google cloud platform, aws, and firebase to deploy and deliver deep learning predictions.

##Hard core, Soft ware 
We used tensorflow to build our deep learning model to help bring the potential of machine learning to human health. 

##Data Storage and Migration 
We improved transplant data analytics.

##Fund Your Dreamscape 
We used the tensorflow library to serve analytics to doctors.

##Go Further 
We connect donors with recipients and allow organs to have an easier trip to the recieving hospital with confidence that it will get to its new home.

##Walking Your Dog Food to Market
Our open source project allows the world to collaborate on saving transplant patients.

##Making Sense Out of Complicated Clinical Information 
We have an open source healthcare analytics project that allows our deep learning model to improve with new and better transplant data. This allows hospitals to use their own EMR data on our open source project.


