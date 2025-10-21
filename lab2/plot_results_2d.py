import numpy as np
import matplotlib.pyplot as plt
import re

# 读取数据
def read_results(filename):
    data = []
    with open(filename, 'r') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        if lines[i].startswith('n='):
            # 解析 n, k, m 值
            n, k, m = map(int, re.findall(r'\d+', lines[i]))
            i += 1
            # 解析性能值
            if i < len(lines) and '平均性能:' in lines[i]:
                perf_str = lines[i].split('平均性能:')[1].strip().replace(' Gflops', '')
                try:
                    perf = float(perf_str)
                    data.append((n, k, m, perf))
                except ValueError:
                    # 如果无法解析性能值，使用默认值
                    data.append((n, k, m, 0.0))
            i += 1
        else:
            i += 1

    return data

# 绘制2D图
def plot_2d_performance(data):
    # 提取数据
    n_vals = np.array([d[0] for d in data])
    k_vals = np.array([d[1] for d in data])
    m_vals = np.array([d[2] for d in data])
    perf_vals = np.array([d[3] for d in data])

    # 创建图形
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Matrix Multiplication Performance Analysis', fontsize=16)

    # 第一个图：N-K平面，颜色表示性能，点大小表示M值
    scatter1 = axes[0, 0].scatter(n_vals, k_vals, c=perf_vals, cmap='RdYlBu_r', s=m_vals/5, alpha=0.7)
    axes[0, 0].set_xlabel('M dimension')
    axes[0, 0].set_ylabel('K dimension')
    axes[0, 0].set_title('Performance vs M and K (point size = M)')
    axes[0, 0].grid(True, alpha=0.3)
    plt.colorbar(scatter1, ax=axes[0, 0], label='Performance (Gflops)')

    # 第二个图：N-M平面，颜色表示性能，点大小表示K值
    scatter2 = axes[0, 1].scatter(n_vals, m_vals, c=perf_vals, cmap='RdYlBu_r', s=k_vals/5, alpha=0.7)
    axes[0, 1].set_xlabel('M dimension')
    axes[0, 1].set_ylabel('N dimension')
    axes[0, 1].set_title('Performance vs M and N (point size = K)')
    axes[0, 1].grid(True, alpha=0.3)
    plt.colorbar(scatter2, ax=axes[0, 1], label='Performance (Gflops)')

    # 第三个图：K-M平面，颜色表示性能，点大小表示N值
    scatter3 = axes[1, 0].scatter(k_vals, m_vals, c=perf_vals, cmap='RdYlBu_r', s=n_vals/5, alpha=0.7)
    axes[1, 0].set_xlabel('K dimension')
    axes[1, 0].set_ylabel('N dimension')
    axes[1, 0].set_title('Performance vs K and N (point size = N)')
    axes[1, 0].grid(True, alpha=0.3)
    plt.colorbar(scatter3, ax=axes[1, 0], label='Performance (Gflops)')

    # 第四个图：3D散点图，显示所有三个维度
    ax3d = fig.add_subplot(2, 2, 4, projection='3d')
    colors = ['red' if p < 0 else 'blue' for p in perf_vals]
    scatter4 = ax3d.scatter(n_vals, k_vals, m_vals, c=perf_vals, cmap='RdYlBu_r', s=50, alpha=0.7)
    ax3d.set_xlabel('M dimension')
    ax3d.set_ylabel('K dimension')
    ax3d.set_zlabel('N dimension')
    ax3d.set_title('M-K-N dimensions (color = Performance)')
    plt.colorbar(scatter4, ax=ax3d, label='Performance (Gflops)')

    plt.tight_layout()
    plt.savefig('performance_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

    # 打印一些统计信息
    print(f"Total data points: {len(data)}")
    print(f"Max performance: {max(perf_vals):.6f} Gflops")
    print(f"Min performance: {min(perf_vals):.6f} Gflops")
    print(f"Average performance: {np.mean(perf_vals):.6f} Gflops")

    # 找到最佳性能的参数
    max_idx = np.argmax(perf_vals)
    print(f"Best performance at m={n_vals[max_idx]}, k={k_vals[max_idx]}, n={m_vals[max_idx]}: {perf_vals[max_idx]:.6f} Gflops")

# 主函数
if __name__ == "__main__":
    # 读取数据
    data = read_results('final_results.txt')

    # 绘制图
    if data:
        plot_2d_performance(data)
    else:
        print("No data found in the results file.")