#!/usr/bin/env python3
"""
SUPER SIMPLE SCRIPT: Just show me what's in the rule files!
No fancy analysis, just print the rules in plain English.
"""

from pathlib import Path

def show_rules_simple(k=150, m=-2, max_rules=10):
    """
    Show the first few rules from a rule file in readable format.
    """
    print("=" * 80)
    print(f"SHOWING RULES FOR k={k}, M={m}")
    print("=" * 80)
    print()
    
    # File paths
    rules_file = Path('birds') / f'birds_v1_k{k}_M{m}_rules.txt'
    names_file = Path('birds') / f'birds_v1_k{k}_M{m}_rules.txt.names'
    
    # Check if files exist
    if not rules_file.exists():
        print(f"❌ ERROR: Could not find {rules_file}")
        print(f"   Make sure you're running this from the hwk3 directory!")
        return
    
    if not names_file.exists():
        print(f"❌ ERROR: Could not find {names_file}")
        return
    
    print("✓ Files found!")
    print()
    
    # Decide which file to read rules from:
    # - Prefer the human-readable .names file when it actually contains rules
    # - Fallback to the numeric rules file otherwise
    def file_has_rules(path: Path) -> bool:
        if not path.exists():
            return False
        try:
            with open(path, 'r') as rf:
                for l in rf:
                    s = l.strip()
                    if s and not s.startswith('#') and ('->' in s or '=>' in s):
                        return True
        except Exception:
            return False
        return False
    
    if file_has_rules(names_file):
        rules_source = names_file
        print(f"📖 Using human-readable rules from: {names_file.name}")
    else:
        rules_source = rules_file
        print(f"📖 Using numeric rules from: {rules_file.name}")
    print()
    
    # Read and display rules
    print(f"📋 Step 2: Reading rules (showing first {max_rules})...")
    print()
    
    rule_count = 0
    with open(rules_source, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            rule_count += 1
            
            if rule_count > max_rules:
                break
            
            # Parse the rule (supports both "antecedent => consequent [stats]" and "antecedent -> consequent fr=... ...")
            arrow = '=>' if '=>' in line else ('->' if '->' in line else None)
            if not arrow:
                continue
            parts = line.split(arrow)
            antecedent = parts[0].strip()
            rest = parts[1].strip()
            
            # Separate consequent from statistics
            # Heuristic: if we see ' fr=' metrics, treat everything after consequent token as stats
            stats = ""
            consequent = rest
            if ' fr=' in rest:
                # consequent is up to the token right before 'fr='
                before_fr, after_fr = rest.split(' fr=', 1)
                consequent = before_fr.strip()
                stats = 'fr=' + after_fr.strip()
            elif '[' in rest and ']' in rest:
                consequent = rest.split('[')[0].strip()
                stats = rest.split('[', 1)[1].rsplit(']', 1)[0].strip()
            else:
                # Fallback: consequent is first token, the rest are stats
                rest_parts = rest.split()
                consequent = rest_parts[0] if rest_parts else ""
                stats = ' '.join(rest_parts[1:]) if len(rest_parts) > 1 else ""
            
            ant_names = antecedent.split()
            cons_names = consequent.split()
            
            # Print in readable format
            print(f"Rule {rule_count}:")
            print(f"  IF a bird has:")
            for name in ant_names:
                print(f"    • {name}")
            print(f"  THEN it typically also has:")
            for name in cons_names:
                print(f"    • {name}")
            if stats:
                print(f"  Statistics: {stats}")
            print()
    
    print("=" * 80)
    print(f"SUMMARY: Found {rule_count} rules in this file")
    print("=" * 80)
    print()
    print("💡 TIP: These rules are what you'll write about in your Results section!")
    print("   Look for patterns like:")
    print("   - Multiple rules about the same bird group")
    print("   - Rules connecting body features to behaviors")
    print("   - Rules about habitat and diet")
    print()

def compare_all_parameters():
    """
    Quick comparison of all parameter combinations.
    """
    print("\n" + "=" * 80)
    print("COMPARING ALL PARAMETER COMBINATIONS")
    print("=" * 80)
    print()
    print(f"{'k':<6} {'M':<6} {'Status':<30} {'File Path'}")
    print("-" * 80)
    
    for k in [100, 150, 170, 200]:
        for m in [-2, -5, -10]:
            rules_file = Path('birds') / f'birds_v1_k{k}_M{m}_rules.txt'
            names_file = Path('birds') / f'birds_v1_k{k}_M{m}_rules.txt.names'
            
            if rules_file.exists() or names_file.exists():
                # Count rules
                count = 0
                # Prefer names_file if it exists
                target = names_file if names_file.exists() else rules_file
                with open(target, 'r') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#') and ('->' in line or '=>' in line):
                            count += 1
                
                if count == 0:
                    status = "❌ No rules found"
                elif count < 20:
                    status = f"⚠️  Only {count} rules"
                else:
                    status = f"✅ {count} rules (GOOD!)"
                
                print(f"{k:<6} {m:<6} {status:<30} {target.name}")
            else:
                print(f"{k:<6} {m:<6} {'❌ File not found':<30} {rules_file.name}")
    
    print()

def main():
    print()
    print("🐦" * 40)
    print("BIRD ASSOCIATION RULES - SIMPLE VIEWER")
    print("🐦" * 40)
    print()
    print("This script will show you what's actually in your rule files")
    print("in plain English, so you can understand what to write about!")
    print()
    
    # First, show what files exist
    compare_all_parameters()
    
    # Ask user which one to view in detail
    print("=" * 80)
    print()
    
    try:
        k = int(input("Which k value do you want to see in detail? (100/150/170/200): "))
        m = int(input("Which M value? (-2/-5/-10): "))
        print()
    except:
        print("Invalid input, using defaults: k=150, M=-2")
        k, m = 150, -2
    
    # Show the rules
    show_rules_simple(k, m, max_rules=15)
    
    print()
    print("=" * 80)
    print("WHAT TO DO NEXT:")
    print("=" * 80)
    print()
    print("1. Look at the rules above - these are REAL patterns from your data!")
    print("2. Think about what makes them interesting:")
    print("   - Do they make biological sense?")
    print("   - Do they reveal ecological relationships?")
    print("   - Are there surprising connections?")
    print()
    print("3. In your Results section, you'll:")
    print("   - Group similar rules together (e.g., all aquatic bird rules)")
    print("   - Describe what each group tells us")
    print("   - Give examples of the most interesting rules")
    print("   - Explain what features were NOT useful")
    print()
    print("4. Use the generate_latex_results.py script to auto-generate")
    print("   a draft Results section, then customize it with your insights!")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()