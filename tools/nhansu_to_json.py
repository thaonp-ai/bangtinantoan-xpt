#!/usr/bin/env python3
"""Chuyển file báo cáo nhân sự (CSV hoặc Excel .xlsx) thành web/data/nhansu.json.

Dùng:  python3 -I tools/nhansu_to_json.py <file.csv|file.xlsx> [web/data/nhansu.json]

- Nhận cột theo tên tiêu đề (không phân biệt hoa/thường, dấu cách thừa), giống mẫu
  "Bao_cao_nhan_su_YYYY.csv": Mã NV, Họ và tên, Năm sinh, Giới tính, Tuổi nghỉ hưu,
  Năm vào nhà máy, Cương vị đang đảm nhận, Ngạch lương, Bậc lương, Hệ số lương,
  Năm tăng lương gần nhất, Phụ cấp, và 11 cột đào tạo (đánh dấu "x").
- Cột tính sẵn (Tuổi, Năm còn lại đến hưu, Số năm làm việc, Cương vị đã hoàn thành)
  bị bỏ qua: web tự tính theo năm đang xem.
- updatedAt = thời điểm chạy, để bản file thắng các chỉnh sửa cũ trên web (xem src/worker.js).
"""
import csv, datetime, io, json, os, re, sys, unicodedata

TRAIN = {"truong ca": "TC", "dcs": "DCS", "noi hoi": "NH", "gt&hrsg": "GT", "river": "RIVER", "demi": "DEMI",
         "nito-mn": "NITO", "raw": "RAW", "nh3-flare": "NH3", "xlnt": "XLNT", "nhr": "NHR"}
POS = {"nồi hơi": "Nồi hơi", "raw": "RAW", "demi": "Demi", "nitơ- mn": "Nitơ-MN", "nitơ-mn": "Nitơ-MN",
       "river": "RIVER", "wwt": "XLNT", "xlnt": "XLNT", "nh3": "NH3", "nhr": "NHR", "dcs": "DCS", "gt": "GT",
       "trưởng ca": "Trưởng ca"}
COLS = {"id": "ma nv", "name": "ho va ten", "birth": "nam sinh", "gender": "gioi tinh", "retireAge": "tuoi nghi huu",
        "join": "nam vao nha may", "pos": "cuong vi dang dam nhan", "grade": "ngach luong", "step": "bac luong",
        "coef": "he so luong", "raise": "nam tang luong gan nhat", "allow": "phu cap"}


def key(s):
    s = unicodedata.normalize("NFD", str(s or "")).replace("đ", "d").replace("Đ", "D")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"\s+", " ", s).strip()


def read_rows(path):
    if path.lower().endswith((".xlsx", ".xlsm")):
        import openpyxl
        wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
        for ws in wb.worksheets:  # sheet đầu tiên có cột "Mã NV"
            rows = [["" if v is None else v for v in r] for r in ws.iter_rows(values_only=True)]
            for i, r in enumerate(rows[:10]):
                if any(key(c) == "ma nv" for c in r):
                    return rows[i:]
        raise SystemExit("Không thấy sheet nào có cột 'Mã NV'")
    raw = open(path, "rb").read()
    for enc in ("utf-8-sig", "cp1258", "cp1252"):
        try:
            text = raw.decode(enc); break
        except UnicodeDecodeError:
            continue
    dialect = ";" if text.split("\n", 1)[0].count(";") > text.split("\n", 1)[0].count(",") else ","
    return list(csv.reader(io.StringIO(text), delimiter=dialect))


def num(v, f=float):
    try:
        return f(str(v).replace(",", ".").strip())
    except ValueError:
        return None


def main():
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "..", "web", "data", "nhansu.json")
    rows = read_rows(src)
    head = [key(h) for h in rows[0]]
    idx = {k: head.index(h) if h in head else -1 for k, h in COLS.items()}
    for k in ("id", "name", "birth", "join"):
        if idx[k] < 0:
            raise SystemExit(f"Thiếu cột '{COLS[k]}'")
    tcols = [(TRAIN[h.replace(" ", "") if h.replace(" ", "") in TRAIN else h], i) for i, h in enumerate(head)
             if h in TRAIN or h.replace(" ", "") in TRAIN]
    get = lambda r, k: (str(r[idx[k]]).strip() if idx[k] >= 0 and idx[k] < len(r) else "")
    data, seen, errs = [], set(), []
    for n, r in enumerate(rows[1:], 2):
        rid = get(r, "id")
        if not rid:
            continue
        if re.fullmatch(r"\d+(\.0)?", rid):  # Excel có thể làm mất số 0 đầu
            rid = str(int(float(rid))).zfill(5)
        try:
            birth = int(float(get(r, "birth"))); join = int(float(get(r, "join")))
        except ValueError:
            errs.append(f"dòng {n} ({rid}): thiếu năm sinh/năm vào"); continue
        if rid in seen:
            errs.append(f"dòng {n}: trùng Mã NV {rid}"); continue
        seen.add(rid)
        g = "Nữ" if key(get(r, "gender")) == "nu" else "Nam"
        pos = get(r, "pos")
        step = get(r, "step").lstrip("'")
        if re.fullmatch(r"\d+(\.\d+)?", step):  # Excel đổi "6/16" thành ngày/số → giữ nguyên chuỗi nếu có thể
            errs.append(f"dòng {n} ({rid}): bậc lương '{step}' không đúng dạng a/b")
        allow = re.sub(r"[^0-9+]", "", get(r, "allow").replace(".0", "")) or "0"
        data.append({
            "id": rid, "name": get(r, "name"), "birth": birth, "gender": g,
            "retireAge": int(num(get(r, "retireAge")) or (60 if g == "Nữ" else 62)), "join": join,
            "pos": POS.get(pos.lower(), pos) or "—", "grade": get(r, "grade"), "step": step,
            "coef": num(get(r, "coef")) or 0, "raise": int(num(get(r, "raise")) or join), "allow": allow,
            "trained": [k for k, i in tcols if i < len(r) and key(r[i]) == "x"],
        })
    doc = {"updatedAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
           "note": "Nạp từ " + os.path.basename(src), "rows": data}
    s = json.dumps(doc, ensure_ascii=False, separators=(",", ":")).replace('},{"id"', '},\n{"id"')
    open(out, "w", encoding="utf-8").write(s + "\n")
    print(f"{len(data)} nhân sự, {sum(len(d['trained']) for d in data)} lượt đào tạo → {out}")
    for e in errs:
        print("CẢNH BÁO:", e)


if __name__ == "__main__":
    main()
