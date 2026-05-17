# api_minimax

Client Python sederhana untuk mencoba MiniMax Chat Completions API.

## Setup

File API key asli boleh disimpan lokal sebagai `api_minimax.env` atau `.env`.
File ini sudah di-ignore oleh Git dan tidak boleh di-upload ke GitHub.

Contoh isi file env:

```env
MINIMAX_API_KEY=your_minimax_api_key_here
MINIMAX_BASE_URL=https://api.minimax.io/v1
MINIMAX_MODEL=MiniMax-M2.7
MINIMAX_MAX_TOKENS=1200
```

## Menjalankan

```bash
python3 minimax_chat.py "Halo, jelaskan API dalam bahasa Indonesia"
```

Secara default skrip menyembunyikan blok `<think>`.
Untuk melihat output mentah dari API:

```bash
python3 minimax_chat.py --show-thinking "Halo"
```

Endpoint yang dipakai:

```text
POST https://api.minimax.io/v1/chat/completions
```
