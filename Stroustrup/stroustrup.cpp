/* First training cpp file for Stroustup exercises*/

#include <iostream>
#include <iterator>
#include <vector>
#include <map>
#include <algorithm>
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

/*functions for exercise 5.11*/
void PrintWordsFromInput()
{
    std::string word = "";
    // initialize vector with input
    std::vector<std::string> words;

    std::cout << "Enter your words:\n";
    std::cin >> word;
    while (word != "Quit")
    {
        words.push_back(word);
        std::cin >> word;
    }

    std::ostream_iterator<std::string> output(std::cout, " ");

    // print words in order of enter
    std::cout << "Words in order of enter:\n";
    std::copy(words.begin(), words.end(), output);
    std::cout << '\n';

    // sort and print w/o duplicates
    std::cout << "Words sorted and w/o duplicates:\n";
    std::sort(words.begin(), words.end());
    std::unique_copy(words.begin(), words.end(), output);
    std::cout << '\n';
}

/*functions for exercise 5.12*/
typedef std::map<std::string, int> Pairs;

void Print(std::pair<std::string, int> in)
{
    if (in.second > 1)
    {
        std::cout << in.first << " " << in.second << '\n';
    }
}

void CalcPairsOfSymbols(std::string& str)
{
    size_t len = str.length();
    if (len < 2)
    {
        std::cout << "Sting has length " << len << '\n';
        return;
    }

    Pairs pairs;

    for (int i = 0; i < len - 1; i++)
    {
        // get pair from the string
        std::string pair = str.substr(i, 2);

        // try to insert the pair to the map
        std::pair<Pairs::iterator, bool> ret;
        ret = pairs.insert(std::pair<std::string, int>(pair, 0));

        // check result of insertion
        if (ret.second == true)
        {
            // pair encountered 1st time. Set counter to 1.
            ret.first->second = 1;
        }
        else
        {
            // pair is already in the map. Increment the counter.
            ret.first->second++;
        }
    }

    std::for_each(pairs.begin(), pairs.end(), Print);
}

void Exercise512()
{
    std::string inputString;
    std::cout << "Enter sequence of letters\n";
    std::cin >> inputString;

    CalcPairsOfSymbols(inputString);
}

MyDate::MyDate()
{
    dd = 16;
    mm = 9;
    yyyy = 1984;
}

/*functions for exercise 5.13*/
bool MyDate::Init(std::string const & init)
{
    if (init.length() != dateLen
        || init.substr(dayDigits, 1) != "."
        || init.substr(dayDigits + monthDigits + 1, 1) != ".")
    {
        return false;
    }

    std::string day = init.substr(0, dayDigits);
    std::string month = init.substr(dayDigits + 1, monthDigits);
    std::string year = init.substr(dayDigits + monthDigits + 2, yearDigits);

    try
    {
        mm = std::stoi(month);
        if (mm <= 0 || mm > monthsNum)
        {
            return false;
        }

        dd = std::stoi(day);
        if (dd <= 0 || dd > monthsLengths[mm - 1])
        {
            return false;
        }

        yyyy = std::stoi(year);
        if (yyyy < 0)
        {
            return false;
        }
    }

    catch(...)
    {
        return false;
    }

    return true;
}

void MyDate::Print()
{
    std::cout << dd << " " << monthsNames[mm - 1] << " of " << yyyy << '\n';
}

void ReadDateAndPrint()
{
    std::string dateStr;
    std::cout << "Enter date in format dd.mm.yyyy: \n";
    std::cin >> dateStr;

    MyDate date = MyDate();

    if (date.Init(dateStr))
    {
        date.Print();
    }
    else
    {
        std::cout << "Incorrect date!\n";
    }
}

int main(int argc, char** argv)
{
    bool incorrectInput = false;
    int exerciseNumber = 0;
    std::istream* input = 0;

    switch (argc)
    {
    case 1:
        input = &std::cin;
        std::cout << "Please enter exercise number: ";
        break;
    case 2:
        input = new std::istringstream(argv[1]);
        break;
    default:
        incorrectInput = true;
        break;
    }

    if (incorrectInput == false)
    {
        *input >> exerciseNumber;
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
        case 511:
            PrintWordsFromInput();
            break;
        case 512:
            Exercise512();
            break;
        case 513:
            ReadDateAndPrint();
            break;
        default:
            incorrectInput = true;
        }
    }

    if (input != &std::cin)
    {
        delete input;
    }

    if (incorrectInput == true)
    {
        std::cout << "\n Incorrect exercise number!\n";
    }

    return 0;
}
