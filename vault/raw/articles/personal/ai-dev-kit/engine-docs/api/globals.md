# Global Functions, Properties and Constants

UrhoX Lua API - Global Scope

---

## Global Properties

Available global objects (accessible without declaration):

```lua
Audio* audio (readonly)
ResourceCache* cache (readonly)
Console* console (readonly)
Context* context (readonly)
Database* database (readonly)
DebugHud* debugHud (readonly)
Engine* engine (readonly)
EventHandler* eventHandler (readonly)
EventSender* eventSender (readonly)
FileSystem* fileSystem (readonly)
Graphics* graphics (readonly)
Input* input (readonly)
Localization* localization (readonly)
Log* log (readonly)
Network* network (readonly)
Renderer* renderer (readonly)
Time* time (readonly)
UI* ui (readonly)
```

---

## Global Functions

### A

- `Audio* GetAudio()`

### C

- `Color ToColor(const String source)`
- `Console* GetConsole()`
- `Context* GetContext()`

### D

- `DBAPI GetDBAPI()`
- `Database* GetDatabase()`
- `DebugHud* GetDebugHud()`

### E

- `Engine* GetEngine()`
- `EventHandler* GetEventHandler() const`

### F

- `FileSystem* GetFileSystem()`

### G

- `Graphics* GetGraphics()`

### I

- `Input* GetInput()`
- `IntRect ToIntRect(const String source)`
- `IntVector2 ToIntVector2(const String source)`
- `IntVector2 VectorCeilToInt(const Vector2& vec)`
- `IntVector2 VectorFloorToInt(const Vector2& vec)`
- `IntVector2 VectorMax(const IntVector2& lhs, const IntVector2& rhs)`
- `IntVector2 VectorMin(const IntVector2& lhs, const IntVector2& rhs)`
- `IntVector2 VectorRoundToInt(const Vector2& vec)`
- `IntVector3 ToIntVector3(const String source)`
- `IntVector3 VectorCeilToInt(const Vector3& vec)`
- `IntVector3 VectorFloorToInt(const Vector3& vec)`
- `IntVector3 VectorMax(const IntVector3& lhs, const IntVector3& rhs)`
- `IntVector3 VectorMin(const IntVector3& lhs, const IntVector3& rhs)`
- `IntVector3 VectorRoundToInt(const Vector3& vec)`

### L

- `Localization* GetLocalization()`
- `Log* GetLog()`

### M

- `Matrix3 ToMatrix3(const String source)`
- `Matrix3x4 ToMatrix3x4(const String source)`
- `Matrix4 ToMatrix4(const String source)`

### N

- `Network* GetNetwork()`

### O

- `Object* GetEventSender()`

### Q

- `Quaternion ToQuaternion(const String source)`

### R

- `Rect ToRect(const String source)`
- `Renderer* GetRenderer()`
- `ResourceCache* GetCache()`

### S

- `String AddTrailingSlash(const String pathName)`
- `String GetConsoleInput()`
- `String GetExtension(const String fullPath, bool lowercaseExtension = true)`
- `String GetFileName(const String fullPath)`
- `String GetFileNameAndExtension(const String fullPath, bool lowercaseExtension = false)`
- `String GetFileSizeString(long memorySize)`
- `String GetHostName()`
- `String GetInternalPath(const String pathName)`
- `String GetLoginName()`
- `String GetMiniDumpDir()`
- `String GetNativePath(const String pathName)`
- `String GetOSVersion()`
- `String GetParentPath(const String pathName)`
- `String GetPath(const String fullPath)`
- `String GetPlatform()`
- `String RemoveTrailingSlash(const String pathName)`
- `String ReplaceExtension(const String fullPath, const String newExtension)`
- `String ToString(void* value)`
- `String ToStringHex(unsigned value)`

### T

- `Time* GetTime()`

### U

- `UI* GetUI()`

### V

- `Variant GetGlobalVar(const String key)`
- `VariantMap& GetGlobalVars()`
- `Vector2 ToVector2(const String source)`
- `Vector2 VectorCeil(const Vector2& vec)`
- `Vector2 VectorFloor(const Vector2& vec)`
- `Vector2 VectorLerp(const Vector2& lhs, const Vector2& rhs, const Vector2& t)`
- `Vector2 VectorMax(const Vector2& lhs, const Vector2& rhs)`
- `Vector2 VectorMin(const Vector2& lhs, const Vector2& rhs)`
- `Vector2 VectorRound(const Vector2& vec)`
- `Vector3 ToVector3(const String source)`
- `Vector3 VectorCeil(const Vector3& vec)`
- `Vector3 VectorFloor(const Vector3& vec)`
- `Vector3 VectorLerp(const Vector3& lhs, const Vector3& rhs, const Vector3& t)`
- `Vector3 VectorMax(const Vector3& lhs, const Vector3& rhs)`
- `Vector3 VectorMin(const Vector3& lhs, const Vector3& rhs)`
- `Vector3 VectorRound(const Vector3& vec)`
- `Vector4 ToVector4(const String source, bool allowMissingCoords = false)`
- `Vector4 VectorCeil(const Vector4& vec)`
- `Vector4 VectorFloor(const Vector4& vec)`
- `Vector4 VectorLerp(const Vector4& lhs, const Vector4& rhs, const Vector4& t)`
- `Vector4 VectorMax(const Vector4& lhs, const Vector4& rhs)`
- `Vector4 VectorMin(const Vector4& lhs, const Vector4& rhs)`
- `Vector4 VectorRound(const Vector4& vec)`
- `VectorBuffer CompressVectorBuffer(VectorBuffer& src)`
- `VectorBuffer DecompressVectorBuffer(VectorBuffer& src)`

### B

- `bool Equals(float lhs, float rhs)`
- `bool GetExecuteConsoleCommands()`
- `bool HasSubscribedToEvent(Object* sender, const String eventName)`
- `bool HasSubscribedToEvent(const String eventName)`
- `bool IsAbsolutePath(const String pathName)`
- `bool IsAlpha(unsigned ch)`
- `bool IsDigit(unsigned ch)`
- `bool IsNaN(float value)`
- `bool IsPowerOfTwo(unsigned value)`
- `bool ToBool(const String source)`

### C

- `const Vector<String>& GetArguments()`

### F

- `float Abs(float value)`
- `float Acos(float x)`
- `float Asin(float x)`
- `float Atan(float x)`
- `float Atan2(float y, float x)`
- `float Ceil(float x)`
- `float Clamp(float value, float min, float max)`
- `float Cos(float angle)`
- `float Floor(float x)`
- `float Fract(float x)`
- `float InverseLerp(float lhs, float rhs, float x)`
- `float Lerp(float lhs, float rhs, float t)`
- `float Ln(float x)`
- `float Max(float lhs, float rhs)`
- `float Min(float lhs, float rhs)`
- `float Mod(float x, float y)`
- `float Pow(float x, float y)`
- `float RandStandardNormal()`
- `float Random()`
- `float Random(float min, float max)`
- `float Random(float range)`
- `float RandomNormal(float meanValue, float variance)`
- `float Round(float x)`
- `float Sign(float value)`
- `float Sin(float angle)`
- `float SmoothStep(float lhs, float rhs, float t)`
- `float Sqrt(float x)`
- `float StableRandom(const Vector2& seed)`
- `float StableRandom(const Vector3& seed)`
- `float StableRandom(float seed)`
- `float Tan(float angle)`
- `float ToFloat(const String source)`

### I

- `int AbsInt(int value)`
- `int CeilToInt(float x)`
- `int ClampInt(int value, int min, int max)`
- `int FloorToInt(float x)`
- `int MaxInt(int lhs, int rhs)`
- `int MinInt(int lhs, int rhs)`
- `int Rand()`
- `int RandomInt(int min, int max)`
- `int RandomInt(int range)`
- `int RoundToInt(float x)`
- `int ToInt(const String source, int base = 10)`
- `int ToInt64(const String source, int base = 10)`
- `int ToUInt64(const String source, int base = 10)`

### L

- `long GetTotalMemory()`

### U

- `unsigned CountSetBits(unsigned value)`
- `unsigned GetNumLogicalCPUs()`
- `unsigned GetNumPhysicalCPUs()`
- `unsigned GetRandomSeed()`
- `unsigned LogBaseTwo(unsigned value)`
- `unsigned NextPowerOfTwo(unsigned value)`
- `unsigned SDBMHash(unsigned hash, char c)`
- `unsigned ToLower(unsigned ch)`
- `unsigned ToUInt(const String source, int base = 10)`
- `unsigned ToUpper(unsigned ch)`

### V

- `void ErrorDialog(const String title, const String message)`
- `void ErrorExit(const String message = String::EMPTY, int exitCode = EXIT_FAILURE)`
- `void OpenConsoleWindow()`
- `void PrintLine(const String str, bool error = false)`
- `void PrintLine(const char* str, bool error = false)`
- `void RegisterEventName(const String eventName)`
- `void SendEvent(const String eventName, VariantMap& eventData)`
- `void SetExecuteConsoleCommands(bool enable)`
- `void SetGlobalVar(const String key, Variant value)`
- `void SetMiniDumpDir(const String pathName)`
- `void SetRandomSeed(unsigned seed)`
- `void SubscribeToEvent(const String eventName, void* functionOrFunctionName)`
- `void SubscribeToEvent(void* sender, const String eventName, void* functionOrFunctionName)`
- `void UnsubscribeFromAllEvents()`
- `void UnsubscribeFromAllEventsExcept(const Vector<String>& exceptionNames)`
- `void UnsubscribeFromEvent(Object* sender, const String eventName)`
- `void UnsubscribeFromEvent(const String eventName)`
- `void UnsubscribeFromEvents(Object* sender)`

---

## Global Constants

```lua
float ANIMATION_LOD_BASESCALE
char CHANNEL_POSITION
char CHANNEL_ROTATION
char CHANNEL_SCALE
unsigned DD_DISABLED
unsigned DD_SOURCE
unsigned DD_SOURCE_AND_TARGET
unsigned DD_TARGET
unsigned DEBUGHUD_SHOW_ALL
unsigned DEBUGHUD_SHOW_EVENTPROFILER
unsigned DEBUGHUD_SHOW_MEMORY
unsigned DEBUGHUD_SHOW_MODE
unsigned DEBUGHUD_SHOW_NONE
unsigned DEBUGHUD_SHOW_PROFILER
unsigned DEBUGHUD_SHOW_STATS
unsigned DEFAULT_LIGHTMASK
unsigned DEFAULT_SHADOWMASK
unsigned DEFAULT_VIEWMASK
unsigned DEFAULT_ZONEMASK
unsigned DRAWABLE_ANY
unsigned DRAWABLE_GEOMETRY
unsigned DRAWABLE_GEOMETRY2D
unsigned DRAWABLE_LIGHT
unsigned DRAWABLE_ZONE
unsigned FIRST_LOCAL_ID
unsigned FIRST_REPLICATED_ID
unsigned FLIP_ALL
unsigned FLIP_DIAGONAL
unsigned FLIP_HORIZONTAL
unsigned FLIP_RESERVED
unsigned FLIP_VERTICAL
unsigned LAST_LOCAL_ID
unsigned LAST_REPLICATED_ID
int LOG_DEBUG
int LOG_ERROR
int LOG_INFO
int LOG_NONE
int LOG_TRACE
int LOG_WARNING
int MAX_VERTEX_LIGHTS
float M_DEGTORAD
float M_DEGTORAD_2
float M_EPSILON
float M_HALF_PI
float M_INFINITY
float M_LARGE_EPSILON
float M_LARGE_VALUE
float M_MAX_FOV
int M_MAX_INT
unsigned M_MAX_UNSIGNED
int M_MIN_INT
float M_MIN_NEARCLIP
unsigned M_MIN_UNSIGNED
float M_PI
float M_RADTODEG
unsigned NUM_FRUSTUM_PLANES
unsigned NUM_FRUSTUM_VERTICES
float PIXEL_SIZE
unsigned SCAN_DIRS
unsigned SCAN_FILES
unsigned SCAN_HIDDEN
String SOUND_AMBIENT
String SOUND_EFFECT
String SOUND_MASTER
String SOUND_MUSIC
String SOUND_VOICE
unsigned VO_DISABLE_OCCLUSION
unsigned VO_DISABLE_SHADOWS
unsigned VO_LOW_MATERIAL_QUALITY
unsigned VO_NONE
```

