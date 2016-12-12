/* First training cpp file for Stroustup exercises*/

#include <iostream>
#include <limits>
#include "stroustrup.h"

/*functions for exercise 4.1*/
void HelloWorld()
{
    std::cout << "Hello world" << '\n';
}

/*functions for exercise 4.3*/
void PrintSizesOfTypes()
{
    std::cout << "Size of char        = " << sizeof(char) << "\n";
    std::cout << "Size of short       = " << sizeof(short) << "\n";
    std::cout << "Size of int         = " << sizeof(int) << "\n";
    std::cout << "Size of long        = " << sizeof(long) << "\n";
    std::cout << "Size of float       = " << sizeof(float) << "\n";
    std::cout << "Size of double      = " << sizeof(double) << "\n";
    std::cout << "Size of long double = " << sizeof(long double) << "\n";
    std::cout << "Size of bool        = " << sizeof(char) << "\n";
    std::cout << "Size of User        = " << sizeof(User) << "\n";
    std::cout << "Size of Beer        = " << sizeof(Beer) << "\n";
    std::cout << "Size of int*        = " << sizeof(int*) << "\n";
    std::cout << "Size of size_t*     = " << sizeof(size_t) << "\n";

}

/*functions for exercise 4.4*/
void PrintSymbols()
{
    // print alphabet symbols and their codes
    for (int i = int('a'); i <= int('z'); i ++)
    {
        std::cout << char(i) << " (" << i << "), ";
    }
    std::cout << '\n';

    // print digits 0-9 and their codes
    for (int i = int('0'); i <= int('9'); i ++)
    {
        std::cout << char(i) << " (" << i << "), ";
    }
    std::cout << '\n';

    // print alphabet symbols and their codes in hex
    for (int i = int('a'); i <= int('z'); i ++)
    {
        std::cout << char(i) << " (0x" << std::hex << i << "), ";
    }
    std::cout << '\n';

    // print digits 0-9 and their codes in hex
    for (int i = int('0'); i <= int('9'); i ++)
    {
        std::cout << char(i) << " (0x" << std::hex << i << "), ";
    }
    std::cout << '\n';
}

/*functions for exercise 4.5*/
#define PRINT_LIMITS(type) \
std::cout << "["#type"] limits are: [" << std::numeric_limits<type>::min() << ", " << std::numeric_limits<type>::max() << "]\n";

void PrintLimits()
{
    PRINT_LIMITS(char);
    PRINT_LIMITS(short);
    PRINT_LIMITS(int);
    PRINT_LIMITS(long);
    PRINT_LIMITS(float);
    PRINT_LIMITS(double);
    PRINT_LIMITS(long double);
    PRINT_LIMITS(unsigned);
}

/*functions for exercise 5.2*/
void PrintInfoAboutPoiners()
{
    std::cout << "Size of char* = " << sizeof(char*) << "\n";
    std::cout << "Size of int*  = " << sizeof(char*) << "\n";
    std::cout << "Size of void* = " << sizeof(char*) << "\n";

    const int arrLength = 4;
    char chArr[arrLength];
    int  intArr[arrLength];

    std::cout << "char:\n";
    for (int i = 0; i < arrLength; i++)
    {
        std::cout << "&chArr[" << i << "] = " << (void*)&chArr[i] << "\n";
    }
    std::cout << "int:\n";
    for (int i = 0; i < arrLength; i++)
    {
        std::cout << "&intArr[" << i << "] = " << &intArr[i] << "\n";
    }
}

/*functions for exercise 5.4*/
void SwapNumbers(int* first, int* second)
{
    int tmp = *first;
    *first = *second;
    *second = tmp;
}

void SwapNumbers(int& first, int& second)
{
    int tmp = first;
    first = second;
    second = tmp;
}

void PrintSwappedNumbers()
{
    int first;
    int second;
    std::cout << "Enter numbers:\n";
    std::cin >> first;
    std::cin >> second;

    SwapNumbers(&first, &second);
    std::cout << "Swapped numbers (by pointers): " << first << ", " << second << "\n";

    SwapNumbers(first, second);
    std::cout << "Swapped again (by refs): " << first << ", " << second << "\n";
}

/*functions for exercise 5.6*/
void f(char ch)
{
    std::cout << ch;
}

void g(char& rch)
{
    std::cout << rch;
}

void h(const char& crch)
{
    std::cout << crch;
}

void CheckFunctionsWithCharInput()
{
    char c = 10;
    unsigned char uc = 10;
    signed char sc = -10;

    f('a');
    f(49);
    f(3300); // truncation to char
    f(c);
    f(uc);
    f(sc);

    //g('a'); // error: 'a' isn't lvalue
    //g(49); // error: 49 isn't lvalue
    //g(3300); // error: 3300 isn't lvalue
    g(c);
    //g(uc); // error: lvalue of type T is required to initialize T&
    //g(sc); // error: lvalue of type T is required to initialize T&

    h('a'); // temporal variable is created as local variable in the function to place 'a' there
    h(49); // temporal variable is created as local variable in the function to place 49 there
    h(3300); // temporal variable is created as local variable in the function to place char(3300) there
    h(c);
    h(uc);
    h(sc);

}

/*functions for exercise 5.7*/
void PrintMonthsLengths()
{
    std::cout << "Output via arrays:\n";
    for (int i = 0; i < monthsNum; i++)
    {
        std::cout << monthsNames[i] << " " << monthsLengths[i] << '\n';
    }

    std::cout << "\nOutput via structure:\n";
    for (int i = 0; i < monthsNum; i++)
    {
        std::cout << months[i].name << " " << months[i].length << '\n';
    }
}

/*functions for exercise 5.8*/
void MeasurePassingThroughArray()
{
    ULL timeIndex, timePtr;
    int numOfPasses = numOfPassesNonOptimized / 2;

    // warming up to reach boost CPU frequency
    for (int i = 0; i < numOfPasses; i++)
    {
        for (int j = 0; j < arrayLen; j++)
        {
            perfArray[j] = j;
        }
    }

    numOfPasses = numOfPassesNonOptimized;

    // measurement by index
    timeIndex = Tick();
    for (int i = 0; i < numOfPasses; i ++)
    {
        for (size_t j = 0; j < arrayLen; j ++)
        {
            perfArray[j] = i;
        }
    }
    timeIndex = Tock(timeIndex);

    // measurement by pointer
    timePtr = Tick();
    int *const pArrStart = perfArray;
    int *const pArrEnd = &perfArray[arrayLen];

    for (int i = 0; i < numOfPasses; i++)
    {
        for (int* p = pArrStart; p < pArrEnd; p ++)
        {
            *p = i;
        }
    }
    timePtr = Tock(timePtr);

    // print results
    std::cout << "By index\n";
    std::cout << "Tick count = " << timeIndex << '\n';

    std::cout << "\nBy pointer\n";
    std::cout << "Tick count = " << timePtr << '\n';
}

/*functions for exercise 5.10*/
typedef char *ArrOfMonths[monthsNum];
void PrintArrayOfMonths(ArrOfMonths arrOfMonths)
{
    std::cout << "Names of 12 months:\n";
    for (int i = 0; i < monthsNum; i++)
    {
        std::cout << arrOfMonths[i] << '\n';
    }
}

int main()
{
    bool incorrectInput = true;
    int exerciseNumber = 0;

    while (incorrectInput == true)
    {
        std::cout << "Please enter exercise number:";

        std::cin >> exerciseNumber;
        std::cout << '\n';

        switch (exerciseNumber)
        {
        case 41:
            HelloWorld();
            break;
        case 43:
            PrintSizesOfTypes();
            break;
        case 44:
            PrintSymbols();
            break;
        case 45:
            PrintLimits();
            break;
        case 52:
            PrintInfoAboutPoiners();
            break;
        case 54:
            PrintSwappedNumbers();
            break;
        case 57:
            PrintMonthsLengths();
            break;
        case 58:
            MeasurePassingThroughArray();
            break;
        case 510:
            PrintArrayOfMonths(arrOfMonths);
            break;
        default:
            std::cout << "Incorrect exercise number. Please reenter.\n";
            continue;
        }

        incorrectInput = false;
    }

    return 0;
}
