# include <iostream>        // standard input/output
# include <vector>          // standard vector
# include <cppad/cppad.hpp> // the CppAD package

#include "AutomaticallyDifferentiables/s2mMuscleHillTypeCppAD.h"

// main program
int main(void)
{
    s2mMuscleHillTypeCppAD muscle("m1");

    // domain space vector
    size_t n = 1;               // number of domain space variables
    std::vector< CppAD::AD<double> > ax(n); // vector of domain space variables
    ax[0] = 3.;                 // value at which function is recorded

    // declare independent variables and start recording operation sequence
    CppAD::Independent(ax);

    // range space vector
    size_t m = 1;               // number of ranges space variables
    std::vector< CppAD::AD<double> > ay(m); // vector of ranges space variables
    ay[0] = muscle.FlCE(ax[0]);     // record operations that compute ay[0]

    // store operation sequence in f: X -> Y and stop recording
    CppAD::ADFun<double> f(ax, ay);

    // compute derivative using operation sequence stored in f
    std::vector<double> jac = f.Jacobian(std::vector<double>({2.}));      // Jacobian for operation sequence

    // print the results
    std::cout << "f'(3) computed by CppAD = " << jac[0] << std::endl;

    return 0;
}
