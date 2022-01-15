# Unity 入门笔记 - 07

> 前言：入门笔记的最后一篇。这个系列教程看完了。接下来有空就看例子项目，动手做点东西。



# 一、主菜单

> 第二十五讲：《[Unity教程2D入门:25 主菜单MainMenu (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 主菜单的界面和关卡一样，属于新建一个场景。该场景中只有UI画布`Canvas`。使用的背景图是之前学对话框中用到的蒙板`Panl`。
- **注意**！！！！创建了画布`Canvas`后，会自动创建另一个游戏对象`EventSystem`。之前我还不知道是什么，删除了也没什么影响。后来我知道这个是给UI事件用的，比如检测鼠标、按钮点击之类的。《[UI创建的Canvas 和 EventSystem 是什么_hu1262340436的博客-CSDN博客](https://blog.csdn.net/hu1262340436/article/details/115656001)》

- **注意**：蒙板`Panl`默认情况下是**圆角矩形的图案**，不希望的话，在组件`Image`中删除`源图像`栏内容。可以点击浏览，最上方的第一个就是`None`无，也可以直接按`DEL`键删除。又或者，你自己有想要设计的背景图，也可以拖拽放置这里。记得修改颜色和透明度，纯白和透明才会显示背景图。

> 教程中创建两个蒙板`Panl`，一个背景图，一个覆盖上面的半透明纯色。大概是为了复习/演示为蒙板`Panl`添加渐变动画的操作（记住添加动画后取消**动画文件**的**循环时间**选项，这个之前也提到过）。还有复习了动画事件，让渐变后才显示UI。

> **注意**：教程中提到了`TextMeshPro`插件，该插件在2019版本中已经集成在项目里了，不需要再额外安装。只能在软件包窗口搜索到，网页商店没有了。

- 在画布`Canvas`中创建按钮、文本等。制作自己喜欢的主界面UI。按钮可以设置不同状态的颜色等。
- **重点**：比较重要的是按钮的事件响应，当按钮被按下时怎么调用函数。在按钮对象的组件`Button`下方一个空列表中点击`+`号，然后拖拽带有脚本的游戏对象，然后选择该游戏对象所含的方法。

```c#
using UnityEngine.SceneManagement; // 场景包

public class MainMenu : MonoBehaviour
{
	
    // Start is called before the first frame update
    void Start() 
    {
		GameObject.Find("Canvas/MainMenu/UI").SetActive(false); // 一开始设置关闭UI
    }
	
	public void PlayGame()
	{
		SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 1); // 开始游戏调用，切换场景。
	}
	
	public void QuitGame()
	{
		Application.Quit(); // 按钮调用退出游戏
	}
	
	public void UIEnable()
	{
		GameObject.Find("Canvas/MainMenu/UI").SetActive(true); // 在动画事件中调用，打开UI
	}
}
```

- unity对场景编号的修改非常奇葩，是打开`文件-生成设置`窗口，然后拖拽场景到窗口内，修改排序就可以修改编号。



# 二、暂停菜单

> 第二十六讲：《[Unity教程2D入门:26 暂停菜单 AudioMixer (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 这一讲的重点是暂停菜单中的音量控制，而暂停菜单按钮和返回菜单按钮都是已经学过的。做法和主页面类似，而菜单则和对话框类似。

```c#
public GameObject pauseMenu; // 创建游戏对象，用于赋值菜单对象

// Start is called before the first frame update
void Start()
{
	pauseMenu.SetActive(false); // 开始时关闭菜单
}

public void PauseGame() // 暂停游戏按钮调用，
{
    pauseMenu.SetActive(true); // 弹出菜单
    Time.timeScale = 0f; // 游戏运行时间系数为0
}

public void PauseOFF() // 返回游戏函数调用
{
    pauseMenu.SetActive(false); // 关闭菜单
    Time.timeScale = 1f; // 类似上
}
```

- 快速做完暂停菜单的其他部分，剩下音量控制来细讲。

> 1. 在项目窗口右键创建`音频混合器（AudioMixer）`，注意这个文件有个小箭头可以展开，里面包含了两样东西：`Master`、`Snapshot`。包括本体`AudioMixer`，三者都可以点击后在检查器窗口查看可编辑属性。
> 2. 在菜单栏选择`Window-音频-音频混合器`，打开音频混合器窗口。在其中可以选择（本体）混合器`AudioMixer`然后弹出所含的：组`Master`、快照`Snapshot`，都可以在其中选择。**重点关注**：组`Master`。它就是对应印象中的修改音量大小的组件。
> 3. 选择要关联的音频组件，在其`输出`栏中选择刚创建的音频混合器，也可以拖拽文件。
> 4. 音频混合器中的参数不可以直接更改，要手动设置。在需要改的参数上右键选择“暴露参数”（中文大意）。这时在音频混合器**窗口**的右上角就会显示`Exposed Parameters(1)`代表暴露参数为1个，可以被外部修改。还可以自定义其暴露的名字。
>
> - 剩下要做的就是关联滑动条和音频混合器。看下面代码。

```c#
using UnityEngine.Audio; // 需要添加的库

public AudioMixer audio0; // 需要创建承载音频混合器的对象

public void SetVolume(float Value) // 类似按钮，在滑动条内调用的函数。注意有个参数
{
	audio0.SetFloat("MainVolume", Value); // 关联音频混合器中的指定参数和滑动条中的变化参数。
}
```

- 最后需要注意的就是在滑动条中选择调用函数时，有两栏函数，一部分是带参数的。注意是选择上面一栏中的函数。上面的代表关联参数，下面的代表手动设置参数。



# 三、手机控制|触控操作|真机测试

> 第二十七讲：《[Unity教程2D入门:27手机控制|触控操作|真机测试(多P视频) (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- unity本身支持多平台，包括安卓、苹果、pc、mac、linux等。所以不同平台之间的转换只需要更改虚拟按键的输入方式即可。pc是键盘、安卓就是摇杆之类的。**注意**：鼠标点触类、滑动条等操作是安卓pc通用的，不需要修改。

- 要实现手机端的操作需要安装安卓环境，毕竟麻烦。

> 1. 安装`Android Build Support`：可以在`Unity Hub`的安装界面内安装，使用添加模块的方法安装。
>
> 2. 切换unity的安卓环境：在菜单栏点击`文件-生成设置-平台-Android-切换`，如果没安装会提示先安装。
> 3. 安装`Android SDK`：教程推荐的方法是通过`Android Studio`安装……`Android Studio`类似`Unity Hub`，只是Android的管理器，安装完毕后还需要另外安装`Android SDK`，还包含了IDE，~~感觉不需要的东西增加了~~。注意默认是c盘……
> 4. 为unity添加`Android SDK`路径：在菜单栏点击`Edit-首选项-外部工具-Android SDK Tools`，取消勾选。点击`Browse`，会自动锁定安装位置。注意，该界面下还有JDK、NDK等，暂不用到，无须在意。
> 5. 安装`unity remote 5 apk`手机应用：自行搜索下载。注意手机要设置为开发者模式，允许usb调试。《[Unity Remote - Unity 手册](https://docs.unity.cn/cn/2020.3/Manual/UnityRemote5.html)》
> 6. 修改unity的操作方式：在菜单栏点击`Edit-项目设置-编辑器-设备-Any Android Device`。**注意**！！！选择`Any Android Device`后就会同步手机调试，可以手机触屏控制，且无视pc键盘输入。如果选择`None`，就和之前一样，手机不会同步显示，可以pc键盘输入。
>
> - 第六步和教程有点不太一样，安卓不会显示型号，直接选择`Any Android Device`即可。

- 下面是我用到的资源下载地址。

> 1. [M_Studio](https://space.bilibili.com/370283072)：需要安卓环境的，请在这里下载Android Studio。链接: https://pan.baidu.com/s/1UOmMyr8VIzvOjUKtKvivag 提取码: r8pd
> 2. [unity remote 5官方下载-unity remote 5 apk下载v3.0 安卓版-当易网 (downyi.com)](http://www.downyi.com/downinfo/261880.html)

- 至此才完成了unity安卓环境的配置。开始制作手机摇杆控制。

> 1. 摇杆需要额外插件，要在资源商店里下载，注意，不是软件包商店。教程介绍的插件名字为`Joystick Pack`，属于免费。
> 2. 在插件目录的`Prefabs`文件夹下的`Variable Joystick`，就是需要的摇杆预设。注意，这些都属于`UI`类的东西，所以都放在画布`Canvas`下。有些可以修改的参数，自行设置。
>
> - 为了增加游戏设置的灵活性，我增加了一个UI部件——`Toggle`，就是一个打勾开关，用于切换是否显示虚拟摇杆（包含代码的使用）。具体使用方法参考：《[Unity UGUI（六）Toggle（开关/切换）_JPF29-CSDN博客](https://blog.csdn.net/NCZ9_/article/details/86307566)》。
>
> 3. 剩下的就是代码的事情了。

```c#
public GameObject Joystick_0; // 获取摇杆对象，
public Toggle toggle_0; // 获取开关对象，

// Update is called once per frame
void Update()
{
    if (toggle_0.isOn == true) // 读取开关属性
    {
    	Joystick_0.SetActive(true); // 直接使能摇杆，下面反之
    }
    else if (toggle_0.isOn == false)
    {
    	Joystick_0.SetActive(false);
    }
}	
```

- 上面是打勾开关的相关代码。

```c#
public Joystick Joystick_0; // 获取摇杆对象
public Toggle toggle_0; // 获取开关对象
	
... /* 左右移动 */

if (toggle_0.isOn == false) // 如果关闭摇杆，就是原来的键盘输入代码
{
	num = Input.GetAxis("Horizontal"); // 获取键盘
}
else if (toggle_0.isOn == true) // 如果是开启摇杆，就是获取摇杆输入
{
	num = Joystick_0.Horizontal; // 注意输入是浮点型，范围是-1~1.
}

.../* 起跳下蹲 */

if (toggle_0.isOn == false)
{
    num = Input.GetAxisRaw("Vertical");	 // 获取整数-1、1
}
else if (toggle_0.isOn == true)
{
    num = Joystick_0.Vertical; // 获取-1~1
}
```

- 上面是角色移动的相关代码。比较多和散，起始就是加了一个if判断。注意别混淆写错即可。
- 顺利完成，就是同步到手机的界面有点畸形……~~我没出现教程的移动bug，毕竟我之前的代码都和他不一样~~。

> 一个有趣的事情，如果不勾选`Any Android Device`，就不会同步手机，不会无视键盘输入。但开启虚拟摇杆还是可以用的。有趣。



# 四、单向平台

> 第二十八讲：《[Unity教程2D入门:28 二段跳 & 单向平台 (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 这一讲视频包含二段跳和单向平台跳跃的介绍。二段跳就是程序上的bug修复和完善，我并没有这个问题，所以跳过。直接关注新功能：单向平台。

- 单向平台，就是下面上去可以，上面下来不行，在2D游戏中常见。这个功能在untiy实现起始就是一个组件`Platform Effector 2D` - 2D平台效果。

> 1. 需要新创建一个瓦片地图，区分地面的平台。同样添加组件`Tilemap Collider 2D` - 瓦片地图碰撞器2D。并使用平铺调色板绘制平台。
> 2. 再添加`Platform Effector 2D`组件，就能看到提示效果——朝上的半圆扇形，表示只能从这个范围碰撞，其他范围不算。（打开`Gizmos`开关）
> 3. 组件中有2个选项要更改，组件`Tilemap Collider 2D` 勾选“由效果器使用”，组件`Platform Effector 2D`取消勾选“使用碰撞器遮罩”。完成。

- 默认表面弧度180，代表如果侧面走过去还是会被碰撞。注意修改跳跃高度（重力、速度等），使角色能跳上平台查看效果……



# 五、静态类

> 第二十九讲：《[Unity教程2D入门:29音效管理SoundManager (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 这一讲实现了音效管理，其实就是创建一个空的对象存储堆在角色对象下的音效。教程主要是想讲述静态类的使用。这应该是C#的语法。

```c#
public class bgm : MonoBehaviour // 类名字
{
    public static bgm instance; // 创建静态类
	
	public AudioSource audio_0; // 音频组件
	
	[SerializeField] // unity独有的关键字，在界面显示私有化变量
	private AudioClip jumpAudio, hurtAudio; // 音乐文件，不希望其他文件能访问，所以设置关键字private

    private void Awake() // 在游戏开始时
    {
        instance = this; // 创建本身的实例
    }
	
	public void JumpAudio() // 外部调用的方法
	{
		audio_0.clip = jumpAudio; // 替换音频
		audio_0.Play(); // 开始播放
	}
	
	public void HurtAudio() // 类似上
	{
		audio_0.clip = hurtAudio;
		audio_0.Play();
	}
}
```

- *这种方法只用一个音频组件，所以同一时间只能播放一个音频*……

> 1. `[SerializeField]`，强制 Unity 对私有字段进行序列化。《[UnityEngine.SerializeField - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/SerializeField.html)》
> 2. `Awake()`，这个函数在手册里找到几个同名不同类的。作用类似，是指一开始调用。《[EditorWindow-Awake - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/EditorWindow.Awake.html)》

```c#
... // 旧方法
enemy enemy_eagle = collision.gameObject.GetComponent<enemy>(); // 创建实例
enemy_eagle.anim_del(); // 调用实例方法。
... // 新方法
bgm.instance.JumpAudio(); // 使用类中的静态变量调用类的方法。
```



# 六、生成游戏

> 第三十讲：《[Unity教程2D入门:30 End 游戏生成Build (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》终于，完结啦。不过才仅刚刚开始，路还很长。

- 教程中演示的是2018版本，和之后的版本（包括2019版）有点差别。主要是界面的位置变了，还有删除了一个启动游戏时的设置窗口。*想起来以前玩小游戏时时常会弹出这中设置窗口*。
- 点击菜单栏中的文件-生成设置，弹出窗口`Build Settings`。选择要生成的平台。
- 点击玩家设置，弹出窗口`Project Settings`，设置各种参数。主要是图标、分辨率和启动图像。
- 设置完成后在窗口`Build Settings`点击生成，选择文件夹，生成。就可以玩啦。

> 不过之前练习做的游戏太粗糙了，ui都有错位的……

- 接下来开始新的篇章。



# 重点推荐

- 《[Ruby's Adventure：2D 初学者 - Unity Learn](https://learn.unity.com/project/ruby-s-adventure-2d-chu-xue-zhe)》
- 《[【游戏开发】新人如何用unity做出第一个属于自己的游戏Demo_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1WK4y1a7Hq)》

