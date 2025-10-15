# 📝 LEMBAR PENILAIAN PRAKTIKUM: ETL vs ELT

**Nama Mahasiswa**: ___________________________  
**NIM**: ___________________________  
**Tanggal**: ___________________________

---

## ✅ CHECKLIST PENYELESAIAN

### Setup Environment (10%)
- [ ] Docker environment berhasil dijalankan
- [ ] Airflow UI dapat diakses (localhost:8080)
- [ ] Database connection berhasil
- [ ] Semua services running (postgres, redis, airflow)

### ETL Pipeline (25%)
- [ ] DAG `etl_iot_pipeline` berhasil dijalankan
- [ ] Semua task completed successfully
- [ ] Data berhasil ter-load ke `daily_sensor_summary_etl`
- [ ] Memahami alur Extract → Transform → Load
- [ ] Dapat menjelaskan dimana transformasi terjadi

### ELT Pipeline (25%)
- [ ] DAG `elt_iot_pipeline` berhasil dijalankan  
- [ ] Staging tables (`raw_sensors`, `raw_readings`) terbentuk
- [ ] Data berhasil ter-load ke `daily_sensor_summary_elt`
- [ ] Memahami alur Extract → Load → Transform
- [ ] Dapat menjelaskan transformasi SQL di database

### Analysis & Comparison (25%)
- [ ] Membandingkan execution time kedua pipeline
- [ ] Menganalisis perbedaan resource usage
- [ ] Memverifikasi konsistensi hasil akhir
- [ ] Memahami trade-offs masing-masing approach

### Documentation & Report (15%)
- [ ] Laporan analisis komparatif lengkap
- [ ] Screenshot/evidence dari eksekusi pipeline
- [ ] Kesimpulan dan rekomendasi use cases
- [ ] Code comments dan dokumentasi

---

## 📊 HASIL ANALISIS

### Performance Metrics
| Metric | ETL Pipeline | ELT Pipeline | Catatan |
|--------|-------------|-------------|---------|
| Total Execution Time | _____ min | _____ min |  |
| Extract Time | _____ sec | _____ sec |  |
| Transform Time | _____ sec | _____ sec |  |
| Load Time | _____ sec | _____ sec |  |
| Memory Usage | High/Medium/Low | High/Medium/Low |  |

### Data Quality Check
```sql
-- Query untuk memverifikasi konsistensi hasil
SELECT COUNT(*) FROM daily_sensor_summary_etl; -- Result: _____
SELECT COUNT(*) FROM daily_sensor_summary_elt; -- Result: _____

-- Check data difference (should be 0)
SELECT COUNT(*) FROM (
    SELECT location, date, avg_temp FROM daily_sensor_summary_etl
    EXCEPT
    SELECT location, date, avg_temp FROM daily_sensor_summary_elt
); -- Result: _____
```

### Key Findings
1. **Performance**: ________________________________
2. **Scalability**: ________________________________  
3. **Complexity**: ________________________________
4. **Maintenance**: ________________________________

---

## 💡 PERTANYAAN EVALUASI

### 1. Conceptual Understanding (20 poin)
**Jelaskan perbedaan fundamental antara ETL dan ELT approach:**

**Jawaban:**
```
ETL (Extract, Transform, Load):
- ________________________________
- ________________________________
- ________________________________

ELT (Extract, Load, Transform):  
- ________________________________
- ________________________________
- ________________________________
```

### 2. Technical Analysis (25 poin)
**Analisis kelebihan dan kekurangan masing-masing approach:**

**ETL Advantages:**
- ________________________________
- ________________________________

**ETL Disadvantages:**
- ________________________________
- ________________________________

**ELT Advantages:**
- ________________________________  
- ________________________________

**ELT Disadvantages:**
- ________________________________
- ________________________________

### 3. Use Cases (25 poin)
**Berikan contoh scenario dimana sebaiknya menggunakan:**

**ETL cocok untuk:**
- ________________________________
- ________________________________
- ________________________________

**ELT cocok untuk:**
- ________________________________
- ________________________________  
- ________________________________

### 4. Troubleshooting (15 poin)
**Sebutkan 3 masalah yang mungkin terjadi dan solusinya:**

**Problem 1:**
- Issue: ________________________________
- Solution: ________________________________

**Problem 2:**
- Issue: ________________________________
- Solution: ________________________________

**Problem 3:**
- Issue: ________________________________
- Solution: ________________________________

### 5. Optimization (15 poin)  
**Bagaimana cara mengoptimasi pipeline untuk data yang lebih besar?**

**ETL Optimizations:**
- ________________________________
- ________________________________

**ELT Optimizations:**
- ________________________________
- ________________________________

---

## 🎯 TUGAS BONUS (Optional)

### Implementasi Lanjutan (+10 poin)
- [ ] Generate data lebih besar (100+ sensors, 30+ days)
- [ ] Tambah data source baru (weather.csv)  
- [ ] Implementasi error handling
- [ ] Setup monitoring/alerting
- [ ] Add data quality checks

### Advanced Analysis (+10 poin)
- [ ] Performance benchmarking dengan berbagai ukuran data
- [ ] Memory profiling
- [ ] Network I/O analysis
- [ ] Scalability testing
- [ ] Cost analysis (cloud scenario)

---

## 📈 GRADING RUBRIC

| Score | Grade | Criteria |
|-------|-------|----------|
| 90-100 | A | Exceptional: All tasks completed perfectly with deep insights and optimization |
| 80-89 | B+ | Proficient: All tasks completed with good analysis and understanding |
| 70-79 | B | Satisfactory: Most tasks completed with basic understanding |
| 60-69 | C+ | Adequate: Some tasks completed but limited understanding |
| 50-59 | C | Minimal: Basic completion but significant gaps in understanding |
| <50 | D/F | Inadequate: Major issues in completion and understanding |

---

## 📋 SUBMISSION

### Required Deliverables:
1. **Filled Assessment Sheet** (this document)
2. **Screenshots** of successful pipeline executions
3. **Database Query Results** showing final tables
4. **Comparative Analysis Report** (2-3 pages)
5. **Code Modifications** (if any bonus tasks completed)

### Submission Format:
- **File Name**: `ETL_ELT_Assessment_[NIM]_[Nama].pdf`
- **Deadline**: ___________________________
- **Submit To**: ___________________________

---

**Final Score: _____ / 100**  
**Grade: _____**

**Instructor Comments:**
```
_________________________________________________
_________________________________________________
_________________________________________________
_________________________________________________
```

**Instructor Signature**: ___________________________  
**Date**: ___________________________