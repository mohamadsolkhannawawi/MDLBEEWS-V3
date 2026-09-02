import os
import glob

target_dir = r"e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS\DOKUMEN SKRIPSI"
md_files = glob.glob(os.path.join(target_dir, "**", "*.md"), recursive=True)

replacements = [
    (
        "ditinjau menggunakan pendekatan *Systematic Literature Review* (SLR),",
        "ditinjau melalui penelusuran literatur,"
    ),
    (
        "ditinjau menggunakan pendekatan _Systematic Literature Review_ (SLR),",
        "ditinjau melalui penelusuran literatur,"
    ),
    (
        "Penelitian terdahulu ditinjau menggunakan pendekatan _Systematic Literature Review_ (SLR), yaitu metode evaluasi dan interpretasi terhadap seluruh penelitian yang relevan dengan suatu pertanyaan penelitian, topik, atau fenomena tertentu melalui metodologi yang tepercaya, sistematis, dan dapat ditelusuri ulang (Kitchenham & Charters, 2007). Berbeda dengan tinjauan pustaka naratif biasa, SLR mensyaratkan proses pencarian literatur yang eksplisit dan kriteria pemilihan yang jelas, sehingga bias pemilihan literatur dapat diminimalkan (Kitchenham & Charters, 2007). Mengacu pada pendekatan tersebut, penelusuran literatur pada penelitian ini dilakukan melalui basis data jurnal terindeks Scopus dengan kata kunci yang mencakup _Earthquake Early Warning System_, _microservices_, _observability_, Prometheus, dan WebSocket, dibatasi pada rentang tahun publikasi 2020–2026 agar tinjauan mencerminkan perkembangan riset terkini.",
        "Penelitian terdahulu ditinjau melalui penelusuran literatur pada basis data jurnal terindeks Scopus dengan kata kunci yang mencakup *Earthquake Early Warning System*, *microservices*, *observability*, Prometheus, dan WebSocket, dibatasi pada rentang tahun publikasi 2020–2026 agar tinjauan mencerminkan perkembangan riset terkini."
    ),
    (
        "Penelitian terdahulu ditinjau menggunakan pendekatan *Systematic Literature Review* (SLR), yaitu metode evaluasi dan interpretasi terhadap seluruh penelitian yang relevan dengan suatu pertanyaan penelitian, topik, atau fenomena tertentu melalui metodologi yang tepercaya, sistematis, dan dapat ditelusuri ulang (Kitchenham & Charters, 2007). Berbeda dengan tinjauan pustaka naratif biasa, SLR mensyaratkan proses pencarian literatur yang eksplisit dan kriteria pemilihan yang jelas, sehingga bias pemilihan literatur dapat diminimalkan (Kitchenham & Charters, 2007). Mengacu pada pendekatan tersebut, penelusuran literatur pada penelitian ini dilakukan melalui basis data jurnal terindeks Scopus dengan kata kunci yang mencakup *Earthquake Early Warning System*, *microservices*, *observability*, Prometheus, dan WebSocket, dibatasi pada rentang tahun publikasi 2020–2026 agar tinjauan mencerminkan perkembangan riset terkini.",
        "Penelitian terdahulu ditinjau melalui penelusuran literatur pada basis data jurnal terindeks Scopus dengan kata kunci yang mencakup *Earthquake Early Warning System*, *microservices*, *observability*, Prometheus, dan WebSocket, dibatasi pada rentang tahun publikasi 2020–2026 agar tinjauan mencerminkan perkembangan riset terkini."
    ),
    (
        "metodologi *Systematic Literature Review* (SLR)",
        "penelusuran literatur"
    )
]

for file_path in md_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content
        for old, new in replacements:
            new_content = new_content.replace(old, new)
            
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {file_path}")
    except Exception as e:
        print(f"Error on {file_path}: {e}")
