import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator

df = pd.read_csv('./convergence_results.csv')

df['Benchmark'] = df['Benchmark'].astype(str).str.strip()
df['Method'] = df['Method'].astype(str).str.strip()

sort_order = ['Macro-RealWorld', 'Micro-Phase-I', 'Micro-Phase-II', 'Micro-Phase-III']

df['Benchmark'] = pd.Categorical(df['Benchmark'], categories=sort_order, ordered=True)

sns.set_theme(style="ticks") 
plt.figure(figsize=(7, 5))

palette = {"Ours": "#00897B", "MFP": "#D84315"}

ax = sns.boxplot(
    x="Benchmark", 
    y="Iterations", 
    hue="Method", 
    data=df,
    palette=palette, 
    width=0.6,     
    linewidth=1.2, 
    fliersize=3,
    dodge=True       
)

ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='gray')
ax.set_xlabel("Benchmark Suite", fontsize=15, fontweight='bold')
ax.set_ylabel("Iterations to Fixpoint ($k$)", fontsize=15, fontweight='bold')

plt.legend(title="", loc='upper left', frameon=True, fontsize=14, 
           bbox_to_anchor=(0.02, 0.98))

sns.despine(trim=True)
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

plt.tight_layout()
plt.show()
plt.savefig('full_convergence_comparison_fixed.pdf', dpi=300)