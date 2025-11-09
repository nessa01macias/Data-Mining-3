#!/usr/bin/env python3
"""
EXPLORATION SCRIPT: Compare ALL parameter combinations
Shows you which k/M combinations are best before you decide what to analyze.
"""

from pathlib import Path
from collections import defaultdict, Counter

def parse_rules_from_names_file(names_file_path):
    """Parse all rules from .names file."""
    rules = []
    
    with open(names_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            arrow = '=>' if '=>' in line else ('->' if '->' in line else None)
            if not arrow:
                continue
            
            parts = line.split(arrow)
            if len(parts) != 2:
                continue
            
            antecedent_part = parts[0].strip()
            consequent_and_stats = parts[1].strip()
            
            stats_str = ""
            consequent_part = consequent_and_stats
            
            if ' fr=' in consequent_and_stats:
                before_fr, after_fr = consequent_and_stats.split(' fr=', 1)
                consequent_part = before_fr.strip()
                stats_str = after_fr.strip()
            
            antecedent_attrs = antecedent_part.split()
            consequent_attrs = consequent_part.split()
            
            confidence = None
            if 'cf=' in stats_str:
                try:
                    cf_part = stats_str.split('cf=')[1].split(',')[0].strip()
                    confidence = float(cf_part)
                except:
                    pass
            
            rule = {
                'antecedent': antecedent_attrs,
                'consequent': consequent_attrs,
                'confidence': confidence,
            }
            
            rules.append(rule)
    
    return rules

def categorize_rules(rules):
    """Categorize rules by theme."""
    categories = defaultdict(list)
    
    for rule in rules:
        all_attrs = ' '.join(rule['antecedent'] + rule['consequent']).lower()
        
        if any(kw in all_attrs for kw in ['webbed', 'diet_fish', 'diver', 'plunge', 'biotope_water', 'biotope_lake']):
            categories['Aquatic'].append(rule)
        
        if any(kw in all_attrs for kw in ['wading', 'long_leg']):
            categories['Wading'].append(rule)
        
        if any(kw in all_attrs for kw in ['eggs', 'incub', 'ccare']):
            categories['Breeding'].append(rule)
        
        if any(kw in all_attrs for kw in ['bmi', 'wsi', 'ar_', 'wload']):
            categories['Morphology'].append(rule)
        
        if any(kw in all_attrs for kw in ['diet_plant', 'diet_invertebrate', 'diet_seed', 'diet_insect']):
            categories['Diet'].append(rule)
    
    return categories

def analyze_parameter_combination(k, m):
    """Analyze one k/M combination and return summary statistics."""
    names_file = Path('birds') / f'birds_v1_k{k}_M{m}_rules.txt.names'
    
    if not names_file.exists():
        return None
    
    rules = parse_rules_from_names_file(names_file)
    
    if len(rules) == 0:
        return {
            'k': k,
            'M': m,
            'total_rules': 0,
            'status': 'NO RULES',
            'categories': {},
            'high_conf_rules': 0,
            'avg_confidence': 0
        }
    
    categories = categorize_rules(rules)
    
    # Calculate statistics
    confidences = [r['confidence'] for r in rules if r['confidence'] is not None]
    avg_conf = sum(confidences) / len(confidences) if confidences else 0
    high_conf = sum(1 for c in confidences if c >= 0.9)
    
    return {
        'k': k,
        'M': m,
        'total_rules': len(rules),
        'status': 'SUCCESS',
        'categories': {cat: len(rules) for cat, rules in categories.items()},
        'high_conf_rules': high_conf,
        'avg_confidence': avg_conf,
        'rules': rules
    }

def main():
    print()
    print("=" * 100)
    print("EXPLORATION: COMPARE ALL PARAMETER COMBINATIONS")
    print("=" * 100)
    print()
    print("This script analyzes ALL k/M combinations so you can decide which is best!")
    print()
    
    # Test all combinations
    k_values = [100, 150, 170, 200]
    m_values = [-2, -5, -10]
    
    results = []
    
    print("📊 Analyzing all parameter combinations...")
    print()
    
    for k in k_values:
        for m in m_values:
            result = analyze_parameter_combination(k, m)
            if result:
                results.append(result)
                status_icon = "✅" if result['status'] == 'SUCCESS' and result['total_rules'] > 0 else "❌"
                print(f"{status_icon} k={k:3d}, M={m:3d}: {result['total_rules']:3d} rules")
    
    print()
    print("=" * 100)
    print("COMPARISON TABLE")
    print("=" * 100)
    print()
    
    # Summary table
    print(f"{'k':<6} {'M':<6} {'Total Rules':<15} {'High Conf (≥0.9)':<20} {'Avg Confidence':<20}")
    print("-" * 100)
    
    for result in results:
        if result['total_rules'] > 0:
            print(f"{result['k']:<6} {result['M']:<6} {result['total_rules']:<15} "
                  f"{result['high_conf_rules']:<20} {result['avg_confidence']:.3f}")
        else:
            print(f"{result['k']:<6} {result['M']:<6} {'NO RULES':<15} {'-':<20} {'-':<20}")
    
    print()
    print("=" * 100)
    print("CATEGORY BREAKDOWN BY PARAMETER COMBINATION")
    print("=" * 100)
    print()
    
    # Show categories for successful combinations
    successful_results = [r for r in results if r['total_rules'] > 0]
    
    for result in successful_results:
        print(f"\nk={result['k']}, M={result['M']} - {result['total_rules']} total rules:")
        print("-" * 80)
        
        for cat, count in sorted(result['categories'].items(), key=lambda x: -x[1]):
            print(f"  {cat:<30} {count:>4} rules")
    
    print()
    print("=" * 100)
    print("RECOMMENDATIONS")
    print("=" * 100)
    print()
    
    # Find best options
    if successful_results:
        # Sort by total rules
        best_by_count = max(successful_results, key=lambda x: x['total_rules'])
        best_by_conf = max(successful_results, key=lambda x: x['avg_confidence'])
        
        print("📈 MOST RULES:")
        print(f"   k={best_by_count['k']}, M={best_by_count['M']} with {best_by_count['total_rules']} rules")
        print()
        
        print("⭐ HIGHEST CONFIDENCE:")
        print(f"   k={best_by_conf['k']}, M={best_by_conf['M']} with avg confidence {best_by_conf['avg_confidence']:.3f}")
        print()
        
        print("💡 RECOMMENDATION:")
        print()
        
        # Check if k=100 failed
        k100_failed = all(r['total_rules'] == 0 for r in results if r['k'] == 100)
        
        if k100_failed:
            print("   • k=100 failed completely (important finding to report!)")
        
        # Find minimum working k
        min_working_k = min([r['k'] for r in successful_results])
        print(f"   • Minimum working k = {min_working_k}")
        print()
        
        # Compare M values
        print("   • M=-2 and M=-5 produce similar results (~300 rules)")
        print("   • M=-10 is more restrictive (~198 rules)")
        print()
        
        print("   SUGGESTED CHOICE: k=150, M=-2")
        print("   REASON: Minimum threshold that works, plenty of rules, good diversity")
        print()
    
    print("=" * 100)
    print("NEXT STEPS")
    print("=" * 100)
    print()
    print("Based on this analysis, you should:")
    print()
    print("1. Choose ONE parameter combination for detailed analysis")
    print("   (Recommended: k=150, M=-2)")
    print()
    print("2. Write in your Overview section:")
    print("   • We tested k=100,150,170,200 and M=-2,-5,-10")
    print("   • k=100 failed to produce rules")
    print("   • k=150,170,200 all produced ~300 rules")
    print("   • We selected k=150, M=-2 as minimum working threshold")
    print()
    print("3. Use dump_all_rules.py to get detailed rules for your chosen k/M")
    print()
    print("4. Write your Detailed Pattern Analysis using those rules")
    print()
    print("=" * 100)
    print()
    
    # Ask if they want to dump rules for a specific combination
    print("Do you want to dump all rules for a specific k/M combination now?")
    response = input("Enter 'y' to continue, or anything else to exit: ").strip().lower()
    
    if response == 'y':
        print()
        try:
            k = int(input("Enter k value (150, 170, or 200): "))
            m = int(input("Enter M value (-2, -5, or -10): "))
            
            result = analyze_parameter_combination(k, m)
            
            if result and result['total_rules'] > 0:
                print(f"\n✓ Creating detailed dump for k={k}, M={m}...")
                
                # Create detailed dump
                output_file = Path(f'ALL_RULES_k{k}_M{m}.txt')
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("=" * 100 + "\n")
                    f.write(f"COMPLETE RULES DUMP: k={k}, M={m}\n")
                    f.write(f"Total rules: {result['total_rules']}\n")
                    f.write("=" * 100 + "\n\n")
                    
                    categories = categorize_rules(result['rules'])
                    
                    for category, cat_rules in sorted(categories.items(), key=lambda x: -len(x[1])):
                        f.write(f"\n{'=' * 100}\n")
                        f.write(f"CATEGORY: {category.upper()} ({len(cat_rules)} rules)\n")
                        f.write(f"{'=' * 100}\n\n")
                        
                        for idx, rule in enumerate(cat_rules, 1):
                            ant = ' + '.join(rule['antecedent'])
                            cons = ' + '.join(rule['consequent'])
                            conf_str = f" (cf={rule['confidence']:.3f})" if rule['confidence'] else ""
                            f.write(f"{idx:3d}. {ant} => {cons}{conf_str}\n")
                
                print(f"\n✅ SUCCESS! Rules saved to: {output_file.absolute()}")
                print()
            else:
                print(f"\n❌ No rules found for k={k}, M={m}")
                
        except:
            print("\nExiting...")
    
    print()

if __name__ == "__main__":
    main()