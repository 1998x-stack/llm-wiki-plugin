---
summary: "Notes on Android BGFX compilation issues, shader path problems, and workarounds"
last_updated: "2026-04-02"
---

编译：
遇到的主要问题是urho的cmake里指定link的库，会被无视掉，在UrhoCommon.cmake里会被替换成指定的宏，然后这些宏不知道在哪里被重置了
最后实在没找到什么好办法，只好在UrhoCommon.cmake里link了这些库（我记得好像只有ABSOLUTE_PATH_LIBS可以写进去，LIBS可能也不行，因为库文件目录好像写不进去），
这样会导致所有编译的target都会去link这些库，不过好像也没什么太大影响。。
其他的问题都是些诸如头文件或者目录之类的小问题，以及编译器的标准不太一样。还有就是要去掉URHO3D_OPENGL宏，这个宏是在UrhoCommon.cmake被写入的


shader相关：
shader编译遇到的最大的问题是路径问题，urho在安卓上会把shader都放在一个叫/APK的虚拟路径下，这个路径是由安卓JNI管理的，bgfx是读不到的，会导致include不到文件
一开始是尝试在外面直接展开include，后来发现bgfx需要每个shader都要有一个"varying_scenepass.def.sc"，只好作罢。
最后改成了程序开始时把shader从/apk下面拷贝到我们能访问到的路径。拷贝过程中用到的urho中有关/apk的函数，表现的也都不太对，可能没有人用过，就也改掉了。
其中有一个函数FileSystem::DirExists是用来判断某个字符串是不是路径的，因为这个路径是虚拟的，不能用linux接口，我改成了判断里面有没有子文件，这样的话会对空文件夹进行误判，不过也想到什么好办法。。
还有就是安卓的shader编译时不允许int和float的隐式类型转换，以及fgets在windows下会去除\r。安卓时不会，这个我在fcpp里加了这段逻辑。
还有就是bgfx会用一个glsl-optimizer来优化shader，这个东西把shader里的float改成低精度的了，导致了骨骼读取异常引起的画不出来问题
还有就是资源大小写问题，目前shader都是在程序外通过CommandTool预处理成了小写的路径，程序内我在fcpp里把include的也都改成了小写，可能服务器资源里也有一些大小写问题

SDL相关：
SDL和bgfx都会去创建egl资源，本来是想都用bgfx来做的，后来发现不行，安卓自己封装了一套SurfaceView的东西来管理surface，遇到一些事件会发消息过来，这些消息必须要处理
SDL是封装了SurfaceView的，bgfx没有，所以现在就让bgfx去用sdl传过来的window handle创建surface，创建完之后再塞给SDL，SDL触发OnRestore（）的时候，bgfx执行resize，重新创建surface 
https://developer.android.com/guide/components/activities/activity-lifecycle 这一篇文章是介绍安卓的activity生命周期的
我们的游戏就是一个activity，在切到游戏外之后，执行onStop（），此时系统可以在任何时候杀掉这个app，拿回运存，且不调用任何析构函数。如果你再切回去，它会执行onCreate（）重新初始化
问题在于，系统并没有能够清理掉我们C++的static变量以及堆内存，会导致状态错误以及内存泄漏等等一系列问题。
我现在是在onCreate（）的时候判断一下，是不是第一次onCreate（），如果不是，就调用Destroy（）析构掉我们的对象，再重新初始化。静态变量也顺便重置掉
不过我也不太清楚我们程序里到底有多少static变量，我这里只是把会引起闪退的几个static变量改掉了，可能还有一些别的static变量没能够清理


