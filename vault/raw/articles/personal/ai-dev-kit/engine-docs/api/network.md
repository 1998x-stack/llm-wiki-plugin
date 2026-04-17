# Network Module

UrhoX Lua API - Network Module

---

## Classes

- [Network](#network)
- [Connection](#connection)
- [NetworkPriority](#networkpriority)
- [HttpManager](#httpmanager)
- [HttpClient](#httpclient)
- [HttpResponse](#httpresponse)
- [RemoteEvent](#remoteevent)

---

## Network



### Methods


- bool Connect(const String address, short port, Scene* scene)
- bool Connect(const String address, short port, Scene* scene, const VariantMap& identity)
- void Disconnect(int waitMSec = 0)
- bool StartServer(short port)
- void StopServer()
- void BroadcastMessage(int msgID, bool reliable, bool inOrder, const VectorBuffer& msg, unsigned contentID = 0)
- void BroadcastRemoteEvent(StringHash eventType, bool inOrder)
- void BroadcastRemoteEvent(StringHash eventType, bool inOrder, const VariantMap& eventData)
- void BroadcastRemoteEvent(const String eventType, bool inOrder)
- void BroadcastRemoteEvent(const String eventType, bool inOrder, const VariantMap& eventData)
- void BroadcastRemoteEvent(Scene* scene, StringHash eventType, bool inOrder)
- void BroadcastRemoteEvent(Scene* scene, StringHash eventType, bool inOrder, const VariantMap& eventData)
- void BroadcastRemoteEvent(Scene* scene, const String eventType, bool inOrder)
- void BroadcastRemoteEvent(Scene* scene, const String eventType, bool inOrder, const VariantMap& eventData)
- void BroadcastRemoteEvent(Node* node, StringHash eventType, bool inOrder)
- void BroadcastRemoteEvent(Node* node, StringHash eventType, bool inOrder, const VariantMap& eventData)
- void BroadcastRemoteEvent(Node* node, const String eventType, bool inOrder)
- void BroadcastRemoteEvent(Node* node, const String eventType, bool inOrder, const VariantMap& eventData)
- void SetUpdateFps(int fps)
- void SetSimulatedLatency(int ms)
- void SetSimulatedPacketLoss(float loss)
- void RegisterRemoteEvent(StringHash eventType)
- void RegisterRemoteEvent(const String eventType)
- void UnregisterRemoteEvent(StringHash eventType)
- void UnregisterRemoteEvent(const String eventType)
- void UnregisterAllRemoteEvents()
- void SetPackageCacheDir(const String path)
- void SendPackageToClients(Scene* scene, PackageFile* package)
- int GetUpdateFps() const
- int GetSimulatedLatency() const
- float GetSimulatedPacketLoss() const
- Connection* GetServerConnection() const
- bool IsServerRunning() const
- bool CheckRemoteEvent(StringHash eventType) const
- const String GetPackageCacheDir() const
- void StartNATClient()
- const String GetGUID() const
- void DiscoverHosts(unsigned port)
- void SetPassword(const String password)
- void SetDiscoveryBeacon(const VariantMap& data)
- void SetNATServerInfo(const String address, short port)
- void AttemptNATPunchtrough(const String guid, Scene* scene)
- void AttemptNATPunchtrough(const String guid, Scene* scene, const VariantMap& identity)

### Properties


- int updateFps
- int simulatedLatency
- float simulatedPacketLoss
- Connection* serverConnection (readonly)
- bool serverRunning (readonly)
- String packageCacheDir



---

**Inherits from**: Object

## Connection : Object


### Methods


- void SendMessage(int msgID, bool reliable, bool inOrder, const VectorBuffer& msg, unsigned contentID = 0)
- void SendRemoteEvent(StringHash eventType, bool inOrder)
- void SendRemoteEvent(StringHash eventType, bool inOrder, const VariantMap& eventData)
- void SendRemoteEvent(const String eventType, bool inOrder)
- void SendRemoteEvent(const String eventType, bool inOrder, const VariantMap& eventData)
- void SendRemoteEvent(Node* node, StringHash eventType, bool inOrder)
- void SendRemoteEvent(Node* node, StringHash eventType, bool inOrder, const VariantMap& eventData)
- void SendRemoteEvent(Node* node, const String eventType, bool inOrder)
- void SendRemoteEvent(Node* node, const String eventType, bool inOrder, const VariantMap& eventData)
- void SetScene(Scene* newScene)
- void SetIdentity(const VariantMap& identity)
- void SetControls(const Controls& newControls)
- void SetPosition(const Vector3& position)
- void SetRotation(const Quaternion& rotation)
- void SetConnectPending(bool connectPending)
- void SetLogStatistics(bool enable)
- void Disconnect(int waitMSec = 0)
- void SendPackageToClient(PackageFile* package)
- VariantMap& GetIdentity()
- Scene* GetScene() const
- const Controls& GetControls() const
- char GetTimeStamp() const
- const Vector3& GetPosition() const
- const Quaternion& GetRotation() const
- bool IsClient() const
- bool IsConnected() const
- bool IsConnectPending() const
- bool IsSceneLoaded() const
- bool GetLogStatistics() const
- String GetAddress() const
- short GetPort() const
- float GetRoundTripTime() const
- float GetLastHeardTime() const
- float GetBytesInPerSec() const
- float GetBytesOutPerSec() const
- float GetPacketsInPerSec() const
- float GetPacketsOutPerSec() const
- String ToString() const
- unsigned GetNumDownloads() const
- const String GetDownloadName() const
- float GetDownloadProgress() const

### Properties


- VariantMap& identity
- Scene* scene
- Controls& controls
- char timeStamp (readonly)
- Vector3& position
- Quaternion& rotation
- bool client (readonly)
- bool connected (readonly)
- bool connectPending
- bool sceneLoaded (readonly)
- bool logStatistics
- String address (readonly)
- short port (readonly)
- float roundTripTime (readonly)
- float lastHeardTime (readonly)
- float bytesInPerSec (readonly)
- float bytesOutPerSec (readonly)
- float packetsInPerSec (readonly)
- float packetsOutPerSec (readonly)
- unsigned numDownloads (readonly)
- String downloadName (readonly)
- float downloadProgress (readonly)



---

**Inherits from**: Component

## NetworkPriority : Component


### Methods


- void SetBasePriority(float priority)
- void SetDistanceFactor(float factor)
- void SetMinPriority(float priority)
- void SetAlwaysUpdateOwner(bool enable)
- float GetBasePriority() const
- float GetDistanceFactor() const
- float GetMinPriority() const
- bool GetAlwaysUpdateOwner() const
- bool CheckUpdate(float distance, float accumulator)

### Properties


- float basePriority
- float distanceFactor
- float minPriority
- bool alwaysUpdateOwner




---

## HttpManager



### Methods


- HttpClient* Create()
- void CancelAllRequests()
- unsigned GetActiveRequestCount() const

### Properties


- unsigned activeRequestCount (readonly)



---

### Global Access

- HttpManager* GetHttp()
- HttpManager* http (readonly)

---

## HttpClient



### Enums

- HttpMethod: HTTP_GET, HTTP_POST, HTTP_PUT, HTTP_DELETE, HTTP_PATCH

### Methods


- HttpClient* SetUrl(const String& url)
- HttpClient* SetMethod(HttpMethod method)
- HttpClient* AddHeader(const String& key, const String& value)
- HttpClient* SetBody(const String& data)
- HttpClient* SetContentType(const String& contentType)
- HttpClient* SetTimeout(unsigned msecs)
- HttpClient* OnSuccess(function callback(client, response))
- HttpClient* OnError(function callback(client, statusCode, error))
- HttpClient* OnProgress(function callback(client, downloaded, total))
- void Send()
- void Cancel()



---

## HttpResponse



### Methods


- int GetStatusCode() const
- String GetStatusText() const
- bool IsSuccess() const
- String GetDataAsString() const
- String GetHeader(const String& name) const
- unsigned long long GetDownloadedBytes() const
- unsigned long long GetTotalBytes() const
- float GetProgress() const

### Properties


- int statusCode (readonly)
- String statusText (readonly)
- bool success (readonly)
- String dataAsString (readonly)
- unsigned long long downloadedBytes (readonly)
- unsigned long long totalBytes (readonly)
- float progress (readonly)



---

## RemoteEvent



### Properties


- unsigned senderID
- StringHash eventType
- VariantMap eventData
- bool inOrder



---

