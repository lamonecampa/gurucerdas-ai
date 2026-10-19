"""Content generator for GuruCerdas AI.

By default it generates editable starter templates without an external AI service.
Set OPENAI_API_KEY and optionally OPENAI_MODEL to enable AI-assisted generation.
All generated educational content should be reviewed by a teacher before use.
"""
import os

def _build_prompt(p):
    return f"""Anda adalah asisten perencanaan pembelajaran berbahasa Indonesia.
Buat dokumen pendidikan yang praktis, terstruktur, sesuai usia, dan tidak mengarang
aturan kurikulum yang tidak diketahui. Gunakan bahasa yang jelas dan instruksi yang dapat
dikerjakan siswa. Jika informasi kurang, nyatakan asumsi secara singkat.
Jenis dokumen: {p['material_label']}
Jenjang: {p['grade']}
Mata pelajaran: {p['subject']}
Kurikulum/acuan: {p['curriculum']}
Topik: {p['topic']}
Tujuan pembelajaran: {p['learning_objective'] or 'Rumuskan tujuan yang relevan dan terukur.'}
Tingkat kesulitan: {p['difficulty']}
Jumlah butir/aktivitas yang diminta: {p['count']}
Catatan guru: {p['teacher_notes'] or 'Tidak ada'}
Ketentuan:
- Gunakan heading Markdown.
- Sertakan identitas dokumen, tujuan, petunjuk, isi utama, dan bagian evaluasi yang sesuai.
- Untuk paket soal, sertakan kunci jawaban dan alasan singkat pada bagian terpisah.
- Untuk kisi-kisi, gunakan tabel Markdown dengan indikator, bentuk soal, nomor, dan level kognitif.
- Untuk LKPD, sertakan alat/bahan jika diperlukan, langkah kerja, dan ruang jawaban.
- Untuk rubrik, buat kriteria dan deskriptor yang terukur serta skala skor.
- Untuk bahan ajar, sertakan penjelasan, contoh, aktivitas, rangkuman, dan cek pemahaman.
- Jangan menyatakan dokumen ini telah divalidasi oleh dinas atau lembaga resmi.
"""

def _openai_generate(prompt):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            input=prompt,
        )
        return response.output_text.strip()
    except Exception as exc:
        # Do not expose credentials or raw provider errors to end users.
        return None

def _template_generate(p):
    title = p["material_label"]
    header = (
        f"# {title}\n\n"
        f"**Jenjang:** {p['grade']}  \n"
        f"**Mata pelajaran:** {p['subject']}  \n"
        f"**Topik:** {p['topic']}  \n"
        f"**Kurikulum/acuan:** {p['curriculum']}  \n"
        f"**Tingkat kesulitan:** {p['difficulty']}\n\n"
    )
    objective = p["learning_objective"] or f"Peserta didik mampu menjelaskan dan menerapkan konsep {p['topic']} sesuai jenjang {p['grade']}."
    notes = f"\n\n**Catatan guru:** {p['teacher_notes']}" if p["teacher_notes"] else ""
    if p["material_type"] == "soal":
        lines = [header, "## Tujuan Pembelajaran\n", objective, "\n\n## Petunjuk\nJawablah setiap pertanyaan dengan teliti. Guru dapat menyesuaikan konteks, angka, dan tingkat kesulitan dengan kebutuhan kelas.\n\n## Soal\n"]
        for i in range(1, p["count"] + 1):
            lines.append(f"{i}. Jelaskan atau selesaikan satu permasalahan tentang **{p['topic']}** yang sesuai dengan {p['grade']}. Tunjukkan alasan atau langkah penyelesaianmu.\n")
        lines.append("\n## Kunci Jawaban dan Pedoman\nKunci jawaban belum diisi otomatis pada mode template. Guru perlu menyusun dan memverifikasi jawaban yang benar sebelum membagikan soal kepada siswa.\n")
        lines.append("\n## Catatan Validasi\nPastikan setiap soal sesuai tujuan pembelajaran, usia siswa, dan materi yang sudah diajarkan.")
        return "".join(lines) + notes
    if p["material_type"] == "kisi_kisi":
        lines = [header, "## Tujuan Pembelajaran\n", objective, "\n\n## Kisi-kisi Penilaian\n\n| No. | Materi/Indikator | Bentuk | Nomor Soal | Level Kognitif |\n|---:|---|---|---:|---|\n"]
        for i in range(1, min(p["count"], 15) + 1):
            lines.append(f"| {i} | Peserta didik menunjukkan pemahaman tentang {p['topic']} | Isian/uraian | {i} | Sesuaikan |\n")
        lines.append("\n## Catatan Guru\nLengkapi indikator dan level kognitif berdasarkan tujuan pembelajaran dan asesmen yang benar-benar digunakan.")
        return "".join(lines) + notes
    if p["material_type"] == "lkpd":
        lines = [header, "## Tujuan Kegiatan\n", objective, "\n\n## Petunjuk Kerja\n1. Baca instruksi sampai selesai.\n2. Kerjakan secara mandiri atau berkelompok sesuai arahan guru.\n3. Tuliskan jawaban dan alasan dengan jelas.\n\n## Aktivitas\n"]
        for i in range(1, min(p["count"], 10) + 1):
            lines.append(f"\n### Aktivitas {i}\nAmati contoh atau situasi yang berkaitan dengan **{p['topic']}**. Tuliskan apa yang kamu ketahui, langkah yang kamu lakukan, dan kesimpulanmu.\n\n**Jawaban:**\n\n........................................................................\n")
        lines.append("\n## Refleksi\n- Hal baru yang saya pelajari:\n- Bagian yang masih membingungkan:\n- Cara saya bekerja sama:\n")
        return "".join(lines) + notes
    if p["material_type"] == "rubrik":
        lines = [header, "## Tujuan Penilaian\n", objective, "\n\n## Rubrik Penilaian\n\n| Kriteria | 4 - Sangat Baik | 3 - Baik | 2 - Berkembang | 1 - Perlu Bimbingan |\n|---|---|---|---|---|\n"]
        criteria = ["Ketepatan konsep", "Langkah/proses kerja", "Kejelasan penjelasan", "Kemandirian/kolaborasi"]
        for c in criteria:
            lines.append(f"| {c} | Tepat, lengkap, dan konsisten | Sebagian besar tepat | Ada kekeliruan penting | Belum menunjukkan pemahaman dasar |\n")
        lines.append("\n## Perhitungan Nilai\nNilai akhir = (skor perolehan / skor maksimal) × 100. Sesuaikan bobot kriteria dengan tujuan pembelajaran.\n")
        lines.append("\n## Catatan Penggunaan\nGunakan deskriptor secara konsisten dan sampaikan kriteria kepada peserta didik sebelum penilaian.")
        return "".join(lines) + notes
    lines = [
        header, "## Tujuan Pembelajaran\n", objective,
        "\n\n## Pengantar\nTopik **", p["topic"], "** dipelajari untuk membantu peserta didik memahami konsep dan menggunakannya dalam situasi yang relevan.\n",
        "\n## Penjelasan Materi\nGuru dapat mengembangkan bagian ini dengan definisi inti, konsep penting, dan contoh yang dekat dengan kehidupan peserta didik. Pastikan setiap penjelasan sesuai dengan materi yang benar-benar diajarkan.\n",
        "\n## Contoh dan Aktivitas\n1. Berikan satu contoh sederhana tentang ", p["topic"], ".\n2. Ajak peserta didik mengamati, menjelaskan, dan mencoba menyelesaikan contoh serupa.\n3. Minta peserta didik menjelaskan alasan di balik jawabannya.\n",
        "\n## Rangkuman\n- Kenali konsep utama pada topik ", p["topic"], ".\n- Hubungkan konsep dengan contoh yang relevan.\n- Periksa kembali pemahaman melalui latihan singkat.\n",
        "\n## Cek Pemahaman\n1. Apa konsep utama yang kamu pelajari?\n2. Berikan contoh penerapan konsep tersebut.\n3. Bagian mana yang perlu dipelajari kembali?\n",
        "\n## Catatan Guru\nLengkapi definisi, contoh, dan sumber belajar yang sesuai dengan buku atau perangkat ajar yang digunakan."
    ]
    return "".join(lines) + notes

def generate_material(payload):
    prompt = _build_prompt(payload)
    ai_result = _openai_generate(prompt)
    if ai_result:
        return {"content": ai_result, "mode": "ai", "notice": "Draf dibantu AI. Periksa akurasi, kesesuaian usia, dan tujuan pembelajaran sebelum digunakan."}
    return {"content": _template_generate(payload), "mode": "template", "notice": "Mode template aktif. Isi yang dihasilkan merupakan kerangka awal dan perlu dilengkapi serta diverifikasi guru. Aplikasi tetap gratis tanpa API key. Pengelola dapat menambahkan OPENAI_API_KEY secara opsional; penggunaan penyedia AI eksternal mungkin berbayar."}
