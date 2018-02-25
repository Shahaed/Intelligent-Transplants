import csv
from DataSynth import *
import numpy as numpy
import random



def match():
	print(donor)
	print()
	print(recipient)



def main():
	global donor
	donor=[]
	global recipient
	recipient=[]
	with open('data.csv', 'w') as csvfile:
		fieldnames=['id','dr', 'age','blood', 'gender', 'organ', 'ethnicity', 'bmi','lod' ,  'acceptance'] 
		writer = csv.DictWriter(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL, fieldnames=fieldnames)

		
		writer.writeheader()

		for i in range(0, 100):
			e=ethnicity()
			r = numpy.random.rand()
			if (r - 0.0110348736356688) <= 0:
				age = int(numpy.random.rand() * 2)
			elif (r - (0.0260938264819792+0.0110348736356688)) <= 0:
				age = 1 + int(numpy.random.rand() * 5)
			elif (r - (0.0221229894631985+0.0260938264819792+0.0110348736356688)) <= 0:
				age = 6 + int(numpy.random.rand() * 5)
			elif (r - (0.0961622684608713+0.0221229894631985+0.0260938264819792+0.0110348736356688)) <= 0:
				age = 11 + int(numpy.random.rand() * 7)
			elif (r - (0.3612242269147870+0.0961622684608713+0.0221229894631985+0.0260938264819792+0.0110348736356688)) <= 0:
				age = 18 + int(numpy.random.rand() * 17)
			elif (r - (0.2702968681568760+0.3612242269147870+0.0961622684608713+0.0221229894631985+0.0260938264819792+0.0110348736356688)) <= 0:
				age = 35 + int(numpy.random.rand() * 15)
			elif (r - (0.1806644969042240+0.2702968681568760+0.3612242269147870+0.0961622684608713+0.0221229894631985+0.0260938264819792+0.0110348736356688)) <= 0:
				age = 50 + int(numpy.random.rand() * 15)
			elif (r - (0.0324004499823957+0.1806644969042240+0.2702968681568760+0.3612242269147870+0.0961622684608713+0.0221229894631985+0.0260938264819792+0.0110348736356688)) <= 0:
				age = 65 + int(numpy.random.rand() * 35)
			else:
				age = 100


			LOD='n/a'
			e=ethnicity()
			g=gender(age)
			BMI=bmi(age, g)
			AR='n/a'
			if(i%10==0):
				DR='D'
				BT=donorABO(e,g)
				o=organ(age, g)
				LOD=liveOrDead(age, recipABO(o))
			else:
				DR='R'
				BT=recipABO(o)
				age=recipAGE(age)
				o=organ(age, g)
				AR=acceptionRate(age, g, o, e, BT)
			
			if(DR=='R'):
				writer.writerow({'id':i,'dr':DR, 'age':age,'blood':BT, 'gender':g,'organ':o, 'ethnicity':e, 'bmi':BMI, 'lod':LOD, 'acceptance':AR})
				recipient.append([i, DR, age, BT, g, o, e, BMI, LOD, AR])

			else:
				writer.writerow({'id':i,'dr':DR, 'age':age,'blood':BT, 'gender':g,'organ':o, 'ethnicity':e, 'bmi':BMI, 'lod':LOD, 'acceptance':AR})
				donor.append([i, DR, age, BT, g, o, e, BMI, LOD, AR])


		match()




		

if __name__ == '__main__':
	main()