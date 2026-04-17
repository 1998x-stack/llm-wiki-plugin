# Audio Module

UrhoX Lua API - Audio Module

---

## Classes

- [Audio](#audio)
- [Sound](#sound)
- [SoundSource](#soundsource)
- [SoundSource3D](#soundsource3d)
- [SoundListener](#soundlistener)

---

**Inherits from**: Object

## Audio : Object


### Methods


- bool SetMode(int bufferLengthMSec, int mixRate, bool stereo, bool interpolation = true)
- bool Play()
- void Stop()
- void SetMasterGain(const String type, float gain)
- void PauseSoundType(const String type)
- void ResumeSoundType(const String type)
- void ResumeAll()
- void SetListener(SoundListener* listener)
- void StopSound(Sound* sound)
- unsigned GetSampleSize() const
- int GetMixRate() const
- bool GetInterpolation() const
- bool IsStereo() const
- bool IsPlaying() const
- bool IsInitialized() const
- bool HasMasterGain(const String type) const
- float GetMasterGain(const String type) const
- bool IsSoundTypePaused(const String type) const
- SoundListener* GetListener() const
- const PODVector<SoundSource*>& GetSoundSources() const
- void AddSoundSource(SoundSource* soundSource)
- void RemoveSoundSource(SoundSource* soundSource)
- void MixOutput(void* dest, unsigned samples)

### Properties


- unsigned sampleSize (readonly)
- int mixRate (readonly)
- bool interpolation (readonly)
- bool stereo (readonly)
- bool playing (readonly)
- bool initialized (readonly)
- SoundListener* listener



---

**Inherits from**: ResourceWithMetadata

## Sound : ResourceWithMetadata

Audio resource. Supports **WAV**, **OGG Vorbis**, **MP3** formats and raw PCM data.

> ✅ **Recommended**: use `cache:GetResource("Sound", "Sounds/file.ogg")` to load audio files. The engine auto-detects format by file extension (`.wav`, `.ogg`, `.mp3`).
>
> `LoadWav()` / `LoadOggVorbis()` / `LoadMp3()` / `LoadRaw()` are lower-level alternatives for manual loading.

### Methods


- Sound() (GC)
- Sound* new()
- void delete()
- bool LoadRaw(Deserializer& source)
- bool LoadWav(Deserializer& source)
- bool LoadOggVorbis(Deserializer& source)
- bool LoadMp3(Deserializer& source)
- bool LoadRaw(const String fileName)
- bool LoadWav(const String fileName)
- bool LoadOggVorbis(const String fileName)
- bool LoadMp3(const String fileName)
- void SetSize(unsigned dataSize)
- void SetData(const void* data, unsigned dataSize)
- void SetFormat(unsigned frequency, bool sixteenBit, bool stereo)
- void SetLooped(bool enable)
- void SetLoop(unsigned repeatOffset, unsigned endOffset)
- void FixInterpolation()
- float GetLength() const
- unsigned GetDataSize() const
- unsigned GetSampleSize() const
- float GetFrequency() const
- unsigned GetIntFrequency() const
- bool IsLooped() const
- bool IsSixteenBit() const
- bool IsStereo() const
- bool IsCompressed() const

### Properties


- float length (readonly)
- unsigned dataSize (readonly)
- unsigned sampleSize (readonly)
- float frequency (readonly)
- int intFrequency (readonly)
- bool looped
- bool sixteenBit (readonly)
- bool stereo (readonly)
- bool compressed (readonly)



---

**Inherits from**: Component

## SoundSource : Component


### Methods


- void Seek(float seekTime)
- void Play(Sound* sound)
- void Play(Sound* sound, float frequency)
- void Play(Sound* sound, float frequency, float gain)
- void Play(Sound* sound, float frequency, float gain, float panning)
- void Stop()
- void SetSoundType(const String type)
- void SetFrequency(float frequency)
- void SetGain(float gain)
- void SetAttenuation(float attenuation)
- void SetPanning(float panning)
- void SetAutoRemoveMode(AutoRemoveMode mode)
- Sound* GetSound() const
- String GetSoundType() const
- float GetTimePosition() const
- float GetFrequency() const
- float GetGain() const
- float GetAttenuation() const
- float GetPanning() const
- AutoRemoveMode GetAutoRemoveMode() const
- bool IsPlaying() const

### Properties


- Sound* sound (readonly)
- String soundType
- float timePosition (readonly)
- float frequency
- float gain
- float attenuation
- float panning
- AutoRemoveMode autoRemoveMode
- bool playing (readonly)



---

**Inherits from**: SoundSource

## SoundSource3D : SoundSource


### Methods


- void SetDistanceAttenuation(float nearDistance, float farDistance, float rolloffFactor)
- void SetAngleAttenuation(float innerAngle, float outerAngle)
- void SetNearDistance(float distance)
- void SetFarDistance(float distance)
- void SetInnerAngle(float angle)
- void SetOuterAngle(float angle)
- void SetRolloffFactor(float factor)
- void CalculateAttenuation()
- float GetNearDistance() const
- float GetFarDistance() const
- float GetInnerAngle() const
- float GetOuterAngle() const
- float RollAngleoffFactor() const

### Properties


- float nearDistance
- float farDistance
- float innerAngle
- float outerAngle
- float rolloffFactor



---

**Inherits from**: Component

## SoundListener : Component




---

