# Physics Module (3D)

UrhoX Lua API - Physics Module (3D)

> **长度单位**: 米（meter）
> **重力加速度**: 米/秒² （如 `gravity = Vector3(0, -9.81, 0)`）
> **速度**: 米/秒

---

## Classes

- [PhysicsWorld](#physicsworld)
- [RigidBody](#rigidbody)
- [CollisionShape](#collisionshape)
- [Constraint](#constraint)
- [PhysicsRaycastResult](#physicsraycastresult)
- [RaycastVehicle](#raycastvehicle)

---

**Inherits from**: Component

## PhysicsWorld : Component


### Methods


- void Update(float timeStep)
- void UpdateCollisions()
- void SetFps(int fps)
- void SetGravity(const Vector3& gravity)
- void SetMaxSubSteps(int num)
- void SetNumIterations(int num)
- void SetUpdateEnabled(bool enable)
- void SetInterpolation(bool enable)
- void SetInternalEdge(bool enable)
- void SetSplitImpulse(bool enable)
- void SetMaxNetworkAngularVelocity(float velocity)
- const PODVector<PhysicsRaycastResult>& Raycast(const Ray& ray, float maxDistance, unsigned collisionMask = M_MAX_UNSIGNED)
- PhysicsRaycastResult RaycastSingle(const Ray& ray, float maxDistance, unsigned collisionMask = M_MAX_UNSIGNED)
- PhysicsRaycastResult RaycastSingleSegmented(const Ray& ray, float maxDistance, float segmentDistance, unsigned collisionMask = M_MAX_UNSIGNED, float overlapDistance = 0.1f)
- PhysicsRaycastResult SphereCast(const Ray& ray, float radius, float maxDistance, unsigned collisionMask = M_MAX_UNSIGNED)
- PhysicsRaycastResult ConvexCast(CollisionShape* shape, const Vector3& startPos, const Quaternion& startRot, const Vector3& endPos, const Quaternion& endRot, unsigned collisionMask = M_MAX_UNSIGNED)
- const PODVector<RigidBody*>& GetRigidBodies(const Sphere& sphere, unsigned collisionMask = M_MAX_UNSIGNED)
- const PODVector<RigidBody*>& GetRigidBodies(const BoundingBox& box, unsigned collisionMask = M_MAX_UNSIGNED)
- const PODVector<RigidBody*>& GetRigidBodies(const RigidBody* body)
- const PODVector<RigidBody*>& GetCollidingBodies(const RigidBody* body)
- void DrawDebugGeometry(bool depthTest)
- void RemoveCachedGeometry(Model* model)
- Vector3 GetGravity() const
- int GetMaxSubSteps() const
- int GetNumIterations() const
- bool IsUpdateEnabled() const
- bool GetInterpolation() const
- bool GetInternalEdge() const
- bool GetSplitImpulse() const
- int GetFps() const
- float GetMaxNetworkAngularVelocity() const

### Properties


- Vector3 gravity
- int maxSubSteps
- int numIterations
- bool updateEnabled
- bool interpolation
- bool internalEdge
- bool splitImpulse
- int fps
- float maxNetworkAngularVelocity



---

**Inherits from**: Component

## RigidBody : Component


### Methods


- void SetMass(float mass)
- void SetPosition(const Vector3& position)
- void SetRotation(const Quaternion& rotation)
- void SetTransform(const Vector3& position, const Quaternion& rotation)
- void SetLinearVelocity(const Vector3& velocity)
- void SetLinearFactor(const Vector3& factor)
- void SetLinearRestThreshold(float threshold)
- void SetLinearDamping(float damping)
- void SetAngularVelocity(const Vector3& angularVelocity)
- void SetAngularFactor(const Vector3& factor)
- void SetAngularRestThreshold(float threshold)
- void SetAngularDamping(float factor)
- void SetFriction(float friction)
- void SetAnisotropicFriction(const Vector3& friction)
- void SetRollingFriction(float friction)
- void SetRestitution(float restitution)
- void SetContactProcessingThreshold(float threshold)
- void SetCcdRadius(float radius)
- void SetCcdMotionThreshold(float threshold)
- void SetUseGravity(bool enable)
- void SetGravityOverride(const Vector3& gravity)
- void SetKinematic(bool enable)
- void SetTrigger(bool enable)
- void SetCollisionLayer(unsigned layer)
- void SetCollisionMask(unsigned mask)
- void SetCollisionLayerAndMask(unsigned layer, unsigned mask)
- void SetCollisionEventMode(CollisionEventMode mode)
- void DisableMassUpdate()
- void EnableMassUpdate()
- void ApplyForce(const Vector3& force)
- void ApplyForce(const Vector3& force, const Vector3& position)
- void ApplyTorque(const Vector3& torque)
- void ApplyImpulse(const Vector3& impulse)
- void ApplyImpulse(const Vector3& impulse, const Vector3& position)
- void ApplyTorqueImpulse(const Vector3& torque)
- void ResetForces()
- void Activate()
- void ReAddBodyToWorld()
- PhysicsWorld* GetPhysicsWorld() const
- float GetMass() const
- Vector3 GetPosition() const
- Quaternion GetRotation() const
- Vector3 GetLinearVelocity() const
- Vector3 GetLinearFactor() const
- Vector3 GetVelocityAtPoint(const Vector3& position) const
- float GetLinearRestThreshold() const
- float GetLinearDamping() const
- Vector3 GetAngularVelocity() const
- Vector3 GetAngularFactor() const
- float GetAngularRestThreshold() const
- float GetAngularDamping() const
- float GetFriction() const
- Vector3 GetAnisotropicFriction() const
- float GetRollingFriction() const
- float GetRestitution() const
- float GetContactProcessingThreshold() const
- float GetCcdRadius() const
- float GetCcdMotionThreshold() const
- bool GetUseGravity() const
- const Vector3& GetGravityOverride() const
- const Vector3& GetCenterOfMass() const
- bool IsKinematic() const
- bool IsTrigger() const
- bool IsActive() const
- unsigned GetCollisionLayer() const
- unsigned GetCollisionMask() const
- CollisionEventMode GetCollisionEventMode() const

### Properties


- PhysicsWorld* physicsWorld (readonly)
- float mass
- Vector3 position
- Quaternion rotation
- Vector3 linearVelocity
- Vector3 linearFactor
- float linearRestThreshold
- float linearDamping
- Vector3 angularVelocity
- Vector3 angularFactor
- float angularRestThreshold
- float angularDamping
- float friction
- Vector3 anisotropicFriction
- float rollingFriction
- float restitution
- float contactProcessingThreshold
- float ccdRadius
- float ccdMotionThreshold
- bool useGravity
- Vector3& gravityOverride
- Vector3& centerOfMass (readonly)
- bool kinematic
- bool trigger
- bool active (readonly)
- unsigned collisionLayer
- unsigned collisionMask
- CollisionEventMode collisionEventMode



---

**Inherits from**: Component

## CollisionShape : Component


### Methods


- void SetBox(const Vector3& size)
- void SetBox(const Vector3& size, const Vector3& position)
- void SetBox(const Vector3& size, const Vector3& position, const Quaternion& rotation)
- void SetSphere(float diameter)
- void SetSphere(float diameter, const Vector3& position)
- void SetSphere(float diameter, const Vector3& position, const Quaternion& rotation)
- void SetStaticPlane()
- void SetStaticPlane(const Vector3& position)
- void SetStaticPlane(const Vector3& position, const Quaternion& rotation)
- void SetCylinder(float diameter, float height)
- void SetCylinder(float diameter, float height, const Vector3& position)
- void SetCylinder(float diameter, float height, const Vector3& position, const Quaternion& rotation)
- void SetCapsule(float diameter, float height)
- void SetCapsule(float diameter, float height, const Vector3& position)
- void SetCapsule(float diameter, float height, const Vector3& position, const Quaternion& rotation)
- void SetCone(float diameter, float height)
- void SetCone(float diameter, float height, const Vector3& position)
- void SetCone(float diameter, float height, const Vector3& position, const Quaternion& rotation)
- void SetTriangleMesh(Model* model, unsigned lodLevel = 0)
- void SetTriangleMesh(Model* model, unsigned lodLevel, const Vector3& scale)
- void SetTriangleMesh(Model* model, unsigned lodLevel, const Vector3& scale, const Vector3& position)
- void SetTriangleMesh(Model* model, unsigned lodLevel, const Vector3& scale, const Vector3& position, const Quaternion& rotation)
- void SetCustomTriangleMesh(CustomGeometry* custom)
- void SetCustomTriangleMesh(CustomGeometry* custom, const Vector3& scale)
- void SetCustomTriangleMesh(CustomGeometry* custom, const Vector3& scale, const Vector3& position)
- void SetCustomTriangleMesh(CustomGeometry* custom, const Vector3& scale, const Vector3& position, const Quaternion& rotation)
- void SetConvexHull(Model* model, unsigned lodLevel = 0)
- void SetConvexHull(Model* model, unsigned lodLevel, const Vector3& scale)
- void SetConvexHull(Model* model, unsigned lodLevel, const Vector3& scale, const Vector3& position)
- void SetConvexHull(Model* model, unsigned lodLevel, const Vector3& scale, const Vector3& position, const Quaternion& rotation)
- void SetCustomConvexHull(CustomGeometry* custom)
- void SetCustomConvexHull(CustomGeometry* custom, const Vector3& scale)
- void SetCustomConvexHull(CustomGeometry* custom, const Vector3& scale, const Vector3& position)
- void SetCustomConvexHull(CustomGeometry* custom, const Vector3& scale, const Vector3& position, const Quaternion& rotation)
- void SetTerrain(unsigned lodLevel = 0)
- void SetShapeType(ShapeType type)
- void SetSize(const Vector3& size)
- void SetPosition(const Vector3& position)
- void SetRotation(const Quaternion& rotation)
- void SetTransform(const Vector3& position, const Quaternion& rotation)
- void SetMargin(float margin)
- void SetModel(Model* model)
- void SetLodLevel(unsigned lodLevel)
- PhysicsWorld* GetPhysicsWorld() const
- ShapeType GetShapeType() const
- const Vector3& GetSize() const
- const Vector3& GetPosition() const
- const Quaternion& GetRotation() const
- float GetMargin() const
- Model* GetModel() const
- unsigned GetLodLevel() const
- BoundingBox GetWorldBoundingBox() const

### Properties


- PhysicsWorld* physicsWorld (readonly)
- ShapeType shapeType
- Vector3& size
- Vector3& position
- Quaternion& rotation
- float margin
- Model* model
- unsigned lodLevel
- BoundingBox worldBoundingBox (readonly)
- ResourceRef modelAttr



---

**Inherits from**: Component

## Constraint : Component


### Methods


- void SetConstraintType(ConstraintType type)
- void SetOtherBody(RigidBody* body)
- void SetPosition(const Vector3& position)
- void SetRotation(const Quaternion& rotation)
- void SetAxis(const Vector3& axis)
- void SetOtherPosition(const Vector3& position)
- void SetOtherRotation(const Quaternion& rotation)
- void SetOtherAxis(const Vector3& axis)
- void SetWorldPosition(const Vector3& position)
- void SetHighLimit(const Vector2& limit)
- void SetLowLimit(const Vector2& limit)
- void SetERP(float erp)
- void SetCFM(float cfm)
- void SetDisableCollision(bool disable)
- PhysicsWorld* GetPhysicsWorld() const
- ConstraintType GetConstraintType() const
- RigidBody* GetOwnBody() const
- RigidBody* GetOtherBody() const
- const Vector3& GetPosition() const
- const Quaternion& GetRotation() const
- const Vector3& GetOtherPosition() const
- const Quaternion& GetOtherRotation() const
- Vector3 GetWorldPosition() const
- const Vector2& GetHighLimit() const
- const Vector2& GetLowLimit() const
- float GetERP() const
- float GetCFM() const
- bool GetDisableCollision() const

### Properties


- PhysicsWorld* physicsWorld (readonly)
- ConstraintType constraintType
- RigidBody* ownBody (readonly)
- RigidBody* otherBody
- Vector3& position
- Quaternion& rotation
- Vector3& axis
- Vector3& otherPosition
- Quaternion& otherRotation
- Vector3& otherAxis
- Vector3 worldPosition
- Vector2& highLimit
- Vector2& lowLimit
- float ERP
- float CFM
- bool disableCollision



---

## PhysicsRaycastResult



### Methods


- PhysicsRaycastResult() (GC)
- PhysicsRaycastResult* new()
- void delete()

### Properties


- Vector3 position
- Vector3 normal
- float distance
- float hitFraction
- RigidBody* body



---

**Inherits from**: LogicComponent

## RaycastVehicle : LogicComponent


### Methods


- RaycastVehicle(Urho3D::Context* context) (GC)
- RaycastVehicle* new(Urho3D::Context* context)
- void delete()
- void RegisterObject(Context* context)
- void ApplyAttributes()
- void AddWheel(Node* wheelNode, Vector3 wheelDirection, Vector3 wheelAxle, float restLength, float wheelRadius, bool frontWheel)
- void ResetSuspension()
- void UpdateWheelTransform(int wheel, bool interpolated)
- void SetSteeringValue(int wheel, float steeringValue)
- void SetWheelSuspensionStiffness(int wheel, float stiffness)
- void SetWheelDampingRelaxation(int wheel, float damping)
- void SetWheelDampingCompression(int wheel, float compression)
- void SetWheelFrictionSlip(int wheel, float slip)
- void SetWheelRollInfluence(int wheel, float rollInfluence)
- void SetEngineForce(int wheel, float force)
- void SetBrake(int wheel, float force)
- void SetWheelRadius(int wheel, float wheelRadius)
- void ResetWheels()
- void SetWheelRestLength(int wheel, float length)
- void SetWheelSkidInfo(int wheel, float factor)
- bool WheelIsGrounded(int wheel) const
- void SetMaxSuspensionTravel(int wheel, float maxSuspensionTravel)
- void SetWheelDirection(int wheel, Vector3 direction)
- void SetWheelAxle(int wheel, Vector3 axle)
- void SetMaxSideSlipSpeed(float speed)
- void SetWheelSkidInfoCumulative(int wheel, float skid)
- void SetInAirRPM(float rpm)
- void SetCoordinateSystem()
- void SetCoordinateSystem(const IntVector3& coordinateSystem)
- void Init()
- Vector3 GetWheelPosition(int wheel)
- Quaternion GetWheelRotation(int wheel)
- Vector3 GetWheelConnectionPoint(int wheel)
- int GetNumWheels()
- Node* GetWheelNode(int wheel)
- float GetSteeringValue(int wheel) const
- float GetWheelSuspensionStiffness(int wheel) const
- float GetWheelDampingRelaxation(int wheel) const
- float GetWheelDampingCompression(int wheel) const
- float GetWheelFrictionSlip(int wheel) const
- float GetWheelRollInfluence(int wheel) const
- float GetEngineForce(int wheel) const
- float GetBrake(int wheel) const
- float GetWheelRadius(int wheel) const
- float GetWheelRestLength(int wheel) const
- float GetWheelSkidInfo(int wheel) const
- float GetMaxSuspensionTravel(int wheel)
- float GetWheelSideSlipSpeed(int wheel) const
- float GetMaxSideSlipSpeed() const
- float GetWheelSkidInfoCumulative(int wheel) const
- Vector3 GetWheelDirection(int wheel) const
- bool IsFrontWheel(int wheel) const
- Vector3 GetWheelAxle(int wheel) const
- Vector3 GetContactPosition(int wheel) const
- Vector3 GetContactNormal(int wheel) const
- float GetInAirRPM() const
- IntVector3 GetCoordinateSystem() const

### Properties


- const IntVector3 RIGHT_UP_FORWARD
- const IntVector3 RIGHT_FORWARD_UP
- const IntVector3 UP_FORWARD_RIGHT
- const IntVector3 UP_RIGHT_FORWARD
- const IntVector3 FORWARD_RIGHT_UP
- const IntVector3 FORWARD_UP_RIGHT



---

