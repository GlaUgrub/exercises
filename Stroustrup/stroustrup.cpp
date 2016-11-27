/* First training cpp file for Stroustup exercises*/

#include <iostream>
#include "stroustrup.h"

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

void HelloWorld()
{
    std::cout << "Hello world" << '\n';
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
        if (exerciseNumber < 41 || int(exerciseNumber) > 250) // out of valid range
        {
            std::cout << "Incorrect exercise number. Please reenter.\n";
            continue;
        }

        switch (exerciseNumber)
        {
        case 41:
            HelloWorld();
            break;
        case 43:
            PrintSizesOfTypes();
            break;
        default:
            std::cout << "Incorrect exercise number. Please reenter.\n";
            continue;
        }

        incorrectInput = false;
    }

    return 0;
}