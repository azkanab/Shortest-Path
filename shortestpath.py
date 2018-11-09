from flask import Flask, render_template, request, jsonify
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import math
import json
from queue import *


class Node:
	name = 0
	value = 0

	def __init__(self, n, v):
		self.name = n
		self.value = v

	def setValue(self, v):
		self.value = v

	def getValue(self):
		return self.value

	def getName(self):
		return self.name

class Position:
	x = 0
	y = 0

	def __init__(self, xx, yy):
		self.x = xx
		self.y = yy

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def setX(self, xx):
		self.x = xx

	def setY(self, yy):
		self.y = yy

class SimpulHidup:
	name = 0
	gn = 0
	hn = 0
	path = []

	def __init__(self, n, g, h, p):
		self.name = n
		self.gn = g
		self.hn = h
		self.path = p

	def getName(self):
		return self.name

	def setName(self, n):
		self.name = n

	def getGN(self):
		return self.gn

	def getHN(self):
		return self.hn

	def setGN(self, g):
		self.gn = g

	def setHN(self, h):
		self.hn = h

	def getPath(self):
		return self.path

	def getCost(self):
		return (self.gn + self.hn)

	def setPath(self, p):
		self.path = p[:]

	def __lt__(self, other):
		return ((self.gn + self.hn) < (other.gn + other.hn))

	def addPath(self, p):
		self.path.append(p)
		return self.path

	def lookPath(self):
		print(self.path)	


def distance(n1, n2, coordinate):
	return math.sqrt((math.pow((coordinate[n1].getX() - coordinate[n2].getX()), 2) + math.pow((coordinate[n1].getY() - coordinate[n2].getY()), 2)))

def aStar(start, finish, arraykoordinat, matriksbobot):
	coordinate = []
	graph = []
	found = False

	for i in range(len(matriksbobot)):
		graph.append([])
		x = 0;
		for j in range(len(matriksbobot[i])):
			if (matriksbobot[i][j] != -1):
				tetangga = Node(x, matriksbobot[i][j])
				graph[i].append(tetangga)

			x = x + 1

	for coor in arraykoordinat:
		point = Position(coor[0], coor[1])
		coordinate.append(point)

	simpulHidup = PriorityQueue(1000)

	simpulHidup.put(SimpulHidup(start-1, 0, 0, []))

	while (not(found) and not(simpulHidup.empty())):
		temp = simpulHidup.get()

		if (int(temp.getName()) == finish-1):
			print("Hasil Path : ")
			temp.addPath(temp.getName() + 1)
			print("Node-node yang dilewati :", temp.getPath())
			print("Cost total untuk mencapai tujuan :", temp.getCost())
			found = True
		else :
			for adj in graph[int(temp.getName())]:
				gn = temp.getGN() + adj.getValue()
				hn = distance(adj.getName(), finish-1, coordinate)
				antrianTetangga = SimpulHidup(int(adj.getName()), gn, hn, [])
				antrianTetangga.setPath(temp.getPath())
				antrianTetangga.addPath(temp.getName() + 1)
				simpulHidup.put(antrianTetangga)

	return temp.getPath(), temp.getCost()

matriksbobot = []
arraykoordinat = []

app = Flask(__name__, template_folder=".")
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDebPwDC5rUy4cCF-uwMMvMty8ivXPrKPg"
GoogleMaps(app)

@app.route("/")
def mapview() :
	return render_template('mapsfix.html')

@app.route('/transfer' , methods = ['POST'])
def getData() :
	data = request.get_json(force = True)

	matriksbobot = data['graf']
	arraykoordinat = data['koordinat']
	simpul_awal = int(data['simpulawal'])
	simpul_tujuan = int(data['simpultujuan'])

	print(matriksbobot)
	print(arraykoordinat)
	print(simpul_awal)
	print(simpul_tujuan)

	#MENGHASILKAN PATH TERPENDEK DAN COSTNYA
	shortestPath = []
	totalCost = 0

	shortestPath, totalCost = aStar(simpul_awal, simpul_tujuan, arraykoordinat, matriksbobot)
	print(shortestPath)
	print(totalCost)

	data['hasil'] = shortestPath;
	data['jarakhasil'] = totalCost;

	return json.dumps(data)


if __name__ == "__main__":
	app.run(debug = True)





