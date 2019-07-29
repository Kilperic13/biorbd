#ifndef S2MMUSCLEHILLTYPE_CPPAD_H
#define S2MMUSCLEHILLTYPE_CPPAD_H
#include "s2mMuscleHillType.h"
#include "cppad/cppad.hpp"

class BIORBD_API s2mMuscleHillTypeCppAD : public s2mMuscleHillType
{
public:
    s2mMuscleHillTypeCppAD(const s2mString& = "");

    // Get individual forces
    CppAD::AD<double> FlCE(const CppAD::AD<double> &EMG);

protected:
    CppAD::AD<double> computeFlCE(const CppAD::AD<double> &EMG);
};

#endif // S2MMUSCLEHILLTYPE_CPPAD_H
