# 🧩 Sudoku Solver & Generator (Tkinter GUI)

Bu proje, Python ile yazılmış bir **Sudoku üretici ve çözücü** uygulamasıdır.
Arayüz `tkinter` ile, algoritmalar ise **backtracking** yöntemi ile gerçekleştirilmiştir.

---

## 🚀 Özellikler

* 🎲 Rastgele sudoku üretimi (`easy`, `medium`, `hard`)
* 🧠 Backtracking ile çözüm bulma
* 🔍 Adım adım çözüm izleme (Step Solver)
* ⏭️ "Next" butonu ile algoritmayı adım adım ilerletme
* ⚡ Tek tıkla çözüm (Solve Immediately)
* 🎨 Hücre renklendirme:

  * Yeşil → yerleştirme
  * Kırmızı → backtracking

---

## 📁 Proje Yapısı

```
project/
│
├── backend.py   # Sudoku algoritmaları
└── gui.py       # Tkinter arayüzü
```

---

## 🧠 Kullanılan Algoritma

Bu projede Sudoku çözmek için **Backtracking Algorithm** kullanılmıştır.

Mantık:

1. Boş hücreyi bul
2. 1–9 arası sayıları dene
3. Geçerliyse yerleştir
4. Devam et
5. Çıkmaza girerse geri dön (backtrack)

---

## ⚙️ Kurulum

### 1. Python kurulu olmalı

Python 3.x gereklidir.

### 2. Tkinter kontrolü

```bash
python -m tkinter
```

Eğer pencere açılırsa her şey hazırdır ✅

---

## ▶️ Çalıştırma

```bash
python gui.py
```

---

## 🎮 Kullanım

### Generate

Seçilen zorlukta yeni sudoku oluşturur.

### Solve Step

Adım adım çözümü başlatır.

### Next

Algoritmayı bir adım ilerletir.

### Solve Immediately

Sudoku’yu anında çözer.

---

## 🎨 Renk Anlamları

| Renk            | Anlam                   |
| --------------- | ----------------------- |
| 🟢 Açık yeşil   | Sayı yerleştirildi      |
| 🔴 Açık kırmızı | Geri alındı (backtrack) |

---

## ⚠️ Notlar

* Boş hücreler `-1` ile temsil edilir
* GUI sadece arayüzdür, tüm algoritma `backend.py` içindedir
* `random.shuffle()` sayesinde her seferinde farklı sudoku üretilir

---

## 🛠️ Geliştirme Fikirleri

* ⏱️ Otomatik çözüm (auto-play)
* 🎯 Tek çözüm garantili sudoku üretimi
* 🎨 Daha gelişmiş UI (dark mode)
* ❌ Hatalı hücreleri kırmızı gösterme
* 💾 Sudoku kaydetme/yükleme

---

## 👨‍💻 Geliştirici Notu

Bu proje, backtracking algoritmasını görselleştirmek ve anlamak için hazırlanmıştır.
Adım adım çözüm özelliği özellikle eğitim amaçlıdır.

---


