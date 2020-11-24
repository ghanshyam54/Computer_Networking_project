# include <iostream>
#include <string>
using namespace std;


class Cars{
	public:
		string model;
		string brand;
		int year;
		void tinput (){
			cin >> model;
			cin >> brand;
			cin >> year;
		}
};

int main() {
  Cars c;
  c.model = "sx4";
  c.brand = "Mauriti";
  c.year = 2000;
  cout << c.model << '\n' << c.brand << '\n' << c.year ;
  c.tinput();
  cout << c.model << '\n' << c.brand << '\n' << c.year ;
  return 0;
}

