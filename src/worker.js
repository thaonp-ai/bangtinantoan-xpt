// Worker cho web Bảng tin An toàn – Xưởng Phụ Trợ.
// Mọi đường dẫn khác /api/* do file tĩnh trong web/ phục vụ (env.ASSETS).
// /api/nhansu: dữ liệu tab Nhân sự.
//   - Xem: công khai (người dùng chọn 17/11/2026).
//   - Sửa: cần mật khẩu quản trị (secret ADMIN_PASSWORD) và KV binding NHANSU.
//   - Nguồn dữ liệu: bản mới hơn (theo updatedAt) giữa KV "current" và file web/data/nhansu.json.

const FILE = "/data/nhansu.json";
const TRAIN = ["TC", "DCS", "NH", "GT", "RIVER", "DEMI", "NITO", "RAW", "NH3", "XLNT", "NHR"];

const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });

async function readFile(env, req) {
  const r = await env.ASSETS.fetch(new Request(new URL(FILE, req.url)));
  if (!r.ok) return null;
  try { return await r.json(); } catch { return null; }
}

function canEdit(env) {
  return !!(env.NHANSU && env.ADMIN_PASSWORD);
}

function safeEqual(a, b) {
  a = String(a || ""); b = String(b || "");
  let d = a.length ^ b.length;
  for (let i = 0; i < Math.max(a.length, b.length); i++) d |= (a.charCodeAt(i) || 0) ^ (b.charCodeAt(i) || 0);
  return d === 0;
}

async function authed(req, env) {
  const h = req.headers.get("authorization") || "";
  const pw = h.startsWith("Bearer ") ? h.slice(7) : "";
  const ok = canEdit(env) && pw && safeEqual(pw, env.ADMIN_PASSWORD);
  if (!ok) await new Promise((r) => setTimeout(r, 600)); // làm chậm dò mật khẩu
  return ok;
}

async function current(env, req) {
  const file = await readFile(env, req);
  const kv = env.NHANSU ? await env.NHANSU.get("current", "json") : null;
  if (kv && (!file || String(kv.updatedAt) > String(file.updatedAt || ""))) return { ...kv, source: "web" };
  return { ...(file || { rows: [] }), source: "file" };
}

function cleanRows(rows) {
  if (!Array.isArray(rows) || rows.length > 3000) throw new Error("Dữ liệu không hợp lệ");
  const ids = new Set();
  return rows.map((r) => {
    if (!r || !r.id || !r.name || !r.birth || !r.join) throw new Error("Thiếu Mã NV / Họ tên / Năm sinh / Năm vào");
    const id = String(r.id).trim().slice(0, 20);
    if (ids.has(id)) throw new Error("Trùng Mã NV " + id);
    ids.add(id);
    const s = (v, n = 60) => String(v ?? "").trim().slice(0, n);
    return {
      id, name: s(r.name, 80), birth: +r.birth | 0, gender: r.gender === "Nữ" ? "Nữ" : "Nam",
      retireAge: +r.retireAge || (r.gender === "Nữ" ? 60 : 62), join: +r.join | 0, pos: s(r.pos) || "—",
      grade: s(r.grade, 20), step: s(r.step, 10), coef: +r.coef || 0, raise: +r.raise || +r.join | 0,
      allow: s(r.allow, 60).replace(/[^0-9+]/g, "") || "0",
      trained: Array.isArray(r.trained) ? r.trained.filter((k) => TRAIN.includes(k)) : [],
    };
  });
}

async function api(req, env, url) {
  const p = url.pathname.replace(/\/+$/, "");
  const m = req.method;

  if (p === "/api/nhansu" && m === "GET") {
    const d = await current(env, req);
    return json({ ...d, canEdit: canEdit(env) });
  }
  if (p === "/api/nhansu/login" && m === "POST") {
    if (!canEdit(env)) return json({ error: "Chưa bật lưu chung (thiếu KV hoặc mật khẩu quản trị)." }, 503);
    return (await authed(req, env)) ? json({ ok: true }) : json({ error: "Sai mật khẩu" }, 401);
  }
  if (p === "/api/nhansu" && m === "PUT") {
    if (!canEdit(env)) return json({ error: "Chưa bật lưu chung (thiếu KV hoặc mật khẩu quản trị)." }, 503);
    if (!(await authed(req, env))) return json({ error: "Sai mật khẩu" }, 401);
    let body;
    try { body = await req.json(); } catch { return json({ error: "Dữ liệu không hợp lệ" }, 400); }
    let rows;
    try { rows = cleanRows(body.rows); } catch (e) { return json({ error: e.message }, 400); }
    const cur = await current(env, req);
    if (body.base && cur.updatedAt && body.base !== cur.updatedAt)
      return json({ error: "Dữ liệu vừa được người khác cập nhật. Trang sẽ tải lại.", conflict: true }, 409);
    const doc = { rows, updatedAt: new Date().toISOString(), note: String(body.note || "").slice(0, 200) };
    if (cur.source === "web") await env.NHANSU.put("prev", JSON.stringify(cur)); // giữ 1 bản trước để cứu
    await env.NHANSU.put("current", JSON.stringify(doc));
    return json({ ok: true, updatedAt: doc.updatedAt });
  }
  if (p === "/api/nhansu/restore" && m === "POST") {
    if (!canEdit(env)) return json({ error: "Chưa bật lưu chung." }, 503);
    if (!(await authed(req, env))) return json({ error: "Sai mật khẩu" }, 401);
    const cur = await env.NHANSU.get("current");
    if (cur) await env.NHANSU.put("prev", cur);
    await env.NHANSU.delete("current");
    return json({ ok: true });
  }
  return json({ error: "Không tìm thấy" }, 404);
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname.startsWith("/api/")) {
      try { return await api(req, env, url); }
      catch (e) { return json({ error: "Lỗi máy chủ: " + (e && e.message) }, 500); }
    }
    return env.ASSETS.fetch(req);
  },
};
