/* First training header file for Stroustup exercises*/

#include <string>
#include <complex>

/*Declarations and difinitions from task 4.1*/
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

/*Declarations and difinitions from task 5.1*/

char* pC = "Hello";
int arr[10] = {0, 1, 2};

// (*pStrArr) means that pStrArr is a poiner to some object with base type [char]. Nature of this object is clarified outside of round brackets - it's *char[4].
char *(*pStrArr)[4];
char *strArr[] = {"a", "bb", "ccc", "dddd"};
char *(*pStrArrDef)[4] = &strArr;

char** ppC = &pC;
const int constInteger = 10;
int const * pToConstInt = &constInteger;
int * const pConstToInt = arr;
