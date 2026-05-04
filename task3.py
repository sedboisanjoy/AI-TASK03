# ---------------------------------------------------------
# Q3: Restaurant Wait Problem - Complete Table + Tree Image
# ---------------------------------------------------------
import math
import pprint

# Try to import matplotlib for plotting
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Installing matplotlib may be needed for tree image.")
    print("Run: pip install matplotlib")

# Dataset: [Alternate, Bar, Fri/Sat, Hungry, Patrons, Price, Rain, Res, Type, Est, Wait?]
dataset = [
    ['Yes', 'No', 'No', 'Yes', 'Some', '$$$', 'No', 'Yes', 'French', '0-10', 'Yes'],
    ['Yes', 'No', 'No', 'Yes', 'Full', '$', 'No', 'No', 'Thai', '30-60', 'No'],
    ['No', 'Yes', 'No', 'No', 'Some', '$', 'No', 'No', 'Burger', '0-10', 'Yes'],
    ['Yes', 'No', 'Yes', 'Yes', 'Full', '$', 'Yes', 'No', 'Thai', '10-30', 'Yes'],
    ['Yes', 'No', 'Yes', 'No', 'Full', '$$$', 'No', 'Yes', 'French', '>60', 'No'],
    ['No', 'Yes', 'No', 'Yes', 'Some', '$$', 'Yes', 'Yes', 'Italian', '0-10', 'Yes'],
    ['No', 'Yes', 'No', 'No', 'None', '$', 'Yes', 'No', 'Burger', '0-10', 'No'],
    ['No', 'No', 'No', 'Yes', 'Some', '$$', 'Yes', 'Yes', 'Thai', '0-10', 'Yes'],
    ['No', 'Yes', 'Yes', 'No', 'Full', '$', 'Yes', 'No', 'Burger', '>60', 'No'],
    ['Yes', 'Yes', 'Yes', 'Yes', 'Full', '$$$', 'No', 'Yes', 'Italian', '10-30', 'No'],
    ['No', 'No', 'No', 'No', 'None', '$', 'No', 'No', 'Thai', '0-10', 'No'],
    ['Yes', 'Yes', 'Yes', 'Yes', 'Full', '$', 'No', 'No', 'Burger', '30-60', 'Yes']
]

features = ['Alternate', 'Bar', 'Fri/Sat', 'Hungry', 'Patrons', 'Price', 'Rain', 'Res', 'Type', 'Est']

def entropy(data):
    """Calculate entropy."""
    results = [row[-1] for row in data]
    if not results:
        return 0.0
    p_yes = results.count('Yes') / len(results)
    p_no = results.count('No') / len(results)
    ent = 0.0
    if p_yes > 0:
        ent -= p_yes * math.log2(p_yes)
    if p_no > 0:
        ent -= p_no * math.log2(p_no)
    return ent

def split_data(data, col_index, value):
    """Filter data where column matches value, remove that column."""
    return [row[:col_index] + row[col_index+1:] for row in data if row[col_index] == value]

def build_tree(data, feature_names):
    """Build decision tree recursively."""
    results = [row[-1] for row in data]
    
    # Base cases
    if results.count(results[0]) == len(results):
        return results[0]
    if len(data[0]) == 1:
        return max(set(results), key=results.count)
    
    # Find best split
    base_ent = entropy(data)
    best_gain = -1
    best_col = -1
    
    for col in range(len(data[0]) - 1):
        values = set(row[col] for row in data)
        new_ent = 0.0
        for val in values:
            subset = [r for r in data if r[col] == val]
            new_ent += (len(subset) / len(data)) * entropy(subset)
        gain = base_ent - new_ent
        if gain > best_gain:
            best_gain = gain
            best_col = col
    
    best_feature = feature_names[best_col]
    tree = {best_feature: {}}
    values = set(row[best_col] for row in data)
    new_features = feature_names[:best_col] + feature_names[best_col+1:]
    
    for val in values:
        subset = split_data(data, best_col, val)
        tree[best_feature][val] = build_tree(subset, new_features)
    
    return tree

# ============================================================
# MAIN: Print Table and Plot Tree
# ============================================================

if __name__ == "__main__":
    total_rows = len(dataset)
    base_ent = entropy(dataset)
    
    # Count total Yes/No
    results = [row[-1] for row in dataset]
    total_yes = results.count('Yes')
    total_no = results.count('No')
    
    print("\n" + "="*100)
    print("BASE ENTROPY")
    print("="*100)
    print(f"Total rows: {total_rows} | Yes: {total_yes} | No: {total_no}")
    print(f"p(Yes) = {total_yes}/{total_rows} = {total_yes/total_rows:.3f}")
    print(f"p(No) = {total_no}/{total_rows} = {total_no/total_rows:.3f}")
    print(f"\nBase Entropy = -{total_yes/total_rows:.3f}×log₂({total_yes/total_rows:.3f}) - {total_no/total_rows:.3f}×log₂({total_no/total_rows:.3f})")
    print(f"             = {base_ent:.4f}\n")
    
    # ============================================================
    # ONE COMPLETE TABLE
    # ============================================================
    print("="*100)
    print("COMPLETE INFORMATION GAIN TABLE")
    print("="*100)
    print(f"\n{'Feature':<15} {'Value':<12} {'Count':<6} {'Yes':<5} {'No':<5} {'Entropy':<10} {'Weight':<10} {'Weighted':<12} {'Gain':<10}")
    print(f"{'-'*100}")
    
    gains_list = []
    num_cols = len(dataset[0]) - 1
    
    for col in range(num_cols):
        feature = features[col]
        values = sorted(set(row[col] for row in dataset))
        feature_weighted_total = 0
        
        for val in values:
            subset = [row for row in dataset if row[col] == val]
            subset_size = len(subset)
            weight = subset_size / total_rows
            
            subset_results = [row[-1] for row in subset]
            subset_yes = subset_results.count('Yes')
            subset_no = subset_results.count('No')
            
            if subset_yes == 0 or subset_no == 0:
                subset_entropy = 0.0
            else:
                p_yes = subset_yes / subset_size
                p_no = subset_no / subset_size
                subset_entropy = -p_yes * math.log2(p_yes) - p_no * math.log2(p_no)
            
            weighted_entropy = weight * subset_entropy
            feature_weighted_total += weighted_entropy
            
            print(f"{feature:<15} {val:<12} {subset_size:<6} {subset_yes:<5} {subset_no:<5} {subset_entropy:<10.4f} {weight:<10.4f} {weighted_entropy:<12.4f} -")
        
        gain = base_ent - feature_weighted_total
        gains_list.append((feature, gain))
        
        # Print summary row for this feature
        print(f"{'-'*100}")
        print(f"{feature:<15} {'TOTAL':<12} {total_rows:<6} {total_yes:<5} {total_no:<5} {feature_weighted_total:<10.4f} {1.0:<10.4f} {feature_weighted_total:<12.4f} {gain:<10.4f}")
        print(f"{'-'*100}")
    
    # ============================================================
    # RANKING BY GAIN
    # ============================================================
    print("\n" + "="*100)
    print("RANKING BY INFORMATION GAIN")
    print("="*100)
    gains_sorted = sorted(gains_list, key=lambda x: x[1], reverse=True)
    for rank, (feature, gain) in enumerate(gains_sorted, 1):
        print(f"{rank}. {feature:<15} Gain = {gain:.4f}")
    
    print(f"\n✅ BEST FEATURE: {gains_sorted[0][0]} (Gain = {gains_sorted[0][1]:.4f})")
    
    # ============================================================
    # BUILD AND PRINT TREE
    # ============================================================
    print("\n" + "="*100)
    print("DECISION TREE (Dictionary Format)")
    print("="*100)
    tree = build_tree(dataset, features)
    pprint.pprint(tree, width=50)
    
    # ============================================================
    # PLOT TREE IMAGE
    # ============================================================
    if MATPLOTLIB_AVAILABLE:
        print("\n" + "="*100)
        print("PLOTTING DECISION TREE...")
        print("="*100)
        
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.axis('off')
        
        node_colors = {
            'feature': dict(boxstyle="square,pad=0.3", fc="lightyellow", ec="orange", lw=2),
            'wait': dict(boxstyle="round,pad=0.3", fc="lightgreen", ec="darkgreen", lw=2),
            'leave': dict(boxstyle="round,pad=0.3", fc="lightcoral", ec="darkred", lw=2)
        }
        
        def draw_node(node, x, y, x_offset, y_offset):
            if isinstance(node, dict):
                feature = list(node.keys())[0]
                ax.text(x, y, feature, ha='center', va='center', 
                       bbox=node_colors['feature'], fontsize=11, weight='bold')
                
                branches = node[feature]
                n_branches = len(branches)
                start_x = x - x_offset * (n_branches - 1) / 2
                
                for i, (val, child) in enumerate(branches.items()):
                    child_x = start_x + i * x_offset
                    child_y = y - y_offset
                    
                    ax.annotate('', xy=(child_x, child_y - 0.02), xytext=(x, y - 0.05),
                               arrowprops=dict(arrowstyle='-', color='gray', lw=1.5))
                    ax.text((x + child_x)/2, (y + child_y)/2 + 0.02, str(val), 
                           ha='center', va='center', fontsize=8, bbox=dict(fc='white', ec='none', pad=1))
                    
                    if isinstance(child, dict):
                        draw_node(child, child_x, child_y, x_offset / 1.5, y_offset)
                    else:
                        decision_text = "WAIT" if child == 'Yes' else "LEAVE"
                        color = node_colors['wait'] if child == 'Yes' else node_colors['leave']
                        ax.text(child_x, child_y, decision_text, ha='center', va='center',
                               bbox=color, fontsize=10, weight='bold')
        
        draw_node(tree, 0.5, 0.9, 0.4, 0.15)
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.0)
        plt.title("Restaurant Waiting Decision Tree\n(Based on Entropy & Information Gain)", 
                  fontsize=16, weight='bold')
        
        legend_elements = [
            plt.Rectangle((0,0), 1, 1, facecolor='lightyellow', edgecolor='orange', label='Question/Feature'),
            plt.Rectangle((0,0), 1, 1, facecolor='lightgreen', edgecolor='darkgreen', label='Decision: WAIT'),
            plt.Rectangle((0,0), 1, 1, facecolor='lightcoral', edgecolor='darkred', label='Decision: LEAVE')
        ]
        ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.08), ncol=3, fontsize=9)
        
        plt.tight_layout()
        plt.savefig("decision_tree.png", dpi=150, bbox_inches='tight')
        print("\n✅ Tree image saved as 'decision_tree.png'")
        plt.show()
    else:
        print("\n⚠️ matplotlib not installed. To get tree image, run: pip install matplotlib")
    
    print("\n" + "="*100)
    print("✅ DONE! Check 'decision_tree.png' for the tree image.")
    print("="*100)
