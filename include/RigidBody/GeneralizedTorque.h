#ifndef BIORBD_UTILS_GENERALIZED_TORQUE_H
#define BIORBD_UTILS_GENERALIZED_TORQUE_H

#include "biorbdConfig.h"
#include "Utils/Vector.h"

namespace biorbd {
namespace rigidbody {
class Joints;

///
/// \brief Class GeneralizedTorque
///
class BIORBD_API GeneralizedTorque : public biorbd::utils::Vector
{
public:

    ///
    /// \brief Construct generalized torque
    ///
    GeneralizedTorque();

    ///
    /// \brief Construct generalized torque
    /// \param Q State vector of the internal joints
    ///
    GeneralizedTorque(const biorbd::rigidbody::GeneralizedTorque& Q);

    ///
    /// \brief Construct generalized torque
    /// \param other TODO:
    ///
    template<typename OtherDerived> GeneralizedTorque(const Eigen::MatrixBase<OtherDerived>& other) :
        biorbd::utils::Vector(other){}

    ///
    /// \brief Construct generalized torque of a vector at a specific position
    /// \param i Position of the vector
    ///
    GeneralizedTorque(unsigned int i);

    ///
    /// \brief Construct generalized torque of specific joint
    /// \param j The joint
    ///
    GeneralizedTorque(const biorbd::rigidbody::Joints& j);

    ///
    /// \brief TODO:
    /// \param other TODO:
    /// \return TODO:
    ///
    template<typename OtherDerived>
        biorbd::rigidbody::GeneralizedTorque& operator=(const Eigen::MatrixBase <OtherDerived>& other){
            this->biorbd::utils::Vector::operator=(other);
            return *this;
        }
};

}}

#endif // BIORBD_UTILS_GENERALIZED_TORQUE_H
