# Core Module

UrhoX Lua API - Core Module

---

## Classes

- [Scene](#scene)
- [Node](#node)
- [Component](#component)
- [Serializable](#serializable)
- [Animatable](#animatable)
- [Object](#object)
- [Context](#context)
- [Engine](#engine)
- [Time](#time)

---

**Inherits from**: Node

## Scene : Node


### Methods


- Scene() (GC)
- Scene* new()
- void delete()
- bool Load(File* source)
- bool Save(File* dest) const
- bool Load(const String fileName)
- bool Save(const String fileName) const
- bool LoadXML(File* source)
- bool SaveXML(File* dest, const String indentation = "\t") const
- bool LoadXML(const String fileName)
- bool SaveXML(const String fileName, const String indentation = "\t") const
- bool LoadJSON(File* source)
- bool SaveJSON(File* dest, const String indentation = "\t") const
- bool LoadJSON(const String fileName)
- bool SaveJSON(const String fileName, const String indentation = "\t") const
- Node* Instantiate(File* source, const Vector3& position, const Quaternion& rotation, CreateMode mode = REPLICATED)
- Node* Instantiate(const String fileName, const Vector3& position, const Quaternion& rotation, CreateMode mode = REPLICATED)
- Node* InstantiateXML(File* source, const Vector3& position, const Quaternion& rotation, CreateMode mode = REPLICATED)
- Node* InstantiateXML(const String fileName, const Vector3& position, const Quaternion& rotation, CreateMode mode = REPLICATED)
- Node* InstantiateJSON(const String fileName, const Vector3& position, const Quaternion& rotation, CreateMode mode = REPLICATED)
- bool LoadAsync(File* file, LoadMode mode = LOAD_SCENE_AND_RESOURCES)
- bool LoadAsyncXML(File* file, LoadMode mode = LOAD_SCENE_AND_RESOURCES)
- bool LoadAsync(const String fileName, LoadMode mode = LOAD_SCENE_AND_RESOURCES)
- bool LoadAsyncXML(const String fileName, LoadMode mode = LOAD_SCENE_AND_RESOURCES)
- void StopAsyncLoading()
- void Clear(bool clearReplicated = true, bool clearLocal = true)
- void SetUpdateEnabled(bool enable)
- void SetTimeScale(float scale)
- void SetElapsedTime(float time)
- void SetSmoothingConstant(float constant)
- void SetSnapThreshold(float threshold)
- void SetAsyncLoadingMs(int ms)
- Node* GetNode(unsigned id) const
- Component* GetComponent(unsigned id) const
- Component* GetComponent(const String type, bool recursive = false) const
- bool IsReplicatedID(unsigned id)
- bool IsUpdateEnabled() const
- bool IsAsyncLoading() const
- float GetAsyncProgress() const
- LoadMode GetAsyncLoadMode() const
- const String GetFileName() const
- unsigned GetChecksum() const
- float GetTimeScale() const
- float GetElapsedTime() const
- float GetSmoothingConstant() const
- float GetSnapThreshold() const
- int GetAsyncLoadingMs() const
- const String GetVarName(StringHash hash) const
- void Update(float timeStep)
- void BeginThreadedUpdate()
- void EndThreadedUpdate()
- void DelayedMarkedDirty(Component* component)
- bool IsThreadedUpdate() const
- unsigned GetFreeNodeID(CreateMode mode)
- unsigned GetFreeComponentID(CreateMode mode)
- void NodeAdded(Node* node)
- void NodeRemoved(Node* node)
- void ComponentAdded(Component* component)
- void ComponentRemoved(Component* component)
- void SetVarNamesAttr(const String value)
- String GetVarNamesAttr() const
- void PrepareNetworkUpdate()
- void CleanupConnection(Connection* connection)
- void MarkNetworkUpdate(Node* node)
- void MarkNetworkUpdate(Component* component)
- void MarkReplicationDirty(Node* node)
- const PODVector<Node*>& GetNodesWithTag(const String tag) const

### Properties


- bool updateEnabled
- bool asyncLoading (readonly)
- float asyncProgress (readonly)
- LoadMode asyncLoadMode (readonly)
- const String fileName
- unsigned checksum (readonly)
- float timeScale
- float elapsedTime
- float smoothingConstant
- float snapThreshold
- int asyncLoadingMs
- bool threadedUpdate (readonly)
- String varNamesAttr



---

**Inherits from**: Animatable

## Node : Animatable


### Methods


- Node() (GC)
- Node* new()
- void delete()
- bool SaveXML(File* dest, const String indentation = "\t") const
- bool SaveJSON(File* dest, const String indentation = "\t") const
- void SetName(const String name)
- void AddTag(const String tag)
- void AddTags(const String tags, char separator)
- bool RemoveTag(const String tag)
- void RemoveAllTags()
- void SetPosition(const Vector3& position)
- void SetPosition2D(const Vector2& position)
- void SetPosition2D(float x, float y)
- void SetRotation(const Quaternion& rotation)
- void SetRotation2D(float rotation)
- void SetDirection(const Vector3& direction)
- void SetScale(float scale)
- void SetScale(const Vector3& scale)
- void SetScale2D(const Vector2& scale)
- void SetScale2D(float x, float y)
- void SetTransform(const Vector3& position, const Quaternion& rotation)
- void SetTransform(const Vector3& position, const Quaternion& rotation, const Vector3& scale)
- void SetTransform(const Vector3& position, const Quaternion& rotation, float scale)
- void SetTransform(const Matrix3x4& transform)
- void SetTransform2D(const Vector2& position, float rotation)
- void SetTransform2D(const Vector2& position, float rotation, const Vector2& scale)
- void SetTransform2D(const Vector2& position, float rotation, float scale)
- void SetWorldPosition(const Vector3& position)
- void SetWorldPosition2D(const Vector2& position)
- void SetWorldPosition2D(float x, float y)
- void SetWorldRotation(const Quaternion& rotation)
- void SetWorldRotation2D(float rotation)
- void SetWorldDirection(const Vector3& direction)
- void SetWorldScale(float scale)
- void SetWorldScale(const Vector3& scale)
- void SetWorldScale2D(const Vector2& scale)
- void SetWorldScale2D(float x, float y)
- void SetWorldTransform(const Vector3& position, const Quaternion& rotation)
- void SetWorldTransform(const Vector3& position, const Quaternion& rotation, const Vector3& scale)
- void SetWorldTransform(const Vector3& position, const Quaternion& rotation, float scale)
- void SetWorldTransform2D(const Vector2& position, float rotation)
- void SetWorldTransform2D(const Vector2& position, float rotation, const Vector2& scale)
- void SetWorldTransform2D(const Vector2& position, float rotation, float scale)
- void Translate(const Vector3& delta, TransformSpace space = TS_LOCAL)
- void Translate2D(const Vector2& delta, TransformSpace space = TS_LOCAL)
- void Rotate(const Quaternion& delta, TransformSpace space = TS_LOCAL)
- void Rotate2D(float delta, TransformSpace space = TS_LOCAL)
- void RotateAround(const Vector3& point, const Quaternion& delta, TransformSpace space = TS_LOCAL)
- void RotateAround2D(const Vector2& point, float delta, TransformSpace space = TS_LOCAL)
- void Pitch(float angle, TransformSpace space = TS_LOCAL)
- void Yaw(float angle, TransformSpace space = TS_LOCAL)
- void Roll(float angle, TransformSpace space = TS_LOCAL)
- bool LookAt(const Vector3& target)
- bool LookAt(const Vector3& target, const Vector3& upAxis, TransformSpace space = TS_WORLD)
- void Scale(float scale)
- void Scale(const Vector3& scale)
- void Scale2D(const Vector2& scale)
- void SetEnabled(bool enable)
- void SetDeepEnabled(bool enable)
- void ResetDeepEnabled()
- void SetEnabledRecursive(bool enable)
- void SetOwner(Connection* owner)
- void MarkDirty()
- Node* CreateChild(const String name = String::EMPTY, CreateMode mode = REPLICATED, unsigned id = 0, bool temporary = false)
- Node* CreateTemporaryChild(const String name = String::EMPTY, CreateMode mode = REPLICATED, unsigned id = 0)
- void AddChild(Node* node, unsigned index = M_MAX_UNSIGNED)
- void RemoveChild(Node* node)
- void RemoveAllChildren()
- void RemoveChildren(bool removeReplicated, bool removeLocal, bool recursive)
- void RemoveComponent(Component* component)
- void RemoveComponent(StringHash type)
- void RemoveComponent(const String type)
- void RemoveComponents(bool removeReplicated, bool removeLocal)
- void RemoveComponents(const String type)
- void RemoveAllComponents()
- void ReorderComponent(Component* component, unsigned index)
- Node* Clone(CreateMode mode = REPLICATED)
- void Remove()
- void SetParent(Node* parent)
- void SetVar(StringHash key, const Variant& value)
- void AddListener(Component* component)
- void RemoveListener(Component* component)
- Component* CreateComponent(const String type, CreateMode mode = REPLICATED, unsigned id = 0)
- Component* GetOrCreateComponent(const String type, CreateMode mode = REPLICATED, unsigned id = 0)
- Component* CloneComponent(Component* component, unsigned id = 0)
- Component* CloneComponent(Component* component, CreateMode mode, unsigned id = 0)
- int CreateScriptObject(const String scriptObjectType)
- int CreateScriptObject(const String fileName, const String scriptObjectType)
- int GetScriptObject() const
- int GetScriptObject(const String scriptObjectType) const
- unsigned GetID() const
- bool IsReplicated() const
- const String GetName() const
- StringHash GetNameHash() const
- Node* GetParent() const
- Scene* GetScene() const
- bool IsChildOf(Node* node) const
- bool IsEnabled() const
- bool IsEnabledSelf() const
- Connection* GetOwner() const
- const Vector3& GetPosition() const
- Vector2 GetPosition2D() const
- const Quaternion& GetRotation() const
- float GetRotation2D() const
- Vector3 GetDirection() const
- Vector3 GetUp() const
- Vector3 GetRight() const
- const Vector3& GetScale() const
- Vector2 GetScale2D() const
- Matrix3x4 GetTransform() const
- Vector3 GetWorldPosition() const
- Vector2 GetWorldPosition2D() const
- Quaternion GetWorldRotation() const
- float GetWorldRotation2D() const
- Vector3 GetWorldDirection() const
- Vector3 GetWorldUp() const
- Vector3 GetWorldRight() const
- Vector3 GetWorldScale() const
- Vector3 GetSignedWorldScale() const
- Vector2 GetWorldScale2D() const
- const Matrix3x4& GetWorldTransform() const
- Vector3 LocalToWorld(const Vector3& position) const
- Vector3 LocalToWorld(const Vector4& vector) const
- Vector2 LocalToWorld2D(const Vector2& vector) const
- Vector3 WorldToLocal(const Vector3& position) const
- Vector3 WorldToLocal(const Vector4& vector) const
- Vector2 WorldToLocal2D(const Vector2& vector) const
- bool IsDirty() const
- unsigned GetNumChildren(bool recursive = false) const
- Node* GetChild(const String name, bool recursive = false) const
- Node* GetChild(StringHash nameHash, bool recursive = false) const
- Node* GetChild(unsigned index) const
- unsigned GetNumComponents() const
- unsigned GetNumNetworkComponents() const
- bool HasComponent(StringHash type) const
- bool HasComponent(const String type) const
- const Variant& GetVar(StringHash key) const
- const VariantMap& GetVars() const
- Component* GetComponent(const String type, bool recursive = false) const
- Component* GetParentComponent(const String type, bool recursive = false) const
- const PODVector<Component*>& GetComponents(const String type, bool recursive = false)
- const PODVector<Node*>& GetChildren(bool recursive = false)
- const PODVector<Node*>& GetChildrenWithComponent(const String type, bool recursive = false)
- bool Load(Deserializer& source, SceneResolver& resolver, bool loadChildren = true, bool rewriteIDs = false, CreateMode mode = REPLICATED)
- bool LoadXML(const XMLElement& source, SceneResolver& resolver, bool loadChildren = true, bool rewriteIDs = false, CreateMode mode = REPLICATED)
- bool LoadJSON(const JSONValue& source, SceneResolver& resolver, bool loadChildren = true, bool rewriteIDs = false, CreateMode mode = REPLICATED)
- Node* CreateChild(unsigned id, CreateMode mode, bool temporary = false)
- void AddComponent(Component* component, unsigned id, CreateMode mode)
- bool HasTag(const String tag) const
- const StringVector& GetTags() const
- const PODVector<Node*>& GetChildrenWithTag(const String tag, bool recursive = false) const
- void SetID(unsigned id)

### Properties


- unsigned ID (readonly)
- bool replicated (readonly)
- String name
- StringHash nameHash (readonly)
- Node* parent
- Scene* scene (readonly)
- bool enabled
- bool enabledSelf (readonly)
- Connection* owner
- Vector3& position
- Vector2 position2D
- Quaternion& rotation
- float rotation2D
- Vector3 direction
- Vector3 up (readonly)
- Vector3 right (readonly)
- Vector3& scale
- Vector2 scale2D
- Matrix3x4 transform (readonly)
- Vector3 worldPosition
- Vector2 worldPosition2D
- Quaternion worldRotation
- float worldRotation2D
- Vector3 worldDirection
- Vector3 worldUp (readonly)
- Vector3 worldRight (readonly)
- Vector3 worldScale
- Vector3 signedWorldScale (readonly)
- Vector2 worldScale2D
- Matrix3x4& worldTransform (readonly)
- bool dirty (readonly)
- unsigned numComponents (readonly)
- unsigned numNetworkComponents (readonly)



---

**Inherits from**: Animatable

## Component : Animatable


### Methods


- void SetEnabled(bool enable)
- void Remove()
- void DrawDebugGeometry(DebugRenderer* debug, bool depthTest)
- unsigned GetID() const
- bool IsReplicated() const
- Node* GetNode() const
- Scene* GetScene() const
- bool IsEnabled() const
- bool IsEnabledEffective() const
- Component* GetComponent(StringHash type) const
- Component* GetComponent(const String type) const

### Properties


- unsigned ID (readonly)
- bool replicated (readonly)
- bool enabled
- bool enabledEffective (readonly)
- Node* node (readonly)
- Scene* scene (readonly)



---

**Inherits from**: Object

## Serializable : Object


### Methods


- void SetTemporary(bool enable)
- bool IsTemporary() const
- void SetInterceptNetworkUpdate(const String attributeName, bool enable)
- bool GetInterceptNetworkUpdate(const String attributeName)

### Properties


- bool temporary



---

**Inherits from**: Serializable

## Animatable : Serializable


### Methods


- void SetAnimationEnabled(bool enable)
- void SetAnimationTime(float time)
- void SetObjectAnimation(ObjectAnimation* objectAnimation)
- void SetAttributeAnimation(const String name, ValueAnimation* attributeAnimation, WrapMode wrapMode = WM_LOOP, float speed = 1.0f)
- void SetAttributeAnimationWrapMode(const String name, WrapMode wrapMode)
- void SetAttributeAnimationSpeed(const String name, float speed)
- void SetAttributeAnimationTime(const String name, float time)
- void RemoveObjectAnimation()
- void RemoveAttributeAnimation(const String name)
- bool GetAnimationEnabled() const
- ObjectAnimation* GetObjectAnimation() const
- ValueAnimation* GetAttributeAnimation(const String name) const
- WrapMode GetAttributeAnimationWrapMode(const String name) const
- float GetAttributeAnimationSpeed(const String name) const
- float GetAttributeAnimationTime(const String name) const

### Properties


- bool animationEnabled
- ObjectAnimation* objectAnimation



---

**Inherits from**: RefCounted

## Object : RefCounted


### Methods


- StringHash GetType() const
- const String GetTypeName() const
- const String GetCategory() const
- void SetBlockEvents(bool block)
- bool GetBlockEvents() const
- void SendEvent(const String eventName, VariantMap* eventData = 0)
- bool HasSubscribedToEvent(const String eventName) const
- bool HasSubscribedToEvent(Object* sender, const String eventName) const

### Properties


- StringHash type (readonly)
- const String typeName (readonly)
- const String category (readonly)



---

## Context



### Methods


- Object* GetEventSender() const
- EventHandler* GetEventHandler() const
- const String GetTypeName(StringHash objectType) const



---

**Inherits from**: Object

## Engine : Object


### Methods


- void RunFrame()
- Console* CreateConsole()
- DebugHud* CreateDebugHud()
- void SetMinFps(int fps)
- void SetMaxFps(int fps)
- void SetMaxInactiveFps(int fps)
- void SetTimeStepSmoothing(int frames)
- void SetPauseMinimized(bool enable)
- void SetAutoExit(bool enable)
- void Exit()
- void DumpProfiler()
- void DumpResources(bool dumpFileName = false)
- void DumpMemory()
- int GetMinFps() const
- int GetMaxFps() const
- int GetMaxInactiveFps() const
- int GetTimeStepSmoothing() const
- bool GetPauseMinimized() const
- bool GetAutoExit() const
- bool IsInitialized() const
- bool IsExiting() const
- bool IsHeadless() const

### Properties


- int minFps
- int maxFps
- int maxInactiveFps
- int timeStepSmoothing
- bool pauseMinimized
- bool autoExit
- bool initialized (readonly)
- bool exiting (readonly)
- bool headless (readonly)



---

**Inherits from**: Object

## Time : Object


### Methods


- unsigned GetFrameNumber() const
- float GetTimeStep() const
- unsigned GetTimerPeriod() const
- float GetElapsedTime()
- float GetFramesPerSecond() const
- unsigned GetSystemTime()
- unsigned GetTimeSinceEpoch()
- String GetTimeStamp()
- void Sleep(unsigned mSec)

### Properties


- unsigned frameNumber (readonly)
- float timeStep (readonly)
- unsigned timerPeriod (readonly)
- float elapsedTime (readonly)



---

