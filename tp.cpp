#include <iostream>
# include <cmath>
using namespace std;

void printcar(string *cars){
	for (int i=0 ;i<3;i++){
		cout << cars[i];
	}
}


int main() {
	string car[3] = {"BMW","Maruti","Ford"};
	string *sample = car;
	printcar(sample);
	
	return 0;
}
