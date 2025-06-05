import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
import re

README_FILE = "README.md"
LOG_FILE = "staking_log.txt"

# All categories (including #11 for display, but not selectable)
categories = {
    0:  "🌱 Root",
    1:  "🧠 AI Data, Training, Inference",
    2:  "🖥️ Compute, Storage, Infrastructure",
    3:  "📈 Trading and Yield",
    4:  "🎨 Generative AI",
    5:  "💡 Coding and AI Agents",
    6:  "🏆 Sports Predictions",
    7:  "🧬 DeSci (Decentralized Science)",
    8:  "🌐 Social & Indexing",
    9:  "📣 Marketing & Discovery Platforms",
    10: "❓ Unknown & For Sale",
    11: "🚫 Not Active (DO NOT BUY)"
}

def parse_subnets_from_readme():
    if not Path(README_FILE).exists():
        print(f"❌ {README_FILE} not found.")
        raise FileNotFoundError

    if not shutil.which("btcli"):
        print("❌ `btcli` not found. Please make sure it is installed and in your path.")
        raise FileNotFoundError

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

def stake(wallet_name: str, wallet_path: str, uids: list[int], amount: float):
    try:
        proc = subprocess.run(
            ["btcli", "stake", "add", "--wallet-name", wallet_name, "--wallet-path", wallet_path, "--netuids", ",".join(str(x) for x in uids), "--amount", str(amount), "--json-output"],
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.stdout, proc.stderr
        captured = json.loads(stdout)
        for netuid_ in captured:
            for staking_address in captured[netuid_]:
                if not captured[netuid_][staking_address]:
                    print(f"⚠️ Error staking to UID {netuid_}")
                    log_entry(f"UID: {netuid_} | FAILED | TAO Used: {amount}")
                else:
                    log_entry(f"UID: {netuid_} | SUCCESS | TAO Used: {amount}")
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
    if choice == 11:
        print("🚫 This category is not active.")
        return

    subnets_by_cat = parse_subnets_from_readme()
    subnets = subnets_by_cat.get(choice, {}).get("uids", [])
    if not subnets:
        print("⚠️ No subnets found for this category.")
        return

    wallet_name = input("🔑 Enter your Bittensor wallet name: [default `default`]:").strip() or "default"
    wallet_path_ = input("🔑 Enter the path to your Bittensor wallets [default: `~/.bittensor/wallets`]:").strip() or "~/.bittensor/wallets"

    while True:
        try:
            total_tao = float(input("💰 Enter total amount of TAO to stake evenly between the selected subnets: "))
            break
        except ValueError:
            print("❌ Invalid amount.")

    print("\n⚠️ You are about to stake {:.4f} TAO equally across subnets in:".format(total_tao))
    print("    Category #{} — {}".format(choice, categories[choice]))
    if input("✅ Confirm? (yes/no): ").strip().lower() != "yes":
        return
    if input("🛑 Final confirmation — proceed with staking? (yes/no): ").strip().lower() != "yes":
        return

    amount_each = total_tao / len(subnets)
    print("📡 Staking {:.6f} TAO to each of {} subnets...".format(amount_each, len(subnets)))

    log_entry("=== Staking Log - {} ===".format(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')))
    stake(
        wallet_name=wallet_name, wallet_path=wallet_path_, uids=subnets, amount=amount_each
    )

if __name__ == "__main__":
    main()
