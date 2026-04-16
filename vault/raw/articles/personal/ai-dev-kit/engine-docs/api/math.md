# Math Types

UrhoX Lua API - Math Types

---

## Classes

- [Vector2](#vector2)
- [Vector3](#vector3)
- [Vector4](#vector4)
- [IntVector2](#intvector2)
- [IntVector3](#intvector3)
- [Quaternion](#quaternion)
- [Matrix3](#matrix3)
- [Matrix3x4](#matrix3x4)
- [Matrix4](#matrix4)
- [Color](#color)
- [Rect](#rect)
- [IntRect](#intrect)
- [BoundingBox](#boundingbox)
- [Sphere](#sphere)
- [Plane](#plane)
- [Ray](#ray)
- [Frustum](#frustum)
- [Polyhedron](#polyhedron)
- [Spline](#spline)
- [SplinePath](#splinepath)

---

## Vector2



### Methods


- Vector2() (GC)
- Vector2* new()
- Vector2(const Vector2& vector) (GC)
- Vector2* new(const Vector2& vector)
- Vector2(const IntVector2& vector) (GC)
- Vector2* new(const IntVector2& vector)
- Vector2(float x, float y) (GC)
- Vector2* new(float x, float y)
- void delete()
- bool operator==(const Vector2& rhs) const
- Vector2 operator+(const Vector2& rhs) const
- Vector2 operator-() const
- Vector2 operator-(const Vector2& rhs) const
- Vector2 operator*(float rhs) const
- Vector2 operator*(const Vector2& rhs) const
- Vector2 operator/(float rhs) const
- Vector2 operator/(const Vector2& rhs) const
- void Normalize()
- float Length() const
- float LengthSquared() const
- float DotProduct(const Vector2& rhs) const
- float AbsDotProduct(const Vector2& rhs) const
- float ProjectOntoAxis(const Vector2& axis) const
- float Angle(const Vector2& rhs) const
- Vector2 Abs() const
- Vector2 Lerp(const Vector2& rhs, float t) const
- bool Equals(const Vector2& rhs) const
- bool IsNaN() const
- Vector2 Normalized() const
- String ToString() const

### Properties


- float x
- float y
- const Vector2 ZERO
- const Vector2 LEFT
- const Vector2 RIGHT
- const Vector2 UP
- const Vector2 DOWN
- const Vector2 ONE



---

## Vector3



### Methods


- Vector3() (GC)
- Vector3* new()
- Vector3(const Vector3& vector) (GC)
- Vector3* new(const Vector3& vector)
- Vector3(const Vector2& vector, float z) (GC)
- Vector3* new(const Vector2& vector, float z)
- Vector3(const Vector2& vector) (GC)
- Vector3* new(const Vector2& vector)
- Vector3(const IntVector3& vector) (GC)
- Vector3* new(const IntVector3& vector)
- Vector3(float x, float y, float z) (GC)
- Vector3* new(float x, float y, float z)
- Vector3(float x, float y) (GC)
- Vector3* new(float x, float y)
- void delete()
- bool operator==(const Vector3& rhs) const
- Vector3 operator+(const Vector3& rhs) const
- Vector3 operator-() const
- Vector3 operator-(const Vector3& rhs) const
- Vector3 operator*(float rhs) const
- Vector3 operator*(const Vector3& rhs) const
- Vector3 operator/(float rhs) const
- Vector3 operator/(const Vector3& rhs) const
- void Normalize()
- float Length() const
- float LengthSquared() const
- float DotProduct(const Vector3& rhs) const
- float AbsDotProduct(const Vector3& rhs) const
- float ProjectOntoAxis(const Vector3& axis) const
- Vector3 ProjectOntoPlane(const Vector3& origin, const Vector3& normal)
- Vector3 ProjectOntoLine(const Vector3& from, const Vector3& to, bool clamped = false)
- float DistanceToPoint(const Vector3& point) const
- float DistanceToPlane(const Vector3& origin, const Vector3& normal) const
- Vector3 Orthogonalize(const Vector3& axis) const
- Vector3 CrossProduct(const Vector3& rhs) const
- Vector3 Abs() const
- Vector3 Lerp(const Vector3& rhs, float t) const
- bool Equals(const Vector3& rhs) const
- bool IsNaN() const
- float Angle(const Vector3& rhs) const
- Vector3 Normalized() const
- String ToString() const

### Properties


- float x
- float y
- float z
- const Vector3 ZERO
- const Vector3 LEFT
- const Vector3 RIGHT
- const Vector3 UP
- const Vector3 DOWN
- const Vector3 FORWARD
- const Vector3 BACK
- const Vector3 ONE



---

## Vector4



### Methods


- Vector4() (GC)
- Vector4* new()
- Vector4(const Vector4& vector) (GC)
- Vector4* new(const Vector4& vector)
- Vector4(const Vector3& vector, float w) (GC)
- Vector4* new(const Vector3& vector, float w)
- Vector4(float x, float y, float z, float w) (GC)
- Vector4* new(float x, float y, float z, float w)
- void delete()
- bool operator==(const Vector4& rhs) const
- Vector4 operator+(const Vector4& rhs) const
- Vector4 operator-() const
- Vector4 operator-(const Vector4& rhs) const
- Vector4 operator*(float rhs) const
- Vector4 operator*(const Vector4& rhs) const
- Vector4 operator/(float rhs) const
- Vector4 operator/(const Vector4& rhs) const
- Vector4 operator/(const Vector4& rhs) const
- float DotProduct(const Vector4& rhs) const
- float AbsDotProduct(const Vector4& rhs) const
- float ProjectOntoAxis(const Vector3& axis) const
- Vector4 Abs() const
- Vector4 Lerp(const Vector4& rhs, float t) const
- bool Equals(const Vector4& rhs) const
- bool IsNaN() const
- String ToString() const

### Properties


- float x
- float y
- float z
- float w
- const Vector4 ZERO
- const Vector4 ONE



---

## IntVector2



### Methods


- IntVector2() (GC)
- IntVector2* new()
- IntVector2(int x, int y) (GC)
- IntVector2* new(int x, int y)
- IntVector2(const IntVector2& rhs) (GC)
- IntVector2* new(const IntVector2& rhs)
- void delete()
- bool operator==(const IntVector2& rhs) const
- IntVector2 operator+(const IntVector2& rhs) const
- IntVector2 operator-() const
- IntVector2 operator-(const IntVector2& rhs) const
- IntVector2 operator*(int rhs) const
- IntVector2 operator*(const IntVector2& rhs) const
- IntVector2 operator/(int rhs) const
- IntVector2 operator/(const IntVector2& rhs) const
- String ToString() const
- unsigned ToHash() const
- float Length() const

### Properties


- int x
- int y
- const IntVector2 ZERO
- const IntVector2 LEFT
- const IntVector2 RIGHT
- const IntVector2 UP
- const IntVector2 DOWN
- const IntVector2 ONE



---

## IntVector3



### Methods


- IntVector3() (GC)
- IntVector3* new()
- IntVector3(int x, int y, int z) (GC)
- IntVector3* new(int x, int y, int z)
- IntVector3(const IntVector3& rhs) (GC)
- IntVector3* new(const IntVector3& rhs)
- void delete()
- bool operator==(const IntVector3& rhs) const
- IntVector3 operator+(const IntVector3& rhs) const
- IntVector3 operator-() const
- IntVector3 operator-(const IntVector3& rhs) const
- IntVector3 operator*(int rhs) const
- IntVector3 operator*(const IntVector3& rhs) const
- IntVector3 operator/(int rhs) const
- IntVector3 operator/(const IntVector3& rhs) const
- String ToString() const
- unsigned ToHash() const
- float Length() const

### Properties


- int x
- int y
- int z
- const IntVector3 ZERO
- const IntVector3 LEFT
- const IntVector3 RIGHT
- const IntVector3 UP
- const IntVector3 DOWN
- const IntVector3 FORWARD
- const IntVector3 BACK
- const IntVector3 ONE



---

## Quaternion



### Methods


- Quaternion() (GC)
- Quaternion* new()
- Quaternion(const Quaternion& quat) (GC)
- Quaternion* new(const Quaternion& quat)
- Quaternion(float w, float x, float y, float z) (GC)
- Quaternion* new(float w, float x, float y, float z)
- Quaternion(float angle, const Vector3& axis) (GC)
- Quaternion* new(float angle, const Vector3& axis)
- Quaternion(float angle) (GC)
- Quaternion* new(float angle)
- Quaternion(float x, float y, float z) (GC)
- Quaternion* new(float x, float y, float z)
- Quaternion(const Vector3& start, const Vector3& end) (GC)
- Quaternion* new(const Vector3& start, const Vector3& end)
- Quaternion(const Vector3& xAxis, const Vector3& yAxis, const Vector3& zAxis) (GC)
- Quaternion* new(const Vector3& xAxis, const Vector3& yAxis, const Vector3& zAxis)
- Quaternion(const Matrix3& matrix) (GC)
- Quaternion* new(const Matrix3& matrix)
- void delete()
- bool operator==(const Quaternion& rhs) const
- Quaternion operator*(float rhs) const
- Quaternion operator-() const
- bool operator==(const Quaternion& rhs) const
- Quaternion operator*(float rhs) const
- Quaternion operator-() const
- Quaternion operator+(const Quaternion& rhs) const
- Quaternion operator-(const Quaternion& rhs) const
- Quaternion operator*(const Quaternion& rhs) const
- Vector3 operator*(const Vector3& rhs) const
- void FromAngleAxis(float angle, const Vector3& axis)
- void FromEulerAngles(float x, float y, float z)
- void FromRotationTo(const Vector3& start, const Vector3& end)
- void FromAxes(const Vector3& xAxis, const Vector3& yAxis, const Vector3& zAxis)
- void FromRotationMatrix(const Matrix3& matrix)
- bool FromLookRotation(const Vector3& direction, const Vector3& up)
- void Normalize()
- Quaternion Normalized() const
- Quaternion Inverse() const
- float LengthSquared() const
- float DotProduct(const Quaternion& rhs) const
- bool Equals(const Quaternion& rhs) const
- bool IsNaN() const
- Quaternion Conjugate() const
- Vector3 EulerAngles() const
- float YawAngle() const
- float PitchAngle() const
- float RollAngle() const
- Vector3 Axis() const
- float Angle() const
- Matrix3 RotationMatrix() const
- Quaternion Slerp(const Quaternion& rhs, float t) const
- Quaternion Nlerp(const Quaternion& rhs, float t, bool shortestPath) const
- String ToString() const

### Properties


- float w
- float x
- float y
- float z
- const Quaternion IDENTITY



---

## Matrix3



### Methods


- Matrix3() (GC)
- Matrix3* new()
- Matrix3(const Matrix3& matrix) (GC)
- Matrix3* new(const Matrix3& matrix)
- Matrix3(float v00, float v01, float v02, float v10, float v11, float v12, float v20, float v21, float v22) (GC)
- Matrix3* new(float v00, float v01, float v02, float v10, float v11, float v12, float v20, float v21, float v22)
- void delete()
- bool operator==(const Matrix3& rhs) const
- Vector3 operator*(const Vector3& rhs) const
- Matrix3 operator+(const Matrix3& rhs) const
- Matrix3 operator-(const Matrix3& rhs) const
- Matrix3 operator*(float rhs) const
- Matrix3 operator*(const Matrix3& rhs) const
- void SetScale(const Vector3& scale)
- void SetScale(float scale)
- Vector3 Scale() const
- Matrix3 Transpose() const
- Matrix3 Scaled(const Vector3& scale) const
- bool Equals(const Matrix3& rhs) const
- Matrix3 Inverse() const
- String ToString() const

### Properties


- float m00
- float m01
- float m02
- float m10
- float m11
- float m12
- float m20
- float m21
- float m22
- const Matrix3 ZERO
- const Matrix3 IDENTITY



---

## Matrix3x4



### Methods


- Matrix3x4() (GC)
- Matrix3x4* new()
- Matrix3x4(const Matrix3x4& matrix) (GC)
- Matrix3x4* new(const Matrix3x4& matrix)
- Matrix3x4(const Matrix3& matrix) (GC)
- Matrix3x4* new(const Matrix3& matrix)
- Matrix3x4(const Matrix4& matrix) (GC)
- Matrix3x4* new(const Matrix4& matrix)
- Matrix3x4(float v00, float v01, float v02, float v03, float v10, float v11, float v12, float v13, float v20, float v21, float v22, float v23) (GC)
- Matrix3x4* new(float v00, float v01, float v02, float v03, float v10, float v11, float v12, float v13, float v20, float v21, float v22, float v23)
- Matrix3x4(const Vector3& translation, const Quaternion& rotation, float scale) (GC)
- Matrix3x4* new(const Vector3& translation, const Quaternion& rotation, float scale)
- Matrix3x4(const Vector3& translation, const Quaternion& rotation, const Vector3& scale) (GC)
- Matrix3x4* new(const Vector3& translation, const Quaternion& rotation, const Vector3& scale)
- void delete()
- bool operator==(const Matrix3x4& rhs) const
- Vector3 operator*(const Vector3& rhs) const
- Vector3 operator*(const Vector4& rhs) const
- Matrix3x4 operator+(const Matrix3x4& rhs) const
- Matrix3x4 operator-(const Matrix3x4& rhs) const
- Matrix3x4 operator*(float rhs) const
- Matrix3x4 operator*(const Matrix3x4& rhs) const
- Matrix4 operator*(const Matrix4& rhs) const
- void SetTranslation(const Vector3& translation)
- void SetRotation(const Matrix3& rotation)
- void SetScale(const Vector3& scale)
- void SetScale(float scale)
- Matrix3 ToMatrix3() const
- Matrix4 ToMatrix4() const
- Matrix3 RotationMatrix() const
- Vector3 Translation() const
- Quaternion Rotation() const
- Vector3 Scale() const
- bool Equals(const Matrix3x4& rhs) const
- void Decompose(Vector3& translation, Quaternion& rotation, Vector3& scale) const
- Matrix3x4 Inverse() const
- String ToString() const

### Properties


- float m00
- float m01
- float m02
- float m03
- float m10
- float m11
- float m12
- float m13
- float m20
- float m21
- float m22
- float m23
- const Matrix3x4 ZERO
- const Matrix3x4 IDENTITY



---

## Matrix4



### Methods


- Matrix4() (GC)
- Matrix4* new()
- Matrix4(const Matrix4& matrix) (GC)
- Matrix4* new(const Matrix4& matrix)
- Matrix4(const Matrix3& matrix) (GC)
- Matrix4* new(const Matrix3& matrix)
- Matrix4(float v00, float v01, float v02, float v03, float v10, float v11, float v12, float v13, float v20, float v21, float v22, float v23, float v30, float v31, float v32, float v33) (GC)
- Matrix4* new(float v00, float v01, float v02, float v03, float v10, float v11, float v12, float v13, float v20, float v21, float v22, float v23, float v30, float v31, float v32, float v33)
- void delete()
- bool operator==(const Matrix4& rhs) const
- Vector3 operator*(const Vector3& rhs) const
- Vector4 operator*(const Vector4& rhs) const
- Matrix4 operator+(const Matrix4& rhs) const
- Matrix4 operator-(const Matrix4& rhs) const
- Matrix4 operator*(float rhs) const
- Matrix4 operator*(const Matrix4& rhs) const
- Matrix4 operator*(const Matrix3x4& rhs) const
- void SetTranslation(const Vector3& translation)
- void SetRotation(const Matrix3& rotation)
- void SetScale(const Vector3& scale)
- void SetScale(float scale)
- Matrix3 ToMatrix3() const
- Matrix3 RotationMatrix() const
- Vector3 Translation() const
- Quaternion Rotation() const
- Vector3 Scale() const
- Matrix4 Transpose() const
- bool Equals(const Matrix4& rhs) const
- void Decompose(Vector3& translation, Quaternion& rotation, Vector3& scale) const
- Matrix4 Inverse() const
- String ToString() const

### Properties


- float m00
- float m01
- float m02
- float m03
- float m10
- float m11
- float m12
- float m13
- float m20
- float m21
- float m22
- float m23
- float m30
- float m31
- float m32
- float m33
- const Matrix4 ZERO
- const Matrix4 IDENTITY



---

## Color



### Methods


- Color() (GC)
- Color* new()
- Color(const Color& color) (GC)
- Color* new(const Color& color)
- Color(const Color& color, float a) (GC)
- Color* new(const Color& color, float a)
- Color(float r, float g, float b) (GC)
- Color* new(float r, float g, float b)
- Color(float r, float g, float b, float a) (GC)
- Color* new(float r, float g, float b, float a)
- void delete()
- bool operator==(const Color& rhs) const
- Color operator*(float rhs) const
- Color operator+(const Color& rhs)
- unsigned ToUInt() const
- Vector3 ToHSL() const
- Vector3 ToHSV() const
- void FromUInt(unsigned color)
- void FromHSL(float h, float s, float l, float a)
- void FromHSV(float h, float s, float v, float a)
- Vector3 ToVector3() const
- Vector4 ToVector4() const
- float SumRGB() const
- float Average() const
- float Luma() const
- float Chroma() const
- float Hue() const
- float SaturationHSL() const
- float SaturationHSV() const
- float Value() const
- float Lightness() const
- float MaxRGB() const
- float MinRGB() const
- float Range() const
- void Clip(bool clipAlpha = false)
- void Invert(bool invertAlpha = false)
- Color Lerp(const Color& rhs, float t) const
- Color Abs() const
- bool Equals(const Color& rhs) const
- String ToString() const

### Properties


- float r
- float g
- float b
- float a
- const Color WHITE
- const Color GRAY
- const Color BLACK
- const Color RED
- const Color GREEN
- const Color BLUE
- const Color CYAN
- const Color MAGENTA
- const Color YELLOW
- const Color TRANSPARENT_BLACK



---

## Rect



### Methods


- Rect() (GC)
- Rect* new()
- Rect(const Rect& rect) (GC)
- Rect* new(const Rect& rect)
- Rect(const Vector2& min, const Vector2& max) (GC)
- Rect* new(const Vector2& min, const Vector2& max)
- Rect(float left, float top, float right, float bottom) (GC)
- Rect* new(float left, float top, float right, float bottom)
- Rect(const Vector4& vector) (GC)
- Rect* new(const Vector4& vector)
- void delete()
- bool operator==(const Rect& rhs) const
- void Define(const Rect& rect)
- void Define(const Vector2& min, const Vector2& max)
- void Define(const Vector2& point)
- void Merge(const Vector2& point)
- void Merge(const Rect& rect)
- void Clear()
- void Clip(const Rect& rect)
- bool Defined() const
- Vector2 Center() const
- Vector2 Size() const
- Vector2 HalfSize() const
- bool Equals(const Rect& rhs) const
- Intersection IsInside(const Vector2& point) const
- Intersection IsInside(const Rect& rect) const
- Vector4 ToVector4() const
- String ToString() const

### Properties


- Vector2 min
- Vector2 max
- const Rect FULL
- const Rect POSITIVE
- const Rect ZERO
- Vector2 center (readonly)
- Vector2 size (readonly)
- Vector2 halfSize (readonly)



---

## IntRect



### Methods


- IntRect() (GC)
- IntRect* new()
- IntRect(int left, int top, int right, int bottom) (GC)
- IntRect* new(int left, int top, int right, int bottom)
- IntRect(const IntVector2& min, const IntVector2& max) (GC)
- IntRect* new(const IntVector2& min, const IntVector2& max)
- void delete()
- bool operator==(const IntRect& rhs) const
- IntVector2 Size() const
- int Width() const
- int Height() const
- Intersection IsInside(const IntVector2& point) const
- void Clip(const IntRect& rect)
- void Merge(const IntRect& rect)

### Properties


- int left
- int top
- int right
- int bottom
- const IntRect ZERO
- IntVector2 size (readonly)
- int width (readonly)
- int height (readonly)



---

## BoundingBox



### Methods


- BoundingBox() (GC)
- BoundingBox* new()
- BoundingBox(const BoundingBox& box) (GC)
- BoundingBox* new(const BoundingBox& box)
- BoundingBox(const Rect& rect) (GC)
- BoundingBox* new(const Rect& rect)
- BoundingBox(const Vector3& min, const Vector3& max) (GC)
- BoundingBox* new(const Vector3& min, const Vector3& max)
- BoundingBox(float min, float max) (GC)
- BoundingBox* new(float min, float max)
- BoundingBox(const Frustum& frustum) (GC)
- BoundingBox* new(const Frustum& frustum)
- BoundingBox(const Polyhedron& poly) (GC)
- BoundingBox* new(const Polyhedron& poly)
- BoundingBox(const Sphere& sphere) (GC)
- BoundingBox* new(const Sphere& sphere)
- void delete()
- bool operator==(const BoundingBox& rhs) const
- void Define(const BoundingBox& box)
- void Define(const Rect& rect)
- void Define(const Vector3& min, const Vector3& max)
- void Define(float min, float max)
- void Define(const Vector3& point)
- void Define(const Frustum& frustum)
- void Define(const Polyhedron& poly)
- void Define(const Sphere& sphere)
- void Merge(const Vector3& point)
- void Merge(const BoundingBox& box)
- void Merge(const Frustum& frustum)
- void Merge(const Polyhedron& poly)
- void Merge(const Sphere& sphere)
- void Clip(const BoundingBox& box)
- void Transform(const Matrix3& transform)
- void Transform(const Matrix3x4& transform)
- void Clear()
- bool Defined() const
- Vector3 Center() const
- Vector3 Size() const
- Vector3 HalfSize() const
- BoundingBox Transformed(const Matrix3& transform) const
- BoundingBox Transformed(const Matrix3x4& transform) const
- Rect Projected(const Matrix4& projection) const
- float DistanceToPoint(const Vector3& point) const
- Intersection IsInside(const Vector3& point) const
- Intersection IsInside(const BoundingBox& box) const
- Intersection IsInsideFast(const BoundingBox& box) const
- Intersection IsInside(const Sphere& sphere) const
- Intersection IsInsideFast(const Sphere& sphere) const
- String ToString() const

### Properties


- Vector3 min
- Vector3 max
- Vector3 center (readonly)
- Vector3 size (readonly)
- Vector3 halfSize (readonly)



---

## Sphere



### Methods


- Sphere() (GC)
- Sphere* new()
- Sphere(const Sphere& sphere) (GC)
- Sphere* new(const Sphere& sphere)
- Sphere(const Vector3& center, float radius) (GC)
- Sphere* new(const Vector3& center, float radius)
- Sphere(const BoundingBox& box) (GC)
- Sphere* new(const BoundingBox& box)
- Sphere(const Frustum& frustum) (GC)
- Sphere* new(const Frustum& frustum)
- Sphere(const Polyhedron& poly) (GC)
- Sphere* new(const Polyhedron& poly)
- void delete()
- bool operator==(const Sphere& rhs) const
- void Define(const Sphere& sphere)
- void Define(const Vector3& center, float radius)
- void Define(const BoundingBox& box)
- void Define(const Frustum& frustum)
- void Define(const Polyhedron& poly)
- void Merge(const Vector3& point)
- void Merge(const BoundingBox& box)
- void Merge(const Frustum& frustum)
- void Merge(const Polyhedron& poly)
- void Merge(const Sphere& sphere)
- void Clear()
- bool Defined() const
- Intersection IsInside(const Vector3& point) const
- Intersection IsInside(const Sphere& sphere) const
- Intersection IsInsideFast(const Sphere& sphere) const
- Intersection IsInside(const BoundingBox& box) const
- Intersection IsInsideFast(const BoundingBox& box) const
- float Distance(const Vector3& point) const
- Vector3 GetLocalPoint(float theta, float phi) const
- Vector3 GetPoint(float theta, float phi) const

### Properties


- Vector3 center
- float radius



---

## Plane



### Methods


- Plane() (GC)
- Plane* new()
- Plane(const Plane& plane) (GC)
- Plane* new(const Plane& plane)
- Plane(const Vector3& v0, const Vector3& v1, const Vector3& v2) (GC)
- Plane* new(const Vector3& v0, const Vector3& v1, const Vector3& v2)
- Plane(const Vector3& normal, const Vector3& point) (GC)
- Plane* new(const Vector3& normal, const Vector3& point)
- Plane(const Vector4& plane) (GC)
- Plane* new(const Vector4& plane)
- void delete()
- void Define(const Vector3& v0, const Vector3& v1, const Vector3& v2)
- void Define(const Vector3& normal, const Vector3& point)
- void Define(const Vector4& plane)
- void Transform(const Matrix3& transform)
- void Transform(const Matrix3x4& transform)
- void Transform(const Matrix4& transform)
- Vector3 Project(const Vector3& point) const
- float Distance(const Vector3& point) const
- Vector3 Reflect(const Vector3& direction) const
- Matrix3x4 ReflectionMatrix() const
- Plane Transformed(const Matrix3& transform) const
- Plane Transformed(const Matrix3x4& transform) const
- Plane Transformed(const Matrix4& transform) const
- Vector4 ToVector4() const

### Properties


- Vector3 normal
- Vector3 absNormal
- float d
- const Plane UP



---

## Ray



### Methods


- Ray() (GC)
- Ray* new()
- Ray(const Vector3& origin, const Vector3& direction) (GC)
- Ray* new(const Vector3& origin, const Vector3& direction)
- Ray(const Ray& ray) (GC)
- Ray* new(const Ray& ray)
- void delete()
- bool operator==(const Ray& rhs) const
- void Define(const Vector3& origin, const Vector3& direction)
- Vector3 Project(const Vector3& point) const
- float Distance(const Vector3& point) const
- Vector3 ClosestPoint(const Ray& ray) const
- float HitDistance(const Plane& plane) const
- float HitDistance(const BoundingBox& box) const
- float HitDistance(const Frustum& frustum, bool solidInside = true) const
- float HitDistance(const Sphere& sphere) const
- float HitDistance(const Vector3& v0, const Vector3& v1, const Vector3& v2) const
- Ray Transformed(const Matrix3x4& transform) const

### Properties


- Vector3 origin
- Vector3 direction



---

## Frustum



### Methods


- Frustum() (GC)
- Frustum* new()
- Frustum(const Frustum& frustum) (GC)
- Frustum* new(const Frustum& frustum)
- void delete()
- void Define(float fov, float aspectRatio, float zoom, float nearZ, float farZ)
- void Define(float fov, float aspectRatio, float zoom, float nearZ, float farZ, const Matrix3x4& transform)
- void Define(const Vector3& near, const Vector3& far)
- void Define(const Vector3& near, const Vector3& far, const Matrix3x4& transform)
- void Define(const BoundingBox& box)
- void Define(const BoundingBox& box, const Matrix3x4& transform)
- void Define(const Matrix4& projection)
- void DefineOrtho(float orthoSize, float aspectRatio, float zoom, float nearZ, float farZ)
- void DefineOrtho(float orthoSize, float aspectRatio, float zoom, float nearZ, float farZ, const Matrix3x4& transform)
- void DefineSplit(const Matrix4& projection, float near, float far)
- void Transform(const Matrix3& transform)
- void Transform(const Matrix3x4& transform)
- Intersection IsInside(const Vector3& point) const
- Intersection IsInside(const Sphere& sphere) const
- Intersection IsInsideFast(const Sphere& sphere) const
- Intersection IsInside(const BoundingBox& box) const
- Intersection IsInsideFast(const BoundingBox& box) const
- float Distance(const Vector3& point) const
- Frustum Transformed(const Matrix3& transform) const
- Frustum Transformed(const Matrix3x4& transform) const
- Rect Projected(const Matrix4& transform) const
- void UpdatePlanes()



---

## Polyhedron



### Methods


- Polyhedron() (GC)
- Polyhedron* new()
- Polyhedron(const Polyhedron& polyhedron) (GC)
- Polyhedron* new(const Polyhedron& polyhedron)
- Polyhedron(const BoundingBox& box) (GC)
- Polyhedron* new(const BoundingBox& box)
- Polyhedron(const Frustum& frustum) (GC)
- Polyhedron* new(const Frustum& frustum)
- void delete()
- void Define(const BoundingBox& box)
- void Define(const Frustum& frustum)
- void AddFace(const Vector3& v0, const Vector3& v1, const Vector3& v2)
- void AddFace(const Vector3& v0, const Vector3& v1, const Vector3& v2, const Vector3& v3)
- void Clip(const Plane& plane)
- void Clip(const BoundingBox& box)
- void Clip(const Frustum& box)
- void Clear()
- void Transform(const Matrix3& transform)
- void Transform(const Matrix3x4& transform)
- Polyhedron Transformed(const Matrix3& transform) const
- Polyhedron Transformed(const Matrix3x4& transform) const
- bool Empty() const

### Properties


- bool empty (readonly)



---

## Spline



### Methods


- Spline() (GC)
- Spline* new()
- Spline(InterpolationMode mode) (GC)
- Spline* new(InterpolationMode mode)
- Spline(const Spline& rhs) (GC)
- Spline* new(const Spline& rhs)
- void delete()
- bool operator==(const Spline& rhs) const
- Variant GetPoint(float f) const
- Variant GetKnot(unsigned index) const
- void SetKnot(const Variant& knot, unsigned tolua_var_1)
- void AddKnot(const Variant& knot)
- void AddKnot(const Variant& knot, unsigned index)
- void RemoveKnot()
- void RemoveKnot(unsigned index)
- void Clear()

### Properties


- InterpolationMode interpolationMode



---

**Inherits from**: Component

## SplinePath : Component


### Methods


- void AddControlPoint(Node* point, unsigned index = M_MAX_UNSIGNED)
- void RemoveControlPoint(Node* point)
- void ClearControlPoints()
- void SetInterpolationMode(InterpolationMode mode)
- void SetPosition(float factor)
- void SetControlledNode(Node* controlled)
- InterpolationMode GetInterpolationMode() const
- float GetSpeed() const
- float GetLength() const
- Vector3 GetPosition() const
- Node* GetControlledNode() const
- Vector3 GetPoint(float factor) const
- void Move(float timeStep)
- void Reset()
- bool IsFinished() const

### Properties


- InterpolationMode interpolationMode
- float speed
- float length (readonly)
- Node* controlledNode



---

