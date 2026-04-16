# Physics Module (2D)

UrhoX Lua API - Physics Module (2D)

> **长度单位**: 米（meter）
> **重力加速度**: 米/秒² （如 `gravity = Vector2(0, -9.81)`）
> **速度**: 米/秒

---

## Classes

- [PhysicsWorld2D](#physicsworld2d)
- [RigidBody2D](#rigidbody2d)
- [CollisionShape2D](#collisionshape2d)
- [CollisionBox2D](#collisionbox2d)
- [CollisionCircle2D](#collisioncircle2d)
- [CollisionPolygon2D](#collisionpolygon2d)
- [CollisionChain2D](#collisionchain2d)
- [CollisionEdge2D](#collisionedge2d)
- [Constraint2D](#constraint2d)
- [ConstraintDistance2D](#constraintdistance2d)
- [ConstraintFriction2D](#constraintfriction2d)
- [ConstraintGear2D](#constraintgear2d)
- [ConstraintMotor2D](#constraintmotor2d)
- [ConstraintMouse2D](#constraintmouse2d)
- [ConstraintPrismatic2D](#constraintprismatic2d)
- [ConstraintPulley2D](#constraintpulley2d)
- [ConstraintRevolute2D](#constraintrevolute2d)
- [ConstraintRope2D](#constraintrope2d)
- [ConstraintWeld2D](#constraintweld2d)
- [ConstraintWheel2D](#constraintwheel2d)
- [PhysicsRaycastResult2D](#physicsraycastresult2d)

---

**Inherits from**: Component

## PhysicsWorld2D : Component


### Methods


- void DrawDebugGeometry()
- void SetUpdateEnabled(bool enable)
- void SetDrawShape(bool drawShape)
- void SetDrawJoint(bool drawJoint)
- void SetDrawAabb(bool drawAabb)
- void SetDrawPair(bool drawPair)
- void SetDrawCenterOfMass(bool drawCenterOfMass)
- void SetAllowSleeping(bool enable)
- void SetWarmStarting(bool enable)
- void SetContinuousPhysics(bool enable)
- void SetSubStepping(bool enable)
- void SetGravity(const Vector2& gravity)
- void SetAutoClearForces(bool enable)
- void SetVelocityIterations(int velocityIterations)
- void SetPositionIterations(int positionIterations)
- const PODVector<PhysicsRaycastResult2D>& Raycast(const Vector2& startPoint, const Vector2& endPoint, unsigned collisionMask = M_MAX_UNSIGNED)
- PhysicsRaycastResult2D RaycastSingle(const Vector2& startPoint, const Vector2& endPoint, unsigned collisionMask = M_MAX_UNSIGNED)
- RigidBody2D* GetRigidBody(const Vector2& point, unsigned collisionMask = M_MAX_UNSIGNED)
- RigidBody2D* GetRigidBody(int screenX, int screenY, unsigned collisionMask = M_MAX_UNSIGNED)
- const PODVector<RigidBody2D*>& GetRigidBodies(const Rect& aabb, unsigned collisionMask = M_MAX_UNSIGNED)
- bool IsUpdateEnabled() const
- bool GetDrawShape() const
- bool GetDrawJoint() const
- bool GetDrawAabb() const
- bool GetDrawPair() const
- bool GetDrawCenterOfMass() const
- bool GetAllowSleeping() const
- bool GetWarmStarting() const
- bool GetContinuousPhysics() const
- bool GetSubStepping() const
- bool GetAutoClearForces() const
- const Vector2& GetGravity() const
- int GetVelocityIterations() const
- int GetPositionIterations() const

### Properties


- bool updateEnabled
- bool drawShape
- bool drawJoint
- bool drawAabb
- bool drawPair
- bool drawCenterOfMass
- bool allowSleeping
- bool warmStarting
- bool continuousPhysics
- bool subStepping
- bool autoClearForces
- Vector2& gravity
- int velocityIterations
- int positionIterations



---

**Inherits from**: Component

## RigidBody2D : Component


### Methods


- void SetBodyType(BodyType2D bodyType)
- void SetMass(float mass)
- void SetInertia(float inertia)
- void SetMassCenter(const Vector2& center)
- void SetUseFixtureMass(bool useFixtureMass)
- void SetLinearDamping(float linearDamping)
- void SetAngularDamping(float angularDamping)
- void SetAllowSleep(bool allowSleep)
- void SetFixedRotation(bool fixedRotation)
- void SetBullet(bool bullet)
- void SetGravityScale(float gravityScale)
- void SetAwake(bool awake)
- void SetLinearVelocity(const Vector2& linearVelocity)
- void SetAngularVelocity(float angularVelocity)
- void ApplyForce(const Vector2& force, const Vector2& point, bool wake)
- void ApplyForceToCenter(const Vector2& force, bool wake)
- void ApplyTorque(float torque, bool wake)
- void ApplyLinearImpulse(const Vector2& impulse, const Vector2& point, bool wake)
- void ApplyLinearImpulseToCenter(const Vector2& impulse, bool wake)
- void ApplyAngularImpulse(float impulse, bool wake)
- BodyType2D GetBodyType() const
- float GetMass() const
- float GetInertia() const
- Vector2 GetMassCenter() const
- bool GetUseFixtureMass() const
- float GetLinearDamping() const
- float GetAngularDamping() const
- bool IsAllowSleep() const
- bool IsFixedRotation() const
- bool IsBullet() const
- float GetGravityScale() const
- bool IsAwake() const
- Vector2 GetLinearVelocity() const
- float GetAngularVelocity() const

### Properties


- BodyType2D bodyType
- float mass
- float inertia
- Vector2 massCenter
- bool useFixtureMass
- float linearDamping
- float angularDamping
- bool allowSleep
- bool fixedRotation
- bool bullet
- float gravityScale
- bool awake
- Vector2 linearVelocity
- float angularVelocity



---

**Inherits from**: Component

## CollisionShape2D : Component


### Methods


- void SetTrigger(bool trigger)
- void SetCategoryBits(int categoryBits)
- void SetMaskBits(int maskBits)
- void SetGroupIndex(int groupIndex)
- void SetDensity(float density)
- void SetFriction(float friction)
- void SetRestitution(float restitution)
- bool IsTrigger() const
- int GetCategoryBits() const
- int GetMaskBits() const
- int GetGroupIndex() const
- float GetDensity() const
- float GetFriction() const
- float GetRestitution() const
- float GetMass() const
- float GetInertia() const
- Vector2 GetMassCenter() const

### Properties


- bool trigger
- int categoryBits
- int maskBits
- int groupIndex
- float density
- float friction
- float restitution
- float mass (readonly)
- float inertia (readonly)
- Vector2 massCenter (readonly)



---

**Inherits from**: CollisionShape2D

## CollisionBox2D : CollisionShape2D


### Methods


- void SetSize(const Vector2& size)
- void SetSize(float width, float height)
- void SetCenter(const Vector2& center)
- void SetCenter(float x, float y)
- void SetAngle(float angle)
- const Vector2& GetSize() const
- const Vector2& GetCenter() const
- float GetAngle() const

### Properties


- Vector2& size
- Vector2& center
- float angle



---

**Inherits from**: CollisionShape2D

## CollisionCircle2D : CollisionShape2D


### Methods


- void SetRadius(float radius)
- void SetCenter(const Vector2& center)
- void SetCenter(float x, float y)
- float GetRadius() const
- const Vector2& GetCenter() const

### Properties


- float radius
- Vector2& center



---

**Inherits from**: CollisionShape2D

## CollisionPolygon2D : CollisionShape2D


### Methods


- void SetVertexCount(unsigned count)
- void SetVertex(unsigned index, const Vector2& vertex)
- void SetVertices(const PODVector<Vector2>& vertices)
- unsigned GetVertexCount() const
- const Vector2& GetVertex(unsigned index) const

### Properties


- unsigned vertexCount



---

**Inherits from**: CollisionShape2D

## CollisionChain2D : CollisionShape2D


### Methods


- void SetLoop(bool loop)
- void SetVertexCount(unsigned count)
- void SetVertex(unsigned index, const Vector2& vertex)
- void SetVertices(const PODVector<Vector2>& vertices)
- bool GetLoop() const
- unsigned GetVertexCount() const
- const Vector2& GetVertex(unsigned index) const

### Properties


- bool loop
- unsigned vertexCount



---

**Inherits from**: CollisionShape2D

## CollisionEdge2D : CollisionShape2D


### Methods


- void SetVertex1(const Vector2& vertex)
- void SetVertex2(const Vector2& vertex)
- void SetVertices(const Vector2& vertex1, const Vector2& vertex2)
- const Vector2& GetVertex1() const
- const Vector2& GetVertex2() const

### Properties


- Vector2& vertex1
- Vector2& vertex2



---

**Inherits from**: Component

## Constraint2D : Component


### Methods


- void SetOtherBody(RigidBody2D* body)
- void SetCollideConnected(bool collideConnected)
- RigidBody2D* GetOwnerBody() const
- RigidBody2D* GetOtherBody() const
- bool GetCollideConnected() const

### Properties


- RigidBody2D* ownerBody (readonly)
- RigidBody2D* otherBody
- bool collideConnected



---

**Inherits from**: Constraint2D

## ConstraintDistance2D : Constraint2D


### Methods


- void SetOwnerBodyAnchor(const Vector2& anchor)
- void SetOtherBodyAnchor(const Vector2& anchor)
- void SetFrequencyHz(float frequencyHz)
- void SetDampingRatio(float dampingRatio)
- void SetLength(float length)
- const Vector2& GetOwnerBodyAnchor() const
- const Vector2& GetOtherBodyAnchor() const
- float GetFrequencyHz() const
- float GetDampingRatio() const
- float GetLength() const

### Properties


- Vector2& ownerBodyAnchor
- Vector2& otherBodyAnchor
- float frequencyHz
- float dampingRatio
- float length



---

**Inherits from**: Constraint2D

## ConstraintFriction2D : Constraint2D


### Methods


- void SetAnchor(const Vector2& anchor)
- void SetMaxForce(float maxForce)
- void SetMaxTorque(float maxTorque)
- const Vector2& GetAnchor() const
- float GetMaxForce() const
- float GetMaxTorque() const

### Properties


- Vector2& anchor
- float maxForce
- float maxTorque



---

**Inherits from**: Constraint2D

## ConstraintGear2D : Constraint2D


### Methods


- void SetOwnerConstraint(Constraint2D* constraint)
- void SetOtherConstraint(Constraint2D* constraint)
- void SetRatio(float ratio)
- Constraint2D* GetOwnerConstraint() const
- Constraint2D* GetOtherConstraint() const
- float GetRatio() const

### Properties


- Constraint2D* ownerConstraint
- Constraint2D* otherConstraint
- float ratio



---

**Inherits from**: Constraint2D

## ConstraintMotor2D : Constraint2D


### Methods


- void SetLinearOffset(const Vector2& linearOffset)
- void SetAngularOffset(float angularOffset)
- void SetMaxForce(float maxForce)
- void SetMaxTorque(float maxTorque)
- void SetCorrectionFactor(float correctionFactor)
- const Vector2& GetLinearOffset() const
- float GetAngularOffset() const
- float GetMaxForce() const
- float GetMaxTorque() const
- float GetCorrectionFactor() const

### Properties


- Vector2& linearOffset
- float angularOffset
- float maxForce
- float maxTorque
- float correctionFactor



---

**Inherits from**: Constraint2D

## ConstraintMouse2D : Constraint2D


### Methods


- void SetTarget(const Vector2& target)
- void SetMaxForce(float maxForce)
- void SetFrequencyHz(float frequencyHz)
- void SetDampingRatio(float dampingRatio)
- const Vector2& GetTarget() const
- float GetMaxForce() const
- float GetFrequencyHz() const
- float GetDampingRatio() const

### Properties


- Vector2& target
- float maxForce
- float frequencyHz
- float dampingRatio



---

**Inherits from**: Constraint2D

## ConstraintPrismatic2D : Constraint2D


### Methods


- void SetAnchor(const Vector2& anchor)
- void SetAxis(const Vector2& axis)
- void SetEnableLimit(bool enableLimit)
- void SetLowerTranslation(float lowerTranslation)
- void SetUpperTranslation(float upperTranslation)
- void SetEnableMotor(bool enableMotor)
- void SetMaxMotorForce(float maxMotorForce)
- void SetMotorSpeed(float motorSpeed)
- const Vector2& GetAnchor() const
- const Vector2& GetAxis() const
- bool GetEnableLimit() const
- float GetLowerTranslation() const
- float GetUpperTranslation() const
- bool GetEnableMotor() const
- float GetMaxMotorForce() const
- float GetMotorSpeed() const

### Properties


- Vector2& anchor
- Vector2& axis
- bool enableLimit
- float lowerTranslation
- float upperTranslation
- bool enableMotor
- float maxMotorForce
- float motorSpeed



---

**Inherits from**: Constraint2D

## ConstraintPulley2D : Constraint2D


### Methods


- void SetOwnerBodyGroundAnchor(const Vector2& groundAnchor)
- void SetOtherBodyGroundAnchor(const Vector2& groundAnchor)
- void SetOwnerBodyAnchor(const Vector2& anchor)
- void SetOtherBodyAnchor(const Vector2& anchor)
- void SetRatio(float ratio)
- const Vector2& GetOwnerBodyGroundAnchor() const
- const Vector2& GetOtherBodyGroundAnchor() const
- const Vector2& GetOwnerBodyAnchor() const
- const Vector2& GetOtherBodyAnchor() const
- float GetRatio() const

### Properties


- Vector2& ownerBodyGroundAnchor
- Vector2& otherBodyGroundAnchor
- Vector2& ownerBodyAnchor
- Vector2& otherBodyAnchor
- float ratio



---

**Inherits from**: Constraint2D

## ConstraintRevolute2D : Constraint2D


### Methods


- void SetAnchor(const Vector2& anchor)
- void SetEnableLimit(bool enableLimit)
- void SetLowerAngle(float lowerAngle)
- void SetUpperAngle(float upperAngle)
- void SetEnableMotor(bool enableMotor)
- void SetMotorSpeed(float motorSpeed)
- void SetMaxMotorTorque(float maxMotorTorque)
- const Vector2& GetAnchor() const
- bool GetEnableLimit() const
- float GetLowerAngle() const
- float GetUpperAngle() const
- bool GetEnableMotor() const
- float GetMotorSpeed() const
- float GetMaxMotorTorque() const

### Properties


- Vector2& anchor
- bool enableLimit
- float lowerAngle
- float upperAngle
- bool enableMotor
- float motorSpeed
- float maxMotorTorque



---

**Inherits from**: Constraint2D

## ConstraintRope2D : Constraint2D


### Methods


- void SetOwnerBodyAnchor(const Vector2& anchor)
- void SetOtherBodyAnchor(const Vector2& anchor)
- void SetMaxLength(float maxLength)
- const Vector2& GetOwnerBodyAnchor() const
- const Vector2& GetOtherBodyAnchor() const
- float GetMaxLength() const

### Properties


- Vector2& ownerBodyAnchor
- Vector2& otherBodyAnchor
- float maxLength



---

**Inherits from**: Constraint2D

## ConstraintWeld2D : Constraint2D


### Methods


- void SetAnchor(const Vector2& anchor)
- void SetFrequencyHz(float frequencyHz)
- void SetDampingRatio(float dampingRatio)
- const Vector2& GetAnchor() const
- float GetFrequencyHz() const
- float GetDampingRatio() const

### Properties


- Vector2& anchor
- float frequencyHz
- float dampingRatio



---

**Inherits from**: Constraint2D

## ConstraintWheel2D : Constraint2D


### Methods


- void SetAnchor(const Vector2& anchor)
- void SetAxis(const Vector2& axis)
- void SetEnableMotor(bool enableMotor)
- void SetMaxMotorTorque(float maxMotorTorque)
- void SetMotorSpeed(float motorSpeed)
- void SetFrequencyHz(float frequencyHz)
- void SetDampingRatio(float dampingRatio)
- const Vector2& GetAnchor() const
- const Vector2& GetAxis() const
- bool GetEnableMotor() const
- float GetMaxMotorTorque() const
- float GetMotorSpeed() const
- float GetFrequencyHz() const
- float GetDampingRatio() const

### Properties


- Vector2& anchor
- Vector2& axis
- bool enableMotor
- float maxMotorTorque
- float motorSpeed
- float frequencyHz
- float dampingRatio



---

## PhysicsRaycastResult2D



### Methods


- PhysicsRaycastResult2D() (GC)
- PhysicsRaycastResult2D* new()
- void delete()

### Properties


- Vector2 position
- Vector2 normal
- float distance
- RigidBody2D* body



---

