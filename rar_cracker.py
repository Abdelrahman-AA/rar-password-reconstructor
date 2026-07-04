import itertools
import os
import re
import subprocess
import sys


def parse_chunks_file(chunks_file):
    """=== Reads the chunks file and parses positions, mandatory flags, and groups ==="""
    groups = []
    mandatory_groups_indices = set()
    fixed_positions = {}

    try:
        with open(chunks_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                is_mandatory = False
                fixed_pos = None

                match = re.match(r"^\[([Mm]|\d+)\]\s*(.*)", line)
                if match:
                    prefix = match.group(1)
                    line = match.group(2).strip()
                    if prefix.lower() == "m":
                        is_mandatory = True
                    else:
                        fixed_pos = int(prefix)

                if not line:
                    continue

                if line.startswith("(") and line.endswith(")"):
                    cleaned = line.strip("() ")
                    cleaned = cleaned.replace(",", "-")
                    alternatives = [
                        item.strip() for item in cleaned.split("-") if item.strip()
                    ]
                    if alternatives:
                        groups.append(alternatives)
                else:
                    groups.append([line])
                
                current_idx = len(groups) - 1
                if is_mandatory:
                    mandatory_groups_indices.add(current_idx)
                if fixed_pos is not None:
                    fixed_positions[current_idx] = fixed_pos

    except Exception as e:
        print(f"Error reading chunks file: {e}")
        return None, None, None

    return groups, mandatory_groups_indices, fixed_positions


def get_valid_group_structures(total_groups, min_chunks, max_chunks, mandatory_groups, fixed_positions):
    """=== Pre-calculates only the valid group index configurations to save massive CPU cycles ==="""
    valid_structures = []
    
    actual_min = max(1, min_chunks)
    actual_max = min(total_groups, max_chunks)
    
    for r in range(actual_min, actual_max + 1):
        if r < len(fixed_positions) or r < len(mandatory_groups):
            continue
            
        for group_indices in itertools.permutations(range(total_groups), r):
            possible = True
            for idx, pos in fixed_positions.items():
                if idx in group_indices:
                    if group_indices.index(idx) + 1 != pos:
                        possible = False
                        break
                else:
                    if pos <= r:
                        possible = False
                        break
            if not possible:
                continue

            if not mandatory_groups.issubset(set(group_indices)):
                continue

            valid_structures.append(group_indices)
            
    return valid_structures


def main():
    print("=== RAR Password Permutation Tool (Super Fast Fix) By... Abdelrahman Abodief ===")

    rar_path = input("⇘ Enter RAR file path: ").strip("\"'")
    chunks_file = input("⇘ Enter text file path containing chunks: ").strip("\"'")

    if not os.path.exists(rar_path) or not os.path.exists(chunks_file):
        print("============= Error: One or both file paths do not exist =============")
        return

    groups, mandatory_groups, fixed_positions = parse_chunks_file(chunks_file)
    if groups is None:
        return

    try:
        min_chunks = int(input("⇾ Enter MINIMUM elements to combine: ").strip())
        max_chunks = int(input("⇾ Enter MAXIMUM elements to combine: ").strip())
    except ValueError:
        print("Invalid input!")
        return

    print("\n...Calculating total combinations (Optimized)...")
    
    valid_structures = get_valid_group_structures(
        len(groups), min_chunks, max_chunks, mandatory_groups, fixed_positions
    )

    total_combinations = 0
    for struct in valid_structures:
        prod_size = 1
        for idx in struct:
            prod_size *= len(groups[idx])
        total_combinations += prod_size

    print(f"---Total valid combinations to test: {total_combinations:,}")

    if total_combinations == 0:
        print("============= No combinations match your criteria =============")
        return

    print("\n...Starting smart brute-force attack...")
    
    winrar_path = r"C:\Program Files\WinRAR\UnRAR.exe"
    if not os.path.exists(winrar_path):
        winrar_path = "unrar"

    index = 0
    found = False

    for struct in valid_structures:
        if found:
            break
        
        group_perm = [groups[idx] for idx in struct]
        for product_combination in itertools.product(*group_perm):
            password = "".join(product_combination)
            index += 1
            
            print(f"---Trying password {index:,} / {total_combinations:,}: {password:<20}", end="\r")

            # Inline execution of unrar to speed up loop slightly
            command = [winrar_path, "t", f"-p{password}", "-inul", rar_path]
            try:
                result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
                if result.returncode == 0:
                    print("\n\n=============....Success....Correct password found....=============")
                    print(f"---Password is: {password}")
                    found = True
                    break
            except (subprocess.TimeoutExpired, FileNotFoundError):
                if not os.path.exists(winrar_path):
                    print("\n=== Error: (UnRAR.exe or unrar) not found ===")
                    return

    if not found:
        print(f"\n\n============= Tested all {index:,} combinations - Password not found =============")


if __name__ == "__main__":
    main()