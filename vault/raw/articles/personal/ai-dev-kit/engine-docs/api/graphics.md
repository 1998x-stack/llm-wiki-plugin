# Graphics Module

UrhoX Lua API - Graphics Module

---

## Classes

- [Graphics](#graphics)
- [Renderer](#renderer)
- [Camera](#camera)
- [Light](#light)
- [StaticModel](#staticmodel)
- [AnimatedModel](#animatedmodel)
- [Skybox](#skybox)
- [StaticModelGroup](#staticmodelgroup)
- [Material](#material)
- [Texture](#texture)
- [Texture2D](#texture2d)
- [Texture3D](#texture3d)
- [TextureCube](#texturecube)
- [Texture2DArray](#texture2darray)
- [Model](#model)
- [Geometry](#geometry)
- [VertexBuffer](#vertexbuffer)
- [IndexBuffer](#indexbuffer)
- [Drawable](#drawable)
- [Octree](#octree)
- [Viewport](#viewport)
- [RenderPath](#renderpath)
- [RenderSurface](#rendersurface)
- [Technique](#technique)
- [Pass](#pass)
- [BillboardSet](#billboardset)
- [Billboard](#billboard)
- [CustomGeometry](#customgeometry)
- [DecalSet](#decalset)
- [RibbonTrail](#ribbontrail)
- [TerrainPatch](#terrainpatch)
- [Terrain](#terrain)

---

**Inherits from**: Object

## Graphics : Object


### Methods


- void SetWindowTitle(const String windowTitle)
- void SetWindowIcon(Image* windowIcon)
- void SetWindowPosition(const IntVector2& position)
- void SetWindowPosition(int x, int y)
- bool SetMode(int width, int height, bool fullscreen, bool borderless, bool resizable, bool highDPI, bool vsync, bool tripleBuffer, int multiSample, int monitor, int refreshRate)
- bool SetMode(int width, int height)
- void SetSRGB(bool enable)
- void SetDither(bool enable)
- void SetFlushGPU(bool enable)
- void SetOrientations(const String orientations)
- bool ToggleFullscreen()
- void Maximize()
- void Minimize()
- void Raise()
- void Close()
- bool TakeScreenShot(Image& destImage)
- void BeginDumpShaders(const String fileName)
- void EndDumpShaders()
- void PrecacheShaders(Deserializer& source)
- void PrecacheShaders(const String fileName)
- void SetShaderCacheDir(const String path)
- bool IsInitialized() const
- void* GetExternalWindow() const
- const String GetWindowTitle() const
- const String GetApiName() const
- IntVector2 GetWindowPosition() const
- int GetWidth() const
- int GetHeight() const
- int GetMultiSample() const
- IntVector2 GetSize() const
- bool GetFullscreen() const
- bool GetResizable() const
- bool GetBorderless() const
- bool GetVSync() const
- int GetMonitor() const
- int GetRefreshRate() const
- bool GetTripleBuffer() const
- bool GetSRGB() const
- bool GetDither() const
- bool GetFlushGPU() const
- const String GetOrientations() const
- bool IsDeviceLost() const
- unsigned GetNumPrimitives() const
- unsigned GetNumBatches() const
- unsigned GetDummyColorFormat() const
- unsigned GetShadowMapFormat() const
- unsigned GetHiresShadowMapFormat() const
- bool GetInstancingSupport() const
- bool GetLightPrepassSupport() const
- bool GetDeferredSupport() const
- bool GetHardwareShadowSupport() const
- bool GetReadableDepthSupport() const
- bool GetSRGBSupport() const
- bool GetSRGBWriteSupport() const
- IntVector2 GetDesktopResolution(int monitor) const
- int GetMonitorCount() const
- const String GetShaderCacheDir() const
- int GetCurrentMonitor() const
- bool GetMaximized() const
- void Raise() const
- Vector3 GetDisplayDPI(int monitor = 0) const
- unsigned GetAlphaFormat()
- unsigned GetLuminanceFormat()
- unsigned GetLuminanceAlphaFormat()
- unsigned GetRGBFormat()
- unsigned GetRGBAFormat()
- unsigned GetRGBA16Format()
- unsigned GetRGBAFloat16Format()
- unsigned GetRGBAFloat32Format()
- unsigned GetRG16Format()
- unsigned GetRGFloat16Format()
- unsigned GetRGFloat32Format()
- unsigned GetFloat16Format()
- unsigned GetFloat32Format()
- unsigned GetLinearDepthFormat()
- unsigned GetDepthStencilFormat()
- unsigned GetReadableDepthFormat()
- unsigned GetFormat(const String formatName)
- unsigned GetMaxBones()

### Properties


- bool initialized (readonly)
- String windowTitle
- String apiName (readonly)
- IntVector2 windowPosition
- int width (readonly)
- int height (readonly)
- int multiSample (readonly)
- IntVector2 size (readonly)
- bool fullscreen (readonly)
- bool resizable (readonly)
- bool borderless (readonly)
- bool vSync (readonly)
- int refreshRate (readonly)
- int monitor (readonly)
- bool tripleBuffer (readonly)
- bool sRGB
- bool dither
- bool flushGPU
- String orientations
- bool deviceLost (readonly)
- unsigned numPrimitives (readonly)
- unsigned numBatches (readonly)
- unsigned dummyColorFormat (readonly)
- unsigned shadowMapFormat (readonly)
- unsigned hiresShadowMapFormat (readonly)
- bool instancingSupport (readonly)
- bool lightPrepassSupport (readonly)
- bool deferredSupport (readonly)
- bool hardwareShadowSupport (readonly)
- bool readableDepthSupport (readonly)
- bool sRGBSupport (readonly)
- bool sRGBWriteSupport (readonly)
- int monitorCount (readonly)
- String shaderCacheDir



---

## Renderer



### Methods


- void SetNumViewports(unsigned num)
- void SetViewport(unsigned index, Viewport* viewport)
- void SetDefaultRenderPath(RenderPath* renderPath)
- void SetDefaultRenderPath(XMLFile* file)
- void SetDefaultTechnique(Technique* technique)
- void SetHDRRendering(bool enable)
- void SetSpecularLighting(bool enable)
- void SetTextureAnisotropy(int level)
- void SetTextureFilterMode(TextureFilterMode mode)
- void SetTextureQuality(MaterialQuality quality)
- void SetMaterialQuality(MaterialQuality quality)
- void SetDrawShadows(bool enable)
- void SetShadowMapSize(int size)
- void SetShadowQuality(ShadowQuality quality)
- void SetShadowSoftness(float shadowSoftness)
- void SetVSMShadowParameters(float minVariance, float lightBleedingReduction)
- void SetVSMMultiSample(int multiSample)
- void SetReuseShadowMaps(bool enable)
- void SetMaxShadowMaps(int shadowMaps)
- void SetDynamicInstancing(bool enable)
- void SetNumExtraInstancingBufferElements(int elements)
- void SetMinInstances(int instances)
- void SetMaxSortedInstances(int instances)
- void SetMaxOccluderTriangles(int triangles)
- void SetOcclusionBufferSize(int size)
- void SetOccluderSizeThreshold(float screenSize)
- void SetThreadedOcclusion(bool enable)
- void SetMobileShadowBiasMul(float mul)
- void SetMobileShadowBiasAdd(float add)
- void SetMobileNormalOffsetMul(float mul)
- void ReloadShaders()
- unsigned GetNumViewports() const
- Viewport* GetViewport(unsigned index) const
- Viewport* GetViewportForScene(Scene* scene, unsigned index) const
- RenderPath* GetDefaultRenderPath() const
- Technique* GetDefaultTechnique() const
- bool GetHDRRendering() const
- bool GetSpecularLighting() const
- bool GetDrawShadows() const
- int GetTextureAnisotropy() const
- TextureFilterMode GetTextureFilterMode() const
- MaterialQuality GetTextureQuality() const
- MaterialQuality GetMaterialQuality() const
- int GetShadowMapSize() const
- ShadowQuality GetShadowQuality() const
- float GetShadowSoftness() const
- Vector2 GetVSMShadowParameters() const
- int GetVSMMultiSample() const
- bool GetReuseShadowMaps() const
- int GetMaxShadowMaps() const
- bool GetDynamicInstancing() const
- int GetNumExtraInstancingBufferElements() const
- int GetMinInstances() const
- int GetMaxSortedInstances() const
- int GetMaxOccluderTriangles() const
- int GetOcclusionBufferSize() const
- float GetOccluderSizeThreshold() const
- bool GetThreadedOcclusion() const
- float GetMobileShadowBiasMul() const
- float GetMobileShadowBiasAdd() const
- float GetMobileNormalOffsetMul() const
- unsigned GetNumViews() const
- unsigned GetNumPrimitives() const
- unsigned GetNumBatches() const
- unsigned GetNumGeometries(bool allViews = false) const
- unsigned GetNumLights(bool allViews = false) const
- unsigned GetNumShadowMaps(bool allViews = false) const
- unsigned GetNumOccluders(bool allViews = false) const
- Zone* GetDefaultZone() const
- Material* GetDefaultMaterial() const
- Texture2D* GetDefaultLightRamp() const
- Texture2D* GetDefaultLightSpot() const
- void DrawDebugGeometry(bool depthTest)

### Properties


- unsigned numViewports
- RenderPath* defaultRenderPath
- Technique* defaultTechnique
- bool HDRRendering
- bool specularLighting
- bool drawShadows
- int textureAnisotropy
- TextureFilterMode textureFilterMode
- MaterialQuality textureQuality
- MaterialQuality materialQuality
- int shadowMapSize
- ShadowQuality shadowQuality
- float shadowSoftness
- int VSMMultiSample
- bool reuseShadowMaps
- int maxShadowMaps
- bool dynamicInstancing
- int numExtraInstancingBufferElements
- int minInstances
- int maxSortedInstances
- int maxOccluderTriangles
- int occlusionBufferSize
- float occluderSizeThreshold
- bool threadedOcclusion
- float mobileShadowBiasMul
- float mobileShadowBiasAdd
- float mobileNormalOffsetMul
- unsigned numViews (readonly)
- unsigned numPrimitives (readonly)
- unsigned numBatches (readonly)
- Zone* defaultZone (readonly)
- Material* defaultMaterial (readonly)
- Texture2D* defaultLightRamp (readonly)
- Texture2D* defaultLightSpot (readonly)



---

**Inherits from**: Component

## Camera : Component


### Methods


- void SetNearClip(float nearClip)
- void SetFarClip(float farClip)
- void SetFov(float fov)
- void SetOrthoSize(float orthoSize)
- void SetOrthoSize(const Vector2& orthoSize)
- void SetAspectRatio(float aspectRatio)
- void SetFillMode(FillMode mode)
- void SetZoom(float zoom)
- void SetLodBias(float bias)
- void SetViewMask(unsigned mask)
- void SetViewOverrideFlags(ViewOverride flags)
- void SetOrthographic(bool enable)
- void SetAutoAspectRatio(bool enable)
- void SetProjectionOffset(const Vector2& offset)
- void SetUseReflection(bool enable)
- void SetReflectionPlane(const Plane& reflectionPlane)
- void SetUseClipping(bool enable)
- void SetClipPlane(const Plane& clipPlane)
- void SetProjection(const Matrix4& projection)
- float GetFarClip() const
- float GetNearClip() const
- float GetFov() const
- float GetOrthoSize() const
- float GetAspectRatio() const
- float GetZoom() const
- float GetLodBias() const
- unsigned GetViewMask() const
- ViewOverride GetViewOverrideFlags() const
- FillMode GetFillMode() const
- bool IsOrthographic() const
- bool GetAutoAspectRatio() const
- const Frustum& GetFrustum() const
- Matrix4 GetProjection() const
- Matrix4 GetGPUProjection() const
- const Matrix3x4& GetView() const
- void GetFrustumSize(Vector3& near, Vector3& far) const
- float GetHalfViewSize() const
- Frustum GetSplitFrustum(float nearClip, float farClip) const
- Frustum GetViewSpaceFrustum() const
- Frustum GetViewSpaceSplitFrustum(float nearClip, float farClip) const
- Ray GetScreenRay(float x, float y) const
- Vector2 WorldToScreenPoint(const Vector3& worldPos) const
- Vector3 ScreenToWorldPoint(const Vector3& screenPos) const
- const Vector2& GetProjectionOffset() const
- bool GetUseReflection() const
- const Plane& GetReflectionPlane() const
- bool GetUseClipping() const
- const Plane& GetClipPlane() const
- float GetDistance(const Vector3& worldPos) const
- float GetDistanceSquared(const Vector3& worldPos) const
- float GetLodDistance(float distance, float scale, float bias) const
- bool IsProjectionValid() const
- Matrix3x4 GetEffectiveWorldTransform() const

### Properties


- float farClip
- float nearClip
- float fov
- float orthoSize
- float aspectRatio
- float zoom
- float lodBias
- unsigned viewMask
- ViewOverride viewOverrideFlags
- FillMode fillMode
- bool orthographic
- bool autoAspectRatio
- Frustum& frustum (readonly)
- Matrix4 projection (readonly)
- Matrix4 GPUProjection (readonly)
- Matrix3x4& view (readonly)
- float halfViewSize (readonly)
- Frustum viewSpaceFrustum (readonly)
- Vector2& projectionOffset
- bool useReflection
- Plane& reflectionPlane
- bool useClipping
- Plane& clipPlane
- bool projectionValid (readonly)
- Matrix3x4 effectiveWorldTransform (readonly)

### ⚠️ 重要提示

#### orthoSize 参数说明

`orthoSize` 代表正交投影的**视野全高度**（单位：世界坐标），但引擎内部使用 `orthoSize * 0.5` 作为**半高度**参与矩阵计算。

```lua
-- orthoSize = 10.0 时：
-- 视野高度 = 10.0 世界单位
-- 视野半高度 = 5.0（内部计算使用）
-- 视野宽度 = 10.0 * aspectRatio
```

**手动计算屏幕坐标到世界坐标时必须注意**：
```lua
-- ✅ 正确：使用 orthoSize * 0.5
local viewX = ndcX * aspect * orthoSize * 0.5
local viewY = ndcY * orthoSize * 0.5

-- ❌ 错误：直接使用 orthoSize（会导致 2x 误差）
local viewX = ndcX * aspect * orthoSize
local viewY = ndcY * orthoSize
```

详见：[gotchas/camera.md](../gotchas/camera.md)

#### GetScreenRay 不使用缓存

`GetScreenRay(x, y)` 每次调用都会基于当前相机状态实时计算，无需担心缓存问题。修改 `orthoSize` 后立即调用即可获得正确结果。

---

**Inherits from**: Drawable

## Light : Drawable


### Methods


- void SetLightType(LightType type)
- void SetPerVertex(bool enable)
- void SetColor(const Color& color)
- void SetTemperature(float temperature)
- void SetRadius(float redius)
- void SetLength(float length)
- void SetUsePhysicalValues(bool enable)
- void SetSpecularIntensity(float intensity)
- void SetBrightness(float brightness)
- void SetRange(float range)
- void SetFov(float fov)
- void SetAspectRatio(float aspectRatio)
- void SetFadeDistance(float distance)
- void SetShadowFadeDistance(float distance)
- void SetShadowBias(const BiasParameters& parameters)
- void SetShadowCascade(const CascadeParameters& parameters)
- void SetShadowFocus(const FocusParameters& parameters)
- void SetShadowIntensity(float intensity)
- void SetShadowResolution(float resolution)
- void SetShadowNearFarRatio(float nearFarRatio)
- void SetShadowMaxExtrusion(float extrusion)
- void SetRampTexture(Texture* texture)
- void SetShapeTexture(Texture* texture)
- LightType GetLightType() const
- bool GetPerVertex() const
- const Color& GetColor() const
- float GetTemperature() const
- float GetRadius() const
- float GetLength() const
- float GetSpecularIntensity() const
- float GetBrightness() const
- Color GetEffectiveColor() const
- Color GetColorFromTemperature() const
- bool GetUsePhysicalValues() const
- float GetEffectiveSpecularIntensity() const
- float GetRange() const
- float GetFov() const
- float GetAspectRatio() const
- float GetFadeDistance() const
- float GetShadowFadeDistance() const
- const BiasParameters& GetShadowBias() const
- const CascadeParameters& GetShadowCascade() const
- const FocusParameters& GetShadowFocus() const
- float GetShadowIntensity() const
- float GetShadowResolution() const
- float GetShadowNearFarRatio() const
- float GetShadowMaxExtrusion() const
- Texture* GetRampTexture() const
- Texture* GetShapeTexture() const
- Frustum GetFrustum() const
- int GetNumShadowSplits() const
- bool IsNegative() const

### Properties


- LightType lightType
- bool perVertex
- Color& color
- float temperature
- float radius
- float length
- bool usePhysicalValues
- float specularIntensity
- float brightness
- float range
- float fov
- float aspectRatio
- float fadeDistance
- float shadowFadeDistance
- BiasParameters& shadowBias
- CascadeParameters& shadowCascade
- FocusParameters& shadowFocus
- float shadowIntensity
- float shadowResolution
- float shadowNearFarRatio
- float shadowMaxExtrusion
- Texture* rampTexture
- Texture* shapeTexture
- Frustum frustum (readonly)
- int numShadowSplits (readonly)
- bool negative (readonly)
- Color effectiveColor (readonly)
- float effectiveSpecularIntensity (readonly)



---

**Inherits from**: Drawable

## StaticModel : Drawable


### Methods


- void SetModel(Model* model)
- void SetMaterial(Material* material)
- bool SetMaterial(unsigned index, Material* material)
- void SetOcclusionLodLevel(unsigned level)
- void ApplyMaterialList(const String fileName = String::EMPTY)
- Model* GetModel() const
- unsigned GetNumGeometries() const
- Material* GetMaterial() const
- Material* GetMaterial(unsigned index) const
- unsigned GetOcclusionLodLevel() const
- bool IsInside(const Vector3& point) const
- bool IsInsideLocal(const Vector3& point) const

### Properties


- Model* model
- Material* material
- BoundingBox& boundingBox (readonly)
- unsigned numGeometries (readonly)
- unsigned occlusionLodLevel



---

**Inherits from**: StaticModel

## AnimatedModel : StaticModel


### Methods


- void SetModel(Model* model)
- AnimationState* AddAnimationState(Animation* animation)
- void RemoveAnimationState(Animation* animation)
- void RemoveAnimationState(const String animationName)
- void RemoveAnimationState(StringHash animationNameHash)
- void RemoveAnimationState(AnimationState* state)
- void RemoveAnimationState(unsigned index)
- void RemoveAllAnimationStates()
- void SetAnimationLodBias(float bias)
- void SetUpdateInvisible(bool enable)
- void SetMorphWeight(const String name, float weight)
- void SetMorphWeight(StringHash nameHash, float weight)
- void SetMorphWeight(unsigned index, float weight)
- void ResetMorphWeights()
- Skeleton& GetSkeleton()
- unsigned GetNumAnimationStates() const
- AnimationState* GetAnimationState(Animation* animation) const
- AnimationState* GetAnimationState(const String animationName) const
- AnimationState* GetAnimationState(StringHash animationNameHash) const
- AnimationState* GetAnimationState(unsigned index) const
- float GetAnimationLodBias() const
- bool GetUpdateInvisible() const
- unsigned GetNumMorphs() const
- float GetMorphWeight(const String name) const
- float GetMorphWeight(StringHash nameHash) const
- float GetMorphWeight(unsigned index) const
- bool IsMaster() const
- void UpdateBoneBoundingBox()

### Properties


- Model* model
- Skeleton& skeleton (readonly)
- unsigned numAnimationStates (readonly)
- float animationLodBias
- bool updateInvisible
- unsigned numMorphs (readonly)
- bool master (readonly)



---

**Inherits from**: StaticModel

## Skybox : StaticModel




---

**Inherits from**: StaticModel

## StaticModelGroup : StaticModel


### Methods


- void AddInstanceNode(Node* node)
- void RemoveInstanceNode(Node* node)
- void RemoveAllInstanceNodes()
- unsigned GetNumInstanceNodes() const
- Node* GetInstanceNode(unsigned index) const

### Properties


- unsigned numInstanceNodes (readonly)



---

**Inherits from**: Resource

## Material : Resource


### Methods


- Material() (GC)
- Material* new()
- void delete()
- void SetNumTechniques(unsigned num)
- void SetTechnique(unsigned index, Technique* tech, MaterialQuality qualityLevel = 0, float lodDistance = 0.0f)
- void SetVertexShaderDefines(const String defines)
- void SetPixelShaderDefines(const String defines)
- void SetShaderParameter(const String name, const Variant& value)
- void SetShaderParameterAnimation(const String name, ValueAnimation* animation, WrapMode wrapMode = WM_LOOP, float speed = 1.0f)
- void SetShaderParameterAnimationWrapMode(const String name, WrapMode wrapMode)
- void SetShaderParameterAnimationSpeed(const String name, float speed)
- void SetTexture(TextureUnit unit, Texture* texture)
- void SetUVTransform(const Vector2& offset, float rotation, const Vector2& repeat)
- void SetUVTransform(const Vector2& offset, float rotation, float repeat)
- void SetCullMode(CullMode mode)
- void SetShadowCullMode(CullMode mode)
- void SetFillMode(FillMode mode)
- void SetDepthBias(const BiasParameters& parameters)
- void SetAlphaToCoverage(bool enable)
- void SetLineAntiAlias(bool enable)
- void SetRenderOrder(char renderOrder)
- void SetOcclusion(bool enable)
- void SetScene(Scene* scene)
- void RemoveShaderParameter(const String name)
- void ReleaseShaders()
- Material* Clone(const String cloneName = String::EMPTY) const
- void SortTechniques()
- void MarkForAuxView(unsigned frameNumber)
- unsigned GetNumTechniques() const
- Technique* GetTechnique(unsigned index) const
- Pass* GetPass(unsigned index, const String passName) const
- Texture* GetTexture(TextureUnit unit) const
- const String GetVertexShaderDefines() const
- const String GetPixelShaderDefines() const
- ValueAnimation* GetShaderParameterAnimation(const String name) const
- WrapMode GetShaderParameterAnimationWrapMode(const String name) const
- float GetShaderParameterAnimationSpeed(const String name) const
- CullMode GetCullMode() const
- CullMode GetShadowCullMode() const
- FillMode GetFillMode() const
- const BiasParameters& GetDepthBias() const
- bool GetAlphaToCoverage() const
- bool GetLineAntiAlias() const
- char GetRenderOrder() const
- bool GetOcclusion() const
- bool GetSpecular() const
- Scene* GetScene() const

### Properties


- String vertexShaderDefines
- String pixelShaderDefines
- CullMode cullMode
- CullMode shadowCullMode
- FillMode fillMode
- BiasParameters depthBias
- bool alphaToCoverage
- bool lineAntiAlias
- char renderOrder
- bool occlusion
- bool specular (readonly)
- Scene* scene



---

**Inherits from**: ResourceWithMetadata

## Texture : ResourceWithMetadata


### Methods


- void SetNumLevels(unsigned levels)
- void SetFilterMode(TextureFilterMode filter)
- void SetAddressMode(TextureCoordinate coord, TextureAddressMode address)
- void SetAnisotropy(unsigned level)
- void SetBorderColor(const Color& color)
- void SetSRGB(bool enable)
- void SetBackupTexture(Texture* texture)
- void SetMipsToSkip(MaterialQuality quality, int toSkip)
- unsigned GetFormat() const
- bool IsCompressed() const
- unsigned GetLevels() const
- int GetWidth() const
- int GetHeight() const
- TextureFilterMode GetFilterMode() const
- TextureAddressMode GetAddressMode(TextureCoordinate coord) const
- unsigned GetAnisotropy() const
- const Color& GetBorderColor() const
- bool GetSRGB() const
- int GetMultiSample() const
- bool GetAutoResolve() const
- bool IsResolveDirty() const
- bool GetLevelsDirty() const
- Texture* GetBackupTexture() const
- int GetMipsToSkip(MaterialQuality quality) const
- int GetLevelWidth(unsigned level) const
- int GetLevelHeight(unsigned level) const
- TextureUsage GetUsage() const
- unsigned GetDataSize(int width, int height) const
- unsigned GetRowDataSize(int width) const
- unsigned GetComponents() const

### Properties


- unsigned format (readonly)
- bool compressed (readonly)
- unsigned levels (readonly)
- int width (readonly)
- int height (readonly)
- unsigned components (readonly)
- TextureFilterMode filterMode
- unsigned anisotropy
- Color& borderColor
- bool sRGB
- int multiSample (readonly)
- bool autoResolve (readonly)
- bool resolveDirty (readonly)
- bool levelsDirty (readonly)
- Texture* backupTexture
- TextureUsage usage (readonly)



---

**Inherits from**: Texture

## Texture2D : Texture


### Methods


- Texture2D() (GC)
- Texture2D* new()
- void delete()
- bool SetSize(int width, int height, unsigned format, TextureUsage usage = TEXTURE_STATIC, int multiSample = 1, bool autoResolve = true)
- bool SetData(Image* image, bool useAlpha = false)
- Image* GetImage() const
- RenderSurface* GetRenderSurface() const

### Properties


- RenderSurface* renderSurface (readonly)



---

**Inherits from**: Texture

## Texture3D : Texture


### Methods


- Texture3D() (GC)
- Texture3D* new()
- void delete()
- bool SetSize(int width, int height, int depth, unsigned format, TextureUsage usage = TEXTURE_STATIC)
- bool SetData(Image* image, bool useAlpha = false)



---

**Inherits from**: Texture

## TextureCube : Texture


### Methods


- TextureCube() (GC)
- TextureCube* new()
- void delete()
- bool SetSize(int size, unsigned format, TextureUsage usage = TEXTURE_STATIC, int multiSample = 1)
- bool SetData(CubeMapFace face, Image* image, bool useAlpha = false)
- Image* GetImage(CubeMapFace face) const
- RenderSurface* GetRenderSurface(CubeMapFace face) const



---

**Inherits from**: Texture

## Texture2DArray : Texture


### Methods


- Texture2DArray() (GC)
- Texture2DArray* new()
- void delete()
- void SetLayers(unsigned layers)
- bool SetSize(unsigned layers, int width, int height, unsigned format, TextureUsage usage = TEXTURE_STATIC)
- bool SetData(unsigned layer, Image* image, bool useAlpha = false)
- unsigned GetLayers() const
- RenderSurface* GetRenderSurface() const

### Properties


- unsigned layers
- RenderSurface* renderSurface (readonly)



---

**Inherits from**: ResourceWithMetadata

## Model : ResourceWithMetadata


### Methods


- Model() (GC)
- Model* new()
- void delete()
- Model* Clone(const String cloneName = String::EMPTY) const
- void SetBoundingBox(const BoundingBox& box)
- bool SetVertexBuffers(const Vector<SharedPtr<VertexBuffer> >& buffers, const PODVector<unsigned>& morphRangeStarts, const PODVector<unsigned>& morphRangeCounts)
- bool SetIndexBuffers(const Vector<SharedPtr<IndexBuffer> >& buffers)
- void SetNumGeometries(unsigned num)
- bool SetNumGeometryLodLevels(unsigned index, unsigned num)
- bool SetGeometry(unsigned index, unsigned lodLevel, Geometry* geometry)
- bool SetGeometryCenter(unsigned index, const Vector3& center)
- const BoundingBox& GetBoundingBox() const
- Skeleton& GetSkeleton()
- unsigned GetNumGeometries() const
- unsigned GetNumGeometryLodLevels(unsigned index) const
- Geometry* GetGeometry(unsigned index, unsigned lodLevel) const
- const Vector3& GetGeometryCenter(unsigned index) const
- unsigned GetNumMorphs() const
- const ModelMorph* GetMorph(const String name) const
- const ModelMorph* GetMorph(StringHash nameHash) const
- const ModelMorph* GetMorph(unsigned index) const
- unsigned GetMorphRangeStart(unsigned bufferIndex) const
- unsigned GetMorphRangeCount(unsigned bufferIndex) const

### Properties


- BoundingBox& boundingBox
- Skeleton skeleton (readonly)
- unsigned numGeometries
- unsigned numMorphs (readonly)



---

**Inherits from**: Object

## Geometry : Object


### Methods


- Geometry() (GC)
- Geometry* new()
- void delete()
- bool SetNumVertexBuffers(unsigned num)
- bool SetVertexBuffer(unsigned index, VertexBuffer* buffer)
- void SetIndexBuffer(IndexBuffer* buffer)
- bool SetDrawRange(PrimitiveType type, unsigned indexStart, unsigned indexCount, bool getUsedVertexRange = true)
- bool SetDrawRange(PrimitiveType type, unsigned indexStart, unsigned indexCount, unsigned vertexStart, unsigned vertexCount, bool checkIllegal = true)
- void SetLodDistance(float distance)
- unsigned GetNumVertexBuffers() const
- VertexBuffer* GetVertexBuffer(unsigned index) const
- IndexBuffer* GetIndexBuffer() const
- PrimitiveType GetPrimitiveType() const
- unsigned GetIndexStart() const
- unsigned GetIndexCount() const
- unsigned GetVertexStart() const
- unsigned GetVertexCount() const
- float GetLodDistance()
- bool IsEmpty() const

### Properties


- unsigned numVertexBuffers
- IndexBuffer* indexBuffer
- PrimitiveType primitiveType (readonly)
- unsigned indexStart (readonly)
- unsigned indexCount (readonly)
- unsigned vertexStart (readonly)
- unsigned vertexCount (readonly)
- float lodDistance
- bool empty (readonly)



---

**Inherits from**: Object

## VertexBuffer : Object


### Methods


- VertexBuffer() (GC)
- VertexBuffer* new()
- void delete()
- void SetShadowed(bool enable)
- bool SetSize(unsigned vertexCount, const PODVector<VertexElement>& elements, bool dynamic = false)
- bool SetSize(unsigned vertexCount, unsigned elementMask, bool dynamic = false)
- bool SetData(VectorBuffer& data)
- bool SetDataRange(VectorBuffer& data, unsigned start, unsigned count, bool discard = false)
- VectorBuffer GetData()
- bool IsShadowed() const
- bool IsDynamic() const
- unsigned GetVertexCount() const
- unsigned GetVertexSize() const
- const PODVector<VertexElement>& GetElements() const
- bool HasElement(VertexElementSemantic semantic, char index = 0) const
- bool HasElement(VertexElementType type, VertexElementSemantic semantic, char index = 0) const
- unsigned GetElementOffset(VertexElementSemantic semantic, char index = 0) const
- unsigned GetElementOffset(VertexElementType type, VertexElementSemantic semantic, char index = 0) const
- unsigned GetElementMask() const

### Properties


- bool shadowed
- bool dynamic (readonly)
- unsigned vertexCount (readonly)
- unsigned vertexSize (readonly)
- unsigned elementMask (readonly)



---

**Inherits from**: Object

## IndexBuffer : Object


### Methods


- IndexBuffer() (GC)
- IndexBuffer* new()
- void delete()
- void SetShadowed(bool enable)
- bool SetSize(unsigned indexCount, bool largeIndices, bool dynamic = false)
- bool SetData(VectorBuffer& data)
- bool SetDataRange(VectorBuffer& data, unsigned start, unsigned count, bool discard = false)
- VectorBuffer GetData()
- bool IsShadowed() const
- bool IsDynamic() const
- unsigned GetIndexCount() const
- unsigned GetIndexSize() const

### Properties


- bool shadowed
- bool dynamic (readonly)
- unsigned indexCount (readonly)
- unsigned indexSize (readonly)



---

**Inherits from**: Component

## Drawable : Component


### Methods


- void SetDrawDistance(float distance)
- void SetShadowDistance(float distance)
- void SetLodBias(float bias)
- void SetViewMask(unsigned mask)
- void SetLightMask(unsigned mask)
- void SetShadowMask(unsigned mask)
- void SetZoneMask(unsigned mask)
- void SetMaxLights(unsigned num)
- void SetCastShadows(bool enable)
- void SetOccluder(bool enable)
- void SetOccludee(bool enable)
- void MarkForUpdate()
- const BoundingBox& GetBoundingBox() const
- const BoundingBox& GetWorldBoundingBox()
- char GetDrawableFlags() const
- float GetDrawDistance() const
- float GetShadowDistance() const
- float GetLodBias() const
- unsigned GetViewMask() const
- unsigned GetLightMask() const
- unsigned GetShadowMask() const
- unsigned GetZoneMask() const
- unsigned GetMaxLights() const
- bool GetCastShadows() const
- bool IsOccluder() const
- bool IsOccludee() const
- bool IsInView() const
- bool IsInView(Camera* tolua_var_2) const
- Zone* GetZone() const

### Properties


- BoundingBox& worldBoundingBox (readonly)
- char drawableFlags (readonly)
- float drawDistance
- float shadowDistance
- float lodBias
- unsigned viewMask
- unsigned lightMask
- unsigned shadowMask
- unsigned zoneMask
- unsigned maxLights
- bool castShadows
- bool occluder
- bool occludee
- bool inView (readonly)
- Zone* zone (readonly)



---

**Inherits from**: Component

## Octree : Component


### Methods


- void SetSize(const BoundingBox& box, unsigned numLevels)
- void Update(const FrameInfo& frame)
- void AddManualDrawable(Drawable* drawable)
- void RemoveManualDrawable(Drawable* drawable)
- const PODVector<OctreeQueryResult>& GetDrawables(const Vector3& point, char drawableFlags = DRAWABLE_ANY, unsigned viewMask = DEFAULT_VIEWMASK) const
- const PODVector<OctreeQueryResult>& GetDrawables(const BoundingBox& box, char drawableFlags = DRAWABLE_ANY, unsigned viewMask = DEFAULT_VIEWMASK) const
- const PODVector<OctreeQueryResult>& GetDrawables(const Frustum& frustum, char drawableFlags = DRAWABLE_ANY, unsigned viewMask = DEFAULT_VIEWMASK) const
- const PODVector<OctreeQueryResult>& GetDrawables(const Sphere& sphere, char drawableFlags = DRAWABLE_ANY, unsigned viewMask = DEFAULT_VIEWMASK) const
- const PODVector<OctreeQueryResult>& GetAllDrawables(char drawableFlags = DRAWABLE_ANY, unsigned viewMask = DEFAULT_VIEWMASK) const
- const PODVector<RayQueryResult>& Raycast(const Ray& ray, RayQueryLevel level, float maxDistance, char drawableFlags, unsigned viewMask = DEFAULT_VIEWMASK) const
- RayQueryResult RaycastSingle(const Ray& ray, RayQueryLevel level, float maxDistance, char drawableFlags, unsigned viewMask = DEFAULT_VIEWMASK) const
- unsigned GetNumLevels() const
- void QueueUpdate(Drawable* drawable)
- void DrawDebugGeometry(bool depthTest)

### Properties


- unsigned numLevels (readonly)



---

## Viewport



### Methods


- Viewport() (GC)
- Viewport* new()
- Viewport(Scene* scene, Camera* camera, RenderPath* renderPath = 0) (GC)
- Viewport* new(Scene* scene, Camera* camera, RenderPath* renderPath = 0)
- Viewport(Scene* scene, Camera* camera, const IntRect& rect, RenderPath* renderPath = 0) (GC)
- Viewport* new(Scene* scene, Camera* camera, const IntRect& rect, RenderPath* renderPath = 0)
- void delete()
- void SetScene(Scene* scene)
- void SetCamera(Camera* camera)
- void SetCullCamera(Camera* camera)
- void SetRect(const IntRect& rect)
- void SetRenderPath(RenderPath* path)
- void SetRenderPath(XMLFile* file)
- void SetDrawDebug(bool enable)
- Scene* GetScene() const
- Camera* GetCamera() const
- Camera* GetCullCamera() const
- const IntRect& GetRect() const
- RenderPath* GetRenderPath() const
- bool GetDrawDebug() const
- Ray GetScreenRay(int x, int y) const
- IntVector2 WorldToScreenPoint(const Vector3& worldPos) const
- Vector3 ScreenToWorldPoint(int x, int y, float depth) const

### Properties


- Scene* scene
- Camera* camera
- Camera* cullCamera
- IntRect& rect
- RenderPath* renderPath
- bool drawDebug



---

## RenderPath



### Methods


- RenderPath* Clone()
- bool Load(XMLFile* file)
- bool Append(XMLFile* file)
- void SetEnabled(const String tag, bool active)
- bool IsEnabled(const String tag) const
- bool IsAdded(const String tag) const
- void ToggleEnabled(const String tag)
- void SetRenderTarget(unsigned index, const RenderTargetInfo& info)
- void AddRenderTarget(const RenderTargetInfo& info)
- void RemoveRenderTarget(const String name)
- void RemoveRenderTarget(unsigned index)
- void RemoveRenderTargets(const String tag)
- void SetCommand(unsigned index, const RenderPathCommand& command)
- void AddCommand(const RenderPathCommand& command)
- void InsertCommand(unsigned index, const RenderPathCommand& command)
- void RemoveCommand(unsigned index)
- void RemoveCommands(const String tag)
- void SetShaderParameter(const String name, const Variant& value)
- unsigned GetNumRenderTargets() const
- unsigned GetNumCommands() const
- RenderPathCommand* GetCommand(unsigned index)
- const Variant& GetShaderParameter(const String name) const



---

## RenderSurface



### Methods


- RenderSurface(Texture* parentTexture) (GC)
- RenderSurface* new(Texture* parentTexture)
- void delete()
- void SetNumViewports(unsigned num)
- void SetViewport(unsigned index, Viewport* viewport)
- void SetUpdateMode(RenderSurfaceUpdateMode mode)
- void SetLinkedRenderTarget(RenderSurface* renderTarget)
- void SetLinkedDepthStencil(RenderSurface* depthStencil)
- void QueueUpdate()
- void Release()
- Texture* GetParentTexture() const
- int GetWidth() const
- int GetHeight() const
- TextureUsage GetUsage() const
- unsigned GetNumViewports() const
- Viewport* GetViewport(unsigned index) const
- RenderSurfaceUpdateMode GetUpdateMode() const
- RenderSurface* GetLinkedRenderTarget() const
- RenderSurface* GetLinkedDepthStencil() const
- bool IsResolveDirty() const

### Properties


- Texture* parentTexture (readonly)
- int width (readonly)
- int height (readonly)
- TextureUsage usage (readonly)
- unsigned numViewports
- RenderSurfaceUpdateMode updateMode
- RenderSurface* linkedRenderTarget
- RenderSurface* linkedDepthStencil
- bool resolveDirty (readonly)



---

**Inherits from**: Resource

## Technique : Resource


### Methods


- void SetIsDesktop(bool enable)
- Pass* CreatePass(const String passName)
- void RemovePass(const String passName)
- void ReleaseShaders()
- Technique* Clone(const String cloneName = String::EMPTY) const
- bool HasPass(const String type) const
- Pass* GetPass(const String type) const
- Pass* GetSupportedPass(const String type) const
- bool IsSupported() const
- bool IsDesktop() const
- unsigned GetNumPasses() const
- const Vector<String>& GetPassTypes() const
- const PODVector<Pass*>& GetPasses() const

### Properties


- bool supported (readonly)
- bool desktop (readonly)
- unsigned numPasses (readonly)



---

**Inherits from**: RefCounted

## Pass : RefCounted


### Methods


- void SetBlendMode(BlendMode mode)
- void SetCullMode(CullMode mode)
- void SetDepthTestMode(CompareMode mode)
- void SetLightingMode(PassLightingMode mode)
- void SetDepthWrite(bool enable)
- void SetAlphaToCoverage(bool enable)
- void SetIsDesktop(bool enable)
- void SetVertexShader(const String name)
- void SetPixelShader(const String name)
- void SetVertexShaderDefines(const String defines)
- void SetPixelShaderDefines(const String defines)
- void SetVertexShaderDefineExcludes(const String excludes)
- void SetPixelShaderDefineExcludes(const String excludes)
- void ReleaseShaders()
- const String GetName() const
- unsigned GetIndex() const
- CullMode GetCullMode() const
- BlendMode GetBlendMode() const
- CompareMode GetDepthTestMode() const
- PassLightingMode GetLightingMode() const
- bool GetDepthWrite() const
- bool GetAlphaToCoverage() const
- bool IsDesktop() const
- const String GetVertexShader() const
- const String GetPixelShader() const
- const String GetVertexShaderDefines() const
- const String GetPixelShaderDefines() const
- const String GetVertexShaderDefineExcludes() const
- const String GetPixelShaderDefineExcludes() const

### Properties


- String name (readonly)
- unsigned index (readonly)
- BlendMode blendMode
- CullMode cullMode
- CompareMode depthTestMode
- PassLightingMode lightingMode
- bool depthWrite
- bool alphaToCoverage
- bool desktop (readonly)
- String vertexShader
- String pixelShader
- String vertexShaderDefines
- String pixelShaderDefines
- String vertexShaderDefineExcludes
- String pixelShaderDefineExcludes



---

**Inherits from**: Drawable

## BillboardSet : Drawable


### Methods


- void SetMaterial(Material* material)
- void SetNumBillboards(unsigned num)
- void SetRelative(bool enable)
- void SetScaled(bool enable)
- void SetSorted(bool enable)
- void SetFixedScreenSize(bool enable)
- void SetFaceCameraMode(FaceCameraMode mode)
- void SetMinAngle(float angle)
- void SetAnimationLodBias(float bias)
- void Commit()
- Material* GetMaterial() const
- unsigned GetNumBillboards() const
- Billboard* GetBillboard(unsigned index)
- bool IsRelative() const
- bool IsScaled() const
- bool IsSorted() const
- bool IsFixedScreenSize() const
- FaceCameraMode GetFaceCameraMode() const
- float GetMinAngle() const
- float GetAnimationLodBias() const

### Properties


- Material* material
- unsigned numBillboards
- bool relative
- bool scaled
- bool sorted
- bool fixedScreenSize
- FaceCameraMode faceCameraMode
- float minAngle
- float animationLodBias



---

## Billboard



### Properties


- Vector3 position
- Vector2 size
- Rect uv
- Color color
- float rotation
- bool enabled



---

**Inherits from**: Drawable

## CustomGeometry : Drawable


### Methods


- void Clear()
- void SetNumGeometries(unsigned num)
- void SetDynamic(bool enable)
- void BeginGeometry(unsigned index, PrimitiveType type)
- void DefineVertex(const Vector3& position)
- void DefineNormal(const Vector3& normal)
- void DefineTangent(const Vector4& tangent)
- void DefineColor(const Color& color)
- void DefineTexCoord(const Vector2& texCoord)
- void DefineGeometry(unsigned index, PrimitiveType type, unsigned numVertices, bool hasNormals, bool hasColors, bool hasTexCoords, bool hasTangents)
- void Commit()
- void SetMaterial(Material* material)
- bool SetMaterial(unsigned index, Material* material)
- unsigned GetNumGeometries() const
- unsigned GetNumVertices(unsigned index) const
- bool IsDynamic() const
- Material* GetMaterial(unsigned index = 0)
- CustomGeometryVertex* GetVertex(unsigned geometryIndex, unsigned vertexNum)

### Properties


- Material* material
- unsigned numGeometries
- bool dynamic



---

**Inherits from**: Drawable

## DecalSet : Drawable


### Methods


- void SetMaterial(Material* material)
- void SetMaxVertices(unsigned num)
- void SetMaxIndices(unsigned num)
- void SetOptimizeBufferSize(bool enable)
- bool AddDecal(Drawable* target, const Vector3& worldPosition, const Quaternion& worldRotation, float size, float aspectRatio, float depth, const Vector2& topLeftUV, const Vector2& bottomRightUV, float timeToLive = 0.0f, float normalCutoff = 0.1f, unsigned subGeometry = M_MAX_UNSIGNED)
- void RemoveDecals(unsigned num)
- void RemoveAllDecals()
- Material* GetMaterial() const
- unsigned GetNumDecals() const
- unsigned GetNumVertices() const
- unsigned GetNumIndices() const
- unsigned GetMaxVertices() const
- unsigned GetMaxIndices() const
- bool GetOptimizeBufferSize() const

### Properties


- Material* material
- unsigned numDecals (readonly)
- unsigned numVertices (readonly)
- unsigned numIndices (readonly)
- unsigned maxVertices
- unsigned maxIndices
- bool optimizeBufferSize



---

**Inherits from**: Drawable

## RibbonTrail : Drawable


### Methods


- void SetMaterial(Material* material)
- void SetVertexDistance(float length)
- void SetWidth(float width)
- void SetStartColor(const Color& c)
- void SetEndColor(const Color& c)
- void SetStartScale(float startScale)
- void SetEndScale(float endScale)
- void SetTrailType(TrailType type)
- void SetBaseVelocity(const Vector3& baseVelocity)
- void SetSorted(bool enable)
- void SetLifetime(float time)
- void SetEmitting(bool emitting)
- void SetUpdateInvisible(bool updateInvisible)
- void SetTailColumn(unsigned tailColumn)
- void SetAnimationLodBias(float bias)
- void Commit()
- Material* GetMaterial() const
- float GetVertexDistance() const
- float GetWidth() const
- const Color& GetStartColor() const
- const Color& GetEndColor() const
- float GetStartScale() const
- float GetEndScale() const
- TrailType GetTrailType() const
- const Vector3& GetBaseVelocity() const
- bool IsSorted() const
- float GetLifetime() const
- unsigned GetTailColumn() const
- bool IsEmitting() const
- bool GetUpdateInvisible() const
- float GetAnimationLodBias() const

### Properties


- Material* material
- float vertexDistance
- float width
- Color& startColor
- Color& endColor
- float startScale
- float endScale
- TrailType trailType
- Vector3 baseVelocity
- bool sorted
- float lifetime
- unsigned tailColumn
- bool emitting
- bool updateInvisible
- float animationLodBias



---

**Inherits from**: Drawable

## TerrainPatch : Drawable


### Methods


- void SetOwner(Terrain* terrain)
- void SetNeighbors(TerrainPatch* north, TerrainPatch* south, TerrainPatch* west, TerrainPatch* east)
- void SetMaterial(Material* material)
- void SetBoundingBox(const BoundingBox& box)
- void SetCoordinates(const IntVector2& coordinates)
- void ResetLod()
- Geometry* GetGeometry() const
- Geometry* GetMaxLodGeometry() const
- Geometry* GetOcclusionGeometry() const
- VertexBuffer* GetVertexBuffer() const
- Terrain* GetOwner() const
- TerrainPatch* GetNorthPatch() const
- TerrainPatch* GetSouthPatch() const
- TerrainPatch* GetWestPatch() const
- TerrainPatch* GetEastPatch() const
- const IntVector2& GetCoordinates() const
- unsigned GetLodLevel() const

### Properties


- Geometry* geometry (readonly)
- Geometry* maxLodGeometry (readonly)
- Geometry* occlusionGeometry (readonly)
- VertexBuffer* vertexBuffer (readonly)
- Terrain* owner
- TerrainPatch* northPatch (readonly)
- TerrainPatch* southPatch (readonly)
- TerrainPatch* westPatch (readonly)
- TerrainPatch* eastPatch (readonly)
- BoundingBox& boundingBox
- IntVector2& coordinates
- unsigned lodLevel (readonly)



---

**Inherits from**: Component

## Terrain : Component


### Methods


- void SetPatchSize(int size)
- void SetSpacing(const Vector3& spacing)
- void SetMaxLodLevels(unsigned levels)
- void SetOcclusionLodLevel(unsigned level)
- void SetSmoothing(bool enable)
- bool SetHeightMap(Image* image)
- void SetMaterial(Material* material)
- void SetNorthNeighbor(Terrain* north)
- void SetSouthNeighbor(Terrain* south)
- void SetWestNeighbor(Terrain* west)
- void SetEastNeighbor(Terrain* east)
- void SetNeighbors(Terrain* north, Terrain* south, Terrain* west, Terrain* east)
- void SetDrawDistance(float distance)
- void SetShadowDistance(float distance)
- void SetLodBias(float bias)
- void SetViewMask(unsigned mask)
- void SetLightMask(unsigned mask)
- void SetShadowMask(unsigned mask)
- void SetZoneMask(unsigned mask)
- void SetMaxLights(unsigned num)
- void SetCastShadows(bool enable)
- void SetOccluder(bool enable)
- void SetOccludee(bool enable)
- void ApplyHeightMap()
- int GetPatchSize() const
- const Vector3& GetSpacing() const
- const IntVector2& GetNumVertices() const
- const IntVector2& GetNumPatches() const
- unsigned GetMaxLodLevels() const
- unsigned GetOcclusionLodLevel() const
- bool GetSmoothing() const
- Image* GetHeightMap() const
- Material* GetMaterial() const
- Terrain* GetNorthNeighbor() const
- Terrain* GetSouthNeighbor() const
- Terrain* GetWestNeighbor() const
- Terrain* GetEastNeighbor() const
- TerrainPatch* GetPatch(unsigned index) const
- TerrainPatch* GetPatch(int x, int z) const
- TerrainPatch* GetNeighborPatch(int x, int z) const
- float GetHeight(const Vector3& worldPosition) const
- Vector3 GetNormal(const Vector3& worldPosition) const
- IntVector2 WorldToHeightMap(const Vector3& worldPosition) const
- Vector3 HeightMapToWorld(const IntVector2& pixelPosition) const
- SharedArrayPtr<float> GetHeightData() const
- float GetDrawDistance() const
- float GetShadowDistance() const
- float GetLodBias() const
- unsigned GetViewMask() const
- unsigned GetLightMask() const
- unsigned GetShadowMask() const
- unsigned GetZoneMask() const
- unsigned GetMaxLights() const
- bool IsVisible() const
- bool GetCastShadows() const
- bool IsOccluder() const
- bool IsOccludee() const

### Properties


- int patchSize
- Vector3& spacing
- IntVector2& numVertices (readonly)
- IntVector2& numPatches (readonly)
- unsigned maxLodLevels
- unsigned occlusionLodLevel
- bool smoothing
- Image* heightMap
- Material* material
- Terrain* northNeighbor
- Terrain* southNeighbor
- Terrain* westNeighbor
- Terrain* eastNeighbor
- float drawDistance
- float shadowDistance
- float lodBias
- unsigned viewMask
- unsigned lightMask
- unsigned shadowMask
- unsigned zoneMask
- unsigned maxLights
- bool visible (readonly)
- bool castShadows
- bool occluder
- bool occludee



---

