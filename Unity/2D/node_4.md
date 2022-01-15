# Unity  入门笔记 - 05

> 前言：无



# 一、动画事件

> 第十六讲：《[Unity教程2D入门:16 Animation Events动画事件 (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 这一讲的主要新知识点是动画事件，其作用就是在动画结束时，自动调用指定函数。
> 教程中结合青蛙怪物的站立和跳跃动画的切换讲解。因为我之前是用老鹰的，所以这次顺带从新做了一个青蛙，一口气做完的感觉真爽。（~~整天玩什么游戏，浪费时光，来学习做游戏多好~~）

- 创建精灵对象，装载青蛙图片，为其创建动画和2个空对象当坐标，创建动画过渡，设立变量和条件。添加刚体和碰撞体组件，开始写代码。（~~依旧是自己重新写代码，和教程里的不一样~~）

```c#
/* 以下是外部赋值变量 */
public LayerMask ground; // 创建地图图层对象
public Collider2D coll; // 创建碰撞器
public Transform leftpoint, rightpoint; // 创建坐标对象
public int speed = 5; // 设定青蛙移动的速度
public Animator anim; // 创建动画器

/* 以下是内部赋值变量 */
private Rigidbody2D rb; // 创建刚体对象
private float leftx, rightx; // 创建存储左右坐标点变量
private int flag_i; // 创建内部临时标志位


// Start is called before the first frame update
void Start()
{
    rb = GetComponent<Rigidbody2D>(); // 获取刚体对象

    leftx = leftpoint.position.x; // 获取左右坐标点
    rightx = rightpoint.position.x;

    Destroy(leftpoint.gameObject); // 删除坐标对象
    Destroy(rightpoint.gameObject);
}
```

- 前面一部分的代码和老鹰的基本一致，需要读取坐标然后删除对象。因为要检测下落，所以还需要配置碰撞器和地图对象。

```c#
// 起跳函数，在站立动画结束时自动调用。
void Movement()
{
    anim.SetInteger("anim_frog", 1); // 改变标志位，切换起跳动作
    // 开始跳跃，给予向上和向前的速度
    rb.velocity = new Vector2(-transform.localScale.x * speed / 2, speed); 
}
```

- 然后就是动画事件中调用的函数，这时运行已经能看到站立动画结束后就切换到起跳动画并起跳了。这里判断往哪边跳的方法是读取当前的朝向。

```c#
// Update is called once per frame
void Update()
{
	down();
}

// 下落函数，循环检测执行
void down()
{
    // 如果正处于起跳状态，且处于向下落速度
    if(anim.GetInteger("anim_frog") == 1 && rb.velocity.y < 0.1f) 
    {
    	anim.SetInteger("anim_frog", 2); // 改变标志位，切换下落动作
    }
    // 如果处于下落状态，且碰撞了地图
    else if(anim.GetInteger("anim_frog") == 2 && coll.IsTouchingLayers(ground)) 
    {
    	if (transform.position.x < leftx) // 已经错过左边坐标
        {
        	transform.localScale = new Vector3(-1, 1, 1); //转头
        }
        else if (transform.position.x > rightx) // 反之亦然
        {
            transform.localScale = new Vector3(1, 1, 1); //转头
        }
    	anim.SetInteger("anim_frog", 0); // 改变标志位，切换站立动作，开始循环
    }
}
```

- 最后剩下的就是循环调用的函数，检测是否要下落，然后切换下落动画。并检测是否落地，切换站立动画。同时需要判断是否到达指定坐标，改变朝向。

- **注意**：可以使用盒装碰撞体，不需要圆形的，因为圆形的会在跳跃时滑……，滑一下很容易超出指定距离就掉出去了。



# 二、类的调用

> 第十七讲：《[Unity教程 Your First Game|入门Tutorial:17 Class调用(互动包括老鹰制作)_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1i4411m7fK/?spm_id_from=333.824.videocard.1)》这是一个互动视频，在播放列表或旧版客户端中无法观看……

- 这一讲主要实现怪物被消灭的动画，通过实例化类对象来实现。体现了c#面向对象的特点！！！！

> 1. 为怪物添加被消灭的动画，创建过渡条件和参数变量。在控制器中，可以选择从`Any State`过渡，代表是任何状态都可以过渡。参数类型可以选择`Tigger`，和`Bool`类似，不同的是前者会自动回复`False`。《[Animator-SetTrigger - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Animator.SetTrigger.html)》
> 2. 在怪物的代码中，添加触发消灭动画的函数。在角色的消灭函数里调用。再在怪物的代码中添加删除对象的函数。将角色的消灭函数里的删除对象代码去除。
> 3. 在怪物被消灭的动画中添加**动画事件**。等到消灭动画结束后，怪物自行调用删除对象函数，进行自我删除。

- 以下是在角色中添加的代码。目前还是常规的调用对象的方法或属性。

```c#
eagle enemy_eagle = collision.gameObject.GetComponent<eagle>(); // 创建：碰撞体.所属对象.所包含的组件/类
enemy_eagle.anim_del(); // 调用怪物代码中的动画标志函数。
// Destroy(collision.gameObject); // 注释掉，成为怪物代码中的调用函数。
```

- 删除代码，改变标志位代码，这两者应该所有怪物都有的共同特点，应该用一个类打包，然后再被所有怪物继承。这是这讲的重点。以下就是独立的怪物脚本代码。

```c#
public class enemy : MonoBehaviour
{
	
	protected Animator animator_0;
	
    // Start is called before the first frame update
    protected virtual void Start() // 注意父类的初始化函数的写法
    {
        animator_0 = GetComponent<Animator>(); // 获取动画器对象
    }

	
	// 开启消灭动画
	public void anim_del()
	{
        // 注意！！所有怪物的开启消灭动画的参数变量都要是bool类型命名del，保持统一才能用。
		animator_0.SetBool("del", true); 
	}
	
	// 执行消除对象
	public void ooj_del()
	{
		Destroy(gameObject);
	}
}
```

- 然后在其他怪物中继承该类，同时子类中就不需要再创建`animator_0`、`anim_del()`、`ooj_del()`这三者了，**注意**，动画器对象变量也不用再创建了。子类怪物的代码修改如下，所有的怪物都要修改如下。

```c#
public class eagle : enemy // 注意这里修改，继承父类
{
	...
	// public Animator animator_0; // 注释掉，该属性已经在父类中继承
	...
	
    protected override void Start() // 注意子类的初始化函数的写法
    {
		base.Start(); // 执行父类的初始化方法。包含了animator_0的赋值
		...
	}
	
	...
}	
```

- 最后，还需要修改角色中的代码，注意和上面的角色代码作对比。

```c#
// eagle enemy_eagle = collision.gameObject.GetComponent<eagle>(); // 不再创建特定一怪物的实例化。
enemy enemy_eagle = collision.gameObject.GetComponent<enemy>(); // 而是创建所有怪物的父类的实例化。
enemy_eagle.anim_del(); // 不变
```

- 如果保持代码不改，会只能触发包含`eagle`类的怪物，因为其即包含父类`enemy`类，也包含本身子类`eagle`类。但是其他子类怪物只包含父类`enemy`类，会在创建`eagle enemy_eagle`时失败。

## 补充

- **注意**！！！消灭的动画的过渡设置中，不能勾选`可以过渡到我自己`，不然会一直卡在第一帧。通过搜索，发现应该是使用bool类型作为触发条件的缘故。《[unity使用Animator时anystate进行转换动画不断卡死在第一帧_MainBack-CSDN博客](https://blog.csdn.net/baidu_38246836/article/details/103728054)》实测，果然，如果不使用bool，使用Trigger类型，可以勾选`可以过渡到我自己`。教程也是这样做的。
- 关于c#类的继承，可以看菜鸟教程，讲解的挺明了的。《[C# 继承 | 菜鸟教程 (runoob.com)](https://www.runoob.com/csharp/csharp-inheritance.html)》《[C# 多态性 | 菜鸟教程 (runoob.com)](https://www.runoob.com/csharp/csharp-polymorphism.html)》



# 三、音效Audio

> 第十八讲：《[Unity教程2D入门:18 音效Audio (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- unity的音效添加有三个重要概念，`Audio Listener`声音接收源，`Audio Source`声音产生源，`Audio Clips`音乐文件。`Audio Listener`就是游戏主窗口/摄像机的组件，`Audio Source`就是添加在游戏对象身上的组件。`Audio Clips`就是`Audio Source`组件的一个属性，即选择音频文件的框框。
- 因为游戏镜头是跟着角色移动的，所以背景音乐bgm就可以添加在角色身上。除此之外还有跳跃、拾取宝石等。而消灭敌人的音效就添加在敌人身上。
- unity的`Audio Source`组件和动画器组件类似，不过一个组件只能装载一个声音，动画则是一个动画控制器控制所有动画。感觉有点麻烦。

> 1. 为角色添加`Audio Source`音频源组件，选个合适的bgm，放入`Audio Clips`栏中。勾选`唤醒时播放`即一开始播放，勾选`循环`。
> 2. 和添加bgm类似，为角色添加起跳、收集拾取物的音效。同时取消勾选`唤醒时播放`和`循环`，然后修改代码。
> 3. 代码部分很简单，只要添加两行即可。一个是创建对象，一个是调用方法。更多方法可到官网查找。《[AudioSource-Play - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/AudioSource.Play.html)》

```c#
public AudioSource BgmGem; // 创建游戏对象，在unity中拖拽组件进行赋值
...
BgmGem.Play(); // 开始播放音乐
```

- 怪物也类似，在怪物对象中添加`Audio Source`音频源组件，不过代码是在父类中修改即可，因为被消灭的代码是写父类中。然后所有子类都会继承。



# 四、对话框Dialog

> 第十九讲：《[Unity教程2D入门:19 对话框Dialog (bilibili.com)](https://www.bilibili.com/medialist/play/370283072?from=space&business=space_series&business_id=212003&desc=1&spm_id_from=333.999.0.0)》

- 对话框是UI画布中的部件，在`Canvas`画布对象下右键选择`UI-Panel`创建对话框，设置相对画布的固定方式、设置颜色和透明度。再右键选择`UI-text`创建文本，因为文本是在对话框层级下，所以相对位置也是相对与对话框，居中即可。
- 另一个**知识点**是触发对话框显示。思路是，其实对话框一直在，只是失能不显示而已。需要设置一个触发器，触发时就使能让对话框部件显示。
- 剩下的就是和拾取物类似了，不同的一点是，我尝试创建一个空的游戏对象`GameObject`，而不是2D选项中的精灵对象。发现也能实现功能。

> 这时明白到，精灵对象其实属于游戏对象的分支，如果有图像需要渲染才用，否者空的内容使用`GameObject`即可。

- 代码是添加在触发器中，教程介绍触发器有种实现，一种是直接在已有对象中添加触发器，另一个是在已有对象层级下创建空的游戏对象再添加触发器。我选择后者，这样之后可以单成预设。

```c#
// using System.Collections;
// using System.Collections.Generic;
using UnityEngine;

public class Panel_kg : MonoBehaviour
{
	public GameObject enterDialog;
	
    // Update is called once per frame
    void Start()
    {
		enterDialog.SetActive(false); // 起初自动关闭，不用手动关闭
    }
	
	// 触发器开始触发时调用
	private void OnTriggerEnter2D(Collider2D collision)
	{
		if(collision.tag == "Player")
		{
			enterDialog.SetActive(true);
		}
	}
	
	// 触发器离开触发时调用
	private void OnTriggerExit2D(Collider2D collision)
	{
		if(collision.tag == "Player")
		{
			enterDialog.SetActive(false);
		}
	}
}
```

- 代码很简单，需要注意的就是每次运行游戏前要使对话框处于失能状态，不然一开始就会显示，虽然之后也会正常触发或消失。~~我原本想在初始化中直接失能，后来发现这样不可行，还不知道原因~~。函数名字写错了。

- 最后一个**知识点**就是给对话框添加动画，自己录制/制作渐变效果，使用动画中的录制功能。这里有一点**重点注意**，取消动画文件中的`循环时间`，否者会一直渐变。选择动画文件，在项目里选择，不是在层级里选择。

> ~~内容较少就不写流程了。这样说说重点就好~~。



# 总结

- 接下来就是制作第二个场景，复习一下之前学过的知识。

> 1. 按照老师布置的作业，制作关卡2时，地图、背景是重新绘制，人物、怪物、画布、收集物都是使用预设。大部分都没有问题，只有怪物相当奇怪，运行游戏时看不到。Z轴坐标确认过都是0，排序图层也没问题。图层默认Default。切换3D视图时能发现怪物明显不在一个平面内……（写到这里忽然发现问题所在，为了记录踩坑分享给其他小白，继续写下去）—— 搭载怪物的空游戏对象的z坐标不为0……作为子目录的怪物即使设置0，也不是相对世界坐标系，而是上一级的相对坐标！！！！
> 2. 快捷键：Shitf+F，快速缩放合适大小。



