import time
import threading
from datetime import datetime

class Product:
    def __init__(self, id, type, model, batch, prod_date, rohs_compliant, image, label_quality, defects):
        self.id = id
        self.type = type
        self.model = model
        self.batch = batch
        self.prod_date = prod_date
        self.rohs_compliant = rohs_compliant
        self.image = image
        self.label_quality = label_quality
        self.defects = defects

    def __repr__(self):
        return f"<Product {self.id} {self.type}>"

class TraceabilityStation:
    def __init__(self):
        self.products = [
            Product("DEV-2023-0456", "Smart Sensor Board", "SSB-X200", "BATCH-2023-Q3-12", "2023-08-15", True, "pcb_with_components.jpg", 0.95, []),
            Product("DEV-2023-0457", "Control Module", "CM-Y330", "BATCH-2023-Q3-12", "2023-08-15", False, "control_module.jpg", 0.85, ["lead_content"]),
            Product("DEV-2023-0458", "Communication Hub", "CH-Z410", "BATCH-2023-Q3-13", "2023-08-16", True, "comm_hub.jpg", 0.75, ["misaligned_label"])
        ]
        self.current_index = 0
        self.conveyor_running = False
        self.process_thread = None
        self.data_log = []

    def start_conveyor(self):
        if self.conveyor_running:
            print("Conveyor already running.")
            return
        print("Starting conveyor...")
        self.conveyor_running = True
        self.process_thread = threading.Thread(target=self.process_cycle, daemon=True)
        self.process_thread.start()

    def stop_conveyor(self):
        print("Stopping conveyor...")
        self.conveyor_running = False
        if self.process_thread:
            self.process_thread.join(timeout=1)

    def process_cycle(self):
        while self.conveyor_running:
            self.process_product(self.products[self.current_index])
            self.current_index = (self.current_index + 1) % len(self.products)
            time.sleep(10)

    def process_product(self, product):
        print("\n--- Processing Product ---")
        print(f"Camera scans: {product.type} ({product.id}) on conveyor.")
        time.sleep(1.5)

        # Step 1: Product Identification
        print(f"Identifying product... ID: {product.id}")
        print(f"  Type: {product.type}, Model: {product.model}, MFG Date: {product.prod_date}")
        time.sleep(0.5)

        # Step 2: RoHS Compliance
        if product.rohs_compliant:
            print("RoHS Compliance: PASS")
        else:
            print("RoHS Compliance: FAIL - Contains restricted substances")
        time.sleep(0.5)

        # Step 3: Batch Verification
        print(f"Batch Verification: PASS ({product.batch})")
        time.sleep(0.5)

        # Step 4: AI-Assisted Verification
        if not product.defects:
            print("AI Analysis: PASS - No defects detected")
        else:
            print(f"AI Analysis: FAIL - Defects found: {', '.join(product.defects)}")
        time.sleep(1)

        # Step 5: Labeling
        label_pass = product.label_quality > 0.8 and all(d != 'misaligned_label' for d in product.defects)
        if label_pass:
            print("Label Generation: PASS")
        else:
            print("Label Generation: FAIL - Poor label quality or misalignment")
        time.sleep(0.5)

        # Step 6: Print Verification
        print("Print Verification: PASS")
        time.sleep(0.5)

        # Step 7: Rejection Mechanism & Final Status
        should_reject = (not product.rohs_compliant) or (not label_pass) or (len(product.defects) > 0)
        if should_reject:
            print("Rejection Mechanism: Unit rejected due to quality issues")
            print("Final Status: REJECTED")
        else:
            print("Rejection Mechanism: Unit passed")
            print("Final Status: ACCEPTED")
        self.log_result(product, not should_reject)
        print("--- End Processing ---\n")

    def log_result(self, product, passed):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "device_id": product.id,
            "batch_id": product.batch,
            "rohs": "YES" if product.rohs_compliant else "NO",
            "status": "Pass" if passed else "Fail",
            "details": "All checks passed" if passed else f"Issues: {', '.join(product.defects)}"
        }
        self.data_log.append(entry)
        print("Logged Result:", entry)

    def test_scenario(self, should_pass=True):
        now = datetime.now()
        test_product = Product(
            id=f"TEST-{now.strftime('%H%M%S')}",
            type="Test Valid Product" if should_pass else "Test Invalid Product",
            model="TVP-1000" if should_pass else "TIP-2000",
            batch="BATCH-TEST",
            prod_date=now.strftime('%Y-%m-%d'),
            rohs_compliant=should_pass,
            image="test_good_product.jpg" if should_pass else "test_bad_product.jpg",
            label_quality=0.95 if should_pass else 0.65,
            defects=[] if should_pass else ["test_defect", "label_issue"]
        )
        self.products.insert(0, test_product)
        self.current_index = 0
        print("\n--- Running Test Scenario ---")
        self.process_product(test_product)
        print("--- End Test Scenario ---\n")

    def print_log(self):
        print("\nTraceability Data Log:")
        for entry in self.data_log:
            print(entry)

if __name__ == "__main__":
    station = TraceabilityStation()
    try:
        station.start_conveyor()
        for _ in range(3):
            time.sleep(12)
        station.stop_conveyor()
        station.test_scenario(should_pass=True)
        station.test_scenario(should_pass=False)
        station.print_log()
    except KeyboardInterrupt:
        station.stop_conveyor()
        print("Conveyor stopped.")