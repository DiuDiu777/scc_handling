import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# data from previous profiling runs
data = {
    'Benchmark': ['Macro-RealWorld', 'Micro-Phase I', 'Micro-Phase II', 'Micro-Phase III'],
    'Decomposition': [9.48, 10.05, 9.30, 10.99],
    'Constraint':    [27.47, 9.51, 9.01, 34.92],
    'Path Synthesis':[193.38, 56.57, 68.37, 532.67],
    'Alias Comp':    [8791.36, 99.26, 110.78, 543.27],
    'Traversal/Misc':[936.681, 40.92, 47.64, 95.59]
}

df = pd.DataFrame(data)

components = ['Decomposition', 'Constraint', 'Path Synthesis', 'Alias Comp', 'Traversal/Misc']
df['Total'] = df[components].sum(axis=1)
for comp in components:
    df[f'{comp}_Pct'] = (df[comp] / df['Total']) * 100

colors = {
    'Decomposition':  '#455A64',  
    'Constraint':     "#B0330D",  
    'Path Synthesis': "#046F64", 
    'Alias Comp':     "#A6ACE1",  
    'Traversal/Misc': '#CFD8DC',  
}

fig, ax = plt.subplots(figsize=(20, 6))

bar_width = 0.6
indices = np.arange(len(df))
left_bottom = np.zeros(len(df))

plot_order = ['Decomposition', 'Constraint', 'Path Synthesis', 'Alias Comp', 'Traversal/Misc']

for i, comp in enumerate(plot_order):
    values = df[f'{comp}_Pct'].values
    bars = ax.barh(indices, values, left=left_bottom, height=bar_width, 
                   color=colors[comp], edgecolor='white', linewidth=0.8, label=comp)
    
    for j, (bar, val) in enumerate(zip(bars, values)):
        if val < 0.1: continue

        width = bar.get_width()
        x_center = bar.get_x() + width/2
        y_center = bar.get_y() + bar.get_height()/2
        
        text_color = 'white' if i <= 2 else '#222222'

        if val >= 3:
            ax.text(x_center, y_center, f"{int(round(val))}%", 
                    ha='center', va='center', color=text_color, 
                    fontsize=16, fontweight='bold')
        
        else:
            offset_dir = 1 if (i + j) % 2 == 0 else -1
            
            xytext_y = bar.get_y() + bar.get_height() + 0.15 if offset_dir == 1 else bar.get_y() - 0.15
            va_align = 'bottom' if offset_dir == 1 else 'top'
            
            ax.annotate(
                f"{val:.1f}%",
                xy=(x_center, y_center),
                xytext=(x_center, xytext_y),
                arrowprops=dict(arrowstyle='-', color='#444444', linewidth=0.8),
                ha='center', va=va_align,
                fontsize=18, color='#333333', fontweight='bold'
            )

    left_bottom += values

ax.xaxis.grid(False) 
ax.yaxis.grid(False)
ax.set_yticks(indices)
ax.set_yticklabels(df['Benchmark'], fontsize=16, fontweight='bold', rotation=30, ha='right')
ax.set_xlabel('Execution Time Distribution (%)', fontsize=18, fontweight='bold')
ax.set_xlim(0, 100)
ax.set_ylim(-0.6, len(df) - 0.4)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_linewidth(1)

ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.12), ncol=5, frameon=False, fontsize=15)

plt.tight_layout()
# plt.show()
plt.savefig('distribution_chart.pdf', dpi=300)