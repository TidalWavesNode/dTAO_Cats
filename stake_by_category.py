import re
from pathlib import Path
import subprocess
import getpass
from datetime import datetime

README_PATH = "README.md"  # Updated to use README.md

def extract_category_subnets_fixed(readme_path):
    with open(readme_path, 'r') as f:
        content = f.read()

    pattern = r"## #(\d+)\s+.*?\n\| UID \| Subnet Name[^\n]*\n\|[-\s]+\|\n((?:\|.*\|\n?)*)"
    matches = re.findall(pattern, content)

    categories_subnets = {}
    for cat_num, table in matches:
        uids = []
        for line in table.strip().split("\n"):
            if line.startswith("|") and line.count("|") >= 3:
                try:
                    uid = int(line.split("|")[1].strip())
                    uids.append(uid)
                except:
                    continue
        categories_subnets[int(cat_num)] = uids

    return categories_subnets

categories = {
     0: "🌱 Root",
     1: "🧠 AI Data, Training, Inference",
     2: "🖥️ Compute, Storage, Infrastructure",
     3: "📈 Trading and Yield",
     4: "🎨 Generative AI",
     5: "💡 Coding and AI Agents",
     6: "🏆 Sports Predictions",
     7: "🧬 DeSci (Decentralized Science)",
     8: "🌐 Social & Indexing",
     9: "📣 Marketing & Discovery Platforms",
    10: "❓ Unknown & For Sale",
    11: "🚫 Not Active (DO NOT BUY)"
}

def stake(wallet_name, password, uid, amount):
    cmd = [
        "btcli", "stake", "add",
        "--wallet-name", wallet_name,
        "--netuid", str(uid),
        "--amount", f"{amount:.9f}",
        "--no_prompt"
    ]
    result = subprocess.run(cmd, input=password + "\n", text=True, capture_output=True)
    return result.stdout, result.stderr

def main():
    print("📊 Bittensor TAO Staking Assistant")
    print("Choose an investment category:\n")
    for k, v in categories.items():
        print(f"{k:>2}: {v}")
    try:
        choice = int(input("\nEnter category number: ").strip())
        if choice == 11:
            print("🚫 Category 11 is not available for staking.")
            return
        if choice not in categories:
            print("❌ Invalid category.")
            return
    except ValueError:
        print("❌ Please enter a valid number.")
        return

    wallet = input("🔑 Enter your Bittensor wallet name: ").strip()
    password = getpass.getpass("🔐 Enter wallet password: ").strip()

    try:
        total_tao = float(input("💰 Enter total amount of TAO to stake: ").strip())
    except ValueError:
        print("❌ Please enter a valid number.")
        return

    print(f"\n⚠️ You are about to stake {total_tao:.4f} TAO equally across subnets in:")
    print(f"    Category #{choice} — {categories[choice]}")
    confirm = input("✅ Confirm? (yes/no): ").strip().lower()
    if confirm != "yes":
        return
    final = input("🛑 Final confirmation — proceed with staking? (yes/no): ").strip().lower()
    if final != "yes":
        return

    subnet_map = extract_category_subnets_fixed(README_PATH)
    subnets = subnet_map.get(choice, [])
    if not subnets:
        print("⚠️ No subnets found for this category.")
        return

    amount_per_subnet = total_tao / len(subnets)
    timestamp = datetime.utcnow().isoformat(timespec='seconds') + "Z"
    log_file = Path("staking_log.txt")
    with log_file.open("a") as log:
        log.write(f"\n=== Staking Log - {timestamp} ===\n")
        for uid in subnets:
            out, err = stake(wallet, password, uid, amount_per_subnet)
            log.write(f"{datetime.utcnow().isoformat()} | UID: {uid} | TAO: {amount_per_subnet:.9f} | Output: {out.strip()} | Error: {err.strip()}\n")
            print(f"✅ Staked {amount_per_subnet:.4f} TAO to UID {uid}")

    print("✅ All staking complete. Log saved to staking_log.txt")

if __name__ == "__main__":
    main()
