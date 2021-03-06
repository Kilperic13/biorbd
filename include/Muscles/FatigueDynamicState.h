#ifndef BIORBD_MUSCLES_FATIGUE_DYNAMIC_STATE_H
#define BIORBD_MUSCLES_FATIGUE_DYNAMIC_STATE_H

#include "biorbdConfig.h"
#include "Muscles/FatigueState.h"

namespace biorbd {
namespace muscles {
class StateDynamics;
class Characteristics;

///
/// \brief Class A state of fatigue that dynamically evolves over the usage of the muscle
///
class BIORBD_API FatigueDynamicState : public biorbd::muscles::FatigueState
{
public:
    ///
    /// \brief Construct the fatigue dynamic state
    /// \param active Muscle activation
    /// \param fatigued Muscle fatigue
    /// \param resting Muscle resting
    ///
    FatigueDynamicState(
            double active = 0,
            double fatigued = 0,
            double resting = 1);

    ///
    /// \brief Construct the fatigue dynamic state from other state
    /// \param other The other fatigue state
    ///
    FatigueDynamicState(
            const std::shared_ptr<biorbd::muscles::FatigueState> other);

    ///
    /// \brief Deep copy of a fatigue dynamic state
    /// \param other The other fatigue state
    /// 
    void DeepCopy(
            const biorbd::muscles::FatigueDynamicState& other);

    ///
    /// \brief Return the active fibers derivative
    /// \return The active fibers derivative
    ///
    double activeFibersDot() const;

    ///
    /// \brief Return the fatigued fibers derivative
    /// \return The fatigued fibers derivative
    ///
    double fatiguedFibersDot() const;

    ///
    /// \brief Return the resting fibers derivative
    /// \return The resting fibers derivative
    ///
    double restingFibersDot() const;

    ///
    /// \brief Compute the derivative of the current state
    /// \param emg EMG data
    /// \param characteristics The muscle characteristics
    ///
    virtual void timeDerivativeState(
            const biorbd::muscles::StateDynamics &emg,
            const biorbd::muscles::Characteristics &characteristics
     ) = 0;

protected:
    std::shared_ptr<double> m_activeFibersDot; ///< The active fibers derivative
    std::shared_ptr<double> m_fatiguedFibersDot; ///< The fatigued fibers derivative
    std::shared_ptr<double> m_restingFibersDot; ///< The resting fibers derivative

};

}}

#endif // BIORBD_MUSCLES_FATIGUE_DYNAMIC_STATE_H
