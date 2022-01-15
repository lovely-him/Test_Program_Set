# Unity 入门笔记 - 02

> 前言：上一篇笔记记录了从零开始安装软件，到搭建最基本的游戏场景和角色，最后开始接触了脚本代码。对unity游戏引擎的工作方式有了基本的认知。接下来开始进一步利用代码完善功能吧。



# 零、补充

> 对上一篇笔记的内容的补充。《[学习笔记：Unity控制台输出_逍遥乐平的博客-CSDN博客_unity控制台输出](https://blog.csdn.net/weixin_43908355/article/details/104289130)》。

- 我已经知道unity是使用脚本运行代码的，那脚本在运行时没有打印反馈信息太不方便了。为此，搜索了一下unity中控制台输出函数是`Debug.Log("***")`。

```c#
Debug.Log(num); // 通过这一行代码，查看Input.GetAxis("Horizontal")的返回值
```

> 根据打印信息，可以知道，每次按下会打印很多次，因为每一帧都会调用一次函数。而打印的是浮点数，如果长期按着就是`A`键就是`-1`，长期按着`D`键就是`1`。如果轻按就是小数。查看官方手册也得知这个函数是返回范围（-1,1），用于模拟摇杆的摇摆程度等。

- 另外，unity软件有个特点，每次脚本文件被修改都会自动读取编译。如果有错控制台就会提示警告或错误。那还要什么VS2019啊，占硬盘空间，使用Notepad或VS Code不香吗。



#  一、改变朝向&跳跃

> 第五讲：《[Unity教程2D入门:05 角色方向&跳跃_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV154411f7Pa)》；

- 在角色的坐标属性里，有一栏缩放，默认值都是1，如果将其改为-1则会有镜像效果。素材里的角色都是朝一个方向的，所以要改变方向就可以使用这个效果实现镜像功能。要实现左右镜像就是X轴改为-1。

- 和角色移动类似，编程读取按键然后修改方向即可。

```c#
void Movement_0() // 为了方便区别，换个函数封装
{
    float num = 0; // 同样弄个临时变量

    num = Input.GetAxisRaw("Horizontal"); // 读取按键输入，注意和上一回用的不一样

    if(num != 0)
    {
    	transform.localScale = new Vector3(num, 1, 1); // 修改坐标属性
        Debug.Log(num); // 打印读取到的信息
    }
}
```

- 代码知识点如下：

> 1. `Input.GetAxisRaw("Horizontal")`不同与`Input.GetAxis("Horizontal")`，是返回整数，所以只有-1、0、1三个数。通过打印函数也能在控制台看到效果。《[Input-GetAxisRaw - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Input.GetAxisRaw.html)》，其实左右移动其实也可以用这个函数。
> 2. `transform.localScale`属性不同于`rb.velocity`，`rb`对象还需要自己创建并赋值对应组件。而这次修改的是角色本身的坐标信息，所以不需要创建直接调用修改。（个人推测）《[Transform-localScale - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Transform-localScale.html)》
> 3. `Vector3()`类比`Vector2()`，作用类似。貌似都是不是unity的api，而是c#的内置api？
> 4. `Debug.Log()`打印运行信息。这个是unity的api，《[Debug-Log - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Debug.Log.html)》。

- 紧接着实现跳跃功能。和左右移动功能也是雷同，读取按键修改y轴坐标。

```c#
void Jump_0() // 重新打包一个函数
{
    bool num = false; // 这里使用布尔变量，同时赋值布尔类型。注意。

    num = Input.GetButtonDown("Jump"); // 读取空格按键，又是不一样的函数

    if(num)
    {
        rb.velocity = new Vector2(rb.velocity.x, speed); // 只修改y轴速度，这个函数是赋值速度的。
        Debug.Log(num); // 打印实际读取到的值
    }
}
```

- 代码知识点如下：

> 1. `Input.GetButtonDown("Jump")`读取空格的函数方法不一样，字符标识同样可以在项目设置里查看。而且这个函数返回的是布尔类型。c#对赋值类型似乎很严格，我使用浮点型临时变量接收时，unity会给我一个警告，所以代码第三行才会使用布尔变量，同时初始化也是布尔变量。
> 2. `Vector2()`，和左右移动用的一样，不过因为布尔变量不用乘于，跳跃肯定是向上的，所以只需要`speed`。
> 3. `Debug.Log()`打印信息时也能看到，num的值为True。

- 视频里还讲了一个确保移动速度不变的修改，防止帧率不同的影响游戏体验。不过这一知识点讨论挺大，很多人都说老师错了。因为`Vector2()`这个函数修改的是速度而不是距离，所以我这里暂不记录这个知识。

- 另外，跳跃可能会跳得很高，只需要修改刚体属性里的重力即可。视频里，老师是新创建一个速度作修改，我觉得也挺好。还发现另一个**问题**，可以一直按空格跳跃，在空中一直多段跳……



# 二、动画效果

> 第六讲：《[Unity教程2D入门:06 动画效果Animation (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》
>
> 角色移动时直接偏移，不生动可爱，需要添加站立和跑动的动画效果。

- 思路：为角色添加动画控制器组件，创建动画控制器文件，将文件添加组件中。在动画控制器中创建动画文件，添加素材。添加需要的切换效果，完成。
- 以下分步讲解：

> 1. 先在角色的检查器中点击添加组件，输入`（英文）Animator/（中文）动画器`。**注意**，输入英文的话不要输入成`Animation/动画`，我一开始就弄错了，估摸着怎么添加不了文件。*19版的图标和18版又不一样，更加迷惑了*。
> 2. 在项目内右键创建，`（英文）Animator Controller/（中文）动画控制器`，修改名字，整理存放位置，然后添加到组件中。
> 3. 在最上方的菜单栏中选择`Window-动画-动画`，英文版就是`Window-Animation-Animation`，我发现还可以在选项卡中，选择添加选项卡，也有动画一项。打开`动画选项卡`后，在层级选项卡中选中角色的文件，这时`动画选项卡`就会有创建动画的选项。
> - **注意**，不要选错或是没选，不然无法创建动画文件。在项目选项卡中也可以右键创建动画文件，但是我发现这二者好像不一样，可能是没关联？要选中需要添加动画的对象，再在动画选项卡中创建。这是重点。
>
> 4. 创建好动画文件后就可以添加素材，注意修改像素大小。然后拖拽拉长进度条，不然播放太快就鬼畜效果了。18版好像有采集帧设置，我在19版中没找到……
> 5. 动画文件也弄好后，打开动画器查看。可以从`Window-动画-动画器`打开，也可以点击之前创建的动画控制器文件，在检查器中有个打开选项，同样可以打开`动画器`窗口。
> 6. 因为动画控制器已经连接到角色的组件上，动画文件也是为角色创建的。所以在动画控制器上可以看到已经有之前创建的动画了，而且自动链接上了。毕竟目前只有一个动画文件。（个人理解）
> 7. 现在就算完成待机时的动画了，点击运行游戏。发现角色一直有动画效果。

- 只有一种动画效果肯定不行，需要设置几种来回切换，并设立切换条件。

> 1. 遵照上面的第3、4步为角色创建动画文件。在动画控制器中即可看见独立，还没有连接的动画效果。
> 2. 需要设置2种动画效果之间的来回切换，对它进行右键，选择创建过渡，指向另一个动画。另一个动画同理，做到互相过渡。
> 3. 设置过渡条件，unity支持使用参数来设置。在动画控制器的左边可以选择参数列表，旋转加号创建新的参数。教程里使用浮点数，采用大于小于的判断条件。我个人更加推崇整数判断，用等于或不等于判断。
> 4. 参数创建好，并选择过渡箭头，在检查器中修改过渡时间。如果不需要过渡时间就写0。然后就开始写代码。

- 类似创建刚体对象，创建一个动画器对象。注意，这里的变量名直接也使用小写的动画器，这样软件里就会自动显示动画器的翻译了。

```c#
public Animator animator;
```

- 然后寻找一个合适的地方修改参数。在上一节讲切换朝向时，使用的参数就是整数型的。很适合直接赋值。

```c#
void Movement_0()
{
    float num = 0; // 注意这个临时变量还是浮点型，如果给整型变量running赋值还需要强制转换。

    num = Input.GetAxisRaw("Horizontal");
    animator.SetInteger("running", (int)(num)); // 和之前的代码只有这里不一样，添加了一行
	// 如果不进行强制转换，unity软件会报错。百度搜了一下强制转换的方法
    
    if(num != 0)
    {
        transform.localScale = new Vector3(num, 1, 1);
        // Debug.Log(num);
    }
}
```

- 介绍用到的函数：

> 1. `animator.SetInteger()`,《[Animator-SetInteger - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Animator.SetInteger.html)》，和教程里的浮点数不一样。这个也是在官方API里找的。
> 2. `(int)(num)`，《[强制转换和类型转换 - C# 编程指南 | Microsoft Docs](https://docs.microsoft.com/zh-cn/dotnet/csharp/programming-guide/types/casting-and-type-conversions)》，c#中的强制类型转换貌似有几种方法，我试了一下这种可用。



#  三、跳跃动画

> 第七讲：《[Unity教程2D入门:07 跳跃动画 LayerMask (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 上一讲完成了站立与跑动的动画，这一讲继续完善跳跃的动画。跳跃分起跳和下落。根据上一讲的知识先快速创建2个角色的动画文件，然后关联起来。采用 “跑动和站立都可以起跳，下落后只会回到站立” 的方案。
- 剩下要考虑两个问题，采用什么方式检测上升顶点然后下落的切换过程，还有怎么检测下落到地面的过程。教程采用的方法是检测速度，如果起跳后且速度向下就代表下落，否者就是上升。还有检测碰撞，就可以检测下落到地面的过程。

> 在得知可以检测速度方向时，我想到，为什么落地不也用检测速度了。弹幕的一句提醒了我，如果在斜坡上。

- 知道要做什么后就开始写代码，教程里使用了两个布尔变量进行判断，我个人认为十分繁琐。对同一物体的不同状态切换，应该尽量减少多个标志位同时切换的现象。我采用一个整形标志位作判断，1代表跳跃起，2代表下落，0代表下落结束等待再次起跳。

```c#
// 读取空格按键，赋予角色速度，使角色竖直移动。
void Jump_0()
{
    int num = 0; 											// 使用整形

    num = animator.GetInteger("jumping"); 					// 读取标志位

    // 直接判断，省去布尔型变量
    // 代表未处于跳跃状态，可以跳跃
    if(num == 0 && Input.GetButtonDown("Jump")) 
    {
        rb.velocity = new Vector2(rb.velocity.x, speed); 	// 赋予向上速度
        animator.SetInteger("jumping", 1); 					// 改变标志位
        // Debug.Log(num);
    }
    // 代表正在向上跳跃状态
    // 判断是否有向下的速度
    else if(num == 1 && rb.velocity.y <= 0) 				// 保留等于0，防止bug
    {
        animator.SetInteger("jumping", 2); 					// 改变标志位
    }
    // 代表正在向下跳跃状态
    // 判断是否与图层进行碰撞
    else if(num == 2 && collider.IsTouchingLayers(ground)) 
    {
        animator.SetInteger("jumping", 0); 					// 改变标志位
    }
}
```

- 这里修改的是本章第一篇跳跃用到的代码。

> 1. 修改了之前的空中多段跳bug，现在只有标志位为0时才会再次检测跳跃。
> 2. 分三个阶段，每个阶段检测到对应条件就切换。

- 使用了2 个新函数。

> 1. `animator.GetInteger()`，读取整形参数，与设置参数相对。《[Animator-GetInteger - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Animator.GetInteger.html)》
> 2. `collider.IsTouchingLayers()`，官方解释：检查该碰撞体是否正在接触指定 `layerMask` 上的任何碰撞体。《[Collider2D-IsTouchingLayers - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Collider2D.IsTouchingLayers.html)》

- 为了实现物体检测还创建了2个新变量，也分别需要在组件中赋值。注意`collider`是代表角色的碰撞组件，`ground`是代表地图的图层。所以别忘记**设置地图的图层**。完成。**重点**，注意，切勿混淆，这里设置的是图层，不是顺序图层。

```c#
public LayerMask ground;
public Collider2D collider;
```



#  四、移动错误

> 第八讲：《[Unity教程2D入门:08 修复移动错误 (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 在第一讲笔记中，我就提到过移动偶尔卡主，且不能上坡的问题。教程在这一讲中解释了为什么：unity模拟太真实了，角色和地面是2个完全正方形在摩擦碰撞，偶尔产生的卡顿。
- 需要做的就是添加一个`2D圆形碰撞体Circke Collider 2D`代替下半身的正方形，也就说上半身还是正方形，下半身是圆形。这样就能正常上坡了，也不会平地摔了。
- 注意，还需要修改脚本组件中的碰撞器，替换为圆形的。因为在下落时还根据下半身的碰撞来检测落地。



# 五、隐藏组件

> 还是第八讲的视频。

- 在脚本文件中，有些对象参数是通过unity设置传入的。部分不需要常修改的组件赋值就不显示在unity界面上，直接在脚本文件内赋值即可。

```c#
private Rigidbody2D rb; // [SerializeField]
private Animator animator; // [SerializeField]

public LayerMask ground;
public Collider2D collider;
public float speed = 10;


// Start is called before the first frame update
void Start()
{
    rb = GetComponent<Rigidbody2D>();
    animator = GetComponent<Animator>();
}
```

- 教程还提到，如果加`[SerializeField]`关键字，就还是可以显示，我以为是灰色显示不能修改，没想到好像还是可以修改的。不过修改后就出现了一个警告。

```
Assets\Script\NewBehaviourScript.cs(11,20): warning CS0108: 'NewBehaviourScript.collider' hides inherited member 'Component.collider'. Use the new keyword if hiding was intended.
```

- 搜索得到结果，《[CS0108号错误是什么_Hoxily的窝窝-CSDN博客](https://blog.csdn.net/hoxily/article/details/56276168)》。不过根据提示修改后还是有警告还多了一个警告。感觉是我设置了`private`隐藏变量后才出现的？最终算了，无奈还是该会原样吧。不隐藏了。

