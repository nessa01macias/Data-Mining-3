#!/usr/bin/env python3
"""
RAW DATA DUMP: All Bird Association Rules by Category
Shows EVERYTHING so you can manually pick the best rules for your report.
"""

from pathlib import Path
from collections import defaultdict

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
            
            # Parse stats
            stats_str = ""
            consequent_part = consequent_and_stats
            
            if ' fr=' in consequent_and_stats:
                before_fr, after_fr = consequent_and_stats.split(' fr=', 1)
                consequent_part = before_fr.strip()
                stats_str = after_fr.strip()
            
            antecedent_attrs = antecedent_part.split()
            consequent_attrs = consequent_part.split()
            
            # Extract confidence
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
                'raw_line': line
            }
            
            rules.append(rule)
    
    return rules

def categorize_rules(rules):
    """Categorize each rule into themes."""
    categories = defaultdict(list)
    
    for rule in rules:
        all_attrs = ' '.join(rule['antecedent'] + rule['consequent']).lower()
        
        # Aquatic and diving
        if any(kw in all_attrs for kw in ['webbed', 'diet_fish', 'diver', 'plunge', 'biotope_water', 'biotope_lake']):
            categories['Aquatic and Diving Birds'].append(rule)
        
        # Wading birds
        if any(kw in all_attrs for kw in ['wading', 'long_leg']):
            categories['Wading Birds'].append(rule)
        
        # Breeding and parental care
        if any(kw in all_attrs for kw in ['eggs', 'incub', 'ccare', 'nest']):
            categories['Breeding and Parental Care'].append(rule)
        
        # Morphological features
        if any(kw in all_attrs for kw in ['bmi', 'wsi', 'ar_', 'wload']):
            categories['Morphological Patterns'].append(rule)
        
        # Diet patterns
        if any(kw in all_attrs for kw in ['diet_plant', 'diet_invertebrate', 'diet_seed', 'diet_insect']):
            categories['Diet Patterns'].append(rule)
        
        # Migration
        if any(kw in all_attrs for kw in ['arrive', 'leave']):
            categories['Migration Patterns'].append(rule)
        
        # Color
        if any(kw in all_attrs for kw in ['back_', 'belly_', 'legcol', 'billcol']):
            categories['Color and Plumage'].append(rule)
    
    return categories

def format_rule_readable(rule, index):
    """Format rule in readable way with index."""
    ant = ' + '.join(rule['antecedent'])
    cons = ' + '.join(rule['consequent'])
    conf_str = f" (cf={rule['confidence']:.3f})" if rule['confidence'] else ""
    
    return f"{index:3d}. {ant} => {cons}{conf_str}"

def dump_all_categories_to_file(categories, output_path, total_rules):
    """Write complete category breakdown to file."""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("COMPLETE RAW DATA DUMP: ALL BIRD ASSOCIATION RULES BY CATEGORY\n")
        f.write("=" * 100 + "\n")
        f.write(f"\nTotal rules analyzed: {total_rules}\n")
        f.write("\nNOTE: Rules can appear in multiple categories if they involve multiple themes.\n")
        f.write("      Use this to manually select the BEST and MOST DIVERSE rules for your report.\n")
        f.write("\n" + "=" * 100 + "\n\n")
        
        # Sort categories by size
        sorted_cats = sorted(categories.items(), key=lambda x: -len(x[1]))
        
        for category, cat_rules in sorted_cats:
            f.write("\n" + "=" * 100 + "\n")
            f.write(f"CATEGORY: {category.upper()}\n")
            f.write(f"Total rules: {len(cat_rules)}\n")
            f.write("=" * 100 + "\n\n")
            
            # Write all rules in this category
            for idx, rule in enumerate(cat_rules, 1):
                f.write(format_rule_readable(rule, idx) + "\n")
            
            f.write("\n")
        
        # Summary at the end
        f.write("\n" + "=" * 100 + "\n")
        f.write("SUMMARY: CATEGORY SIZES\n")
        f.write("=" * 100 + "\n\n")
        
        for category, cat_rules in sorted_cats:
            f.write(f"{category:<40} {len(cat_rules):>4} rules\n")
        
        f.write("\n" + "=" * 100 + "\n")

def main():
    print()
    print("=" * 100)
    print("RAW DATA DUMP: ALL RULES BY CATEGORY")
    print("=" * 100)
    print()
    
    # Get parameters
    try:
        k = int(input("Enter k value (150, 170, or 200): "))
        m = int(input("Enter M value (-2, -5, or -10): "))
    except:
        print("\nUsing defaults: k=150, M=-2")
        k, m = 150, -2
    
    print(f"\n✓ Loading rules for k={k}, M={m}")
    
    # Find file
    names_file = Path('birds') / f'birds_v1_k{k}_M{m}_rules.txt.names'
    
    if not names_file.exists():
        print(f"❌ ERROR: Could not find {names_file}")
        return
    
    print(f"✓ Found: {names_file.name}")
    print("📖 Reading all rules...")
    
    # Parse all rules
    rules = parse_rules_from_names_file(names_file)
    print(f"✓ Parsed {len(rules)} rules")
    
    # Categorize
    print("📊 Categorizing rules...")
    categories = categorize_rules(rules)
    
    print(f"✓ Categorized into {len(categories)} themes\n")
    print("Category breakdown:")
    for cat, cat_rules in sorted(categories.items(), key=lambda x: -len(x[1])):
        print(f"  • {cat:<40} {len(cat_rules):>4} rules")
    
    # Dump to file
    output_file = Path('ALL_RULES_BY_CATEGORY.txt')
    print(f"\n📝 Writing complete data dump to: {output_file}")
    
    dump_all_categories_to_file(categories, output_file, len(rules))
    
    print()
    print("=" * 100)
    print(f"✅ SUCCESS! Complete data written to: {output_file.absolute()}")
    print("=" * 100)
    print()
    print("WHAT TO DO NOW:")
    print()
    print("1. OPEN the file in a text editor")
    print("   • You'll see ALL rules organized by category")
    print("   • Each category lists every single rule that belongs to it")
    print()
    print("2. READ through each category")
    print("   • Look for interesting patterns")
    print("   • Note which rules are most meaningful biologically")
    print("   • Identify diverse examples (not just variations of same pattern)")
    print()
    print("3. MANUALLY SELECT 3-5 best rules per category")
    print("   • Choose rules that:")
    print("     - Show different aspects of the category")
    print("     - Have high confidence values")
    print("     - Make biological sense")
    print("     - Are interesting/surprising")
    print()
    print("4. WRITE your Results section")
    print("   • Use your selected rules as examples")
    print("   • Explain WHY each rule is interesting")
    print("   • Connect to biological theory")
    print()
    print("5. (Optional) Use the automated script later for formatting help")
    print()
    print("=" * 100)
    print()
    print("TIP: Search the file for specific keywords to find related rules:")
    print("     - 'fish' - all fish-related rules")
    print("     - 'egg' - all egg/clutch size rules")
    print("     - 'cf=1.000' - all perfect confidence rules")
    print()
    print("=" * 100)
    print()

if __name__ == "__main__":
    main()