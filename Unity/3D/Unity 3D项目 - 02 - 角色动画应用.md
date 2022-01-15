# Unity 3D项目 - 02 - 角色动画应用



## 一、常用代码

### 0.枚举

- `enum`；和C语言类似，属于整形，自动累加。和C语言不一样，**不同种类的枚举元素可以重名**！！

```c#
enum MoveStatus_E				// 枚举，运动状态
{	
    BackwardsRight	= -3,		// 右后退
    BackwardsLeft	= -2,		// 左后退
    Backwards		= -1,		// 后退
    Ldile 			= 0,		// 原地
    Forwards 		= 1,		// 前进
    ForwardsLeft 	= 2,		// 左前进
    ForwardsRight 	= 3,		// 右前进
    Left 			= 4,		// 左
    Right 			= 5, 		// 右
}
MoveStatus_E MoveStatus = MoveStatus_E.Ldile;				// 创建枚举变量

enum SpeedStatus_E				// 枚举，速度状态
{
    Wlak = 0,					// 步行
    Run,						// 小跑
    Sprint,						// 疾跑
    Jump,						// 起跳
}		
SpeedStatus_E SpeedStatus = SpeedStatus_E.Wlak;				// 创建枚举变量
```



### 1.根据名字获取对象

- `GameObject.Find()`；按 `name` 查找 GameObject，然后返回它。《[GameObject-Find - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/GameObject.Find.html)》

```c#
// 通过对象名称（Find方法）,再获取组件
player = GameObject.Find("/Casual1").transform; 	
PlayerAnim = PlayerTrans.GetComponent<Animator>();		
// 上下两行作用一样，标明trans可以借指object
// PlayerAnim = PlayerTrans.gameObject.GetComponent<Animator>();
```



### 2.获取键盘按键状态

- `Input.GetKey()`；在用户按下 `name` 标识的键时返回 true。
- 《[Input-GetKey - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Input.GetKey.html)》
- 《[Unity键位输入及Input类_t1446242775的博客-CSDN博客](https://blog.csdn.net/t1446242775/article/details/80271709)》
- 《[Unity键值(KeyCode) - 赵青青 - 博客园 (cnblogs.com)](https://www.cnblogs.com/zhaoqingqing/p/3378246.html)》
- 《[Unity - Scripting API: KeyCode (unity3d.com)](https://docs.unity3d.com/ScriptReference/KeyCode.html)》

```c#
if (Input.GetKey(KeyCode.W)) 			
	MoveStatus = MoveStatus_E.Forwards;				// 前进
else if (Input.GetKey(KeyCode.S))
	MoveStatus = MoveStatus_E.Backwards;			// 后退
```

> 处理输入时，建议改用 Input.GetAxis 和 Input.GetButton，因为 这允许最终用户对键进行配置。

- `Input.GetAxis[Raw]()`；返回(-1,1)的范围数或[-1，0，1]的整数。《[Input-GetAxis - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Input.GetAxis.html)》《[Input-GetAxisRaw - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Input.GetAxisRaw.html)》

```c#
float Turn_i  = Input.GetAxisRaw("Horizontal"); // 读取键盘输入，返回-1、0、1
float Speed_i = Input.GetAxisRaw("Vertical");	
```

- `Input.GetButtonDown()`；在用户按下由 `buttonName` 标识的虚拟按钮的帧期间返回 true。《[Input-GetButtonDown - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Input.GetButtonDown.html)》

```c#
if (Input.GetButtonDown("Fire3") && is_shift == false)	// 读取 left shift 返回 true
	is_shift = true;
```



### 3.设置动画参数

- `Animator.SetInteger()`；设置给定整数参数的值。《[Animator-SetInteger - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Animator.SetInteger.html)》《[动画参数 - Unity 手册](https://docs.unity.cn/cn/2020.3/Manual/AnimationParameters.html)》

```c#
PlayerAnim.SetInteger("WlakState", (int)MoveStatus);// 最后转换类型赋值
```

> 如果想动画播放完毕就退出，可以建立返回过渡但不设立参数条件，保留退出时间等。

- `Animator.SetFloat()`；将浮点值发送到动画器以影响过渡。《[Animator-SetFloat - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Animator.SetFloat.html)》

> 另一种重载方式：public void **SetFloat** (string **name**, float **value**, float **dampTime**, float **deltaTime**);
>
> - **使参数、动画更加平滑的变动**；《[Unity---动画系统学习(4)---使用混合树(Blend Tree)来实现走、跑、转弯等的动画切换 - Fflyqaq - 博客园 (cnblogs.com)](https://www.cnblogs.com/Fflyqaq/p/10777793.html)》
>
> - 第3个参数表示完成变化所需要的时间；第4个参数表示执行该方法的时间间隔（Time.deltaTime）；

```c#
anim.SetFloat("Turn", Turn_i, 0.1f, Time.deltaTime);
anim.SetFloat("Speed", Speed_i, 0.1f, Time.deltaTime);
```

- **重点**！！走路拐弯的动画使用**混合树**功能实现，更加方便快捷平滑！！



### 4.空间坐标转换

- `Transform.TransformDirection()`；将 `direction` 从本地空间变换到世界空间。《[Transform-TransformDirection - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Transform.TransformDirection.html)》

```c#
PlayerRigid.velocity = PlayerTrans.TransformDirection(vector_i);		// 赋值
```

- `Vector3.Normalize()`；归一化处理；《[unity中的四元数，欧拉角，方向向量之间的相互转换方法。_Mansutare的博客-CSDN博客](https://blog.csdn.net/qq_27719553/article/details/118571637)》

> 没有返回值，直接修改

```c#
MoveVector.Normalize();						// 先归一化
```



### 5.刚体运动

- `Rigidbody.velocity`； 刚体的速度矢量。它表示刚体位置的变化率。《[Rigidbody-velocity - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Rigidbody-velocity.html)》

> 在大多数情况下，不应该直接修改速度，因为这可能导致行为失真 - 改用 AddForce 请勿在每个物理步骤中设置对象的速度，这将导致不真实的物理模拟。

```c#
PlayerRigid.velocity = PlayerTrans.TransformDirection(vector_i);		// 赋值
```

- `Rigidbody.rotation`；使用 Rigidbody.rotation 以通过物理引擎获取和设置刚体的旋转。《[Rigidbody-rotation - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Rigidbody-rotation.html)》

> 1. 使用 `Rigidbody.rotation` 更改刚体的旋转会在下一个物理模拟步骤后更新变换。这比使用 `Transform.rotation` 更新旋转要快，因为 `Transform.rotation` 将导致所有附加的碰撞体重新计算其相对于刚体的旋转，而 `Rigidbody.rotation` 会直接将值设置到物理系统。
>
> 2. 如果需要连续旋转刚体，请改为使用 [MoveRotation](https://docs.unity.cn/cn/2019.4/ScriptReference/Rigidbody.MoveRotation.html)，[MoveRotation](https://docs.unity.cn/cn/2019.4/ScriptReference/Rigidbody.MoveRotation.html) 会考虑插值问题。
>
> 3. **注意**：使用世界空间。

```c#
if (PlayerRigid.rotation != Quaternion.LookRotation(-vector_i))
	PlayerRigid.rotation = Quaternion.LookRotation(-vector_i);	
```

> - `Rigidbody.AddForce()`；向 [Rigidbody](https://docs.unity.cn/cn/2019.4/ScriptReference/Rigidbody.html) 添加力，大小为向量的模。《[Rigidbody-AddForce - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Rigidbody.AddForce.html)》 （在 `FixedUpdate` 中计算）
> - `Rigidbody.MoveRotation()`；将刚体旋转到。《[Rigidbody-MoveRotation - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Rigidbody.MoveRotation.html)》（在 `FixedUpdate` 中计算）
> - 经过测试，使用添加力的方式不符合人物控制的运动现象，更加适合抛掷物等自由物体。或者跳跃的时候。



### 6.AI导航

- `NavMeshAgent.destination`；获取代理在世界坐标系单位中的目标或尝试设置代理在其中的目标。《[AI.NavMeshAgent-destination - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/AI.NavMeshAgent-destination.html)》

```c#
PlayerAgent.destination = vector_i;
```

- `NavMeshAgent.isStopped`；此属性持有导航网格代理的停止或恢复条件。《[AI.NavMeshAgent-isStopped - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/AI.NavMeshAgent-isStopped.html)》

```c#
agent.isStopped = true; // 是否启用静止状态 
```



### 7.时间差

- `Time.deltaTime`；完成上一帧所用的时间（以秒为单位）（只读）。《[Time-deltaTime - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Time-deltaTime.html)》

```c#
escjump_time += Time.deltaTime;		// 累加时间
```



### 8.角色控制器

- `CharacterController.Move()`；为 GameObject 的移动提供附加的 CharacterController 组件。《[CharacterController-Move - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/CharacterController.Move.html)》

> 真的是简单粗暴，还自己写什么，那么好用的组件。

```c#
controller.Move(v3 * Time.deltaTime * playerSpeed);
```



### 9.四元数旋转

- `Quaternion.LookRotation()`；使用指定的 `forward` 和 `upwards` 方向创建旋转。《[Quaternion-LookRotation - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Quaternion.LookRotation.html)》

```c#
PlayerRigid.rotation = Quaternion.LookRotation(-vector_i);		// 方向相反，所以使用负号
```

- `Quaternion.FromToRotation()`；创建一个从 `fromDirection` 旋转到 `toDirection` 的旋转，返回四元素。《[Quaternion-FromToRotation - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Quaternion.FromToRotation.html)》

```c#
// 最后乘于自身旋转，得到目标旋转
Quaternion a3 = Quaternion.FromToRotation(tran.forward, cam.forward) * tran.rotation;
```

- `Quaternion.Slerp()`；**Quaternion** 在四元数 a 和 b 之间进行球形插值的四元数。《[Quaternion-Slerp - Unity 脚本 API](https://docs.unity.cn/cn/2019.4/ScriptReference/Quaternion.Slerp.html)》

```c#
tran.rotation = Quaternion.Slerp(tran.rotation, a3, playerTurn * Time.deltaTime);
```





## 二、常用插件

- `Cinemachine`；虚拟相机；《[unity 的Cinemachine组件运用_farcor_cn的博客-CSDN博客](https://blog.csdn.net/farcor_cn/article/details/109136293)》



## 三、文字版步骤

1. 导入场景资源，并打包抠出；

> 官方商店-免费：Low Poly Farm Pack Lite；
>
> 注意：加载新资源时记得设置为通用渲染管线。

2. 导入人物模型、动画资源，并加载模型预设；

> 官方商店-免费：日本動漫風角色 : 惠兒 (免費版 / 高中制服版 / 包含VRM)；Basic Motions FREE；

3. 安装插件Cinemachine；

> 官方商店-注册表内；

4. 设置光照、灯光、环境等。
5. 导入`freeLook`虚拟相机，设置目标、参数等；

> 注意：为人物设立新的空的对象坐标，设为追踪目标。调整跟随范围，防止距离抖动。

6. 拷贝人物动画，避免源文件不可修改或被修改；
7. 设置多层动画，同层动画的过渡关系；

8. 设置动画参数，过渡条件；

> 注意：所有动画都不需要退出时间和过渡时间，会导致响应缓慢。返回上一状态时可以有过渡时间，酌情设置，比如跳跃返回。

9. 设置地图的导航参数，添加可运动区域和不可运动区域，烘焙地图；

> 注意：设置导航时需要选择确切的地图对象，地图对象的空父类不可已。

10. 添加人物导航组件、刚体组件、胶囊碰撞体组件（暂无用？）、脚本文件；

11. 编写键盘输入获取的代码；

> 包含方向键WSAD、步行小跑键CTRL、疾跑Shift，和空格跳跃键Space。

12. 编写切换动画参数的代码；

> 包含退出跳跃动画的判断；

13. 编写刚体运动的代码；

> 尝试了添加力的方法，但是没有效果，不知为何，暂没找到原因。所以还是使用了旧方法，直接给速度。转向也是。

14.编写导航运动的代码；

> 可以选择导航时是否有多个方向的动画，因为导航会自动先朝向目标再移动，之前用Q版人物时感觉挺不错的。



## 四、视频版步骤

- 《[Unity 3D项目 - 02 - 角色动画应用_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV17Q4y1e7yy?spm_id_from=333.999.0.0)》

> BGM：网易云免费下载
>
> 《末廣健一郎 - 終ワリノ歌》
>
> 《水瀬いのり,久保ユリカ - Endless Journey》
>
> 《久保ユリカ,水瀬いのり - 雨だれの歌》

- 

> 人物模型：官方商店免费下载
>
> Humanoid Bot
>
> 人物动画：官方商店免费下载
>
> Basic Motions FREE
>
> BGM：网易云免费下载
>
> 《久保ユリカ,水瀬いのり - 雨だれの歌》



## 五、总结

1. 导航组件用在人形上感觉不太好，不知道哪里设置错了；
2. 刚体选择经常卡死不能旋转，不知道是不是物理碰撞体卡主了，需要在编辑器里手动旋转一下才能继续旋转；
3. 根据API手册的说明，不建议使用直接修改速度和角度；我也认为不太真实，但是使用添加力和力矩的方式不知为何无效果；
4. 从主菜单切换进入第二个场景时，不知为何灯光直接暗了许多；如果直接从第二个场景启动则不会；



> 之前写的一篇关于镜头跟随和键盘移动的笔记：《[Unity 知识点 - 3D游戏 - 视角跟随和键盘移动_Lovely_him的博客-CSDN博客](https://blog.csdn.net/Lovely_him/article/details/121324398?spm=1001.2014.3001.5501)》



- 关于人物旋转方向的代码，参考了这位up的教程。《[【Unity快速教学】3D RPG的人物移动_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV13v411i76p?from=search&seid=837040548704258618&spm_id_from=333.337.0.0)》
- 关于人物移动坐标的代码，采用人物控制器组件，代码参考官方API。
- 动画控制器的使用，运用混合树控制过渡，参考了这位up的（转载的？）教程。《[使用 Unity让动画角色 移动、行走、奔跑和跳跃_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1VX4y1A73U)》

