#include <math.h>

void LaguerreMatrix(double* P, double** L, int m, int n){
    
    for (int i = 0; i < m; i++){
        for (int j = 0; j < n; j++){
            if (j == 0){
                L[i][0] = 1.0;
            } else if (j == 1) {
                L[i][1] = 1.0 - P[i];
            } else {
                L[i][j] = (((2 * (j-1)) + 1 - P[i]) * L[i][j-1] - (j-1) * L[i][j-2]) / j;
            }
        }
    }
}

void MatrixMultiply(double** A, double** B, double** C, int k, int m, int n){
    
    double entry = 0.00;

    for (int i=0; i<k; i++){
        for (int j=0; j<n; j++){
            for (int s = 0; s < m; s++){
                entry = entry + A[i][s] * B[s][j];
            }
            C[i][j] = entry;
            entry = 0.00;
        }
    }
}

void VectorMultiply(double** A, double* b, double* c, int m, int n){
    
    double entry = 0.00;

    for (int i=0; i<m; i++){
        for (int j = 0; j < n; j++){
            entry = entry + A[i][j] * b[j];
        }
        c[i] = entry;
        entry = 0.0;
    }
}

double dot_product(double** A, double** Q, int j, int k, int n){
    double dot = 0.0;
    for (int i = 0; i < n; i++){
        dot = dot + A[i][j] * Q[i][k];
    }

    return dot;
}

void normalize(double** Q, int j, int n){
    double norm = 0.0;
    for (int i = 0; i < n; i++){
        norm = norm + Q[i][j]*Q[i][j];
    }

    norm = sqrt(norm);
    
    for (int i = 0; i < n; i++){
        Q[i][j] = Q[i][j] / norm;
    }
}

void QR(double** A, double** R,  int n){
    double** Q = new double*[n];
    for (int i = 0; i < n; i++){
        Q[i] = new double[n];
    }
    double norm = 0.0;
    double dot_prod_scaler = 0.0;
    
    /*** Gram-Schmidt Process ***/

    for (int j = 0; j < n; j++){
        
        for (int i = 0; i < n; i++){
            Q[i][j] = A[j][i];
        }

        for (int k = 0; k < j; k++){
            dot_prod_scaler = dot_product(A, Q, j, k, n);
            for (int i = 0; i < n; i++){
                Q[i][j] = Q[i][j] - dot_prod_scaler * Q[i][k];
            }
        }
        normalize(Q, j, n);
        for (int i = 0; i < n; i++){
            if (i <= j){
                R[i][j] = dot_product(A, Q, j, i, n);
            } else {
                R[i][j] = 0;
            }
        }
    }

    for (int i = 0; i < n; i++){
        for(int j = 0; j < n; j++){
            A[i][j] = Q[i][j];
        }
    }

    for (int i = 0; i < n; ++i){
        delete [] Q[i];
    }
    delete [] Q;
}

void InverseUpperTriangular(double** M, int n){
    double* x = new double[n];
    double** Inv = new double*[n];
    double value = 0.0;

    for (int i = 0; i < n; i++){
        Inv[i] = new double[n];
    }

    for (int r = n-1; r > -1; r--){
        for (int i = n-1; i > -1; i--){
            for (int j = i+1; j < n; j++){
                value = value + M[i][j] * x[j];
            }
            if (i == r){
                value = (1 / M[i][i]) * (1 - value);
            } else {
                value = - (1 / M[i][i]) * value;
            }
            x[i] = value;
            value = 0.0;
        }
        for (int j = n-1; j > -1; j--){
            Inv[j][r] = x[j];
        }
    }
    
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            M[i][j] = Inv[i][j];
        }
    }
    
    for (int i = 0; i < n; i++){
        delete [] Inv[i];
    }
    delete [] Inv;
    delete [] x;
}

void Transpose(double** M, double** MT, int m, int n){

    for (int i = 0; i < n; i++){
        for (int j = 0; j < m; j++){
            MT[i][j] = M[j][i];
        }
    }
}

void DeleteDynamicArray(double** A, double m, double n){
    for (int i = 0; i < m; i++){
        delete [] A[i];
    }
    delete [] A;
}