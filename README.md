# Cara Menjalankan Program 

## Program Exclusive Lock
1. Buka direktori /ExclusiveLock
2. Untuk menjalankan salah satu contoh, masukan perintah python3 transaction1.py / transaction2.py / transaction3.py / transaction4.py

## Program Optimistic Concurrency Control / Validation Based Protocol
1. Buka direktori /OCC
2. Untuk menjalankan program, masukan perintah python3 occ.py
3. Masukkan transaksi secara berurutan dengan format: jenis_task data(jika ada) no_transaksi
contoh: read A 1, write B 2, validate 1, dll.
4. Jika seluruh transaksi telah diinput, akhiri dengan input "execute"