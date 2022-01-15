# Unity 3D项目 - 01 - 开始游戏主界面

## 一、常用代码

### 0.打印调试

- `Debug.Log()`；将消息记录到 Unity 控制台。《[Debug-Log - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Debug.Log.html)》

```c#
Debug.Log("测试代码：" + Welcome.color); // 测试代码
```

###  1.获取子对象组件

- `Transform.GetChild (int index)`；返回`Transform`索引位置处的变换子项。《[Transform-GetChild - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Transform.GetChild.html)》

```c#
// 通过本对象的transform组件获取子物体的transform组件，再获取子物体的其他组件？……
newGameBtn = transform.GetChild(1).GetComponent<Button>(); 
```

### 2.为按钮添加事件

- `UnityEvent.AddListener (Events.UnityAction call)`；向 `UnityEvent` 添加非持久性监听器。《[Events.UnityEvent-AddListener - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Events.UnityEvent.AddListener.html)》《[Unity3D的按钮添加事件有三种方式 - 神来钥匙-陈诗友 - 博客园 (cnblogs.com)](https://www.cnblogs.com/shenlaiyaoshi/p/8110440.html)》

```c#
// 为按钮添加触发事件（参数是函数名字，不是字符串！！）
escGameBtn.onClick.AddListener(QuitGame);
```

### 3.完成上一帧所用的时间

- `Time.deltaTime`；完成上一帧所用的时间（以秒为单位）（只读）。此属性提供当前帧和上一帧之间的时间。《[Time-deltaTime - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Time-deltaTime.html)》

```c#
FadeTime -= Time.deltaTime;							// 减去每帧运行时间
```

### 4.删除一个对象

- `Destroy()`；移除 GameObject、组件或资源。《[Object-Destroy - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Object.Destroy.html)》

```c#
Destroy(Welcome.gameObject);				// 通过组件变量，获取所属对象，然后删除对象
```

### 5.切换场景

- `SceneManager.LoadScene()`；按照参数中的名称或索引加载场景。《[SceneManagement.SceneManager-LoadScene - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/SceneManagement.SceneManager.LoadScene.html)》

```c#
SceneManager.LoadScene(1); 			// 填写场景的序号，在生成项目里修改
// SceneManager.LoadScene("填写场景的名字，字符串");
```

> **注意：**在大多数情况下，为了避免在加载时出现暂停或性能中断现象， 您应该使用此命令的异步版，即： [LoadSceneAsync](https://docs.unity.cn/cn/2019.4/ScriptReference/SceneManagement.SceneManager.LoadSceneAsync.html)。

### 6.退出游戏

- `Application.Quit()`；关闭正在运行的应用程序。**编辑器中会忽略** Application.Quit 调用。《[Application-Quit - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Application.Quit.html)》

```c#
Application.Quit(); 				// 退出游戏
```

### 7.修改颜色和透明度

- `color`；有颜色和透明度设置的组件都有这个属性，可以通过赋值修改颜色和透明度。《[unity更改文字透明度 - WalkingSnail - 博客园 (cnblogs.com)](https://www.cnblogs.com/WalkingSnail/p/12176739.html)》《[UnityEngine.Color - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Color.html)》

```c#
Welcome.color = new Color(0.4f, 0.8f, 0.4f, (float)(FadeTime/FadeTime_s)); 	
```



## 二、常用插件

- `Universal Render Pipeline`；通用渲染管线；《[Unity 升级项目到Urp（通用渲染管线）以及画面后处理_xinzhilinger的博客-CSDN博客_unity升级urp](https://blog.csdn.net/xinzhilinger/article/details/115189246)》



##  三、文字版步骤

1. 新建项目；
2. 寻找合适且免费的场景资源；
3. 安装插件Urp（通用渲染管线）；
4. 导入刚找到的场景资源；

> 记得转换素材文件为Urp；

5. 导入天空盒资源（提前找好的合适且免费资源）；

6. 创建Urp文件；

> 记得设置阴影距离；

7. 创建灯光文件；

8. 设置天空盒文件；

9. 设置Urp文件；

10. 创建新场景；

11. 打包拷贝场景资源；

12. 设置镜头位置（Ctrl+Shift+F）；

13. 设置雾的参数；

14. 创建UI画布，设置参数；

> 记得设置跟随窗口大小；

15. 设置灯光参数；

16. 导入TMP插件且创建标题文本；

17. 创建署名信息文本；

18.创建开始游戏按钮且保存为预设；

19. 创建退出游戏按钮；
20. 将署名信息也改成按钮（个人喜好）；
21. 为画布添加脚本文件，开始编程；
22. 设置场景文件的序号；
23. 完成。



## 四、视频版步骤

- 《[Unity 3D项目 - 01 - 开始游戏主界面_哔哩哔哩_bilibili](https://www.bilibili.com/video/bv1Y44y1Y7xC)》



## 五、推荐

- 场景素材（unity商店-免费）：RPG Poly Pack - Lite
-  天空盒素材（unity商店-免费）：FREE Skybox Extended Shader
- unity教程（bilibili-免费）：《[Unity官方游戏开发认证教程：3D RPG系列课程介绍(Unity2020)｜Unity中文课堂 (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=211995&desc=1&spm_id_from=333.999.0.0)》

