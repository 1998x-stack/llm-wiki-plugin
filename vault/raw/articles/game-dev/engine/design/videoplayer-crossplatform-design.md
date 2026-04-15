---
summary: "Cross-platform VideoPlayer implementation for PC, Android, iOS with render-to-texture and A/V sync"
related_paths:
  - engine/Source/Urho3D/Video/**
last_updated: "2026-04-02"
---

# VideoPlayer 跨平台实现方案

## 一、目标

将现有仅支持 WASM 的 VideoPlayer 扩展到 **PC (Windows/Linux/macOS)**、**Android**、**iOS** 平台，实现：

1. **渲染到纹理** - 与引擎渲染管线集成
2. **音视频同步** - 画面和声音同步播放
3. **通用格式支持** - MP4/H.264/AAC 为主
4. **网络视频支持** - HTTP/HTTPS URL 播放

---

## 二、整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        Lua API (不变)                            │
│         videoPlayer:Load() / Play() / Pause() / GetTexture()    │
├─────────────────────────────────────────────────────────────────┤
│                     VideoPlayer (C++ 统一接口)                   │
│                  管理播放状态、音视频同步、对外暴露 API            │
├─────────────────────────────────────────────────────────────────┤
│                      VideoDecoder (抽象接口)                     │
│                        负责视频解码，输出 RGBA 帧                 │
├──────────────┬──────────────┬───────────────┬───────────────────┤
│   FFmpeg     │  MediaCodec  │ AVFoundation  │   HTML5 Video     │
│  (PC 全平台)  │  (Android)   │    (iOS)      │   (WASM 现有)     │
├──────────────┴──────────────┴───────────────┴───────────────────┤
│                      AudioPlayer (抽象接口)                      │
│                        负责音频解码和播放                         │
├──────────────┬──────────────┬───────────────┬───────────────────┤
│ FFmpeg+OpenAL│  AudioTrack  │ AVFoundation  │   HTML5 Audio     │
│  (PC 全平台)  │  (Android)   │    (iOS)      │   (WASM 现有)     │
├──────────────┴──────────────┴───────────────┴───────────────────┤
│                     VideoTexture (纹理管理)                      │
│              继承 Texture2D，接收 RGBA 数据更新到 GPU             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 三、各平台技术选型

| 平台 | 视频解码 | 音频播放 | 理由 |
|------|----------|----------|------|
| **Windows** | FFmpeg (LGPL) | OpenAL Soft | 跨平台、格式支持广、动态链接无许可证问题 |
| **Linux** | FFmpeg (LGPL) | OpenAL Soft | 同上 |
| **macOS** | FFmpeg (LGPL) | OpenAL Soft | 同上（也可选 AVFoundation） |
| **Android** | MediaCodec | AudioTrack | 系统自带、硬件加速、零额外体积 |
| **iOS** | AVFoundation | AVFoundation | 系统自带、硬件加速、API 简洁 |
| **WASM** | HTML5 Video | HTML5 Audio | 现有实现，浏览器原生支持 |

### FFmpeg 许可证说明

使用 **LGPL 2.1/3.0** 许可：
- 动态链接时：无需开源应用代码
- 仅使用解码器（H.264/H.265/AAC），不使用 GPL 组件（如 libx264 编码器）
- 对商业项目无影响

---

## 四、核心类设计

### 4.1 VideoFrame - 视频帧数据

```cpp
struct VideoFrame
{
    unsigned char* data;    // RGBA 像素数据
    int width;              // 帧宽度
    int height;             // 帧高度
    int stride;             // 每行字节数
    double pts;             // 显示时间戳 (秒)
};
```

### 4.2 AudioFrame - 音频帧数据

```cpp
struct AudioFrame
{
    float* data;            // PCM 浮点数据 (交错格式)
    int sampleCount;        // 采样数
    int channels;           // 声道数
    int sampleRate;         // 采样率
    double pts;             // 显示时间戳 (秒)
};
```

### 4.3 VideoDecoder - 视频解码抽象接口

```cpp
class VideoDecoder : public Object
{
public:
    // 打开视频 (本地路径或网络 URL)
    virtual bool Open(const String& source) = 0;

    // 关闭并释放资源
    virtual void Close() = 0;

    // 解码下一帧，返回是否成功
    virtual bool DecodeFrame(VideoFrame& frame) = 0;

    // 跳转到指定时间 (秒)
    virtual bool Seek(double time) = 0;

    // 获取视频信息
    virtual int GetWidth() const = 0;
    virtual int GetHeight() const = 0;
    virtual double GetDuration() const = 0;
    virtual double GetFrameRate() const = 0;

    // 工厂方法：根据平台创建对应解码器
    static VideoDecoder* Create(Context* context);
};
```

### 4.4 AudioDecoder - 音频解码抽象接口

```cpp
class AudioDecoder : public Object
{
public:
    virtual bool Open(const String& source) = 0;
    virtual void Close() = 0;
    virtual bool DecodeFrame(AudioFrame& frame) = 0;
    virtual bool Seek(double time) = 0;

    virtual int GetSampleRate() const = 0;
    virtual int GetChannels() const = 0;

    static AudioDecoder* Create(Context* context);
};
```

### 4.5 AudioPlayer - 音频播放抽象接口

```cpp
class AudioPlayer : public Object
{
public:
    // 初始化播放器
    virtual bool Initialize(int sampleRate, int channels) = 0;

    // 提交音频数据到播放队列
    virtual void QueueAudio(const AudioFrame& frame) = 0;

    // 获取当前播放位置 (用于音视频同步)
    virtual double GetPlaybackPosition() const = 0;

    // 播放控制
    virtual void Play() = 0;
    virtual void Pause() = 0;
    virtual void Stop() = 0;

    // 音量控制
    virtual void SetVolume(float volume) = 0;
    virtual void SetMuted(bool muted) = 0;

    static AudioPlayer* Create(Context* context);
};
```

### 4.6 VideoPlayer - 统一播放控制器

```cpp
class VideoPlayer : public Object
{
public:
    // 加载视频
    bool Load(const String& source, int textureWidth = 0, int textureHeight = 0);

    // 播放控制
    void Play();
    void Pause();
    void Stop();
    void Seek(float time);

    // 音量控制
    void SetVolume(float volume);
    void SetMuted(bool muted);
    void SetLoop(bool loop);

    // 状态查询
    float GetCurrentTime() const;
    float GetDuration() const;
    bool IsPlaying() const;
    bool IsReady() const;
    VideoState GetState() const;

    // 获取纹理 (用于渲染)
    VideoTexture* GetTexture() const;

    // 每帧更新 (必须调用)
    void Update(float deltaTime);

private:
    SharedPtr<VideoDecoder> videoDecoder_;
    SharedPtr<AudioDecoder> audioDecoder_;
    SharedPtr<AudioPlayer> audioPlayer_;
    SharedPtr<VideoTexture> texture_;

    // 音视频同步
    double masterClock_;        // 主时钟 (以音频为准)
    double videoPts_;           // 当前视频帧 PTS
    VideoFrame currentFrame_;   // 当前待显示帧

    // 状态
    VideoState state_;
    bool loop_;
    float volume_;
    bool muted_;
};
```

---

## 五、音视频同步机制

采用 **音频为主时钟** 的同步策略（业界标准）：

```
┌─────────────────────────────────────────────────────────────────┐
│                       Update() 每帧调用                          │
├─────────────────────────────────────────────────────────────────┤
│  1. 获取音频播放位置作为主时钟                                    │
│     masterClock = audioPlayer_->GetPlaybackPosition()            │
│                                                                  │
│  2. 解码音频帧并送入播放队列                                      │
│     while (audioQueue 不满) {                                    │
│         audioDecoder_->DecodeFrame(audioFrame)                   │
│         audioPlayer_->QueueAudio(audioFrame)                     │
│     }                                                            │
│                                                                  │
│  3. 根据主时钟决定视频帧显示                                      │
│     if (videoPts_ <= masterClock) {                              │
│         // 当前帧该显示了，更新纹理                               │
│         texture_->SetData(currentFrame_.data)                    │
│                                                                  │
│         // 解码下一帧                                             │
│         videoDecoder_->DecodeFrame(currentFrame_)                │
│         videoPts_ = currentFrame_.pts                            │
│     }                                                            │
│                                                                  │
│  4. 处理音视频不同步情况                                          │
│     if (videoPts_ < masterClock - 0.1) {                         │
│         // 视频落后太多，丢帧追赶                                 │
│         跳过当前帧，解码下一帧                                    │
│     }                                                            │
└─────────────────────────────────────────────────────────────────┘
```

**同步原理**：
- 音频播放是连续的，人耳对音频不连续非常敏感
- 视频可以丢帧或重复帧，人眼不太敏感
- 因此以音频时间为基准，视频去追赶音频

---

## 六、PC 平台实现 (FFmpeg + OpenAL)

### 6.1 FFmpeg 库依赖

| 库 | 用途 |
|---|------|
| libavformat | 解封装 (读取 MP4/WebM 等容器) |
| libavcodec | 解码 (H.264/H.265/VP9/AAC 等) |
| libswscale | 视频像素格式转换 (YUV → RGBA) |
| libswresample | 音频重采样 (统一为 float 格式) |
| libavutil | 工具函数 |

### 6.2 解码流程

```
Open():
  avformat_open_input()       打开文件/URL
  avformat_find_stream_info() 读取流信息
  找到视频流和音频流索引
  avcodec_find_decoder()      找到解码器
  avcodec_open2()             打开解码器
  sws_getContext()            创建 YUV→RGBA 转换器
  swr_alloc_set_opts()        创建音频重采样器

DecodeVideoFrame():
  av_read_frame()             读取一个压缩包
  avcodec_send_packet()       送入解码器
  avcodec_receive_frame()     获取解码后的 YUV 帧
  sws_scale()                 YUV → RGBA 转换
  填充 VideoFrame 结构返回

DecodeAudioFrame():
  av_read_frame()             读取压缩包
  avcodec_send_packet()       送入解码器
  avcodec_receive_frame()     获取解码后的 PCM
  swr_convert()               重采样为统一格式
  填充 AudioFrame 结构返回
```

### 6.3 网络视频支持

FFmpeg 原生支持网络协议：

```cpp
// 本地文件和网络 URL 使用相同 API
avformat_open_input(&formatCtx, "file:///path/to/video.mp4", ...);
avformat_open_input(&formatCtx, "https://example.com/video.mp4", ...);
```

### 6.4 OpenAL 音频播放

使用三缓冲队列实现流式播放：

```cpp
class AudioPlayerOpenAL : public AudioPlayer
{
    ALuint source_;           // 音源
    ALuint buffers_[3];       // 三缓冲队列
    ALenum format_;           // AL_FORMAT_STEREO_FLOAT32

    void QueueAudio(const AudioFrame& frame);
    double GetPlaybackPosition() const;
};
```

---

## 七、Android 平台实现 (MediaCodec + AudioTrack)

### 7.1 架构

```
┌─────────────────────────────────────────┐
│           C++ VideoPlayer               │
├─────────────────────────────────────────┤
│              JNI 桥接                    │
├─────────────────────────────────────────┤
│  Java: MediaExtractor + MediaCodec      │
│  Java: AudioTrack                        │
└─────────────────────────────────────────┘
```

### 7.2 关键组件

| 组件 | 用途 |
|------|------|
| MediaExtractor | 解封装，读取视频/音频轨道 |
| MediaCodec | 硬件加速解码 |
| AudioTrack | 音频播放 |

### 7.3 特点

- 系统自带，零额外体积
- 硬件加速解码，性能优异
- 支持网络 URL

---

## 八、iOS 平台实现 (AVFoundation)

### 8.1 架构

```
┌─────────────────────────────────────────┐
│           C++ VideoPlayer               │
├─────────────────────────────────────────┤
│      Objective-C++ Bridge (.mm)         │
├─────────────────────────────────────────┤
│  AVPlayer + AVPlayerItemVideoOutput     │
└─────────────────────────────────────────┘
```

### 8.2 实现方案

使用 AVPlayer + AVPlayerItemVideoOutput：

- AVPlayer 自动处理音视频同步
- AVPlayerItemVideoOutput 输出 CVPixelBuffer
- 每帧从 CVPixelBuffer 提取 RGBA 数据更新纹理

### 8.3 特点

- 系统自带，零额外体积
- 硬件加速
- 自动处理网络缓冲
- 代码简洁

---

## 九、纹理更新机制

所有平台统一使用 `VideoTexture::SetData()` 更新纹理：

```cpp
bool VideoTexture::SetData(int x, int y, int width, int height, const void* data)
{
    const bgfx::Memory* mem = bgfx::copy(data, width * height * 4);
    bgfx::updateTexture2D(
        bgfx::TextureHandle{GetGPUObjectIdx()},
        0, 0,           // layer, mip
        x, y,           // offset
        width, height,
        mem
    );
    return true;
}
```

**与 WASM 版本的区别**：
- WASM：JavaScript 直接操作 WebGL 纹理，使用 `bgfx::overrideInternal()`
- 其他平台：C++ 解码后通过 `bgfx::updateTexture2D()` 上传数据

---

## 十、文件结构

```
engine/Source/Urho3D/Graphics/
├── VideoPlayer.h                 # 统一接口 (修改)
├── VideoPlayer.cpp               # 跨平台实现 (重写)
├── VideoTexture.h                # 纹理管理 (修改)
├── VideoTexture.cpp              # 添加 SetData (修改)
│
├── VideoDecoder.h                # 视频解码抽象接口 (新增)
├── VideoDecoder.cpp              # 工厂方法 (新增)
├── VideoDecoderFFmpeg.h          # PC 实现 (新增)
├── VideoDecoderFFmpeg.cpp        # PC 实现 (新增)
├── VideoDecoderMediaCodec.h      # Android 实现 (新增)
├── VideoDecoderMediaCodec.cpp    # Android 实现 (新增)
├── VideoDecoderAVFoundation.h    # iOS 实现 (新增)
├── VideoDecoderAVFoundation.mm   # iOS 实现 (新增)
│
├── AudioDecoder.h                # 音频解码抽象接口 (新增)
├── AudioDecoder.cpp              # 工厂方法 (新增)
├── AudioDecoderFFmpeg.h          # PC 实现 (新增)
├── AudioDecoderFFmpeg.cpp        # PC 实现 (新增)
│
├── AudioPlayer.h                 # 音频播放抽象接口 (新增)
├── AudioPlayer.cpp               # 工厂方法 (新增)
├── AudioPlayerOpenAL.h           # PC 实现 (新增)
├── AudioPlayerOpenAL.cpp         # PC 实现 (新增)
├── AudioPlayerAndroid.h          # Android 实现 (新增)
├── AudioPlayerAndroid.cpp        # Android 实现 (新增)
└── AudioPlayerAVFoundation.mm    # iOS 实现 (新增)

3rd/
└── ffmpeg/                       # FFmpeg 预编译库 (新增)
    ├── include/
    ├── lib/
    │   ├── win64/
    │   ├── linux64/
    │   └── macos/
    └── CMakeLists.txt
```

---

## 十一、实现计划

| 阶段 | 内容 | 平台 |
|------|------|------|
| **Phase 1** | 抽象接口设计 + FFmpeg 集成 + 基础视频播放 | Windows |
| **Phase 2** | 音频播放 (OpenAL) + 音视频同步 | Windows |
| **Phase 3** | 网络视频支持 + 测试完善 | Windows |
| **Phase 4** | MediaCodec + AudioTrack 实现 | Android |
| **Phase 5** | AVFoundation 实现 | iOS |

---

## 十二、API 使用示例

```lua
-- Lua 层 API 保持不变
local Video = require("urhox-libs/Video")

local player = Video.VideoPlayer {
    src = "https://example.com/video.mp4",  -- 支持网络 URL
    width = "100%",
    height = "100%",
    autoPlay = true,
    loop = false,
    volume = 0.8,

    onReady = function(self)
        print("视频就绪")
    end,

    onEnded = function(self)
        print("播放结束")
    end,
}

-- 或者直接使用 C++ API
local videoPlayer = VideoPlayer:new()
videoPlayer:Load("Data/Videos/intro.mp4")
videoPlayer:Play()

-- 每帧更新
function HandleUpdate(eventType, eventData)
    videoPlayer:Update()
end

-- 获取纹理用于渲染
local texture = videoPlayer:GetTexture()
```

---

## 十三、支持的格式

| 格式 | 容器 | 视频编码 | 音频编码 | 支持平台 |
|------|------|----------|----------|----------|
| **MP4/H.264** | .mp4 | H.264 (AVC) | AAC | 全平台 |
| **MP4/H.265** | .mp4 | H.265 (HEVC) | AAC | 全平台 |
| **WebM/VP9** | .webm | VP9 | Opus/Vorbis | PC, WASM |
| **MOV** | .mov | H.264/ProRes | AAC | 全平台 |

---

## 十四、异步加载（AsyncLoad）

### 14.1 背景与动机

`VideoPlayer::Load()` 在 Native 平台上是**同步阻塞**的，对于 HTTPS URL 视频源，主线程会被阻塞在网络连接、TLS 握手、格式探测等操作上。WASM 平台例外——浏览器 `<video>` 元素天然异步加载。

各平台 `Load()` 阻塞点分析：

| 平台 | 后端 | 阻塞操作 |
|------|------|----------|
| **FFmpeg** (Win/Linux/macOS) | `avformat_open_input` + `avformat_find_stream_info` | TCP+TLS+HTTP+格式探测 |
| **Android** (MediaCodec NDK) | `AMediaExtractor_setDataSource(url)` × 2 | HTTP 连接+格式探测，执行两次 |
| **iOS** (AVFoundation) | `AVAsset loadValuesAsynchronouslyForKeys` + `dispatch_semaphore_wait` | 系统 API 本身异步，但代码用 semaphore 强制等成同步（超时 10s） |
| **WASM** (HTML5 Video) | 无阻塞 | `<video preload="auto">` 天然异步 |

> **注**：本地文件的 `Open()` 也统一走异步路径。虽然本地 I/O 通常只需几毫秒，但主流引擎（Unity、Unreal）同样不区分本地/网络，统一异步——代码路径统一减少分支 bug，且某些场景本地 I/O 也可能慢（机械硬盘、移动设备存储、加密容器）。

### 14.2 API 设计

#### C++ 接口

```cpp
/// Callback type for async load completion.
using AsyncLoadCallback = std::function<void(bool success)>;

class URHO3D_API VideoPlayer : public Object
{
public:
    // 现有接口（保持不变）
    bool Load(const String& source, int width = 1920, int height = 1080);

    // === 新增接口 ===

    /// Asynchronously load video from URL/path.
    /// @return True if async load was successfully started.
    bool AsyncLoad(const String& source, int width = 1920, int height = 1080,
                   const AsyncLoadCallback& callback = nullptr);

    /// Return whether async loading is in progress.
    bool IsAsyncLoading() const { return asyncLoading_; }
};
```

#### Lua 接口

```lua
--- 异步加载视频（立即返回，不阻塞主线程）
--- @param source string 视频 URL 或路径
--- @param width? number 纹理宽度（默认 1920）
--- @param height? number 纹理高度（默认 1080）
--- @param callback? function 加载完成回调 function(success: boolean)
--- @return boolean 是否成功触发异步加载
function VideoPlayer:AsyncLoad(source, width, height, callback) end

--- 是否正在异步加载中
--- @return boolean
function VideoPlayer:IsAsyncLoading() end
```

#### 使用示例

```lua
local player = VideoPlayer()

-- 方式 1: 回调
player:AsyncLoad("https://cdn.example.com/video.mp4", 0, 0, function(success)
    if success then
        player:Play()
    else
        print("Video load failed")
    end
end)

-- 方式 2: 轮询 ready
player:AsyncLoad("https://cdn.example.com/video.mp4")

function Update(dt)
    player:Update()
    if player.ready and not player.playing then
        player:Play()
    end
end
```

### 14.3 内部实现

#### Load 函数重构

将现有 `Load()` 拆分为 `PrepareLoad()` + `FinalizeLoad()`，`AsyncLoad` 复用这两段逻辑：

| 新函数 | 内容 |
|--------|------|
| `PrepareLoad()` | 清理旧状态 + 创建 decoder + 解析 URL |
| `FinalizeLoad()` | 获取尺寸 + 初始化纹理 + 创建解码线程 + 创建音频 |

重构后的 `Load()` 变为：

```cpp
bool VideoPlayer::Load(const String& source, int width, int height)
{
    String resolvedSource;
    if (!PrepareLoad(source, resolvedSource))
        return false;
    if (!decoder_->Open(resolvedSource))  // 同步阻塞点
    {
        URHO3D_LOGERRORF("VideoPlayer: Failed to open '%s'", source.CString());
        decoder_.Reset();
        return false;
    }
    return FinalizeLoad(width, height);
}
```

#### 异步加载数据结构

```cpp
struct AsyncLoadData
{
    // 输入（主线程写入，后台线程只读）
    String resolvedSource;
    int width{0};
    int height{0};
    SharedPtr<VideoDecoder> decoder;

    // 输出（后台线程写入，主线程在 completed 后读取）
    bool success{false};

    // 控制标志
    std::atomic<bool> completed{false};
    std::atomic<bool> cancelled{false};

    // 生命周期（selfRef 防止任务执行期间数据被释放）
    std::shared_ptr<AsyncLoadData> selfRef;
};
```

#### AsyncLoad 流程

```cpp
bool VideoPlayer::AsyncLoad(const String& source, int width, int height,
                            const AsyncLoadCallback& callback)
{
    String resolvedSource;
    if (!PrepareLoad(source, resolvedSource))
    {
        if (callback) callback(false);
        return false;
    }

    asyncLoadCallback_ = callback;

    auto data = std::make_shared<AsyncLoadData>();
    data->resolvedSource = resolvedSource;
    data->width = width;
    data->height = height;
    data->decoder = decoder_;  // 转移所有权
    decoder_.Reset();          // 主线程不再持有，避免 SharedPtr refcount 数据竞争
    data->selfRef = data;      // 自引用保活
    asyncLoadData_ = data;

    auto* bgQueue = GetSubsystem<BackgroundWorkQueue>();
    asyncWorkItem_ = bgQueue->GetFreeItem();
    asyncWorkItem_->workFunction_ = AsyncLoadWorkFunction;
    asyncWorkItem_->aux_ = data.get();

    asyncLoading_ = true;
    bgQueue->AddWorkItem(asyncWorkItem_);
    return true;
}
```

#### 后台 Work Function

静态函数，不访问 VideoPlayer 成员，只通过 `AsyncLoadData*` 操作：

```cpp
void VideoPlayer::AsyncLoadWorkFunction(const WorkItem* item, unsigned threadIndex)
{
    auto* data = static_cast<AsyncLoadData*>(item->aux_);
    if (data->cancelled) { data->completed = true; data->selfRef.reset(); return; }

    data->success = data->decoder->Open(data->resolvedSource);
    data->completed = true;
    data->selfRef.reset();
}
```

#### 主线程 Finalize

`Update()` 每帧检查 `asyncLoadData_->completed`，成功时调 `FinalizeAsyncLoad()`：

```cpp
bool VideoPlayer::FinalizeAsyncLoad()
{
    decoder_ = asyncLoadData_->decoder;   // 接收 decoder 所有权
    asyncLoadData_->decoder.Reset();

    bool success = FinalizeLoad(asyncLoadData_->width, asyncLoadData_->height);

    if (success && decodeThread_)
        decodeThread_->Start();           // 预缓冲帧数据

    asyncLoading_ = false;

    if (!success) decoder_.Reset();

    if (asyncLoadCallback_)
    {
        asyncLoadCallback_(success);
        asyncLoadCallback_ = nullptr;
    }

    // 延迟播放
    if (success && pendingPlay_)
    {
        pendingPlay_ = false;
        Play();
    }
    return success;
}
```

#### 取消异步加载

非阻塞取消，`std::shared_ptr` 原子引用计数保证跨线程 reset 安全：

```cpp
void VideoPlayer::CancelAsyncLoad()
{
    if (!asyncLoading_) return;
    if (asyncLoadData_) asyncLoadData_->cancelled = true;
    asyncLoading_ = false;
    pendingPlay_ = false;
    asyncLoadData_.reset();
    asyncWorkItem_.Reset();
    asyncLoadCallback_ = nullptr;
}
```

### 14.4 Play() 延迟播放

异步加载期间调 `Play()` 不阻塞，设 `pendingPlay_` 标志，`FinalizeAsyncLoad` 成功后自动播放：

```cpp
void VideoPlayer::Play()
{
    if (asyncLoading_)
    {
        pendingPlay_ = true;
        return;
    }
    // ... 原有 Play 逻辑 ...
}
```

### 14.5 析构安全性

`AsyncLoadWorkFunction` 是静态函数，只通过 `AsyncLoadData*` 操作，**不访问 VideoPlayer 成员**。析构时 `CancelAsyncLoad()` 非阻塞释放引用，后台任务通过 `selfRef` 自行清理。

```
VideoPlayer 析构 → CancelAsyncLoad():
  1. asyncLoadData_->cancelled = true
  2. asyncLoadData_.reset()      ← 非阻塞
  3. asyncWorkItem_.Reset()

后台任务继续执行 → 只访问 AsyncLoadData（selfRef 保活）
  → 任务结束 → selfRef.reset() → AsyncLoadData 析构 → decoder 释放
  → 全程无 VideoPlayer 成员访问，安全 ✓
```

### 14.6 各平台实现细节

| 平台 | 说明 |
|------|------|
| **FFmpeg** | API 线程安全，无需特殊处理。`Open()` 内部已启动 `PacketReadThread`，完成后 packet 队列已在填充 |
| **Android** | NDK API 线程安全；`SDL_AndroidGetJNIEnv()` 自动处理 JNI `AttachCurrentThread` |
| **iOS** | 复用现有同步 `Open()`（semaphore 阻塞发生在工作线程），后续可优化为原生异步 |
| **WASM** | `AsyncLoad()` 直接转发 `Load()`（浏览器天然异步），`Update()` 中检测 `IsReady()` 触发回调 |

### 14.7 `IsReady()` 语义

```cpp
bool VideoPlayer::IsReady() const
{
    if (asyncLoading_)
        return false;
    return decoder_ && decoder_->IsOpen();
}
```

### 14.8 状态机

```
                    AsyncLoad()
    IDLE ──────────────────────────► ASYNC_LOADING
     │                                    │
     │ Load()                             │ 工作线程完成
     │ (同步)                             ▼
     │                              ASYNC_COMPLETE
     │                                    │
     │                                    │ FinalizeAsyncLoad() (主线程 Update)
     ▼                                    ▼
   LOADED ◄───────────────────────── LOADED
     │
     │ Play()
     ▼
   PLAYING ──► PAUSED ──► PLAYING
     │
     ▼
   ENDED / STOPPED
```

### 14.9 边界情况

| 场景 | 处理方式 |
|------|---------|
| 重复调用 `AsyncLoad` | `PrepareLoad` 入口调 `CancelAsyncLoad()` 取消前一个 |
| `AsyncLoad` 期间调 `Load` | `PrepareLoad` 入口调 `CancelAsyncLoad()` |
| `AsyncLoad` 期间调 `Play` | 设 `pendingPlay_`，不阻塞，完成后自动播放 |
| `AsyncLoad` 失败 | `Update()` 检测到 `success=false`，触发 `callback(false)` |
| 析构时仍在异步加载 | `CancelAsyncLoad()` 非阻塞，后台任务通过 `selfRef` 自行清理 |
| `AsyncLoad` 期间调 `SetVolume/SetMuted/SetLoop` | 正常生效：值存在成员变量，`FinalizeLoad` 创建 `audioSource_` 时使用 |

### 14.10 Lua 回调实现

通过自定义 tolua 绑定，将 Lua 函数包装为 `AsyncLoadCallback`（`std::function<void(bool)>`）：

- `WeakPtr<LuaScript>` 跟踪 `lua_State` 生命周期，避免 use-after-free
- `SharedPtr<LuaFunction>` 持有 Lua 函数 registry 引用，防止 GC 回收
- 模式与 `DownloadManager.pkg` 一致

### 14.11 Lua Widget 层集成

`urhox-libs/Video/VideoPlayer.lua` 的 `LoadVideo()` 使用 `AsyncLoad` 替代 `Load`。

`UIGuard.lua` 提供兜底：旧引擎没有 `AsyncLoad` 时，自动构造同步包装版本。

### 14.12 文件改动清单

| 文件 | 改动内容 |
|------|---------|
| `VideoPlayer.h` | 新增 `AsyncLoadCallback`、`AsyncLoadData`、`AsyncLoad()`、`IsAsyncLoading()`、`CancelAsyncLoad()` 等 |
| `VideoPlayer.cpp` | 拆分 `Load()` 为 `PrepareLoad()`+`FinalizeLoad()`；实现 `AsyncLoad`/`FinalizeAsyncLoad`/`CancelAsyncLoad`；修改 `Play()`/`Update()`/析构函数 |
| `VideoPlayer.pkg` | 新增 `AsyncLoad`、`IsAsyncLoading` 绑定（含 Lua callback 支持） |
| `VideoPlayer.lua` | `LoadVideo()` 改用 `AsyncLoad` |
| `UIGuard.lua` | `AsyncLoad` 兜底（旧引擎兼容） |

### 14.13 后续优化（可选）

1. **FFmpeg interrupt_callback**：检查 `cancelled` 标志实现 `Open()` 可中断退出
2. **iOS 原生异步**：去掉 semaphore，用 AVFoundation completion handler
3. **预缓冲控制**：暴露 `SetPrewarmFrameCount(unsigned count)` 控制预缓冲帧数

---

*文档创建: 2026-01-29*
*AsyncLoad 章节: 2026-03-19*
