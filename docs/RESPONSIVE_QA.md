# HemaLens Responsive QA Matrix

Dokumen ini digunakan setelah automated tests lulus. Pemeriksaan visual tetap
wajib karena unit test tidak dapat membuktikan tidak adanya clipping, overlap,
atau masalah keyboard pada browser mobile nyata.

## Viewport Matrix

| Target | Viewport |
|---|---:|
| Mobile kecil | 360 × 800 |
| iPhone umum | 390 × 844 |
| Mobile besar | 430 × 932 |
| Tablet portrait | 768 × 1024 |
| Tablet landscape | 1024 × 768 |
| Desktop | 1440 × 900 |

## Navigation

- [ ] Tombol menu memiliki area sentuh minimum 44 × 44 px.
- [ ] Menu dapat dibuka dan ditutup.
- [ ] Tombol Escape menutup menu pada keyboard.
- [ ] Focus tetap berada di dalam drawer saat menu terbuka.
- [ ] Scroll body terkunci ketika drawer aktif.
- [ ] Research, About, dan Try Model dapat dibuka.

## Landing and Splash

- [ ] Splash menutup penuh viewport, termasuk safe area.
- [ ] Heading typewriter tidak terpotong.
- [ ] Kalimat heading maksimal dua baris pada ponsel umum.
- [ ] Dua information card tersusun vertikal pada mobile.
- [ ] Footer tidak menyebabkan horizontal overflow.

## Form

- [ ] Enam input tersusun satu kolom pada mobile.
- [ ] Keyboard numerik muncul untuk seluruh input.
- [ ] Safari iPhone tidak melakukan auto-zoom.
- [ ] Field description tidak bertabrakan dengan label.
- [ ] Checkbox acknowledgement mudah disentuh.
- [ ] Clear form dan Run analysis memenuhi lebar mobile.

## Result and Error

- [ ] Outcome dan score panel tersusun vertikal.
- [ ] Nilai score dan model version tidak keluar dari panel.
- [ ] Threshold scale tetap terlihat utuh.
- [ ] Label berbunyi “Score target”, bukan “Class”.
- [ ] Tombol aksi memenuhi lebar mobile.
- [ ] Heading hasil menerima focus setelah HTMX swap.

## Research and About

- [ ] Heading tidak terpotong.
- [ ] Card tersusun satu kolom.
- [ ] Tombol aksi dapat disentuh dan tidak overflow.
- [ ] Navbar mobile konsisten dengan halaman utama.

## Three.js

- [ ] Pointer parallax tidak aktif pada touch device.
- [ ] Frame rate dibatasi sekitar 30 FPS pada mobile.
- [ ] Scene dihancurkan ketika masuk form atau result.
- [ ] Scene berhenti ketika tab tidak aktif.
- [ ] Save Data dan Reduce Motion menggunakan fallback statis.

## Commands

```bash
source .venv/bin/activate
python -m scripts.audit_responsive
pytest
npm run build
```
