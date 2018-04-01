---
title: Spark算子之TransFormation
comments: true
date: 2018-2-2
keywords: Spark,TransFormation,算子

tags:
- Spark
- BigData
categories:
- technology

---

- Spark算子分为 Transformations | Action 两类
- Transformations 为懒加载，只记录元数据，并不触发计算行为
- Action 将触发计算行为
> [官方文档](http://spark.apache.org/docs/latest/rdd-programming-guide.html)

WordCount e.g. 

- 目标 : 实现从hdfs中读取一组文件，统计其中单词出现的次数
- 步骤 :
1. 创建words.txt单词源文件,并将words.txt放入hdfs的/wc下
```
[root@server01 tmp]# cat words.txt
hello tom
hello abel
hello pro
hello tom
hello xml
[root@server01 tmp]# hadoop dfs -mkdir /wc
[root@server01 tmp]# hadoop dfs -put words.txt /wc/1.log
[root@server01 tmp]# hadoop dfs -put words.txt /wc/2.log
[root@server01 tmp]# hadoop dfs -put words.txt /wc/3.log
```
2. 启动spark-shell
```
[root@server01 tmp]# /apps/spark-2.2.1-bin-hadoop2.7/bin/spark-shell --master spark://server01:7077
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
18/02/02 10:53:46 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Spark context Web UI available at http://192.168.0.201:4040
Spark context available as 'sc' (master = spark://server01:7077, app id = app-20180202105348-0002).
Spark session available as 'spark'.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 2.2.1
      /_/

Using Scala version 2.11.8 (Java HotSpot(TM) 64-Bit Server VM, Java 1.8.0_151)
Type in expressions to have them evaluated.
Type :help for more information.

scala>
```
3. 输入单词统计逻辑(Scala),得到返回结果
```
scala> sc.textFile("hdfs://server01:9000/wc").flatMap(_.split(" ")).map((_,1)).reduceByKey(_+_).sortBy(_._2,false).collect
res0: Array[(String, Int)] = Array((hello,15), (tom,6), (pro,3), (xml,3), (abel,3))
```
4. 逻辑分解
这里返回了一个RDD类型的数组,但并没有真正去读取数据，只是记录的源文件的位置信息
```
scala> sc.textFile("hdfs://server01:9000/wc")
res1: org.apache.spark.rdd.RDD[String] = hdfs://server01:9000/wc MapPartitionsRDD[11] at textFile at <console>:25
```
	在经历了flatMap,map,reduceByKey,sortBy后仍没有真正进行计算
```
scala> sc.textFile("hdfs://server01:9000/wc").flatMap(_.split(" ")).map((_,1)).reduceByKey(_+_).sortBy(_._2,false)
res2: org.apache.spark.rdd.RDD[(String, Int)] = MapPartitionsRDD[28] at sortBy at <console>:25
```
	可以看到当进行collect的时候，真正进行的计算
```
scala> res2.collect
res3: Array[(String, Int)] = Array((hello,15), (tom,6), (pro,3), (xml,3), (abel,3))
```
	这是因为flatMap,map,reduceByKey,sortBy都是Transformation,是懒加载的，而collect是Action，能够触发计算行为

## Transformations

1. map(func) 
> Return a new distributed dataset formed by passing each element of the source through a function func.
```
scala> val rdd1 = sc.parallelize(List(5,6,4,7,3,8,2,9,1,10)).map(_*2)
rdd1: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[1] at map at <console>:24

scala> rdd1.collect
res0: Array[Int] = Array(10, 12, 8, 14, 6, 16, 4, 18, 2, 20)
```
2. filter(func)
> Return a new dataset formed by selecting those elements of the source on which func returns true.
```
scala> val rdd2 = rdd1.filter(_>10)
rdd2: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[2] at filter at <console>:26

scala> rdd2.collect
res1: Array[Int] = Array(12, 14, 16, 18, 20)
```
3. flatMap(func)
> Similar to map, but each input item can be mapped to 0 or more output items (so func should return a Seq rather than a single item).
```
scala> val rdd3 = sc.parallelize(Array("a b c", "d e f", "h i j"))
rdd3: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[3] at parallelize at <console>:24

scala> rdd3.flatMap(_.split(' ')).collect
res2: Array[String] = Array(a, b, c, d, e, f, h, i, j)

scala> val rdd4 = sc.parallelize(List(List("a b c", "a b b"),List("e f g", "a f g"), List("h i j", "a a b")))
rdd4: org.apache.spark.rdd.RDD[List[String]] = ParallelCollectionRDD[5] at parallelize at <console>:24

scala> rdd4.flatMap(_.flatMap(_.split(" "))).collect
res4: Array[String] = Array(a, b, c, a, b, b, e, f, g, a, f, g, h, i, j, a, a, b)
```
4. union(otherDataset)
> Return a new dataset that contains the union of the elements in the source dataset and the argument.
**Note:类型要一致**
```
scala> val rdd5 = sc.parallelize(List(5,6,4,7))
rdd5: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[7] at parallelize at <console>:24

scala> val rdd6 = sc.parallelize(List(1,2,3,4))
rdd6: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[8] at parallelize at <console>:24

scala> val rdd7 = rdd5 union rdd6
rdd7: org.apache.spark.rdd.RDD[Int] = UnionRDD[9] at union at <console>:28

scala> rdd7.distinct.sortBy(x=>x).collect
res5: Array[Int] = Array(1, 2, 3, 4, 5, 6, 7)
```
5. intersection(otherDataset)
> Return a new RDD that contains the intersection of elements in the source dataset and the argument.
```
scala> val rdd8 = rdd5 intersection rdd6
rdd8: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[32] at intersection at <console>:28

scala> rdd8.collect
res7: Array[Int] = Array(4)
```
6. join(otherDataset, [numTasks])
> When called on datasets of type (K, V) and (K, W), returns a dataset of (K, (V, W)) pairs with all pairs of elements for each key. Outer joins are supported through leftOuterJoin, rightOuterJoin, and fullOuterJoin.
```
scala> val rdd1 = sc.parallelize(List(("tom", 1), ("jerry", 2), ("kitty", 3)))
rdd1: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[33] at parallelize at <console>:24

scala> val rdd2 = sc.parallelize(List(("jerry", 9), ("tom", 8), ("shuke", 7)))
rdd2: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[34] at parallelize at <console>:24

scala> val rdd3 = rdd1.join(rdd2)
rdd3: org.apache.spark.rdd.RDD[(String, (Int, Int))] = MapPartitionsRDD[37] at join at <console>:28

scala> rdd3.collect
res8: Array[(String, (Int, Int))] = Array((tom,(1,8)), (jerry,(2,9)))
```
7. groupByKey([numTasks])
> When called on a dataset of (K, V) pairs, returns a dataset of (K, Iterable<V>) pairs.Note: If you are grouping in order to perform an aggregation (such as a sum or average) over each key, using reduceByKey or aggregateByKey will yield much better performance.Note: By default, the level of parallelism in the output depends on the number of partitions of the parent RDD. You can pass an optional numTasks argument to set a different number of tasks.
```
scala> val rdd3 = rdd1 union rdd2
rdd3: org.apache.spark.rdd.RDD[(String, Int)] = UnionRDD[38] at union at <console>:28

scala> rdd3.groupByKey.collect
res11: Array[(String, Iterable[Int])] = Array((tom,CompactBuffer(1, 8)), (jerry,CompactBuffer(2, 9)), (shuke,CompactBuffer(7)), (kitty,CompactBuffer(3)))

scala> rdd3.groupByKey.map(x=>(x._1,x._2.sum)).collect
res12: Array[(String, Int)] = Array((tom,9), (jerry,11), (shuke,7), (kitty,3))
```
8. cogroup(otherDataset, [numTasks])
> When called on datasets of type (K, V) and (K, W), returns a dataset of (K, (Iterable<V>, Iterable<W>)) tuples. This operation is also called groupWith. 
```
scala> val rdd1 = sc.parallelize(List(("tom", 1), ("tom", 2), ("jerry", 3), ("kitty", 2)))
rdd1: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[43] at parallelize at <console>:24

scala> val rdd2 = sc.parallelize(List(("jerry", 2), ("tom", 1), ("shuke", 2)))
rdd2: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[44] at parallelize at <console>:24

scala> val rdd3 = rdd1.cogroup(rdd2)
rdd3: org.apache.spark.rdd.RDD[(String, (Iterable[Int], Iterable[Int]))] = MapPartitionsRDD[46] at cogroup at <console>:28

scala> rdd3.collect
res13: Array[(String, (Iterable[Int], Iterable[Int]))] = Array((tom,(CompactBuffer(1, 2),CompactBuffer(1))), (jerry,(CompactBuffer(3),CompactBuffer(2))), (shuke,(CompactBuffer(),CompactBuffer(2))), (kitty,(CompactBuffer(2),CompactBuffer())))

scala> rdd3.map(t=>(t._1, t._2._1.sum + t._2._2.sum)).collect
res14: Array[(String, Int)] = Array((tom,4), (jerry,5), (shuke,2), (kitty,2))
```
9. cartesian(otherDataset)
> When called on datasets of types T and U, returns a dataset of (T, U) pairs (all pairs of elements).
```
scala> val rdd1 = sc.parallelize(List("tom", "jerry"))
rdd1: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[48] at parallelize at <console>:24

scala> val rdd2 = sc.parallelize(List("tom", "kitty", "shuke"))
rdd2: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[49] at parallelize at <console>:24

scala> rdd1.cartesian(rdd2).collect
res15: Array[(String, String)] = Array((tom,tom), (tom,kitty), (tom,shuke), (jerry,tom), (jerry,kitty), (jerry,shuke))
```
