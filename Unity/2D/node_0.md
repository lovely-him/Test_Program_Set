# Unity 入门笔记 - 01

> 前言：玩游戏着实无聊荒废时光，我决定还是找点不需要烧钱又感兴趣，同时以前没入门过的知识学习一下。无意中刷到了`unity`的科普视频，心想，这是个不错的机遇，说干就干。

> 视频安利：《[【游戏开发】新人如何用unity做出第一个属于自己的游戏Demo](https://www.bilibili.com/video/BV1WK4y1a7Hq)》；《[Unity 10分钟快速入门 #U3D #Unity3D](https://www.bilibili.com/video/BV1PL4y1e7hy)》；



# 一、软件安装

> 根据科普视频的安利，我选择up主**[M_Studio](https://space.bilibili.com/370283072?spm_id_from=333.788.b_765f7570696e666f.2)**的入门系列教程学习，入门笔记也是按照教程顺序来。
>
> 第一讲：《 [Unity教程2D入门:01安装软件&导入素材](https://www.bilibili.com/video/BV1W4411Z7UC?spm_id_from=333.999.0.0)》

- 因为`unity`在国内有中文官网，所以方便很多，直接上官网下载免费的个人版使用即可。（发现官网其中还有好多课程广告、社区等内容。真厉害，有个完整的生态圈。）我选择**2019**的版本，现在日期是2021.10.19。
- 可以选择直接下载`Unity`软件本体，也可以通过`Unity Hub`管理工具下载。为了方便小白入门，我选择`Unity Hub`。同样是在官网下载，然后安装。**注意不要有中文，避免玄学问题**。
- 需要注意两点，在选择unity软件版本后，选择附带工具：`VS 2019`和中文语言包等。在`Unity Hub`启动unity先要弄许可证，虽然是免费的但还是需要。不然会报错。

> 《[Unity开发备忘录000022：Unity许可证无效，怎么办？](https://blog.csdn.net/sunbowen63/article/details/97884511)》
>
> 《[Unity设置中文](https://blog.csdn.net/u013654125/article/details/109892758)》

- 完成后就可以无误启动unity软件本体啦。

> **关于素材的导入**：好像直接丢到工程文件夹里就可以了，反正都是内置文件浏览器查看。教程里是用软件内自带的浏览器窗口查看素材并下载。看弹幕说高版本取消了这个内置功能，要单独从浏览器打开了？



# 二、编辑素材

> 第二讲：《[Unity教程2D入门:02 编辑素材& Tilemap_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1W4411Z7xs?spm_id_from=333.999.0.0)》

- 添加背景，直接将文件从`项目栏`拖进`层级栏`中即可；
- 添加组合元素，使用不同方块搭建关卡：

> 1. 拥有一张元素贴图，包含了所有元素，需要将它们切割出来。选择`检查器`内的`Sprite模式`为多个，点击应用。弹出用于切割多个的窗口，选择自己设置切割的像素格大小。完成。
> 2. 在项目栏右键选择`2D对象`的`瓦片地图`选项，再选择`Window`中的`2D`的`平铺调色板`。新建调色板（`New Palette`），再将上一步分割好的图片文件拖拽进去，就可以使用了。
> 3. 点击平铺调色板内的工具，就可以选择元素再点击放在瓦片地图内就可以了。

- **注意**，因为是像素风格，所以都要设置每单元格的像素量，根据教程统一设置16即可。

> 课外实践：
>
> 1. 发现层级栏中的`Main Camera`是摄像机，而且摄像机的Z坐标是`-10`，如果点击坐标重置会回到`0`，这样会导致游戏画面完全没有。
> 2. 记录问题：绘制瓦片地图时隐藏了背景，事后再显示时发现背景的图层一直在瓦片地图上面，也就是被挡住了……。虽然在场景栏里没被挡住，但是游戏栏里确实被挡住了？



# 三、添加角色&图层&组建

> 第三讲：《[Unity教程2D入门:03 图层layer&角色建立_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1r4411Z7dD?spm_id_from=333.999.0.0)》

- 解决上一讲遇到的问题，背景遮住了瓦片地图，果然是图层的问题。和其他软件不同，改变层级中的顺序并不影响图层顺序。应该修改检查器栏中的`排序图层`选项。可自定义添加不同图层，同一个图层也可以修改各自优先级。注意先后层叠即可。
- 添加角色一般使用`右键-2D对象-精灵`选项，然后将角色元素添加在检查器的`精灵`框内。（也可以类似添加背景似的直接拖拽）

> 注意：别忘记修改角色图层，避免被遮挡。同时需要重置坐标，刚创建时Z轴的坐标好像不是0，没法被摄像机拍到，出现场景里看到但是游戏里看不到的情况。上一讲也有遇到过。看来这是个常掉的坑。

- 再者，对`2D对象`（瓦片地图和角色）添加组件：因为用的是中文版，组件的名字也翻译了，好评，同时搜英文也是可以搜到的。

> 1. **2D刚体** - `Rigidbody 2D`（角色用）：使角色成为一个刚体，拥有重力，会下坠。
> 2. **2D盒装碰撞器** - `Box Collider 2D`（角色用）：使角色拥有碰撞体积。
> 3. **瓦片地图碰撞器** - `Tilemap Collider 2D`（瓦片地图用）：使地图拥有碰撞体积。
>
> 三者都添加上后就可以使角色立在地图上啦~~~~
>
> 有趣的事情：将角色在斜坡上掉下来，会滑下翻滚，真实的物理引擎~



# 四、角色移动&代码编程

> 第四讲：《[Unity教程2D入门:04 角色移动_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1f4411Z7oL)》

- 为角色添加新的组件，选择`新建脚本`。同时会在项目目录Assets中新建脚本文件。为了方便管理将代码放到一个集中的文件内。**注意**，如果手动改变脚本目录路径，会导致脚本组件找不到脚本文件，只需要拖拽重新添加即可。

- 剩下的就是喜闻乐见的写代码环节了。新建的脚本文件会有一部分内置代码，如下。unity使用`C#`编程语言，我之前也没学过，只学过c语言、python、js，我会结合对比学习。

```c#
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NewBehaviourScript : MonoBehaviour
{
    // Start is called before the first frame update
    // 在第一个帧更新之前调用Start
    void Start()
    {
        
    }

    // Update is called once per frame
    // Update 每帧调用一次
    void Update()
    {
        
    }
}
```

- 结合`菜鸟教程`等平台，补充一下c#的知识。

> 1. `using`关键字用于在程序中包含`System`命名空间。有点类似与python的导入包`import `。假设，之后有个方法的调用为`System.get()`，那就可以省略写成`get()`。这是c#中的命名空间相关知识点：《[C# 命名空间（Namespace） | 菜鸟教程 (runoob.com)](https://www.runoob.com/csharp/csharp-namespace.html)》。
> 2. `class`关键字用于类的创建，和python与c++一样。《[C# 类（Class） | 菜鸟教程 (runoob.com)](https://www.runoob.com/csharp/csharp-class.html)》。
> 3. `class`关键字后续的冒号后接的是继承类。《[C# 继承 | 菜鸟教程 (runoob.com)](https://www.runoob.com/csharp/csharp-inheritance.html)》。
> 4. `public`关键字代表的访问范围（类比作用域），是c#中的封装相关知识：《[C# 封装 | 菜鸟教程 (runoob.com)](https://www.runoob.com/csharp/csharp-encapsulation.html)》。这个关键字如果不写会有原本的默认值，如果要用的不是默认值就要标明。
> 5. 再后续的就是注释和函数的创建，每一行结束代码要使用分号结束，和c语言一致。

- 第一步创建2个新的变量，一个用于装载（赋值）角色（刚体组件），一个用于设置移动速度。在大类中添加这2个成员变量，保存后返回unity软件查看，就发现脚本组件内多了这2个名字的选项栏。而且`speed`那一栏还贴心的自动翻译成中文`速度`。
- 将`Rigidbody 2D`组件拖拽到`rb`栏中，即可完成添加。`速度`栏也可以修改，而且注意吗，软件内修改后保存即可生效显示已修改，但是原脚本的值是不会改变，还是原本的初始值`10`。

```c#
public Rigidbody2D rb; // 创建一个Rigidbody2D空对象
public float speed = 10; // 创建一个浮点数，给定初始值。（不给定值也可以，在unity软件内就会默认是0）
```

- 接着，需要创建一个函数，用于读取按键的输入，并根据按键的输入修改角色的x坐标，实现角色的左右移动（~~为什么教程包含上下移动~~）。直接看代码。

```c#
void Movement()
{
    float num = 0; // 创建一个临时变量保存按键输入值

    num = Input.GetAxis("Horizontal"); // 读取按键输入

    if(num != 0) // 判断按键输入是否有按下左右键
    {
        rb.velocity = new Vector2(num * speed, rb.velocity.y); // 根据按键输入修改坐标
    }
}
```

- 关于用到的2个unity脚本API，我们到unity官网的手册里看看解释。（~~虽然有中国分站，但是校园网太差老是打不开，气得跺脚~~）

> 1. `Input.GetAxis()`函数：《[Input-GetAxis - Unity 脚本 API](https://docs.unity.cn/cn/current/ScriptReference/Input.GetAxis.html)》。官方解释：返回由 `axisName` （括号内的字符）标识的虚拟轴的值。
>
> To set up your input or view the options for `axisName`, go to **Edit** > **Project Settings** > **Input Manager**. This brings up the Input Manager. Expand **Axis** to see the list of your current inputs. You can use one of these as the `axisName`. To rename the input or change the positive button etc., expand one of the options, and change the name in the **Name** field or **Positive Button** field. Also, change the **Type** to **Joystick Axis**. To add a new input, add 1 to the number in the **Size** field.
>
> 要设置输入或查看`axisName`的选项，请转到**编辑**>**项目设置**>**输入管理器**。这将打开输入管理器。展开**Axis**以查看当前输入的列表。您可以使用其中一个作为`axisName`。要重命名输入或更改正按钮等，展开其中一个选项，并更改**名称字段**或**正按钮字段中的名称**。同时，将**类型**改为**操纵杆轴**。若要添加新输入，请向**Size**字段中的数字添加1。
>
> - 意思就是可以到**项目设置**中查看有哪些**标识**，问题是中文版把这些标识也汉化了，不然这些选项的名字就是可以直接作为`Input.GetAxis()`函数的参数传入。这个需要自己注意查找原文了。
>
> 2. `Vector2()`函数：《[Rigidbody2D-velocity - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Rigidbody2D-velocity.html)》。个人理解，就是用来生成新的`Rigidbody2D.velocity`对象代替原本的`rb.velocity`。传入的2个参数分别是新的x与y轴的速度。程序中，使y轴的速度保持，x轴的速度为设定的`speed`。因为`num`变量是`-1或1`仅代表方向。
>
> - 这个api函数在2021的版本中没找到，特地切换到2019才找到了，教程是用2018版本……感觉差一点就要重新安装了（虽然教程开始也说过本教程使用2019和2018）。另外，我一开始还以为改变的是移动量，原来是改变速度，根据官方手册说法是默认设置的阻力，所以会停下来。
> - 再者，关于`new`关键字，在js中也有见过，感觉就是个创建对象的关键字？

- 最后在每帧调用函数`Update()`中调用`Movement()`，点击保存代码。返回unity软件，点击运行游戏。

```c#
void Update()
{
	Movement();
}
```

- 在实现时遇到的一些问题：

> 1. 偶尔突然输入失灵，怎么按动AD键都无效。然后我点其他地方再点回游戏栏，就又可以了……
> 2. 不会爬坡。遇到坡道就直接顶住了……和撞墙一样。也可能是我场景的刚体碰撞没弄好。

