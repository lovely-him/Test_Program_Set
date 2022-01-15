# Unity 入门笔记 - 03

> 前言：前面两篇完成了游戏的大概界面和基本动作动画。接下来完善游戏其他内容。



# 一、镜头跟随

> 第九讲：《[Unity教程2D入门:09 镜头控制Cinemachine (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 镜头跟随有两种方式，一种是简单粗暴的移动摄像头，另一种是使用插件。
- 移动摄像头的方法就是修改`Main Camera`对象的坐标，在组件中添加脚本文件，读取角色的坐标，同时将坐标复制给摄像头。这样就能做到镜头始终跟随角色。这种方法比较简单，直接上代码。

```c#
public Transform player; // 创建对象，用于赋值角色的坐标。在unity界面中拖拽赋值。

void Update()
{
    // 参考角色平移的代码，直接平移摄像头。z轴保持-10，y轴采用缩小的数值防止剧烈抖动，也可为0。
	transform.position = new Vector3(player.position.x, player.position.y / 2, -10f);
}
```

> **注意**，这里修改的是`transform.position`属性，而不是`transform.velocity`属性，代表的是坐标，而不是速度。

- 另一种方法，使用插件。选择`Window-Package Manager`打开包下载页面，搜索`Cinemachine`插件，点击下载后，菜单栏就会多一个`Cinemachine`选项。点击子菜单中的`Create 2D Camera`选项，添加2D摄像头。（记得先选中`Main Camera`对象？）

> 注意，创建`Create 2D Camera`后需要设置相机的跟随目标，忘记为什么第一次弄时不用了？《[使用Cinemachine实现2D游戏的相机控制 - 简书 (jianshu.com)](https://www.jianshu.com/p/f9f7a3a58d8c)》

- 这个插件添加后，会替换`Main Camera`对象的部分参数。直接运行看效果就能发现有跟随效果了，很方便。还可以通过修改参数拉动滑块，调整跟随速度和范围等设置。
- 教程中提到，要防止镜头跳出可以用的方法。不过我跟着做后效果不太一样。（~~因为懒得截图，下面的描述逐渐胡言乱语~~）

> 1. 在新创建的`CM vcam1`对象中的`CinemachineVirtualCame`组件的最下面的`Add Extension`选项中选择`Cinemachine Confiner`组件添加。注意，并非是`添加组件`选项，而是`Add Extension`选项。
> 2. `Cinemachine Confiner`组件可以防止跟随镜头离开规定区域。这个规定区域为`Polyaon Collider 2D`属性。在背景中添加该组件，然后框住背景全部即可。再将背景元素添加到`Cinemachine Confiner`组件中。
> 3. 另外，在修改地图前，先扩充一下背景，复制三份，拉长横向面积。再用一个`GameObject(游戏对象)`存储。（不是承载角色用的也是这个，别搞混了）在unity中，`GameObject(游戏对象)`貌似起到承载打包的作用。
> 4. 完成以上步骤，最后还需要将背景的`Polygon Collider 2D`组件的`Is Trigger（是触发器）`选项勾选上，代表忽略这个碰撞器的物理碰撞，只作为触发功能使用。

- ~~最后我的效果是只有跟随镜头的中心黄点没有离开设定的背景范围，下半个屏幕还是离开的背景。而教程视频中是完全不下落的。起初我以为背景的脚本组件的问题，但是我怎么改都没法实现一样的效果。挖坑~~。我重新做第二个关卡时发现又可以效果了，很奇怪。

> 疑惑，这里介绍了2种镜头跟随的效果，按道理来说只需要选择一种用就可以了。我看教程中前面写了脚本后没有注释就开始用了插件，也就是说两者是都用上了，但是好像没有起到冲突。可能也是因为摄像头的部分参数被跟随镜头组件替换了吧。我实测用了插件后那个跟随脚本要不要也不影响。

```
我现在一直有报错：Object reference not set to an instance of an object。和警告：NewBehaviourScript.collider hides inherited member Component.collider. Use the new keyword if hiding was intended.但是却又可以运行，强迫症要死啦
```



# 二、物品收集

> 第十讲：《[Unity教程2D入门:10 物品收集 & Perfabs (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 物品收集有两个知识点，一个是创建放置物品，一个是碰撞删除物品。以下是创建物品的步骤。

> 1. 创建放置物品，和创建角色站立类似。创建一个精灵对象，将宝石的第一帧赋予。然后创建循环动画。
>
> - 我发现可以快捷创建动画，不需要在对象中添加组件、创建动画器文件，创建动画。直接为对象创建动画即可自动补充完成前两个步骤。
>
> 2. 物品创建完成后还需要添加2D盒装碰撞器`Box Collider 2D`组件，用于被角色检测到碰撞。但是并不需要产生物理效果，所以勾选`是触发器`选项，在上一讲也用到了。
> 3. 最后还需要为物品对象更换一个新的标签，方便之后检测。

- 然后需要为角色对象添加代码。用于检测碰撞特定标签的物品后，将该物品直接删除。

```c#
// 注意有个形参，每次角色产生碰撞都会调用这个函数
private void OnTriggerEnter2D(Collider2D collision) 
{
    if(collision.tag == "cherry") 				// 判断碰撞的物品的标签是否符合
    {
        Destroy(collision.gameObject);			// 删除物品
        Cherry_num += 1;						// 创建一个变量，用于累加次数
        Debug.Log(Cherry_num);					// 打印返回这个次数，方便查看。
    }
}
```

- **注意**，代码层面这次并没有创建一个新的对象变量储存组件等，而是直接通过一个新的特定函数名执行所需功能。

- **额外知识**:

> 1. 可以将层级窗口中的游戏对象反向拖入项目窗口中保存，相当于存作预设，方便日后调用。
> 2. 丰富地图时需要用到`其他设置-排序图层`，这个设置是可以写中文的，unity也识别中文！！！（话说，unity中`图层`和`排序图层`，有什么区别？）



# 三、角色材质

> 第十一讲：《[Unity教程2D入门:11 物理材质&空中跳跃 (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 在默认不赋予碰撞体材质时，2个碰撞体相互摩擦会有摩擦力。导致角色会在墙边卡住。真实的物理引擎……
- 解决方法就是为上半身添加物理材质，把摩擦力改成零即可。下半身是圆形点接触就不用了。（个人理解）

> 1. 在项目窗口右键创建`物理材质2D`，然后修改第一个选项`Friction`摩擦力，值为0。然后拖拽文件到角色`Box Collider 2D`组件的材质中即可。



# 四、角色下蹲

> 同上一讲，只是提到，没说具体怎么做，交给学习者自行发挥。

- 模仿跳跃的步骤，读取按键，修改动画。前面这几步都还很熟系，但是后面有一步容易忽略的，就是修改碰撞体，如果下蹲后碰撞体没有跟着缩小，那下蹲也没有意义。
- 代码上，下蹲时需要注意只能在非跳的时候下蹲。所以我写了一个下蹲函数，然后在之前跳跃的函数内调用。实现在非跳的情况下检测跳跃或下蹲。

```c#
public BoxCollider2D boxcoll2d; // 创建新变量，用于赋予`Box Collider 2D`组件

// 读取S按键，改变角色动作，使角色下蹲。
void down_0()
{
    float num = 0;

    num = Input.GetAxisRaw("Vertical"); // 检测WS按键，返回1或-1

    if(num != 0)
    {
        animator_0.SetInteger("downing", (int)(num)); // 改变标志位
        boxcoll2d.size = new Vector2((float)(0.01), (float)(0.01)); // 修改碰撞体大小
        // Debug.Log(num);
    }
    else
    {
        animator_0.SetInteger("downing", (int)(num)); // 非下蹲时要确保标志位为0
        boxcoll2d.size = new Vector2((float)(0.9633), (float)(0.8512));	// 恢复大小
    }
}
```

- 这段代码有两个不好的地方，一直检测按键并修改标志位。练习没考虑那么多。还有，我通过修改碰撞体的大小达到可以下蹲走的效果。但是如果在下蹲到一半站起来，即使头顶有东西顶住。按理来说不可以的，评论区有挺多奇思妙想。然后学习可能有更好的方法。

> 1. `Vector2.Vector2()` 函数，《[C# Vector2_Barrett_的博客-CSDN博客_c# vector2](https://blog.csdn.net/Barrett_/article/details/111353133)》；上面代码加了强制类型转换，为了消除警告，unity貌似默认浮点数是双精度。
> 2. `BoxCollider2D.size()`函数，《[BoxCollider2D-size - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/BoxCollider2D-size.html)》；

