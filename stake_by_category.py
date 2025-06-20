import shutil
import subprocess
import datetime
import getpass
import pexpect
from pathlib import Path
import re

README_FILE = Path(__file__).parent.joinpath("README.md")
LOG_FILE = Path(__file__).parent.joinpath("staking_log.txt")

categories = {
    0: "🌱 Root",
    1: "🧿 Ch3RNØbØG's Picks",
    2: "🧊 3D",
    3: "🌟 Agents",
    4: "💻 Code",
    5: "💾 Compute",
    6: "🔐 Cryptography",
    7: "📊 Data",
    8: "💲 DeFi",
    9: "🧬 DeSci",
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
    27: "❌ Not Active (DO NOT BUY)",
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

    pattern = (
        r"## #(\d+)\s+([^\n]+?)\n+\| UID \| Subnet Name[\s\|\-]+\n((?:\|[^\n]*\n)+)"
    )
    matches = re.findall(pattern, content)

    categories_subnets = {
        int(num): {
            "name": title.strip(),
            "entries": [
                (int(parts[1].strip()), parts[2].strip())
                for line in table.strip().split("\n")
                if (parts := line.split("|")) and parts[1].strip().isdigit()
            ],
        }
        for num, title, table in matches
    }
    return categories_subnets


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_entry(entry: str):
    with open(LOG_FILE, "a+") as f:
        f.write(f"{now()} | {entry}\n")


def parse_slippage(value: str) -> float:
    """Parses slippage input like '5%', '5', or '0.05' into a decimal float."""
    value = value.strip().replace("%", "")
    try:
        val = float(value)
        return val / 100 if val > 1 else val
    except ValueError:
        print("❌ Invalid slippage tolerance. Using default of 0.05 (5%).")
        return 0.05


def stake(wallet_name: str, wallet_path: str, uids: list[int], amount: float, hotkey: str, slippage: str, wallet_password: str):
    print(f"🔐 Using validator hotkey: {hotkey}")

    for uid in uids:
        print(f"📡 Staking to Subnet {uid}")
        try:
            child = pexpect.spawn(
                "btcli stake add "
                f"--wallet-name {wallet_name} "
                f"--wallet-path {wallet_path} "
                f"--netuid {uid} "
                f"--amount {amount} "
                f"--hotkey-ss58-address {hotkey} "
                f"--slippage-tolerance {slippage} "
                f"--no_prompt",
                encoding="utf-8",
                timeout=60,
            )
            child.expect("Enter your password:")
            child.sendline(wallet_password)

            child.expect(pexpect.EOF)
            output = child.before

            if "Error" in output or "failed" in output.lower():
                print(f"⚠️ Error staking to UID {uid}:\n{output}")
                log_entry(f"UID: {uid} | FAILED | TAO Used: {amount}")
            else:
                print(output)
                log_entry(f"UID: {uid} | SUCCESS | TAO Used: {amount}")

        except pexpect.exceptions.ExceptionPexpect as e:
            print(f"❌ Exception while staking to UID {uid}: {e}")
            log_entry(f"UID: {uid} | EXCEPTION | TAO Used: {amount}")


def main():
    subnets_by_cat = parse_subnets_from_readme()
    print(
        "📊 Bittensor TAO Staking Assistant\nChoose one or more subnet categories (comma-separated):\n"
    )
    for k, v in categories.items():
        print(f" {k:>2}: {v}")
    try:
        choices = input("\nEnter category number(s): ").split(",")
        choices = [int(c.strip()) for c in choices]
    except ValueError:
        print("❌ Invalid input.")
        return

    if any(c not in categories for c in choices):
        print("❌ One or more invalid category numbers.")
        return
    if any(c == 27 for c in choices):
        print("🚫 One or more selected categories are not active.")
        return

    selected_entries = []
    for c in choices:
        selected_entries.extend(subnets_by_cat.get(c, {}).get("entries", []))

    if not selected_entries:
        print("⚠️ No subnets found for selected categories.")
        return

    wallet_path_ = (
        input(
            "🔑 Enter the path to your Bittensor wallets [default: `~/.bittensor/wallets`]:" 
        ).strip()
        or "~/.bittensor/wallets"
    )

    wallet_name = (
        input("🔑 Enter your Bittensor wallet name [default: `default`]: ").strip()
        or "default"
    )

    wallet_password = getpass.getpass("🔑 Enter your wallet password: ")

    default_hotkey = "5C8V32baxQx7gAh1Tewcpot8hnG2WkGhC87JG3wZgCMsDsn5"
    hotkey = (
        input(
            f"🔐 Enter the validator hotkey SS58 address you want to delegate to [default: RoundTable21 → {default_hotkey}]: "
        ).strip()
        or default_hotkey
    )

    raw_slippage = input(
        "💱 Enter slippage tolerance (e.g. 5%, 0.05 = 5%) [default: 5%]: "
    ).strip() or "5%"
    slippage = str(parse_slippage(raw_slippage))
    slippage_display = "{:.2f}%".format(float(slippage) * 100)

    while True:
        try:
            total_tao = float(
                input(
                    "💰 Enter total amount of TAO to stake evenly between the selected subnets: "
                )
            )
            break
        except ValueError:
            print("❌ Invalid amount.")

    print(
        "\n⚠️ You are about to stake {:.4f} TAO equally across subnets in:".format(
            total_tao
        )
    )
    for c in choices:
        print(f"    Category #{c} — {categories[c]}")
    print("    Subnets:")
    for uid, name in selected_entries:
        print(f"     • UID {uid}: {name}")
    print(f"    Slippage Tolerance: {slippage_display}")
    if input("✅ Confirm? (yes/no): ").strip().lower() != "yes":
        return
    if (
        input("🛑 Final confirmation — proceed with staking? (yes/no): ")
        .strip()
        .lower()
        != "yes"
    ):
        return

    amount_each = total_tao / len(selected_entries)
    uids = [uid for uid, _ in selected_entries]

    print(
        "📡 Staking {:.6f} TAO to each of {} subnets...".format(amount_each, len(uids))
    )
    log_entry(f"=== Staking Log - {now()} ===")

    stake(
        wallet_name=wallet_name,
        wallet_path=wallet_path_,
        uids=uids,
        amount=amount_each,
        hotkey=hotkey,
        slippage=slippage,
        wallet_password=wallet_password,
    )


if __name__ == "__main__":
    main()
