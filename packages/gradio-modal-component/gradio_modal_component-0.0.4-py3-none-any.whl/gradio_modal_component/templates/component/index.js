const {
  SvelteComponent: se,
  assign: _e,
  create_slot: de,
  detach: re,
  element: ue,
  get_all_dirty_from_scope: me,
  get_slot_changes: be,
  get_spread_update: ge,
  init: he,
  insert: we,
  safe_not_equal: ve,
  set_dynamic_element_data: Q,
  set_style: y,
  toggle_class: L,
  transition_in: p,
  transition_out: x,
  update_slot_base: ke
} = window.__gradio__svelte__internal;
function ye(t) {
  let e, l, f;
  const i = (
    /*#slots*/
    t[18].default
  ), o = de(
    i,
    t,
    /*$$scope*/
    t[17],
    null
  );
  let a = [
    { "data-testid": (
      /*test_id*/
      t[7]
    ) },
    { id: (
      /*elem_id*/
      t[2]
    ) },
    {
      class: l = "block " + /*elem_classes*/
      t[3].join(" ") + " svelte-1uxx6fq"
    }
  ], c = {};
  for (let n = 0; n < a.length; n += 1)
    c = _e(c, a[n]);
  return {
    c() {
      e = ue(
        /*tag*/
        t[14]
      ), o && o.c(), Q(
        /*tag*/
        t[14]
      )(e, c), L(
        e,
        "hidden",
        /*visible*/
        t[10] === !1
      ), L(
        e,
        "padded",
        /*padding*/
        t[6]
      ), L(
        e,
        "border_focus",
        /*border_mode*/
        t[5] === "focus"
      ), L(e, "hide-container", !/*explicit_call*/
      t[8] && !/*container*/
      t[9]), y(
        e,
        "height",
        /*get_dimension*/
        t[15](
          /*height*/
          t[0]
        )
      ), y(e, "width", typeof /*width*/
      t[1] == "number" ? `calc(min(${/*width*/
      t[1]}px, 100%))` : (
        /*get_dimension*/
        t[15](
          /*width*/
          t[1]
        )
      )), y(
        e,
        "border-style",
        /*variant*/
        t[4]
      ), y(
        e,
        "overflow",
        /*allow_overflow*/
        t[11] ? "visible" : "hidden"
      ), y(
        e,
        "flex-grow",
        /*scale*/
        t[12]
      ), y(e, "min-width", `calc(min(${/*min_width*/
      t[13]}px, 100%))`), y(e, "border-width", "var(--block-border-width)");
    },
    m(n, s) {
      we(n, e, s), o && o.m(e, null), f = !0;
    },
    p(n, s) {
      o && o.p && (!f || s & /*$$scope*/
      131072) && ke(
        o,
        i,
        n,
        /*$$scope*/
        n[17],
        f ? be(
          i,
          /*$$scope*/
          n[17],
          s,
          null
        ) : me(
          /*$$scope*/
          n[17]
        ),
        null
      ), Q(
        /*tag*/
        n[14]
      )(e, c = ge(a, [
        (!f || s & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          n[7]
        ) },
        (!f || s & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          n[2]
        ) },
        (!f || s & /*elem_classes*/
        8 && l !== (l = "block " + /*elem_classes*/
        n[3].join(" ") + " svelte-1uxx6fq")) && { class: l }
      ])), L(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), L(
        e,
        "padded",
        /*padding*/
        n[6]
      ), L(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), L(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), s & /*height*/
      1 && y(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), s & /*width*/
      2 && y(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), s & /*variant*/
      16 && y(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), s & /*allow_overflow*/
      2048 && y(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), s & /*scale*/
      4096 && y(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), s & /*min_width*/
      8192 && y(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`);
    },
    i(n) {
      f || (p(o, n), f = !0);
    },
    o(n) {
      x(o, n), f = !1;
    },
    d(n) {
      n && re(e), o && o.d(n);
    }
  };
}
function ze(t) {
  let e, l = (
    /*tag*/
    t[14] && ye(t)
  );
  return {
    c() {
      l && l.c();
    },
    m(f, i) {
      l && l.m(f, i), e = !0;
    },
    p(f, [i]) {
      /*tag*/
      f[14] && l.p(f, i);
    },
    i(f) {
      e || (p(l, f), e = !0);
    },
    o(f) {
      x(l, f), e = !1;
    },
    d(f) {
      l && l.d(f);
    }
  };
}
function Ce(t, e, l) {
  let { $$slots: f = {}, $$scope: i } = e, { height: o = void 0 } = e, { width: a = void 0 } = e, { elem_id: c = "" } = e, { elem_classes: n = [] } = e, { variant: s = "solid" } = e, { border_mode: r = "base" } = e, { padding: m = !0 } = e, { type: u = "normal" } = e, { test_id: w = void 0 } = e, { explicit_call: j = !1 } = e, { container: z = !0 } = e, { visible: C = !0 } = e, { allow_overflow: q = !0 } = e, { scale: g = null } = e, { min_width: h = 0 } = e, H = u === "fieldset" ? "fieldset" : "div";
  const I = (d) => {
    if (d !== void 0) {
      if (typeof d == "number")
        return d + "px";
      if (typeof d == "string")
        return d;
    }
  };
  return t.$$set = (d) => {
    "height" in d && l(0, o = d.height), "width" in d && l(1, a = d.width), "elem_id" in d && l(2, c = d.elem_id), "elem_classes" in d && l(3, n = d.elem_classes), "variant" in d && l(4, s = d.variant), "border_mode" in d && l(5, r = d.border_mode), "padding" in d && l(6, m = d.padding), "type" in d && l(16, u = d.type), "test_id" in d && l(7, w = d.test_id), "explicit_call" in d && l(8, j = d.explicit_call), "container" in d && l(9, z = d.container), "visible" in d && l(10, C = d.visible), "allow_overflow" in d && l(11, q = d.allow_overflow), "scale" in d && l(12, g = d.scale), "min_width" in d && l(13, h = d.min_width), "$$scope" in d && l(17, i = d.$$scope);
  }, [
    o,
    a,
    c,
    n,
    s,
    r,
    m,
    w,
    j,
    z,
    C,
    q,
    g,
    h,
    H,
    I,
    u,
    i,
    f
  ];
}
class Se extends se {
  constructor(e) {
    super(), he(this, e, Ce, ze, ve, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const je = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], R = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
je.reduce(
  (t, { color: e, primary: l, secondary: f }) => ({
    ...t,
    [e]: {
      primary: R[e][l],
      secondary: R[e][f]
    }
  }),
  {}
);
const {
  SvelteComponent: qe,
  attr: Y,
  create_slot: Le,
  detach: Me,
  element: Ie,
  get_all_dirty_from_scope: Be,
  get_slot_changes: Ee,
  init: Ne,
  insert: He,
  null_to_empty: U,
  safe_not_equal: Te,
  set_style: A,
  toggle_class: M,
  transition_in: Ye,
  transition_out: Ae,
  update_slot_base: De
} = window.__gradio__svelte__internal;
function Fe(t) {
  let e, l, f = `calc(min(${/*min_width*/
  t[2]}px, 100%))`, i;
  const o = (
    /*#slots*/
    t[8].default
  ), a = Le(
    o,
    t,
    /*$$scope*/
    t[7],
    null
  );
  return {
    c() {
      e = Ie("div"), a && a.c(), Y(
        e,
        "id",
        /*elem_id*/
        t[3]
      ), Y(e, "class", l = U(
        /*elem_classes*/
        t[4].join(" ")
      ) + " svelte-1m1obck"), M(
        e,
        "gap",
        /*gap*/
        t[1]
      ), M(
        e,
        "compact",
        /*variant*/
        t[6] === "compact"
      ), M(
        e,
        "panel",
        /*variant*/
        t[6] === "panel"
      ), M(e, "hide", !/*visible*/
      t[5]), A(
        e,
        "flex-grow",
        /*scale*/
        t[0]
      ), A(e, "min-width", f);
    },
    m(c, n) {
      He(c, e, n), a && a.m(e, null), i = !0;
    },
    p(c, [n]) {
      a && a.p && (!i || n & /*$$scope*/
      128) && De(
        a,
        o,
        c,
        /*$$scope*/
        c[7],
        i ? Ee(
          o,
          /*$$scope*/
          c[7],
          n,
          null
        ) : Be(
          /*$$scope*/
          c[7]
        ),
        null
      ), (!i || n & /*elem_id*/
      8) && Y(
        e,
        "id",
        /*elem_id*/
        c[3]
      ), (!i || n & /*elem_classes*/
      16 && l !== (l = U(
        /*elem_classes*/
        c[4].join(" ")
      ) + " svelte-1m1obck")) && Y(e, "class", l), (!i || n & /*elem_classes, gap*/
      18) && M(
        e,
        "gap",
        /*gap*/
        c[1]
      ), (!i || n & /*elem_classes, variant*/
      80) && M(
        e,
        "compact",
        /*variant*/
        c[6] === "compact"
      ), (!i || n & /*elem_classes, variant*/
      80) && M(
        e,
        "panel",
        /*variant*/
        c[6] === "panel"
      ), (!i || n & /*elem_classes, visible*/
      48) && M(e, "hide", !/*visible*/
      c[5]), n & /*scale*/
      1 && A(
        e,
        "flex-grow",
        /*scale*/
        c[0]
      ), n & /*min_width*/
      4 && f !== (f = `calc(min(${/*min_width*/
      c[2]}px, 100%))`) && A(e, "min-width", f);
    },
    i(c) {
      i || (Ye(a, c), i = !0);
    },
    o(c) {
      Ae(a, c), i = !1;
    },
    d(c) {
      c && Me(e), a && a.d(c);
    }
  };
}
function Ge(t, e, l) {
  let { $$slots: f = {}, $$scope: i } = e, { scale: o = null } = e, { gap: a = !0 } = e, { min_width: c = 0 } = e, { elem_id: n = "" } = e, { elem_classes: s = [] } = e, { visible: r = !0 } = e, { variant: m = "default" } = e;
  return t.$$set = (u) => {
    "scale" in u && l(0, o = u.scale), "gap" in u && l(1, a = u.gap), "min_width" in u && l(2, c = u.min_width), "elem_id" in u && l(3, n = u.elem_id), "elem_classes" in u && l(4, s = u.elem_classes), "visible" in u && l(5, r = u.visible), "variant" in u && l(6, m = u.variant), "$$scope" in u && l(7, i = u.$$scope);
  }, [o, a, c, n, s, r, m, i, f];
}
let Je = class extends qe {
  constructor(e) {
    super(), Ne(this, e, Ge, Fe, Te, {
      scale: 0,
      gap: 1,
      min_width: 2,
      elem_id: 3,
      elem_classes: 4,
      visible: 5,
      variant: 6
    });
  }
};
const {
  SvelteComponent: Ke,
  append: v,
  attr: k,
  binding_callbacks: V,
  create_component: $,
  create_slot: Oe,
  destroy_component: ee,
  detach: E,
  element: S,
  get_all_dirty_from_scope: Pe,
  get_slot_changes: Qe,
  init: Re,
  insert: N,
  listen: D,
  mount_component: le,
  noop: Ue,
  run_all: Ve,
  safe_not_equal: We,
  set_data: G,
  set_style: b,
  space: B,
  text: J,
  toggle_class: W,
  transition_in: K,
  transition_out: O,
  update_slot_base: Xe
} = window.__gradio__svelte__internal;
function X(t) {
  let e, l, f;
  return {
    c() {
      e = S("div"), e.innerHTML = '<svg width="10" height="10" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 1L9 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M9 1L1 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>', k(e, "class", "close svelte-sz1hib");
    },
    m(i, o) {
      N(i, e, o), l || (f = D(
        e,
        "click",
        /*close*/
        t[14]
      ), l = !0);
    },
    p: Ue,
    d(i) {
      i && E(e), l = !1, f();
    }
  };
}
function Ze(t) {
  let e;
  const l = (
    /*#slots*/
    t[23].default
  ), f = Oe(
    l,
    t,
    /*$$scope*/
    t[27],
    null
  );
  return {
    c() {
      f && f.c();
    },
    m(i, o) {
      f && f.m(i, o), e = !0;
    },
    p(i, o) {
      f && f.p && (!e || o & /*$$scope*/
      134217728) && Xe(
        f,
        l,
        i,
        /*$$scope*/
        i[27],
        e ? Qe(
          l,
          /*$$scope*/
          i[27],
          o,
          null
        ) : Pe(
          /*$$scope*/
          i[27]
        ),
        null
      );
    },
    i(i) {
      e || (K(f, i), e = !0);
    },
    o(i) {
      O(f, i), e = !1;
    },
    d(i) {
      f && f.d(i);
    }
  };
}
function pe(t) {
  let e, l, f, i, o = (
    /*display_close_icon*/
    t[3] && X(t)
  );
  return f = new Je({
    props: {
      elem_classes: ["centered-column"],
      $$slots: { default: [Ze] },
      $$scope: { ctx: t }
    }
  }), {
    c() {
      o && o.c(), e = B(), l = S("div"), $(f.$$.fragment), k(l, "class", "modal-content svelte-sz1hib"), k(
        l,
        "style",
        /*getSizeStyle*/
        t[17]()
      );
    },
    m(a, c) {
      o && o.m(a, c), N(a, e, c), N(a, l, c), le(f, l, null), i = !0;
    },
    p(a, c) {
      /*display_close_icon*/
      a[3] ? o ? o.p(a, c) : (o = X(a), o.c(), o.m(e.parentNode, e)) : o && (o.d(1), o = null);
      const n = {};
      c & /*$$scope*/
      134217728 && (n.$$scope = { dirty: c, ctx: a }), f.$set(n);
    },
    i(a) {
      i || (K(f.$$.fragment, a), i = !0);
    },
    o(a) {
      O(f.$$.fragment, a), i = !1;
    },
    d(a) {
      a && (E(e), E(l)), o && o.d(a), ee(f);
    }
  };
}
function Z(t) {
  let e, l, f, i, o, a, c, n, s, r = (
    /*close_message_style*/
    t[10].confirm_text + ""
  ), m, u, w, j = (
    /*close_message_style*/
    t[10].cancel_text + ""
  ), z, C, q;
  return {
    c() {
      e = S("div"), l = S("div"), f = S("h3"), i = J(
        /*close_message*/
        t[5]
      ), o = B(), a = S("br"), c = B(), n = S("div"), s = S("button"), m = J(r), u = B(), w = S("button"), z = J(j), b(
        f,
        "color",
        /*close_message_style*/
        t[10].message_color
      ), k(f, "class", "svelte-sz1hib"), k(s, "class", "yes-button svelte-sz1hib"), b(
        s,
        "background-color",
        /*close_message_style*/
        t[10].confirm_bg_color
      ), b(
        s,
        "color",
        /*close_message_style*/
        t[10].confirm_text_color
      ), k(w, "class", "no-button svelte-sz1hib"), b(
        w,
        "background-color",
        /*close_message_style*/
        t[10].cancel_bg_color
      ), b(
        w,
        "color",
        /*close_message_style*/
        t[10].cancel_text_color
      ), k(n, "class", "confirmation-buttons svelte-sz1hib"), k(l, "class", "confirmation-content svelte-sz1hib"), b(
        l,
        "background-color",
        /*close_message_style*/
        t[10].modal_bg_color
      ), k(e, "class", "confirmation-modal svelte-sz1hib");
    },
    m(g, h) {
      N(g, e, h), v(e, l), v(l, f), v(f, i), v(l, o), v(l, a), v(l, c), v(l, n), v(n, s), v(s, m), v(n, u), v(n, w), v(w, z), C || (q = [
        D(
          s,
          "click",
          /*closeModal*/
          t[15]
        ),
        D(
          w,
          "click",
          /*cancelClose*/
          t[16]
        )
      ], C = !0);
    },
    p(g, h) {
      h & /*close_message*/
      32 && G(
        i,
        /*close_message*/
        g[5]
      ), h & /*close_message_style*/
      1024 && b(
        f,
        "color",
        /*close_message_style*/
        g[10].message_color
      ), h & /*close_message_style*/
      1024 && r !== (r = /*close_message_style*/
      g[10].confirm_text + "") && G(m, r), h & /*close_message_style*/
      1024 && b(
        s,
        "background-color",
        /*close_message_style*/
        g[10].confirm_bg_color
      ), h & /*close_message_style*/
      1024 && b(
        s,
        "color",
        /*close_message_style*/
        g[10].confirm_text_color
      ), h & /*close_message_style*/
      1024 && j !== (j = /*close_message_style*/
      g[10].cancel_text + "") && G(z, j), h & /*close_message_style*/
      1024 && b(
        w,
        "background-color",
        /*close_message_style*/
        g[10].cancel_bg_color
      ), h & /*close_message_style*/
      1024 && b(
        w,
        "color",
        /*close_message_style*/
        g[10].cancel_text_color
      ), h & /*close_message_style*/
      1024 && b(
        l,
        "background-color",
        /*close_message_style*/
        g[10].modal_bg_color
      );
    },
    d(g) {
      g && E(e), C = !1, Ve(q);
    }
  };
}
function xe(t) {
  let e, l, f, i, o, a, c, n;
  f = new Se({
    props: {
      allow_overflow: !1,
      elem_classes: ["modal-block"],
      $$slots: { default: [pe] },
      $$scope: { ctx: t }
    }
  });
  let s = (
    /*showConfirmation*/
    t[13] && Z(t)
  );
  return {
    c() {
      e = S("div"), l = S("div"), $(f.$$.fragment), i = B(), s && s.c(), k(l, "class", "modal-container svelte-sz1hib"), b(
        l,
        "width",
        /*width*/
        t[7] + "px"
      ), b(
        l,
        "height",
        /*height*/
        t[8] + "px"
      ), k(e, "class", o = "modal " + /*elem_classes*/
      t[2].join(" ") + " svelte-sz1hib"), k(
        e,
        "id",
        /*elem_id*/
        t[1]
      ), b(e, "backdrop-filter", "blur(" + /*bg_blur*/
      t[6] + ")"), b(e, "background-color", "rgba(0, 0, 0, " + /*opacity_level*/
      t[9] + ")"), W(e, "hide", !/*visible*/
      t[0]);
    },
    m(r, m) {
      N(r, e, m), v(e, l), le(f, l, null), t[24](l), v(e, i), s && s.m(e, null), t[25](e), a = !0, c || (n = D(
        e,
        "click",
        /*click_handler*/
        t[26]
      ), c = !0);
    },
    p(r, [m]) {
      const u = {};
      m & /*$$scope, display_close_icon*/
      134217736 && (u.$$scope = { dirty: m, ctx: r }), f.$set(u), (!a || m & /*width*/
      128) && b(
        l,
        "width",
        /*width*/
        r[7] + "px"
      ), (!a || m & /*height*/
      256) && b(
        l,
        "height",
        /*height*/
        r[8] + "px"
      ), /*showConfirmation*/
      r[13] ? s ? s.p(r, m) : (s = Z(r), s.c(), s.m(e, null)) : s && (s.d(1), s = null), (!a || m & /*elem_classes*/
      4 && o !== (o = "modal " + /*elem_classes*/
      r[2].join(" ") + " svelte-sz1hib")) && k(e, "class", o), (!a || m & /*elem_id*/
      2) && k(
        e,
        "id",
        /*elem_id*/
        r[1]
      ), (!a || m & /*bg_blur*/
      64) && b(e, "backdrop-filter", "blur(" + /*bg_blur*/
      r[6] + ")"), (!a || m & /*opacity_level*/
      512) && b(e, "background-color", "rgba(0, 0, 0, " + /*opacity_level*/
      r[9] + ")"), (!a || m & /*elem_classes, visible*/
      5) && W(e, "hide", !/*visible*/
      r[0]);
    },
    i(r) {
      a || (K(f.$$.fragment, r), a = !0);
    },
    o(r) {
      O(f.$$.fragment, r), a = !1;
    },
    d(r) {
      r && E(e), ee(f), t[24](null), s && s.d(), t[25](null), c = !1, n();
    }
  };
}
function $e(t, e, l) {
  let { $$slots: f = {}, $$scope: i } = e, { elem_id: o = "" } = e, { elem_classes: a = [] } = e, { visible: c = !1 } = e, { display_close_icon: n = !1 } = e, { close_on_esc: s } = e, { close_outer_click: r } = e, { close_message: m } = e, { bg_blur: u } = e, { width: w } = e, { height: j } = e, { content_width_percent: z } = e, { content_height_percent: C } = e, { content_padding: q } = e, { opacity_level: g } = e, { gradio: h } = e, { close_message_style: H = {
    message_color: "var(--body-text-color)",
    confirm_text: "Yes",
    cancel_text: "No",
    confirm_bg_color: "var(--primary-500)",
    cancel_bg_color: "var(--neutral-500)",
    confirm_text_color: "white",
    cancel_text_color: "white",
    modal_bg_color: "var(--background-fill-primary)"
  } } = e, I = null, d = null, T = !1;
  const F = () => {
    m ? l(13, T = !0) : P();
  }, P = () => {
    l(0, c = !1), l(13, T = !1), h.dispatch("blur");
  }, te = () => {
    l(13, T = !1);
  };
  document.addEventListener("keydown", (_) => {
    s && _.key === "Escape" && F();
  });
  const fe = () => {
    const _ = q ? `${q}` : "0px", oe = z ? `${z}%` : "100%", ce = C ? `${C}%` : "100%";
    return `width: ${oe}; max-height: ${ce}; padding: ${_};`;
  };
  function ne(_) {
    V[_ ? "unshift" : "push"](() => {
      d = _, l(12, d);
    });
  }
  function ie(_) {
    V[_ ? "unshift" : "push"](() => {
      I = _, l(11, I);
    });
  }
  const ae = (_) => {
    r && (_.target === I || _.target === d) && F();
  };
  return t.$$set = (_) => {
    "elem_id" in _ && l(1, o = _.elem_id), "elem_classes" in _ && l(2, a = _.elem_classes), "visible" in _ && l(0, c = _.visible), "display_close_icon" in _ && l(3, n = _.display_close_icon), "close_on_esc" in _ && l(18, s = _.close_on_esc), "close_outer_click" in _ && l(4, r = _.close_outer_click), "close_message" in _ && l(5, m = _.close_message), "bg_blur" in _ && l(6, u = _.bg_blur), "width" in _ && l(7, w = _.width), "height" in _ && l(8, j = _.height), "content_width_percent" in _ && l(19, z = _.content_width_percent), "content_height_percent" in _ && l(20, C = _.content_height_percent), "content_padding" in _ && l(21, q = _.content_padding), "opacity_level" in _ && l(9, g = _.opacity_level), "gradio" in _ && l(22, h = _.gradio), "close_message_style" in _ && l(10, H = _.close_message_style), "$$scope" in _ && l(27, i = _.$$scope);
  }, [
    c,
    o,
    a,
    n,
    r,
    m,
    u,
    w,
    j,
    g,
    H,
    I,
    d,
    T,
    F,
    P,
    te,
    fe,
    s,
    z,
    C,
    q,
    h,
    f,
    ne,
    ie,
    ae,
    i
  ];
}
class l0 extends Ke {
  constructor(e) {
    super(), Re(this, e, $e, xe, We, {
      elem_id: 1,
      elem_classes: 2,
      visible: 0,
      display_close_icon: 3,
      close_on_esc: 18,
      close_outer_click: 4,
      close_message: 5,
      bg_blur: 6,
      width: 7,
      height: 8,
      content_width_percent: 19,
      content_height_percent: 20,
      content_padding: 21,
      opacity_level: 9,
      gradio: 22,
      close_message_style: 10
    });
  }
}
export {
  l0 as default
};
