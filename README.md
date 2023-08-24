# segmentation-3D
for chapter 2

## segment 使用：
- 1 先写 farm{day-num}.py 文件拆分出单个点云。 
  数据记录在flight-result-segement.xlsx的flights中。
- 2 使用moveCluster.py 将站立牛的文件移动到一起。并复制到mac中
- 3 查看每个standing点云记录姿态、噪音、以及方向到flight-result-segement.xslx的standing-cattle和direction中。
- 4 对有待处理点云（uncertain）创建farm{day-num}文件夹。对单个点云创建处理文件。并如3记录
- 5 使用entitie.py将点云从farm点云中切出。
- 6 补充data.csv 目的是自动化移动点云。
- 7 使用move_individual_batch.py 完成点云移动。

## extraction
- 1 先完成data-direction.xslx
- 2 使用transDirectionData.py将data-direction.xlsx打平到data-direction-flat.xlsx
- 3 使用normalisation_batch.py将点云旋转
- 4 使用denoise_batch.py 过滤
- 5 使用backbone_batch.py获取相关的脊柱点云
- 6 使用belly.py更新宽度
- 7 从bbInCattle 文件中截取hip点云
- 8 使用hipHeight.py 更新hipheight数据。

## data-measurment.xlsx 属性说明
-  hip H #使用bounding box框高 
-  HH # bounding box框高 - ground height
-
-  joint hip H #使用color[0] = 1来区分坐标值的 第一高点
-  joint HH # joint hip H - ground height
-
-  JHH #使用color[0] = 1, color[1] = 0来区分坐标值的 第一高点
-  JHHG # JHH - ground height
-  Bsize # backbone 点个数

-  joint #截面与backbone相交的右边第一点坐标

-  waist height # 从截面往左0.4m 找寻到最高z值作为waist height
-  waist H # waist height - ground height
-  waistgap # 截面左侧 > 0.5 m

-  withers height # 截面右侧 0.6 -0.8m 找寻到最高z值作为withers height
-  withers H  # withers height - ground height
-  withersgap	 # 最高点x距离截面x + 0.6 距离

-  withers height2 # 截面右侧 0.55 -0.8m 找寻到最高z值作为withers height
-  withers H2	# withers height - ground height
-  withersgap2 # 最高点x距离截面x + 0.6 距离

-  back height # 从截面到截面+ 0.5 中找寻最低z值作为back height
-  back H # back height - ground height
