#define BIORBD_API_EXPORTS
#include "s2mContacts.h"

#include <rbdl/Kinematics.h>
#include "s2mJoints.h"
#include "Utils/String.h"
#include "Utils/Error.h"
#include "Utils/GenCoord.h"
#include "s2mNode.h"
#include "Utils/Attitude.h"

s2mContacts::s2mContacts() :
    RigidBodyDynamics::ConstraintSet (),
    m_nbreConstraint(0),
    m_binded(false)
{

}

s2mContacts::~s2mContacts()
{

}

unsigned int s2mContacts::AddConstraint(unsigned int body_id, const s2mNode& body_point, const s2mNode& world_normal, const s2mString& name, double acc){
    ++m_nbreConstraint;
    return RigidBodyDynamics::ConstraintSet::AddContactConstraint(body_id, body_point, world_normal, name.c_str(), acc);
}
unsigned int s2mContacts::AddConstraint(unsigned int body_id, const s2mNode& body_point, const s2mString& axis, const s2mString& name, double acc){
    unsigned int ret(0);
    for (unsigned int i=0; i<axis.length(); ++i){
        ++m_nbreConstraint;
        if      (axis.tolower()[i] == 'x')
            ret += RigidBodyDynamics::ConstraintSet::AddContactConstraint(body_id, body_point, s2mNode(1,0,0), (name + "_X").c_str(), acc);
        else if (axis.tolower()[i] == 'y')
            ret += RigidBodyDynamics::ConstraintSet::AddContactConstraint(body_id, body_point, s2mNode(0,1,0), (name + "_Y").c_str(), acc);
        else if (axis.tolower()[i] == 'z')
            ret += RigidBodyDynamics::ConstraintSet::AddContactConstraint(body_id, body_point, s2mNode(0,0,1), (name + "_Z").c_str(), acc);
        else
            s2mError::s2mAssert(0,"Wrong axis!");
    }
    return ret;
}

unsigned int s2mContacts::AddLoopConstraint(unsigned int body_id_predecessor,
        unsigned int body_id_successor,
        const s2mAttitude &X_predecessor,
        const s2mAttitude &X_successor,
        const s2mVector &axis,
        bool enableStabilization,
        const double stabilizationParam,
        const s2mString &name)
{
    ++m_nbreConstraint;
    return RigidBodyDynamics::ConstraintSet::AddLoopConstraint(
                body_id_predecessor, body_id_successor,
                RigidBodyDynamics::Math::SpatialTransform(X_predecessor.rot(), X_predecessor.trans()),
                RigidBodyDynamics::Math::SpatialTransform(X_successor.rot(), X_successor.trans()),
                RigidBodyDynamics::Math::SpatialVector(axis),
                enableStabilization, stabilizationParam, name.c_str());
}


s2mContacts &s2mContacts::getConstraints_nonConst(const s2mJoints &m){
    if (!m_binded){
        Bind(m);
        m_binded = true;
    }
    return *this;
}

s2mContacts &s2mContacts::getConstraints_nonConst()
{
    if (!m_binded)
        s2mError::s2mAssert(0, "Please call getConstraints with s2mJoints model before!" );
    return *this;
}
const s2mContacts &s2mContacts::getConstraints() const {
    if (!m_binded)
        s2mError::s2mAssert(0, "Please call getConstraints with s2mJoints model before!" );
    return *this;
}

bool s2mContacts::hasContacts() const {
    if (m_nbreConstraint>0) return true; else return false;
}

unsigned int s2mContacts::nContacts() const {
    return m_nbreConstraint;
}

s2mString s2mContacts::name(unsigned int i) {
    s2mError::s2mAssert(i<m_nbreConstraint, "Idx for name is too high..");
    return RigidBodyDynamics::ConstraintSet::name[i];
}


std::vector<s2mNode> s2mContacts::constraintsInGlobal(
        s2mJoints& m,
        const biorbd::utils::GenCoord &Q,
        const bool updateKin){
    if (updateKin)
        RigidBodyDynamics::UpdateKinematicsCustom(m, &Q, nullptr, nullptr);

    // Variable de sortie
    std::vector<s2mNode> tp;


    // Sur chaque controle, appliquer la rotation et enregistrer sa position
    for (unsigned int i=0; i<size(); ++i)
        tp.push_back(RigidBodyDynamics::CalcBodyToBaseCoordinates(m, Q,body[i],point[i],false));

    return tp;
}

s2mVector s2mContacts::getForce() const
{
    return this->force;
}
