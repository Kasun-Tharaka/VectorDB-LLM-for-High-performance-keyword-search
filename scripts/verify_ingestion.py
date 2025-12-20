import sys
from pathlib import Path

# Add project root to python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.ingestion.reader import DatasetReader

def create_sample_file():
    content = """www.amazon.co.jp/ap/signin:kazumy.mukunoki.111@docomo.ne.jp:marukan
accounts.epicgames.com/resetPassword:f8bc58b45897469488e01dbfc474b1b8:chavezcasani123
www.kabasakalonline.com/yeni-uye-kaydi/:ahmet4585858@gmail.com:56638900"""
    
    file_path = project_root / "data" / "raw" / "sample_test.txt"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return str(file_path)

def test_ingestion():
    file_path = create_sample_file()
    print(f"Created sample file at {file_path}")
    
    reader = DatasetReader(file_path)
    print("Testing Ingestion...")
    count = 0
    for batch in reader.read_batch(batch_size=2):
        print(f"Batch parsed: {len(batch)} entries")
        for entry in batch:
            print(f" - URL: {entry.url}, Email: {entry.email}")
            count += 1
            
    print(f"Total entries processed: {count}")

if __name__ == "__main__":
    test_ingestion()
