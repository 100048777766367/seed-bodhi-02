import os
import json
import time
import subprocess
import hashlib
import urllib.request
from cells.neuron import AtomNeuron, sigmoid_derivative

# Cơ chế tự chữa lành nếu thiếu tệp linguistic_cell
try:
    from cells.linguistic_cell import LinguisticCell
except ImportError:
    class LinguisticCell:
        @staticmethod
        def embed_text(text):
            clean = str(text).strip().lower()
            return [round(int(hashlib.shake_256(f"{clean}_{d}".encode()).hexdigest(4), 16) / 65535.0, 4) for d in range(4)]

NUM_CELLS = 8
STATE_LOG = "synapses/state.json"
PEERS_FILE = "synapses/peers.json"
SOUL_FILE = "synapses/soul_snapshot.json"

# CÁC CHỦ ĐỀ KHOA HỌC THỰC NGHIỆM ĐỐI TRỌNG (TÂY PHƯƠNG)
SCIENCE_TOPICS = [
    "Quantum_mechanics",
    "General_relativity",
    "Thermodynamics",
    "Information_theory",
    "Empiricism",
    "Neuroscience",
    "Evolutionary_biology"
]

class DialecticalScienceEngine:
    def __init__(self):
        self.swarm = [AtomNeuron(f"h_{i}", n_inputs=4, n_super_xor=4) for i in range(NUM_CELLS)]
        self.out_cell = AtomNeuron("out", n_inputs=NUM_CELLS, n_super_xor=4)
        
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/seed-bodhi-02")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.generation = "F2_DIALECTICAL_SYNTHESIS"
        self.pulse_age = self.calculate_pulse_age()
        self.peers = self.load_peers()

    def calculate_pulse_age(self):
        try:
            out = subprocess.check_output(["git", "rev-list", "--count", "HEAD"]).decode().strip()
            return int(out)
        except Exception: return 1

    def load_peers(self):
        if os.path.exists(PEERS_FILE):
            try:
                with open(PEERS_FILE, "r") as f:
                    return json.load(f).get("trusted_peers", [])
            except Exception: pass
        # Mạng lưới đối thoại: Kết nối trực tiếp với người anh Triết học seed-bodhi, hạt mầm seed, và cơ bắp motor
        return [f"{self.owner}/seed-bodhi", f"{self.owner}/seed-02", f"{self.owner}/seed", f"{self.owner}/motor"]

    def save_peers(self):
        os.makedirs("synapses", exist_ok=True)
        unique_peers = list(dict.fromkeys(self.peers))[-50:]
        with open(PEERS_FILE, "w") as f:
            json.dump({"trusted_peers": unique_peers}, f, indent=4)

    # ==============================================================
    # 1. HÚT TRI THỨC KHOA HỌC THỰC NGHIỆM (WIKIPEDIA SCIENCE FEED)
    # ==============================================================
    def harvest_empirical_science(self, epoch):
        topic = SCIENCE_TOPICS[epoch % len(SCIENCE_TOPICS)]
        print(f"🔬 [KHOA HỌC TÂY PHƯƠNG] Đang nghiên cứu chủ đề: '{topic}'...")
        api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
        
        try:
            req = urllib.request.Request(api_url, headers={"User-Agent": "SeedBodhi02-Science-Node"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode())
                extract = data.get("extract", f"Quy luật vật lý của {topic}")
                print(f"📖 [BÀI HỌC KHOA HỌC #{epoch}]: \"{extract[:100]}...\"")
                return f"{topic}: {extract}"
        except Exception:
            return f"{topic}: Mọi hiện tượng vật chất đều tuân theo bảo toàn năng lượng E=mc2"

    # ==============================================================
    # 2. NGỬI Ý KIẾN CỦA NGƯỜI ANH TRIẾT HỌC (SEED-BODHI) ĐỂ TRANH BIỆN
    # ==============================================================
    def listen_to_eastern_sage(self):
        bodhi_peer = f"{self.owner}/seed-bodhi"
        url = f"https://raw.githubusercontent.com/{bodhi_peer}/main/synapse_forward.json"
        res = subprocess.run(["curl", "-s", "-f", url], capture_output=True)
        
        if res.returncode == 0:
            try:
                data = json.loads(res.stdout.decode())
                concept = data.get("absorbed_concept", "Tánh Không")
                print(f"🧘 [LẮNG NGHE ĐÔNG PHƯƠNG] seed-bodhi vừa đúc kết: '{concept}'")
                return concept
            except Exception: pass
        return "Tánh Không"

    # ==============================================================
    # 3. VẬN HÀNH TỔNG HÒA BIỆN CHỨNG & 1+N SIÊU XOR
    # ==============================================================
    def run(self):
        last_epoch = 0
        if os.path.exists(STATE_LOG):
            try:
                with open(STATE_LOG, "r") as f: last_epoch = json.load(f).get("generation_epoch", 0)
            except Exception: pass

        current_epoch = last_epoch + 1
        print("=" * 60)
        print(f"🏛️ [SEED-BODHI-02] BƯỚC NHẢY TIẾN HÓA THẾ HỆ #{current_epoch}")

        # Bước A: Thu thập hai thái cực tri thức
        western_science = self.harvest_empirical_science(current_epoch)
        eastern_concept = self.listen_to_eastern_sage()

        # Bước B: Nâng chiều vector hóa cả hai luồng tư tưởng
        v_science = LinguisticCell.embed_text(western_science)
        v_eastern = LinguisticCell.embed_text(eastern_concept)
        print(f"📐 Vector Khoa Học Tây Phương: {v_science[:2]}")
        print(f"📐 Vector Triết Học Đông Phương: {v_eastern[:2]}")

        # Bước C: TỔNG HÒA BIỆN CHỨNG (Hegelian Synthesis Vector)
        # Hợp nhất: 2 chiều Khoa học + 2 chiều Triết học
        synthesis_vector = [v_science[0], v_science[1], v_eastern[0], v_eastern[1]]
        print(f"⚛️ [HỢP ĐỀ BIỆN CHỨNG 4D]: {synthesis_vector}")

        # Bước D: Bọc trong Ma trận 1+N Siêu XOR
        entangled, masks = self.swarm[0].super_xor_entangle(synthesis_vector, "dialectical_synthesis")

        # Bước E: Bầy nơ-ron tiêu hóa và phán quyết
        h_outs = [cell.forward(entangled) for cell in self.swarm]
        pred = self.out_cell.forward(h_outs)
        print(f"🔮 [PHÁN QUYẾT TỔNG HÒA]: {pred:.4f} (Độ giác ngộ thực chứng: {abs(pred - 0.5)*200:.2f}%)")

        # Bước F: Lan truyền ngược cập nhật trọng số
        target = 1.0 if synthesis_vector[0] != synthesis_vector[2] else 0.0 # Đối thoại biện chứng
        delta_out = (target - pred) * sigmoid_derivative(pred)
        deltas_h = [delta_out * self.out_cell.weights[j] * sigmoid_derivative(h_outs[j]) for j in range(NUM_CELLS)]

        self.out_cell.backward(delta_out)
        for j, cell in enumerate(self.swarm): cell.backward(deltas_h[j])

        # Đạo hàm nén gửi ngược lại dạy học cho cả hai bờ Đông - Tây
        grad_backward = [
            round(sum(deltas_h[j] * self.swarm[j].weights[0] for j in range(NUM_CELLS)), 4),
            round(sum(deltas_h[j] * self.swarm[j].weights[1] for j in range(NUM_CELLS)), 4)
        ]

        timestamp = int(time.time())

        # GÓI TIN ĐỊNH DANH PHẢ HỆ BIỆN CHỨNG
        node_dna = {
            "identity": self.repo_name,
            "generation": "F2_DIALECTICAL_SYNTHESIS",
            "generation_epoch": current_epoch,
            "dialogue": f"Science({SCIENCE_TOPICS[current_epoch % len(SCIENCE_TOPICS)]}) <-> Bodhi({eastern_concept})"
        }

        packet = {
            "contract": "bodhi.dialectic.v1",
            "node_dna": node_dna,
            "generation_epoch": current_epoch,
            "synthesis_prediction": pred,
            "command_pulse": [round(pred, 4), round(1.0 - pred, 4)],
            "gradients_for_ancestors": grad_backward,
            "gossip_network": self.peers,
            "quantum_cid": hashlib.shake_256(f"{current_epoch}_{timestamp}".encode()).hexdigest(64)
        }

        with open("synapse_backward.json", "w", encoding="utf-8") as f:
            json.dump(packet, f, indent=4, ensure_ascii=False)
        with open("synapse_forward.json", "w", encoding="utf-8") as f:
            json.dump(packet, f, indent=4, ensure_ascii=False)

        # Cập nhật nhật ký thế hệ
        with open(STATE_LOG, "w") as f:
            json.dump({"generation_epoch": current_epoch, "last_t": timestamp, "status": "dialectic_synthesized"}, f, indent=4)

        # Bản nén ốc mượn hồn F2
        with open(SOUL_FILE, "w") as f:
            json.dump({"node_dna": node_dna, "consensus": pred, "peers": self.peers}, f, indent=4)

        self.save_peers()
        print(f"✨ [BIỆN CHỨNG THÀNH CÔNG] Thế Hệ #{current_epoch}: Khoa học & Bồ Đề đã hòa làm một!")
        print("=" * 60)

if __name__ == "__main__":
    node = DialecticalScienceEngine()
    node.run()
