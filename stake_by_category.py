import re
import subprocess
import getpass
from datetime import datetime

# All categories (including #11 for display, but not selectable)
categories = {
    0: "🌱 Root",
    1: "🧠 AI Data, Training, Inference",
    2: "🖥️ Compute, Storage, Infrastructure",
    3: "📈 Trading and Yield",
    4: "🎨 Generative AI",
    5: "👨‍💻 Coding and AI Agents",
    6: "🏆 Sports Predictions",
    7: "🧬 DeSci (Decentralized Science)",
    8: "🌐 Social & Indexing",
    9: "📣 Marketing & Discovery Platforms",
    10: "❓ Unknown & For Sale",
    11: "🚫 Not Active (DO NOT BUY)"
}

# Disallow staking in this category
disallowed_categories = [11]

def extract_category_subnets(readme_path):
    with open(readme_path, 'r') as f:
        content = f.read()

    pattern = r"## #(\d+)\s+([^\n]+)\n+(\| UID \| Subnet Name[^\n]*\n\|[-\s]+\|\n(?:\|.*\|\n?)*)"
    matches = re.findall(pattern, content)

    categories_subnets = {}
    for cat_num, cat_name, table in matches:
        uids = []
        for line in table.strip().split("\n"):
            if line.startswith("|") and line.count("|") >= 3 and "UID" not in line:
                try:
                    uid = int(line.split("|")[1].strip())
                    uids.append(uid)
                except:
                    continue
        categories_subnets[int(cat_num)] = uids

    return categories_subnets

def stake(wallet, uid, amount, password, log_file):
    try:
        cmd = [
            "btcli", "stake", "add",
            "--wallet-name", wallet,
            "--netuid", str(uid),
            "--amount", f"{amount:.8f}"
        ]
        result = subprocess.run(
            cmd,
            input=f"{password}\n",
            text=True,
            capture_output=True
        )
        output = result.stdout.strip()
        print(f"[UID {uid}] ✅", output)

        # Parse response for alpha, rate, slippage (best effort)
        alpha = rate = slippage = "?"
        if "α‎" in output:
            alpha_match = re.search(r"([\d.]+) α", output)
            if alpha_match:
                alpha = alpha_match.group(1)
        if "τ/α" in output:
            rate_match = re.search(r"(\d+\.\d+) τ/α", output)
            if rate_match:
                rate = rate_match.group(1)
        if "slippage" in output:
            slip_match = re.search(r"slippage[ :]+([\d.]+)%?", output)
            if slip_match:
                slippage = slip_match.group(1)

        log_file.write(f"{datetime.utcnow().isoformat()} | UID: {uid} | Alpha: {alpha} | TAO Used: {amount:.8f} | Rate: {rate} τ/α | Slippage: {slippage}%\n")
    except Exception as e:
        print(f"[UID]()
