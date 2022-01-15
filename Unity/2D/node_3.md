# Unity 入门笔记 - 03

> 前言，无了，直接开始。



# 一、UI界面

> 第十二讲：《[Unity教程2D入门:12 UI入门 (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 步骤比较简单，直接上流程：

> 1. 层级窗口右键选择`UI-Canvas`创建UI的载体，所以UI的东西都放在里面。快捷键`Shitf+F`可快速缩放合适的查看大小。
> 2. 选中创建的`Canvas`对象，再创建一个`UI-Text`对象，可以修改内容，字体等。移动修改位置。还有相对位置需要修改，适应窗口大小的变化，将相对位置参考点设好。
> 3. 在角色的脚本中添加代码，当拾取物增加时修改变量。注意需要新增的代码。

```c#
using UnityEngine.UI; // 类比python/c的导入包/库

public Text CherryNum; // 创建对象变量，记得在unity中拖拽赋值

private void OnTriggerEnter2D(Collider2D collision) // 之前写的拾取物函数。
{
    if(collision.tag == "cherry")
    {
        Destroy(collision.gameObject);
        Cherry_num += 1;
        CherryNum.text = Cherry_num.ToString();  // 只新增了这一行，将值赋予。记住是字符串格式
        Debug.Log(Cherry_num);			
    }
}
```

- 如果要添加图片就选择创建`UI-Image`对象，基本同理，需要创建动画也可以，和角色动画同理。



# 二、消灭敌人

> 第十三讲：《[Unity教程2D入门:13 敌人Enemy! (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 创建敌人的步骤和角色类似，添加动画和碰撞体组件。然后在角色的程序中判断是否碰撞，和收集拾取物类似。
- 教程中还为怪物添加了刚体组件，因为创建的是地面类怪物，我还想着换个空中类怪物创建，但是发现如果我添加了刚体，那就不会在空中飞了。
- 创建怪物的部分已经学过，这里直接讲述用了什么新代码。

```c#
//关于碰撞输入2D On Collision Enter 2D
private void OnCollisionEnter2D(Collision2D collision)
{
    // 碰撞了相应标签 && 处于下落标志位
    if(collision.gameObject.tag == "eagle" && animator_0.GetInteger("jumping") == 2) 
    {
        Destroy(collision.gameObject);
        Debug.Log("消灭了老鹰eagle");	
    }
}
```

> 1. `OnCollisionEnter2D()`函数，就是专门为了碰撞而检测的。不同与收集拾取物中的`OnTriggerEnter2D()`，拾取物修改为了触发器，而不是碰撞触发。教程中使用了刚体，如果也用触发器就会直接掉落地图外，有重力。但是我没用刚体，所以其实2种都可以用？
> 2. `collision.gameObject.tag`属性，使用也和拾取物时的不一样。**注意**。
> 3. `animator_0.GetInteger()`函数，拷贝于跳跃部分的代码，用来判断标志位阶段。为了实现是下落时消灭的。但是其实应该是要做到踩在头顶才消灭才对。应该弄成和落地一样？
> 4. `Debug.Log()`，经过测试也可以打印中文无错误。unity对中文的支持真好。

- 扩展练习：消灭的碰撞添加受伤效果等。



# 三、受伤效果

> 第十四讲：《[Unity教程2D入门:14 受伤效果Hurt (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 这一讲没有用到新的函数或知识，只是在代码上有点需要注意的。

> 1. 为角色创建受伤动画，在动画器中创建过渡链接。**注意**，需要在跑动、下落、站立、跳起创建过渡。也就是除了下落。
> 2. 创建过渡条件的变量标志，依旧是整形`int`。为零时站立，不为零时就切换的受伤状态。
> 3. 在代码层面，这次没有用到新的函数，只是修改一下之前写过的代码。

- 在消灭老鹰的代码中，在判断不能消灭时就触发受伤效果，而且产生回弹效果。这里为了判断回弹方向，直接使用了属性`transform.localScale.x`，而且经过测试这个值需要是负的。然后触发受伤的代码就完成了。

```C#
//关于碰撞输入2D On Collision Enter 2D
private void OnCollisionEnter2D(Collision2D collision)
{		
    // 碰撞了相应标签 && 处于下落标志位
    if(collision.gameObject.tag == "eagle") 
    {
        if(animator_0.GetInteger("jumping") == 2)
        {
            Destroy(collision.gameObject); // 删除老鹰
            Debug.Log("消灭了老鹰eagle");	
        }
        else
        {
            animator_0.SetInteger("hurting", 1); // 改变标志位
            rb.velocity = new Vector2(-transform.localScale.x * 15, rb.velocity.y); // 回弹效果
            Debug.Log("开始受伤啦");
        }
    }
}
```

- 下面是接触是受伤的代码，因为受伤时不能继续其他操作，所以我直接在总调用函数里加判断。如果处于受伤时就一直判断什么时候退出，不执行其他操作。不受伤时才可以操作。

> 退出的条件是参考视频教程的，其他代码没有参考。视频教程的代码愈加感觉乱。

```c#
// Update is called once per frame
void Update()
{
    if(animator_0.GetInteger("hurting") == 0) // 没有处于受伤标志
    {
        Movement();
        Movement_0();
        Jump_0();
    }
    else if(rb.velocity.x > -0.1 && rb.velocity.x < 0.1) // 上面不成立，这里肯定就是处于受伤标志，然后只需要判断符不符合退出条件
    {
        animator_0.SetInteger("hurting", 0); // 改变标志位
        Debug.Log("停止受伤啦");
    }
}
```

- 其实严谨一点，应该判断为`1`时才算受伤，因为以后可能还有其他受伤状态。所以前期写时就要考虑好。



# 四、敌人移动

> 第十五讲：《[Unity教程2D入门:15 AI敌人移动 (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 这一讲用到的敌人移动和角色移动类似，不同的是敌人会按照预先设定的两点坐标间移动。而设定两点的方法是创建2个空的游戏对象`GameObject`，获取它们的坐标后删除。

```c#
private Rigidbody2D rb; // 刚体组件对象

public Transform leftpoint, rightpoint; // 记录坐标的两个空对象
public float Speed = 10; // 移动的速度
private float leftx, rightx; // 临时变量，记录坐标点

private int Faceleft = 0; // 标志位，记录向左向右

// Start is called before the first frame update
void Start()
{
    rb = GetComponent<Rigidbody2D>(); // 内部自动赋值刚体对象
    leftx = leftpoint.position.x; // 获取空对象坐标
    rightx = rightpoint.position.x;

    // transform.DetachChildren(); //教程中用到的，解除捆绑关系。
    Destroy(leftpoint.gameObject); // 直接删除空对象
    Destroy(rightpoint.gameObject);
}
```

- 注意代码用到了刚体对象，让敌人移动就是给敌人初速度，和角色移动一样。所以上一话才用到了刚体。除了那个“解除捆绑关系”的函数外。

```c#
void Movement() // 这是调用函数，自行在`Update()`内调用。
{
    if (Faceleft == 0)
    {
        rb.velocity = new Vector2(-Speed, rb.velocity.y);
        if (transform.position.x < leftx) // 判断是否到达坐标
        {
            transform.localScale = new Vector3(-1, 1, 1); // 敌人转向，也就说镜像，和角色的方法一样
            Faceleft = 1; // 改变标志位
            Debug.Log("往左边"); // 打印信息
        }
	}
	else // 和上面类似，逻辑相反
	{
        rb.velocity = new Vector2(Speed, rb.velocity.y);
        if (transform.position.x > rightx)
        {
            transform.localScale = new Vector3(1, 1, 1);
            Faceleft = 0;
            Debug.Log("往右边");	
        }
    }
}
```

- 注意，刚体记得锁定z轴。完成后可以拖拽敌人项目保存预设。



# 总结

1. 层级的对象名字不能出现中文，不然在调用时unity会有一个红色错误，但又不影响运行。而且改正后还是显示有错误。只有重启软件才能消除。
2. 代码中的变量命名不能和类同名，虽然程序是区分大小写能运行，但是unity还是有一个黄色的警告，一直存在。很烦。

- 以上是2个让我困扰很久的问题。
