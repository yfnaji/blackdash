class LongstaffSchwartz
{
    private:
    double discount(double t1, double t2);
    void InitialiseBrownianBridge(double* X, double t);
    void BrownianBridge(double* X, double t, double prev_t);
    double PayoffFunction(double St);
    void InitialisePayoffs(double* X, double* paths);
    int n_simulations = 1000;
    int bases = 100;
    // int timestep;
    
    public:
    double mu;
    double sigma;
    int days;
    double S0;
    double K;
    bool put_option;
    double days_in_year;
    double option_price;
    double stopping_time;
    double delta;
    double gamma;
    double vega;
    double rho;
    double theta;
    LongstaffSchwartz(double mu, double sigma, int days, double S0, double K, bool put_option, double days_in_year);
    void CalculateOptionPrice();
    void CalculateGreeks();
};