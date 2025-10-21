#!/bin/bash

# 测试参数
sizes=(16 32 64 128 192 256 320)
executable="./build/dist/bins/lab2_gemm_opt_prefetch"
final_results_file="final_results.txt"

# 清空结果文件
> $final_results_file

echo "开始运行测试..."

# 遍历所有n, k, m组合
for n in "${sizes[@]}"; do
  for k in "${sizes[@]}"; do
    for m in "${sizes[@]}"; do
      echo "测试 n=$n, k=$k, m=$m"
      echo "n=$n, k=$k, m=$m" >> $final_results_file

      # 存储10次测试结果
      declare -a results

      # 运行10次测试
      for i in {1..10}; do
        # 运行测试并提取性能差异值
        result=$($executable $n $k $m | grep "Performance difference(Gflops)" | awk '{print $3}')
        results+=($result)
        echo "  运行 $i: $result"
      done

      # 对结果进行排序
      IFS=$'\n' sorted_results=($(sort -g <<<"${results[*]}"))
      unset IFS

      # 删除2个极值（第一个和最后一个）
      trimmed_results=("${sorted_results[@]:1:8}")

      # 计算平均值
      sum=0
      for val in "${trimmed_results[@]}"; do
        sum=$(echo "$sum + $val" | bc -l)
      done
      average=$(echo "scale=8; $sum / 10" | bc -l)

      echo "  平均性能 (去除极值后): $average Gflops"
      echo "  平均性能: $average Gflops" >> $final_results_file
      echo "" >> $final_results_file

      # 清理数组
      unset results
      unset sorted_results
      unset trimmed_results
    done
  done
done

echo "所有测试完成，最终结果保存在 $final_results_file"