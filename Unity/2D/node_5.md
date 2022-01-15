# Unity 入门笔记 - 06

> 前言：快结束了，已经过半了。坚持住。





# 一、下蹲

> 第二十讲：《[Unity教程2D入门:20 趴下效果Crouch (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》之前自己有尝试实现下蹲，但是并不完善，比如下蹲时还能跳跃，有东西挡住还能站起等。教程这期解决了这些问题。一起学习一下。

- 在那之前先补充一些遗漏的知识点。

> 1. `Time.deltaTime`，《[Time-deltaTime - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Time-deltaTime.html)》完成上一帧所用的时间（以秒为单位）（只读）。此属性提供当前帧和上一帧之间的时间。`float` 浮点型变量。
> 2. `Time.fixedDeltaTime`，《[Time-fixedDeltaTime - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Time-fixedDeltaTime.html)》执行物理和其他固定帧率更新（如 MonoBehaviour 的 [FixedUpdate](https://docs.unity.cn/cn/2019.4/ScriptReference/MonoBehaviour.FixedUpdate.html)）的时间间隔（以秒为单位）。
> 3. `MonoBehaviour.FixedUpdate()`，《[MonoBehaviour-FixedUpdate() - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/MonoBehaviour.FixedUpdate.html)》用于物理计算且独立于帧率的 [MonoBehaviour.FixedUpdate](https://docs.unity.cn/cn/2019.4/ScriptReference/MonoBehaviour.FixedUpdate.html) 消息。
> 4.  `MonoBehaviour.Update()`，《[MonoBehaviour-Update() - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/MonoBehaviour.Update.html)》如果启用了 `MonoBehaviour`，则每帧调用 `Update()`。在实现任何类型的游戏脚本时，`Update()` 都是最常用函数。 但并非所有 `MonoBehaviour` 脚本都需要 。
> 5. （1）搭配（4）使用，（2）搭配（3）使用。

> 1. `BoxCollider2D`，《[UnityEngine.BoxCollider2D - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/BoxCollider2D.html)》表示轴对齐的矩形的 2D 物理碰撞体。
> 2. `Collider2D`，《[UnityEngine.Collider2D - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Collider2D.html)》2D 游戏玩法使用的碰撞体类型的父类。
> 3. 其他碰撞体以此类推。
> 4. `Physics2D.OverlapCircle()`，《[Physics2D-OverlapCircle - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Physics2D.OverlapCircle.html)》检查某碰撞体是否位于一个圆形区域内。
> 5. `BoxCollider2D.center`，【已移除】《[BoxCollider2D-center - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/BoxCollider2D-center.html)》该碰撞体在本地空间中的中心点。*我还想用来着*……

- 下蹲时跳跃不会切换至起跳动画：没有建立动画过渡，建立后就解决了。因为标志位同时满足，会显示最终的动画。~~应该不会有闭环的bug吧~~。

- 下蹲时头顶有东西挡着还能起跳或站立：判断指定坐标的指定范围无其他碰撞体。指定的坐标使用空对象获取，参考怪物的左右移动。指定范围内的判断使用方法`Physics2D.OverlapCircle()`。
- ~~本来还想修改，起跳后不能移动，回来发现这样操作极其不流畅，然后就改回去了~~。
- 教程检测下蹲是使用检测按下和松开的瞬间，这样会有bug，导致不能松开时松开了，之后就不会触发了。所以我采用持续检测。



# 二、场景控制

> 第二十一讲：《[Unity教程2D入门:21 场景控制SceneManager (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 场景功能是使用unity的API方法，其中包括切换场景和重置场景。
- 重置场景的触发条件是新建碰撞体，放在地图外触发。不检测y轴判断的原因是游戏地形不规则。代码写在角色脚本中，和拾取物放一起。教程还用到延迟函数。

```c#
// 重新加载场景，参数为当前场景名字
void Restart() // 注意写在调用前面
{
    SceneManager.LoadScene(SceneManager.GetActiveScene().name);
}

if(collision.tag == "DeadLine")
{
    GetComponent<AudioSource>().enabled = false; // 禁用所用声音（背景音乐等就停止了）
    Invoke(nameof(Restart),1f); // 延时函数，注意，函数名要写字符串，为了通用使用nameof转换
}
```

> 1. `UnityEvent.Invoke()`，《[Events.UnityEvent-Invoke - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Events.UnityEvent.Invoke.html)》调用所有已注册的回调（运行时和持久性）。
> 2. `SceneManager.LoadScene()`，《[SceneManagement.SceneManager-LoadScene - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/SceneManagement.SceneManager.LoadScene.html)》按照 Build Settings 中的名称或索引加载场景。
> 3. `SceneManager.GetActiveScene()`，《[SceneManagement.SceneManager-GetActiveScene - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/SceneManagement.SceneManager.GetActiveScene.html)》获取当前活动的场景。然后再使用属性`name`获取当前场景的名字。

- 场景切换的脚本为另外新建。原本设想写在原本触发对话框的门框碰撞器脚本上，但是发现触发器碰撞函数调用不是持续的。而且为了通用，将脚本放在对话框里更加妙一点。因为对话框只有触发才会出现。

```c#
using UnityEngine.SceneManagement;

// Update is called once per frame
void Update() // 持续运行
{
    if (Input.GetKeyDown(KeyCode.E)) // 检测特定按键。
    {
        Debug.Log("你按下E了");
        // 切换场景，切换到指定的编号，获取当前编号，并加一
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 1);
    }
}
```

> 1. `SceneManager.LoadScene()`，和重置场景同一个函数。
> 2. `SceneManager.GetActiveScene()`，和重置场景同一个函数。获取场景编号。
> 3. `Input.GetKeyDown()`，《[Input-GetKeyDown - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Input.GetKeyDown.html)》在用户**开始**按下 `name` 标识的键的帧期间返回 true。

- 切换场景修改东西时记得同步预设和保存。注意，脚本文件名和脚本类名要一样！！



# 三、场景光效

> 第二十二讲：《[Unity教程2D入门:22 2D光效(ver. Unity2018) (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》这其实是使用3D光源实现的。
>
> 《[Unity2019.3最新Universal RP通用渲染管线使用指南(2D Light + Post processing)_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1t54y1d7DW)》这个是使用专门的创建实现的。

- *灯光效果不需要代码*，使用插件完成。我学习的是2019版的插件，也就是上面第二个视频链接。步骤比较繁琐，功能比较多，下面详细介绍。

## 1.准备插件

1. 在菜单栏选择`Window-Package Manager`选项，打开包管理窗口。搜索`Universal RP`插件，点击下载，等待完成。
2. 在项目窗口右键选择`创建 - 渲染 - Universal Render Pipeline - Pipeline Asset`选项，创建得到2个文件。（个人理解为）一个是“控制器”`Asset`，一个是“3D应用文件”`Renderer`。
3. 我们需要的是“2D应用文件”，项目窗口右键选择`创建 - 渲染 - Universal Render Pipeline - 2D Renderer`选项，创建文件。然后选择刚刚创建的“控制器”`Asset`，在渲染器列表中更换为创建的`2D Renderer`。
4. 在菜单栏选择`Edit - 项目设置`选项，打开`Project Settings`窗口。选择`图形`页面，在`可编写脚本的渲染管道设置`选择刚创建的“控制器”`Asset`文件。
5. 在菜单栏选择`Edit - Render Pipeline - Universal Render Pipeline - 2D Renderer ` 选项，里面有2个选项。一个是`...Scenes...`，为当前场景添加“插件渲染”；另一个是`...project...`，为整个工程所有场景添加“插件渲染”。添加过后就会全黑，然后就可以开始添加光源了。
6. *如果没有变黑请看这* ：所有需要渲染的对象都有一个`Sprite Renderer`组件，里面有一个材质选项。如果没有变黑表示选择不正确，点击打开选择窗口，选择正确的材质即可。

> 发现个重大事件，部分游戏对象创建时在材质栏找不到`Sprite-Lit-Default`材质，可以点击其他有的对象，会在项目窗口定位到`Sprite-Lit-Default`材质文件。然后直接拖拽就可以了……也就是说这个材质其实是大家通用的，不是每个单独的……

## 2.发散、遮罩、全范围、多边形灯光

- 完成`准备插件`的工作后，就可以在层级窗口创建灯光游戏对象。目前先介绍三个通俗易懂的，分别是`Point Light 2D`发散型灯光、`Sprite Light 2D`遮罩型灯光、`Global Light 2D`全范围灯光、`Freeform Light 2D`多边形灯光。
- 在**使用前请打开场景的左上角**的`Gizmos`开关，以便修改范围参数。这个开关在下蹲时查看碰撞器时也用过。

1. `Point Light 2D`，创建一个圆形的灯光，也可以修改角度，弄成扇形。还有各种过渡、颜色参数等。
2. `Sprite Light 2D`，创建一个需要遮罩图像的灯光，可以模拟阳光漫射的图案。还有各种过渡、颜色参数等。
3. `Global Light 2D`，创建一个全范围照亮的灯光，用来照亮整个场景。还有各种颜色参数等。
4. `Freeform Light 2D`，创建一个多边型的灯光，在没有遮罩图像时可以用来自定义图案的灯光。还有各种过渡、颜色参数等。

- 前三种灯光效果还有一个`Alpha Blend on Overlap`选项，代表和其他灯光效果融合。
- 如果**灯光没有效果**，那**可能作用图层没选对**！！！！！！在灯光组件内有一个`Target Sorting Layers`选项，选择“全部”作用。还可以选择在此基础上排除那些图层。

> ~~起初我还以为插件下载错了，又重新弄了一次~~。

## 3.法线贴图

- 为了使2D人物更加具有立体效果，为其添加法线贴图。

> 跳过，没有相关素材……

## 4.Volume

> 中文翻译离大谱，居然翻译是“音量”。完全想不到是和渲染图案有关的。

- 这个功能类似创建一个对象，然后再在对象里`Add Override`添加功能（**注意**，不是添加组件）。教程里快速介绍了光晕组件、黑影组件等。
- 创建了`Volume`对象后需要先选择`Profile`栏中的文件，一开始没有新建，自动创建在`Scenes`场景的文件夹下。
- **注意**，要先启用相机对象中的`渲染-Post Processing`选项。

- 介绍有：泛光效果`Bloom`、场景的畸变`Chromatic Aberration`、晕影效果`Vignette`，还有很多功能，可以自己一个个添加尝试修改参数。



# 四、视觉差

> 第二十三讲：《[Unity教程2D入门:23 优化代码Fix code (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》这个视频是解决移动不顺畅的问题，但是我没感觉有这个问题，而且我的代码本来就和教程不一样。所以就不实现了。主要是传达使用`FixedUpdate()`和`Update()`使用的结合。

> 第二十四讲：《[Unity教程2D入门:24 视觉差Parallax (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 视觉差，实现方法就是将前中后多个背景进行错落有致的跟随位移。使用代码读取摄像机坐标并乘于系数赋值给需要移动的背景即可。
- 需要注意的是，移动背景时，背景的多边形碰撞体组件`Polygon Collider 2D`也跟着一起移动，如果不希望如此，可以另起一个游戏对象保存这个组件。

```c#
public class middels : MonoBehaviour
{
	public Transform Cam; // 摄像机坐标对象
	public float moveRate; // 跟随系数
	
	private float startPoint; // 初始坐标
	
    // Start is called before the first frame update
    void Start()
    {
        startPoint = transform.position.x; // 获取坐标点
    }

    // Update is called once per frame
    void Update()
    {
		// 修改坐标点，非速度
        transform.position = new Vector2(startPoint + Cam.position.x * moveRate, transform.position.y);
    }
}
```

- 获取的摄像机坐标，可以赋值主摄像机`Main Camera`，也可以赋值插件摄像机`CM vcam`。因为他们的坐标是一样的，所以没区别。

> ~~场景还没内容，感觉移动了也不美~~……



