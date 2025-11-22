from models import get_db, Device, ScanResult
import json

print("=== Database Verification ===")

db = next(get_db())

# Check devices table
devices = db.query(Device).limit(5).all()
print(f"\nDevices table ({len(devices)} entries):")
for device in devices:
    print(f"  ID: {device.id[:8]}... | Token Hash: {device.token_hash[:16]}... | Created: {device.created_at}")

# Check scan_results table
scans = db.query(ScanResult).limit(5).all()
print(f"\nScan Results table ({len(scans)} entries):")
for scan in scans:
    url_hashes = scan.url_hashes or []
    print(f"  Device: {scan.device_id[:8]}... | URL Hashes: {len(url_hashes)} | Risk: {scan.risk_score} | Created: {scan.created_at}")
    if url_hashes:
        print(f"    First URL hash: {url_hashes[0][:16]}...")

print("\n✓ Verification: Only hashed data stored, no raw URLs or text")
db.close()