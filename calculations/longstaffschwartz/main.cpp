#include "longstaff_schwartz.h"
#include <iostream>
#include <fstream>
#include <cstring>

int main(int argc, char* argv[]){

    double mu = std::stod(argv[1]);
    double sigma = std::stod(argv[2]);
    int days = std::stoi(argv[3]);
    double S0 = std::stod(argv[4]);
    double strike = std::stod(argv[5]);
    bool put_option;

    if (strcmp(argv[6], "1") == 0){
        put_option = true;
    } else {
        put_option = false;
    }
    double days_in_year = std::stod(argv[7]);

    LongstaffSchwartz solution(mu, sigma, days, S0, strike, put_option, days_in_year);
    solution.CalculateOptionPrice();

    std::cout << solution.option_price << " ";
    std::cout << solution.delta << " ";
    std::cout << solution.gamma << " ";
    std::cout << solution.vega << " ";
    std::cout << solution.rho << " ";
    std::cout << solution.theta << " ";

    return 0;
}
