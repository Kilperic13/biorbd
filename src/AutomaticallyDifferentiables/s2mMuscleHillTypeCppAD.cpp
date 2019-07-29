#define BIORBD_API_EXPORTS
#include "AutomaticallyDifferentiables/s2mMuscleHillTypeCppAD.h"


s2mMuscleHillTypeCppAD::s2mMuscleHillTypeCppAD(const s2mString& name) :
    s2mMuscleHillType(name)
{

}

CppAD::AD<double> s2mMuscleHillTypeCppAD::FlCE(const CppAD::AD<double> &EMG)
{
    return computeFlCE(EMG);
}

CppAD::AD<double> s2mMuscleHillTypeCppAD::computeFlCE(const CppAD::AD<double> &EMG){
    return exp( -pow(( m_position.length() / caract().optimalLength() / (m_cste_FlCE_1*(1-EMG)+1) -1 ), 2)/m_cste_FlCE_2   );
}
