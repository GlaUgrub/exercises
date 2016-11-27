/* First training header file for Stroustup exercises*/

#include <string>
#include <complex>

char ch; // definition

std::string s; // definition

int count = 1; // definition

const double pi = 3.14; // definition

extern int error_number; // declaration only
int error_number; // definition

const char* name = "Me"; // definition
const char* season[] = {"spring", "summer", "autumn", "winter"}; // definition

struct Date // definition
{
    int d, m, y;
};

int day(Date* p) // definition
{
    return p->d;
}

double SqrtMy(double); // declaration only
double SqrtMy(double in) // definition
{
    return in * in;
}

template<class T> T abs(T a) // definition
{
    return a >= 0 ? a : -a;
}

typedef std::complex<short> Point; // definition

struct User; // declaration only
struct User // definition
{
    std::string name;
    std::string surname;
    std::string login;
    std::string password;
    std::string cellNumber;
    unsigned int id;
};

enum Beer // definition
{
    Carlsberg,
    Tuborg,
    Thor
};

namespace NS  // definition
{
    int a;
}