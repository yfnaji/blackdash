#include "longstaff_schwartz.h"
#include "blackdash_linear_algebra.h"
#include <random>
#include <chrono>

LongstaffSchwartz::LongstaffSchwartz(double mu_, double sigma_, int days_, double S0_, double K_, bool put_option_, double days_in_year_)
{
    mu=mu_;
    sigma=sigma_;
    days=days_;
    S0=S0_;
    K=K_;
    put_option=put_option_;
    days_in_year=days_in_year_;
}

double LongstaffSchwartz::discount(double t1, double t2){
    return exp(- mu * (t2 - t1) / days_in_year);
}
void LongstaffSchwartz::InitialiseBrownianBridge(double* X, double t){
    unsigned seed;
    std::default_random_engine generator(seed);
    std::normal_distribution<double> phi(0, 1);
    double Z;

    for (int i = 0; i < n_simulations; i++){
        seed = std::chrono::system_clock::now().time_since_epoch().count();
        generator.seed(seed);
        Z = phi(generator);

        X[i] = ((mu - 0.5 * sigma * sigma) * t / days_in_year) + sigma * sqrt(t / days_in_year) * Z;
    }
}
double LongstaffSchwartz::PayoffFunction(double St){
    double payoff_value;

    if (put_option == true){
        payoff_value = K - St;
    } else {
        payoff_value = St - K;
    }

    if (payoff_value > 0.0){
        return payoff_value;
    } else {
        return 0.0;
    }
}

void LongstaffSchwartz::InitialisePayoffs(double* X, double* paths){
    for (int i = 0; i < n_simulations; i++){
        paths[i] = PayoffFunction(S0 * exp(X[i]));
    }
}

void LongstaffSchwartz::BrownianBridge(double* X, double t, double prev_t){
    unsigned seed;
    std::default_random_engine generator(seed);
    std::normal_distribution<double> phi(0, 1);
    double Z;

    for (int i = 0; i < n_simulations; i++){
        seed = std::chrono::system_clock::now().time_since_epoch().count();
        generator.seed(seed);
        Z = phi(generator);

        X[i] = X[i] * (t / (prev_t)) + sigma * sqrt(t * (prev_t - t) / (prev_t * days_in_year)) * Z;
    }
}

void LongstaffSchwartz::CalculateGreeks(){
    unsigned seed;
    std::default_random_engine generator(seed);
    std::normal_distribution<double> phi(0, 1);
    double Z;
    
    double* payoffs = new double[n_simulations];
    double p;
    delta = 0;
    vega = 0;
    rho = 0;
    theta = 0;
    gamma = 0;
    theta = 0;
    double St;
    stopping_time = (double)stopping_time / days_in_year;
    
    for (int sim = 0; sim < n_simulations; sim++){
        seed = std::chrono::system_clock::now().time_since_epoch().count();
        generator.seed(seed);
        Z = phi(generator);
        St = S0 * exp(((mu - 0.5 * sigma * sigma) * stopping_time) + sigma * sqrt(stopping_time) * Z) ;
        p = PayoffFunction(St);
        rho = rho - stopping_time * exp(- mu * stopping_time) * p;

        if (p > 0){
            seed = std::chrono::system_clock::now().time_since_epoch().count();
            generator.seed(seed);
            Z = phi(generator);
            delta = delta + exp((mu - 0.5 * sigma * sigma) * (stopping_time) + sigma * sqrt(stopping_time) * Z);
            vega = vega + (sqrt(stopping_time) * Z - sigma * (stopping_time)) * exp((mu - 0.5 * sigma * sigma)*(stopping_time) + sigma * sqrt(stopping_time) * Z);
            rho = rho + exp(- mu * stopping_time) * (stopping_time) * S0 * exp(((mu - 0.5 * sigma * sigma) * stopping_time) + sigma * sqrt(stopping_time) * Z);
        }
    }

    delta = exp(-stopping_time * mu) * delta / n_simulations;
    vega = exp(-stopping_time * mu) * vega / n_simulations;
    rho = exp(-stopping_time * mu) * rho / n_simulations;
    gamma = vega / (S0 * S0 * sigma * stopping_time);
    theta = mu * (option_price - S0 * delta) - 0.5 * sigma * sigma * S0 * S0 * gamma;
}

void LongstaffSchwartz::CalculateOptionPrice(){
    double* P = new double[n_simulations];
    for (int i = 0; i < n_simulations; i++){
        P[i] = 0;
    }

    double prev_t = (double)days;
    double* simulation =  new double[n_simulations];

    InitialiseBrownianBridge(simulation, prev_t);
    InitialisePayoffs(simulation, P);

    int n;
    double* paths = new double[n_simulations];
    double* payoffs = new double[n_simulations];
    int index;

    double** L = new double*[n_simulations];
    for (int i = 0; i < n_simulations; i++){
        L[i] = new double[bases];
    }

    double** LT = new double*[bases];
    for (int i = 0; i < bases; i++){
        LT[i] = new double[n_simulations];
    }

    double** LTL = new double*[bases];
    for (int i = 0; i < bases; i++){
        LTL[i] = new double[bases];

    }

    double** RInv = new double*[bases];
    for (int i = 0; i < bases; i++){
        RInv[i] = new double[bases];
    }


    double** QT = new double*[bases];
    for (int i = 0; i < bases; i++){
        QT[i] = new double[bases];
    }

    double** RInvQT = new double*[bases];
    for (int i = 0; i < bases; i++){
        RInvQT[i] = new double[bases];
    }

    double** RInvQTLT = new double*[bases];
    for (int i = 0; i < bases; i++){
        RInvQTLT[i] = new double[bases];
    }

    double* C = new double[n_simulations];
    for (int i = 0; i < n_simulations; i++){
        C[i] = 0;
    }
    double* regression_coeff = new double[bases];
    int* in_the_money_paths = new int[n_simulations];
    double St;
    double temp_payoff;

    double* delta = new double[n_simulations];

    int timesteps = 1000;
    // double h = (double)days / 1000.0;
    double t_now;

    // for (int t = days - 1; t > 0; t--){
    for (int step = timesteps - 1; step > 0; step--){
        // t = (double)t;
        t_now = days - ((double)days * (double)step / (days_in_year * (double)timesteps));
        n = 0;

        BrownianBridge(simulation, t_now, prev_t);

        for (int i = 0; i < n_simulations; i++){
            St = S0 * exp(simulation[i]);
            temp_payoff = PayoffFunction(St);
            if (temp_payoff > 0){
                paths[n] = St;
                payoffs[n] = discount(t_now, prev_t) * (temp_payoff);
                in_the_money_paths[n] = i;
                n++;
            } else {
                P[i] = discount(t_now, prev_t) * P[i];
            }
        }
        if (n > 0){
            LaguerreMatrix(paths, L, bases, n);
            Transpose(L, LT, n, bases);
            MatrixMultiply(LT, L, LTL, bases, n, bases);

            QR(LTL, RInv, bases);

            InverseUpperTriangular(RInv, bases);
            Transpose(LTL, QT, bases, bases);

            MatrixMultiply(RInv, QT, RInvQT, bases, bases, bases);
            MatrixMultiply(RInvQT, LT, RInvQTLT, bases, bases, n);
            VectorMultiply(RInvQTLT, payoffs, regression_coeff, bases, n);
            
            for (int i = 0; i < bases; i++){
                C[i] = 0;
            }

            // Amend to only pull C values required (if possible)
            // for (int i = 0; i < bases; i++){
            //     for (int s = 0; s < bases; s++){
            //         C[i] = C[i] + regression_coeff[s] * L[i][s];
            //     }
            // }

            VectorMultiply(L, regression_coeff, C, n, bases);

            for (int i = 0; i < n; i++){
                index = in_the_money_paths[i];
                temp_payoff = PayoffFunction(paths[index]);
                if (temp_payoff > C[i]){
                    stopping_time = t_now;
                    P[index] = temp_payoff;
                } else {
                    P[index] = discount(t_now, prev_t) * P[index];
                }
            }
        }
        prev_t = t_now;
    }

    double price = 0.0;
    for (int i = 0; i < n_simulations; i++){
        price = price + P[i];
    }
    price = discount(0, days) * price / (double)n_simulations;

    
    option_price = price;

    // DeleteDynamicArray(LTL, bases, bases);
    // DeleteDynamicArray(L, n_simulations, bases);
    // DeleteDynamicArray(RInv, bases, bases);
    // DeleteDynamicArray(QT, bases, bases);
    // DeleteDynamicArray(RInvQT, bases, bases);
    // DeleteDynamicArray(LT, bases, n_simulations);
    // DeleteDynamicArray(RInvQTLT, bases, bases);
    // delete [] payoffs;
    // delete [] C;
    // delete [] in_the_money_paths;
    // delete [] P;
    // delete [] simulation;

    CalculateGreeks();
}
