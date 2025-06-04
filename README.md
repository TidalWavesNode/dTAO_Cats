## 🛠️ How to Use the TAO Staking Script

This script helps you automatically stake a chosen amount of TAO across all subnets in a selected category.

### 📋 Requirements

- Python 3.7+
- `btcli` installed and in your `$PATH`
- This `README.md` must be present in the same folder as the script

### 🚀 Quick Start

1. Install prereqs
```
sudo apt update
sudo apt install python3 python3-pip -y
```

2. **Clone this repository**
```
git clone https://github.com/TidalWavesNode/dTAO_Cats.git
```
```
cd dTAO_Cats
```
3. Run the script
```
python3 stake_by_category.py
```

4. Follow the prompts
Choose a category (0–10)
*Category 11 is shown for reference only and cannot be selected.
Enter wallet name and password.
Enter the total TAO to distribute equally across all subnets in the chosen category.
Confirm and stake.

📁 Example Log Output
```
=== Staking Log - 2025-06-04T15:21:12Z ===
2025-06-04T15:21:13Z | UID: 1 | Alpha: 0.3745 | TAO Used: 0.11400000 | Rate: 0.3041 τ/α | Slippage: 0.4%
```
---

⚠️ Disclaimer
This project is experimental and intended for educational and testing purposes only.

🧪 Category mappings are based on current public documentation and community knowledge. Subnets may evolve, rebrand, or change purpose at any time.

🧠 This is not financial advice. Always do your own research before staking or investing in any subnet.

⚙️ Use this script and associated tools at your own risk. The authors make no guarantees regarding accuracy, uptime, or rewards.

🔐 Always verify wallet addresses and security practices when interacting with the Bittensor network or any blockchain system.

---

# 🌐 Bittensor Subnet Directory

A categorized reference of Bittensor subnets.

---
## #0 🌱 Root

| UID | Subnet Name                  |
|-----|------------------------------|
| 0   | Root                         |

## #1 🧠 AI Data, Training, Inference

| UID | Subnet Name                  |
|-----|------------------------------|
| 1   | Apex                         |
| 3   | τemplar                      |
| 4   | Targon                       |
| 6   | Infinite Games               |
| 9   | iota                         |
| 13  | Data Universe                |
| 18  | Zeus                         |
| 19  | Nineteen.ai                  |
| 21  | OMEGA Any-to-Any             |
| 24  | OMEGA Labs                   |
| 29  | Coldint                      |
| 33  | ReadyAI                      |
| 34  | BitMind                      |
| 37  | Finetuning                   |
| 38  | Distributed Training         |
| 40  | Chunking                     |
| 42  | Real-Time Data by Masa       |
| 52  | Dojo                         |
| 56  | Gradients                    |
| 57  | Gaia                         |
| 72  | StreetVision by NATIX        |
| 80  | AI Factory                   |
| 81  | Patrol (TAO.com)             |
| 96  | FLock OFF                    |
| 105 | SoundsRight                  |

## #2 🖥️ Compute, Storage, Infrastructure

| UID | Subnet Name           |
|-----|-----------------------|
| 2   | omron                 |
| 7   | SubVortex             |
| 12  | Compute Horde         |
| 14  | TAOHash               |
| 26  | Storb                 |
| 27  | NI Compute            |
| 39  | w.ai (Parked)         |
| 43  | Graphite              |
| 49  | polariscloud.ai       |
| 51  | Celium                |
| 64  | Chutes                |
| 65  | TAO Private Network   |
| 73  | merit                 |
| 75  | Hippius               |
| 91  | tensorprox            |
| 97  | FlameWire             |

## #3 📈 Trading and Yield

| UID | Subnet Name                      |
|-----|----------------------------------|
| 8   | Proprietary Trading Network      |
| 10  | Sturdy                           |
| 31  | CANDLES                          |
| 50  | Synth                            |
| 53  | EfficientFrontier                |
| 55  | Precog                           |
| 63  | Alpha Trader Exchange (ATX)      |
| 77  | Liquidity                        |
| 79  | τaos                             |
| 88  | Sταking                          |
| 106 | Liquidity Provisioning           |

## #4 🎨 Generative AI

| UID | Subnet Name         |
|-----|---------------------|
| 11  | Dippy               |
| 17  | 404—GEN             |
| 32  | ItsAI               |
| 46  | Neural3D            |
| 58  | Dippy Speech        |
| 70  | Vericore            |
| 84  | Docs-Insights (Taτsu)|
| 85  | Vidaio              |
| 86  | MIAO                |

## #5 👨‍💻 Coding and AI Agents

| UID | Subnet Name             |
|-----|-------------------------|
| 20  | BitAgent - Rizzo        |
| 35  | LogicNet                |
| 36  | Web Agents - Autoppia   |
| 45  | SWE - Rizzo             |
| 59  | Agent Arena by Masa     |
| 60  | Bitsec.ai               |
| 61  | RedTeam                 |
| 62  | Ridges AI               |
| 92  | ReinforcedAI            |
| 94  | Eastworld               |

## #6 🏆 Sports Predictions

| UID | Subnet Name   |
|-----|---------------|
| 30  | Bettensor     |
| 41  | SPORTSTENSOR  |
| 44  | Score         |

## #7 🧬 DeSci (Decentralized Science)

| UID | Subnet Name |
|-----|-------------|
| 25  | Mainframe   |
| 68  | NOVA        |
| 76  | Safe Scan   |

## #8 🌐 Social & Indexing

| UID | Subnet Name |
|-----|-------------|
| 5   | OpenKaito   |
| 22  | Desearch    |
| 23  | Nuance      |

## #9 📣 Marketing & Discovery Platforms

| UID | Subnet Name |
|-----|-------------|
| 16  | BitAds      |
| 48  | NextPlace   |
| 66  | FakeNews    |
| 87  | CheckerChain|
| 93  | Bitcast     |

## #10 ❓ Unknown & For Sale

| UID | Subnet Name |
|-----|-------------|
| 15  | Unknown     |
| 28  | Unknown     |
| 47  | for sale    |
| 67  | Unknown     |
| 69  | Unknown     |
| 71  | Unknown     |
| 74  | Unknown     |
| 78  | Unknown     |
| 82  | Unknown     |
| 102 | for sale    |
| 104 | Unknown     |

## #11 🚫 Not Active (DO NOT BUY)

| UID | Subnet Name             |
|-----|-------------------------|
| 83  | Unknown                 |
| 89  | Unknown                 |
| 90  | brain                   |
| 95  | Unknown                 |
| 98  | Creator                 |
| 99  | Algo                    |
| 100 | Unknown                 |
| 101 | Unknown                 |
| 103 | Unknown                 |
| 107 | Tiger Alpha             |
| 108 | Internet of Intelligence|
| 109 | Si                      |
| 110 | Unknown                 |
| 111 | Unknown                 |
| 112 | TopSecret               |
| 113 | taonado                 |
| 114 | Єclipse Project         |
| 115 | Cognify                 |
| 116 | SolMev                  |

---

⚠️ Disclaimer
This project is experimental and intended for educational and testing purposes only.

🧪 Category mappings are based on current public documentation and community knowledge. Subnets may evolve, rebrand, or change purpose at any time.

🧠 This is not financial advice. Always do your own research before staking or investing in any subnet.

⚙️ Use this script and associated tools at your own risk. The authors make no guarantees regarding accuracy, uptime, or rewards.

🔐 Always verify wallet addresses and security practices when interacting with the Bittensor network or any blockchain system.

---
