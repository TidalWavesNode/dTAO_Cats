import os
import sys
import getpass
import subprocess
from datetime import datetime
from pathlib import Path
import re

README_FILE = "README.md"
LOG_FILE = "staking_log.txt"

# All categories (including #27 for display, but not selectable)
categories = {
    0:  "🌱 Root",
    1:  "🧿 Ch3RNØbØG's Picks",
    2:  "🧊 3D",
    3:  "🌟 Agents",
    4:  "💻 Code",
    5:  "💾 Compute",
    6:  "🔐 Cryptography",
    7:  "📊 Data",
    8:  "💲 DeFi",
    9:  "🧬 DeSci",
    10: "🕵️  Detection",
    11: "🧠 Inference",
    12: "🛠️  Infra",
    13: "🌀 Latent Holdings",
    14: "🌌 Macrocosmos",
    15: "📣 Marketing",
    16: "🎥 Multimodal",
    17: "⚙️  Nickel5",
    18: "🔮 Prediction",
    19: "🧪 Rayon Labs",
    20: "🛡️  Security",
    21: "🏅 Sports",
    22: "💾 Storage",
    23: "📈 Trading",
    24: "🧐 Training",
    25: "🧹 Yuma",
    26: "❓ Unknown & For Sale",
    27: "❌ Not Active (DO NOT BUY)"
}

def parse_subnets_from_readme():
    if not Path(README_FILE).exists():
        print(f"❌ {README_FILE} not found.")
        sys.exit(1)

    with open(README_FILE, "r") as f:
        content = f.read()

    pattern = r"## #(\d+)\s+([^\n]+?)\n+\| UID \| Subnet Name[\s\|\-]+\n((?:\|[^\n]*\n)+)"
    matches = re.findall(pattern, content)

    categories_subnets = {
        int(num): {
            "name": title.strip(),
            "uids": [
                int(parts[1].strip())
                for line in table.strip().split("\n")
                if (parts := line.split("|")) and parts[1].strip().isdigit()
            ]
        }
        for num, title, table in matches
    }
    return categories_subnets

def log_entry(entry: str):
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(LOG_FILE, "a") as f:
        f.write(f"{now} | {entry}\n")

def stake(wallet_name, password, uid, amount):
    try:
        proc = subprocess.Popen(
            ["btcli", "stake", "add", "--wallet-name", wallet_name, "--netuid", str(uid), "--amount", str(amount)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(password + "\n")
        print(stdout)
        if proc.returncode != 0:
            print(f"⚠️ Error staking to UID {uid}: {stderr}")
            log_entry(f"UID: {uid} | FAILED | TAO Used: {amount}")
        else:
            log_entry(f"UID: {uid} | SUCCESS | TAO Used: {amount}")
    except Exception as e:
        print(f"❌ Exception: {e}")
        log_entry(f"UID: {uid} | EXCEPTION | TAO Used: {amount}")

def main():
    print("📊 Bittensor TAO Staking Assistant\nChoose a subnet category:\n")
    for k, v in categories.items():
        print(f" {k:>2}: {v}")
    try:
        choice = int(input("\nEnter category number: "))
    except ValueError:
        print("❌ Invalid input.")
        return

    if choice not in categories:
        print("❌ Invalid category.")
        return
    if choice == 27:
        print("🚫 This category is not active.")
        return

    subnets_by_cat = parse_subnets_from_readme()
    subnets = subnets_by_cat.get(choice, {}).get("uids", [])
    if not subnets:
        print("⚠️ No subnets found for this category.")
        return

    wallet_name = input("🔑 Enter your Bittensor wallet name: ").strip()
    password = getpass.getpass("🔐 Enter wallet password: ").strip()
    try:
        total_tao = float(input("💰 Enter total amount of TAO to stake: "))
    except ValueError:
        print("❌ Invalid amount.")
        return

    print("\n⚠️ You are about to stake {:.4f} TAO equally across subnets in:".format(total_tao))
    print("    Category #{} — {}".format(choice, categories[choice]))

    # Show all subnet names under the selected category
    subnet_lines = []
with open(README_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Build a normalized header to find
header_prefix = f"## #{choice}"
start = end = None

for i, line in enumerate(lines):
    if line.strip().startswith(header_prefix):
        start = i
        continue
    if start is not None and line.strip().startswith("## #") and i > start:
        end = i
        break

if start is not None:
    table_lines = lines[start:end]
    for line in table_lines:
        if "|" in line and line.count("|") >= 2 and "UID" not in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3 and parts[1].isdigit():
                subnet_lines.append(f"        UID {parts[1]}: {parts[2]}")

if subnet_lines:
    print("    Subnets:")
    for subnet in subnet_lines:
        print(subnet)
else:
    print("    Subnets: (not found)")

    if input("✅ Confirm? (yes/no): ").lower() != "yes":
        return
    if input("🛑 Final confirmation — proceed with staking? (yes/no): ").lower() != "yes":
        return

    amount_each = total_tao / len(subnets)
    print("📡 Staking {:.6f} TAO to each of {} subnets...".format(amount_each, len(subnets)))

    log_entry("=== Staking Log - {} ===".format(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')))
    for uid in subnets:
        stake(wallet_name, password, uid, amount_each)

if __name__ == "__main__":
    main()
